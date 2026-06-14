"""Extractor del Costo Marginal del SEN via API SIP (endpoint costo-marginal-online),
agregado a resolucion horaria.

Decision de fuente (D-012, usuario 2026-06-14), verificada empiricamente en el
runner: el endpoint `costo-marginal-real/v4/findByDate` SOLO entrega el regimen
"nuevo" (>=2024-07-15) — enero 2024 devolvio 0 filas en 1.3s; agosto 2024 si
trajo datos. Para cubrir TODO el historico con UNA fuente continua (sin la
costura del quiebre 2024-07-15) se usa:

    https://sipub.api.coordinador.cl/costo-marginal-online/v4/findByDate
        ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&limit=&user_key=...

Es el mismo endpoint que consumen los pipelines productivos de terceros
(TM3-Corp/pudidi_cmg_prediction, bess-solutions/open-bess-edge), con profundidad
historica >=2018 segun la documentacion oficial de la API SIP. El CMg "en linea"
se determina a mas tardar 15 min despues de cada intervalo de 15 min; aca se
**agrega a horario** (media de los 4 intervalos por barra) para alinearse con la
granularidad horaria de la demanda y del resto de la tabla maestra.

- Hasta ~31 dias por request -> tramos mensuales (meses_entre).
- Requiere COORDINADOR_USER_KEY (portal.api.coordinador.cl).

Anti-fuga: el CMg se incorpora a la tabla maestra con rezago (LAG_CMG en
construir_tabla_maestra.py); nunca como informacion del propio dia D+1.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from cen_api import get_paginado, parsear_cmg, pausar, user_key
from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "cen_cmg_real"

URL = "https://sipub.api.coordinador.cl/costo-marginal-online/v4/findByDate"

# Tamano de pagina: el diagnostico (run #27484278704) confirmo que la API
# respeta `limit` (devolvio exactamente 1000/pagina). Con 4000 se cuartean las
# paginas y baja ~4x el costo de paginacion del backfill.
LIMIT = 4000

COLUMNAS = ["barra", "fecha", "hora", "cmg_usd_mwh"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON (intervalos de 15 min) -> DataFrame horario
    [barra, fecha, hora, cmg_usd_mwh].

    Mapeo defensivo de campos via cen_api.parsear_cmg (filtra a las barras de
    referencia) y luego **agregacion a horario**: media de los (hasta 4)
    intervalos de 15 min de cada (barra, fecha, hora)."""
    df = parsear_cmg(json_obj)
    if df.empty:
        return df[COLUMNAS] if set(COLUMNAS).issubset(df.columns) else \
            pd.DataFrame(columns=COLUMNAS)
    horario = (df.groupby(["barra", "fecha", "hora"], as_index=False)
                 .agg(cmg_usd_mwh=("cmg_usd_mwh", "mean")))
    horario = horario.sort_values(["fecha", "hora", "barra"]).reset_index(drop=True)
    return horario[COLUMNAS]


def _descargar_tramo(s, ini: date, fin: date) -> list:
    params = {"startDate": ini.isoformat(), "endDate": fin.isoformat(),
              "user_key": user_key(), "limit": LIMIT}
    return get_paginado(s, URL, params)


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        pausar()
        filas = con_reintentos(lambda i=ini, f=fin: _descargar_tramo(s, i, f))
        df = parsear_respuesta(filas)
        if df.empty:
            # No se escribe particion vacia: asi la proxima corrida reintenta
            # en vez de dar el mes por cerrado con cero datos.
            log.warning("%s: 0 filas utiles en %s..%s (%d filas crudas); "
                        "particion no escrita", FUENTE, ini, fin, len(filas))
            continue
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas horarias, %d barras)",
                 FUENTE, destino.name, len(df), df.barra.nunique())
    registrar_manifiesto(FUENTE, rutas, dir_datos)
    return rutas


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inicio", type=date.fromisoformat, required=True)
    p.add_argument("--fin", type=date.fromisoformat, required=True)
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()
    extract(a.inicio, a.fin, forzar=a.forzar)
