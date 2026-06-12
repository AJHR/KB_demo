"""Orquestador del ETL — backfill e incremento nocturno.

Codigo deterministico puro: sin agentes ni LLMs en el camino critico
(decision de la mision, fase 2.6).

Uso:
  python3 run_etl.py --modo backfill --inicio 2019-01-01 --fin 2026-06-10
  python3 run_etl.py --modo incremental            # ultimos N dias (default 7)
  python3 run_etl.py --fuentes calendario,combustibles --modo incremental

Manejo de credenciales: las fuentes cen_* requieren COORDINADOR_USER_KEY
(registro gratuito en portal.api.coordinador.cl). Si falta, la fuente se
marca "omitida_sin_credencial" — no cuenta como fallo (evita spam de issues
nocturnos) pero queda visible en data/raw/estado_etl.json.

Tracking de fallos consecutivos por fuente en data/raw/estado_etl.json:
el workflow nocturno abre un issue si fallos_consecutivos >= 2.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
from datetime import date, datetime, timedelta
from pathlib import Path

from comun import DIR_RAW, log

# fuente -> modulo extractor. El orden importa solo por cortesia de logs.
FUENTES = {
    "calendario": "extractor_calendario",
    "clima_observado": "extractor_clima",
    "clima_pronostico": "extractor_clima_pronostico",
    "combustibles": "extractor_combustibles",
    "cen_cmg_real": "extractor_cen_cmg_real",
    "cen_cmg_programado": "extractor_cen_cmg_programado",
    "cen_demanda": "extractor_cen_demanda",
    "cen_generacion": "extractor_cen_generacion",
    "cen_embalses": "extractor_cen_embalses",
    "cen_po": "extractor_cen_po",
}

MARCADOR_CREDENCIAL = "COORDINADOR_USER_KEY"


def _cargar_estado() -> dict:
    ruta = DIR_RAW / "estado_etl.json"
    if ruta.exists():
        return json.loads(ruta.read_text())
    return {}


def _guardar_estado(estado: dict) -> None:
    DIR_RAW.mkdir(parents=True, exist_ok=True)
    (DIR_RAW / "estado_etl.json").write_text(
        json.dumps(estado, indent=2, ensure_ascii=False))


def ejecutar(fuentes: list[str], inicio: date, fin: date,
             forzar: bool = False) -> int:
    estado = _cargar_estado()
    fallos = 0
    for fuente in fuentes:
        modulo_nombre = FUENTES[fuente]
        registro = estado.setdefault(fuente, {"fallos_consecutivos": 0})
        registro["ultima_corrida"] = datetime.utcnow().isoformat() + "Z"
        try:
            modulo = importlib.import_module(modulo_nombre)
            rutas = modulo.extract(inicio, fin, forzar=forzar)
            registro.update(fallos_consecutivos=0, ultimo_error=None,
                            estado="ok", particiones=len(rutas))
            log.info("fuente %s OK (%d particiones)", fuente, len(rutas))
        except Exception as e:  # noqa: BLE001 - aislar fallos por fuente
            mensaje = f"{type(e).__name__}: {e}"
            if MARCADOR_CREDENCIAL in str(e):
                registro.update(estado="omitida_sin_credencial",
                                ultimo_error=mensaje)
                log.warning("fuente %s omitida: falta credencial", fuente)
            else:
                registro["fallos_consecutivos"] = \
                    registro.get("fallos_consecutivos", 0) + 1
                registro.update(estado="error", ultimo_error=mensaje)
                log.error("fuente %s FALLO (%d consecutivos):\n%s",
                          fuente, registro["fallos_consecutivos"],
                          traceback.format_exc())
                fallos += 1
    _guardar_estado(estado)
    return fallos


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fuentes", default="todas",
                   help="lista separada por comas o 'todas'")
    p.add_argument("--modo", choices=["backfill", "incremental"],
                   default="incremental")
    p.add_argument("--inicio", type=date.fromisoformat, default=None)
    p.add_argument("--fin", type=date.fromisoformat, default=None)
    p.add_argument("--ventana-dias", type=int, default=7,
                   help="dias hacia atras en modo incremental")
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()

    if a.fuentes == "todas":
        fuentes = list(FUENTES)
    else:
        fuentes = [f.strip() for f in a.fuentes.split(",")]
        desconocidas = set(fuentes) - set(FUENTES)
        if desconocidas:
            p.error(f"fuentes desconocidas: {desconocidas}; "
                    f"validas: {list(FUENTES)}")

    hoy = date.today()
    if a.modo == "incremental":
        inicio = a.inicio or (hoy - timedelta(days=a.ventana_dias))
        # las particiones son mensuales: anclar al dia 1 del mes para que la
        # re-escritura del mes corriente siempre contenga el mes completo
        # (una ventana a mitad de mes sobreescribiria la particion con solo
        # los dias de la ventana — bug detectado en el dry-run local)
        inicio = inicio.replace(day=1)
        fin = a.fin or hoy
    else:
        inicio = a.inicio or date(2019, 1, 1)
        fin = a.fin or hoy

    log.info("ETL %s: fuentes=%s rango=%s..%s", a.modo, fuentes, inicio, fin)
    fallos = ejecutar(fuentes, inicio, fin, a.forzar)
    if fallos:
        log.error("%d fuente(s) fallaron", fallos)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
