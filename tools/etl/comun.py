"""Utilidades comunes para los extractores del pipeline de costos SEN.

Interfaz que implementa cada extractor (modulo en tools/etl/extractor_*.py):

    def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
                forzar: bool = False) -> list[Path]

- Idempotente: si la particion mensual ya existe y `forzar=False`, no se re-descarga.
- Reintentos con backoff exponencial en errores de red.
- Escritura atomica de Parquet (tmp + rename) para que un corte a mitad de
  descarga nunca deje particiones corruptas.
- Particionado: data/raw/{fuente}/{YYYY}/{fuente}_{YYYY-MM}.parquet
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable, Iterator

import pandas as pd

RAIZ_REPO = Path(__file__).resolve().parents[2]
DIR_RAW = RAIZ_REPO / "data" / "raw"
DIR_PROCESSED = RAIZ_REPO / "data" / "processed"

UA = "KB-demo-costos-SEN/1.0 (pipeline academico; contacto en repo)"

log = logging.getLogger("etl")
logging.basicConfig(level=os.environ.get("ETL_LOG_LEVEL", "INFO"),
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")


def sesion_http():
    """Sesion requests con User-Agent identificable y reintentos a nivel transporte."""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    retry = Retry(total=4, backoff_factor=2.0,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=frozenset(["GET", "POST"]))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    return s


class ErrorCredencial(RuntimeError):
    """Falta una credencial obligatoria. NO es un error de red: no tiene
    sentido reintentar ni cuenta como fallo del ETL (el orquestador la marca
    como 'omitida_sin_credencial')."""


def con_reintentos(fn: Callable, intentos: int = 6, base_seg: float = 2.0):
    """Ejecuta fn() con reintentos y backoff exponencial (2,4,8,16,32,64s).

    6 intentos (~2min de backoff acumulado) para aguantar rachas de 502 del
    gateway SIP cuando varios jobs comparten el user_key.

    Una ErrorCredencial se propaga de inmediato (sin reintentos ni envoltura)
    para que el orquestador la reconozca: de lo contrario el marcador se
    perderia tras 4 reintentos y la fuente contaria como fallo real."""
    ultimo_error = None
    for i in range(intentos):
        try:
            return fn()
        except ErrorCredencial:
            raise
        except Exception as e:  # noqa: BLE001 - reintento generico de red
            ultimo_error = e
            espera = base_seg * (2 ** i)
            log.warning("intento %d/%d fallo (%s); reintento en %.0fs",
                        i + 1, intentos, e, espera)
            time.sleep(espera)
    raise RuntimeError(f"agotados {intentos} intentos") from ultimo_error


def meses_entre(fecha_inicio: date, fecha_fin: date) -> Iterator[tuple[date, date]]:
    """Itera (primer_dia_mes, ultimo_dia_mes_o_fecha_fin) entre dos fechas."""
    cursor = fecha_inicio.replace(day=1)
    while cursor <= fecha_fin:
        if cursor.month == 12:
            siguiente = cursor.replace(year=cursor.year + 1, month=1)
        else:
            siguiente = cursor.replace(month=cursor.month + 1)
        ini = max(cursor, fecha_inicio)
        fin = min(siguiente - timedelta(days=1), fecha_fin)
        yield ini, fin
        cursor = siguiente


def ruta_particion(fuente: str, anomes: date, dir_datos: Path | None = None) -> Path:
    base = (dir_datos or DIR_RAW) / fuente / f"{anomes.year:04d}"
    return base / f"{fuente}_{anomes.year:04d}-{anomes.month:02d}.parquet"


def escribir_parquet_atomico(df: pd.DataFrame, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destino.parent, suffix=".tmp",
                                     delete=False) as tmp:
        ruta_tmp = Path(tmp.name)
    try:
        df.to_parquet(ruta_tmp, index=False)
        os.replace(ruta_tmp, destino)
    finally:
        ruta_tmp.unlink(missing_ok=True)
    return destino


def particion_completa(ruta: Path, anomes_fin: date) -> bool:
    """Una particion mensual se considera cerrada si existe y el mes ya termino.

    El mes corriente siempre se re-descarga (datos parciales)."""
    if not ruta.exists():
        return False
    hoy = date.today()
    return (anomes_fin.year, anomes_fin.month) < (hoy.year, hoy.month)


def registrar_manifiesto(fuente: str, rutas: list[Path],
                         dir_datos: Path | None = None, **extra) -> None:
    """Manifiesto por fuente: cuando se descargo que. Sirve de evidencia de
    inmutabilidad y para los validadores de completitud."""
    base = (dir_datos or DIR_RAW) / fuente
    base.mkdir(parents=True, exist_ok=True)
    manifiesto = base / "manifiesto.json"
    historico = []
    if manifiesto.exists():
        historico = json.loads(manifiesto.read_text())
    historico.append({
        "descargado_en": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "particiones": [str(r.relative_to(dir_datos or DIR_RAW)) for r in rutas],
        **extra,
    })
    manifiesto.write_text(json.dumps(historico, indent=2, ensure_ascii=False))
