"""Extractor de PRONOSTICO de clima para D+1 sin fuga de datos.

Para predecir el dia D+1 desde el dia D (corte 20:00 Chile) solo es legitimo
usar el pronostico que existia el dia D. Dos modos:

- Backfill historico: Open-Meteo **Previous Runs API** con sufijo
  `_previous_day2`. previous_day2 = valor pronosticado ~48 h antes del tiempo
  valido, garantizado emitido antes del cierre de las 20:00 del dia D para
  cualquier hora de D+1 (previous_day1 filtra informacion post-20:00 en las
  horas tardias de D+1 — ver catalogo de fuentes, hallazgo anti-fuga).
  Archivo disponible desde ~2024-01 (algunas variables GFS desde 2021).
- Pipeline nocturno: Forecast API estandar pidiendo manana (el cron corre
  ~02:00 del dia D+1 usando la corrida 12z/18z del dia D ya publicada;
  operacionalmente equivale al pronostico disponible a las 20:00 de D).

Granularidad: horaria agregada a diaria por punto.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)
from extractor_clima import PUNTOS

FUENTE = "clima_pronostico"

URL_PREVIOUS_RUNS = "https://previous-runs-api.open-meteo.com/v1/forecast"
URL_FORECAST = "https://api.open-meteo.com/v1/forecast"

VARS_HORARIAS = ["temperature_2m", "shortwave_radiation", "wind_speed_100m",
                 "precipitation"]
LEAD = "_previous_day2"


def _agregar_diario(df_h: pd.DataFrame, sufijo: str) -> pd.DataFrame:
    """Agrega variables horarias pronosticadas a resumen diario."""
    df_h["fecha"] = pd.to_datetime(df_h["time"]).dt.date
    cols = {f"temperature_2m{sufijo}": ("temp_media", "mean"),
            f"shortwave_radiation{sufijo}": ("radiacion_media", "mean"),
            f"wind_speed_100m{sufijo}": ("viento100m_medio", "mean"),
            f"precipitation{sufijo}": ("precipitacion_total", "sum")}
    agg = {}
    for col, (nombre, fn) in cols.items():
        if col in df_h:
            agg[nombre] = (col, fn)
    out = df_h.groupby("fecha").agg(**agg).reset_index()
    # maximos diarios ademas de medias (peaks de viento/temp mueven despacho)
    for col, nombre in [(f"temperature_2m{sufijo}", "temp_max"),
                        (f"wind_speed_100m{sufijo}", "viento100m_max")]:
        if col in df_h:
            out[nombre] = df_h.groupby("fecha")[col].max().to_numpy()
    return out


def _descargar_punto_previous(s, nombre: str, lat: float, lon: float,
                              ini: date, fin: date) -> pd.DataFrame:
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": ini.isoformat(), "end_date": fin.isoformat(),
        "hourly": ",".join(v + LEAD for v in VARS_HORARIAS),
        "timezone": "America/Santiago",
    }
    r = s.get(URL_PREVIOUS_RUNS, params=params, timeout=120)
    r.raise_for_status()
    j = r.json()
    if "hourly" not in j:
        raise ValueError(f"respuesta sin bloque hourly: {list(j)}")
    df = _agregar_diario(pd.DataFrame(j["hourly"]), LEAD)
    df["punto"] = nombre
    df["lead"] = "previous_day2"
    return df


def _descargar_punto_manana(s, nombre: str, lat: float, lon: float) -> pd.DataFrame:
    """Modo nocturno: pronostico vigente para manana (1 dia)."""
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": ",".join(VARS_HORARIAS),
        "forecast_days": 2, "timezone": "America/Santiago",
    }
    r = s.get(URL_FORECAST, params=params, timeout=60)
    r.raise_for_status()
    df = _agregar_diario(pd.DataFrame(r.json()["hourly"]), "")
    df["punto"] = nombre
    df["lead"] = "operacional"
    return df.tail(1)  # solo manana


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
            con_reintentos(lambda n=n, la=la, lo=lo: _descargar_punto_previous(s, n, la, lo, ini, fin))
            for n, (la, lo) in PUNTOS.items()
        ]
        df = pd.concat(partes, ignore_index=True)
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas)", FUENTE, destino.name, len(df))
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
