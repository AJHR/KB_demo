"""Extractor de clima OBSERVADO via Open-Meteo Archive API (ERA5).

Granularidad diaria por punto representativo. El archivo ERA5 tiene rezago de
~2-5 dias: estos datos solo se usan como features con lag >= 5 dias o para
backfill historico. El clima "reciente" del pipeline nocturno y el pronostico
D+1 vienen de extractor_clima_pronostico.py.

Regla anti-fuga: una observacion del dia X queda disponible ~X+5; la tabla
maestra solo la expone con ese lag (ver construir_tabla_maestra.py).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "clima_observado"

URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

# Puntos representativos del SEN. Justificacion en
# sources/costos_sen/catalogo_fuentes.md (seccion clima).
PUNTOS = {
    # zona solar
    "solar_maria_elena": (-22.35, -69.66),
    "solar_diego_almagro": (-26.39, -70.05),
    # zona eolica
    "eolica_taltal": (-25.41, -70.49),
    "eolica_renaico": (-37.67, -72.59),
    "eolica_chiloe": (-41.87, -73.83),
    # cuencas hidro
    "hidro_maule": (-35.72, -71.00),
    "hidro_biobio_laja": (-37.28, -71.50),
    "hidro_rapel": (-34.03, -71.59),
    # centros de demanda
    "demanda_santiago": (-33.45, -70.66),
    "demanda_concepcion": (-36.83, -73.05),
    "demanda_antofagasta": (-23.65, -70.40),
}

VARS_DIARIAS = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "shortwave_radiation_sum", "precipitation_sum",
    "wind_speed_10m_max", "wind_gusts_10m_max",
]


def _descargar_punto(s, nombre: str, lat: float, lon: float,
                     ini: date, fin: date) -> pd.DataFrame:
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": ini.isoformat(), "end_date": fin.isoformat(),
        "daily": ",".join(VARS_DIARIAS),
        "timezone": "America/Santiago",
    }
    r = s.get(URL_ARCHIVE, params=params, timeout=60)
    r.raise_for_status()
    j = r.json()
    if "daily" not in j:
        raise ValueError(f"respuesta sin bloque daily: {list(j)}")
    df = pd.DataFrame(j["daily"]).rename(columns={"time": "fecha"})
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    df["punto"] = nombre
    df["latitud"] = lat
    df["longitud"] = lon
    return df


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        partes = [
            con_reintentos(lambda n=n, la=la, lo=lo: _descargar_punto(s, n, la, lo, ini, fin))
            for n, (la, lo) in PUNTOS.items()
        ]
        df = pd.concat(partes, ignore_index=True)
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas, %d puntos)",
                 FUENTE, destino.name, len(df), len(PUNTOS))
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
