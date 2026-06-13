"""Extractor de precios internacionales de combustibles + USD/CLP.

Stack por defecto SIN credenciales (decision D-007 en wiki/decisiones.md):
- Futuros front-month via stooq.com (CSV directo, sin key): Brent (cb.f),
  Henry Hub (ng.f), heating oil proxy diesel (ho.f). yfinance como respaldo.
- USD/CLP via mindicador.cl (JSON, sin key, historico por ano).

Mejora opcional con EIA_API_KEY en el entorno: series spot oficiales EIA
(RNGWHHD Henry Hub, RBRTE Brent, EER_EPD2DXL0_PF4_RGC_DPG diesel USGC).

Rezago anti-fuga: los cierres de futuros del dia D liquidan ~17:00 ET
(18-19h Chile) — usables el mismo dia D. Las series spot EIA llegan con
dias de rezago: la tabla maestra las expone con lag>=7 dias.
"""

from __future__ import annotations

import io
import os
from datetime import date
from pathlib import Path

import pandas as pd

from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "combustibles"

# (serie, ticker stooq, ticker yahoo)
FUTUROS = [
    ("brent_usd_bbl", "cb.f", "BZ=F"),
    ("henry_hub_usd_mmbtu", "ng.f", "NG=F"),
    ("diesel_ho_usd_gal", "ho.f", "HO=F"),
    ("carbon_api2_usd_t", None, "MTF=F"),  # solo Yahoo; baja liquidez
]

SERIES_EIA = {
    "brent_spot_usd_bbl": ("petroleum/pri/spt", "RBRTE"),
    "henry_hub_spot_usd_mmbtu": ("natural-gas/pri/fut", "RNGWHHD"),
    "diesel_usgc_spot_usd_gal": ("petroleum/pri/spt", "EER_EPD2DXL0_PF4_RGC_DPG"),
}


def _stooq(s, ticker: str, ini: date, fin: date) -> pd.DataFrame | None:
    url = (f"https://stooq.com/q/d/l/?s={ticker}&d1={ini:%Y%m%d}"
           f"&d2={fin:%Y%m%d}&i=d")
    r = s.get(url, timeout=60)
    r.raise_for_status()
    if not r.text.startswith("Date"):
        return None
    df = pd.read_csv(io.StringIO(r.text))
    return df.rename(columns={"Date": "fecha", "Close": "valor"})[["fecha", "valor"]]


def _yahoo(ticker: str, ini: date, fin: date) -> pd.DataFrame | None:
    try:
        import yfinance as yf
    except ImportError:
        return None
    h = yf.Ticker(ticker).history(start=ini.isoformat(), end=fin.isoformat(),
                                  auto_adjust=False)
    if h.empty:
        return None
    df = h.reset_index()[["Date", "Close"]]
    df.columns = ["fecha", "valor"]
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date.astype(str)
    return df


def _eia(s, ruta_api: str, serie: str, ini: date, fin: date,
         api_key: str) -> pd.DataFrame | None:
    url = f"https://api.eia.gov/v2/{ruta_api}/data/"
    params = {"api_key": api_key, "frequency": "daily",
              "data[0]": "value", "facets[series][]": serie,
              "start": ini.isoformat(), "end": fin.isoformat(),
              "length": 5000}
    r = s.get(url, params=params, timeout=60)
    r.raise_for_status()
    filas = r.json().get("response", {}).get("data", [])
    if not filas:
        return None
    df = pd.DataFrame(filas)[["period", "value"]]
    df.columns = ["fecha", "valor"]
    return df


def _usdclp(s, ini: date, fin: date) -> pd.DataFrame:
    partes = []
    for ano in range(ini.year, fin.year + 1):
        r = s.get(f"https://mindicador.cl/api/dolar/{ano}", timeout=60)
        r.raise_for_status()
        serie = r.json().get("serie", [])
        if serie:
            df = pd.DataFrame(serie)
            df["fecha"] = pd.to_datetime(df["fecha"]).dt.date.astype(str)
            partes.append(df.rename(columns={"valor": "valor"})[["fecha", "valor"]])
    if not partes:
        return pd.DataFrame(columns=["fecha", "valor"])
    df = pd.concat(partes, ignore_index=True)
    return df[(df.fecha >= ini.isoformat()) & (df.fecha <= fin.isoformat())]


def _descargar_mes(s, ini: date, fin: date) -> pd.DataFrame:
    marcos = []

    def agregar(nombre_serie: str, origen: str, df: pd.DataFrame | None):
        if df is None or df.empty:
            log.warning("combustibles: %s via %s sin datos %s..%s",
                        nombre_serie, origen, ini, fin)
            return
        d = df.copy()
        d["serie"] = nombre_serie
        d["origen"] = origen
        marcos.append(d[["fecha", "serie", "valor", "origen"]])

    for nombre_serie, tk_stooq, tk_yahoo in FUTUROS:
        df = None
        if tk_stooq:
            try:
                df = con_reintentos(lambda t=tk_stooq: _stooq(s, t, ini, fin),
                                    intentos=2)
            except Exception:
                df = None
        if df is not None:
            agregar(nombre_serie, f"stooq:{tk_stooq}", df)
            continue
        try:
            agregar(nombre_serie, f"yahoo:{tk_yahoo}",
                    con_reintentos(lambda t=tk_yahoo: _yahoo(t, ini, fin), intentos=2))
        except Exception as e:
            log.warning("combustibles: %s fallo en stooq y yahoo (%s)", nombre_serie, e)

    api_key = os.environ.get("EIA_API_KEY")
    if api_key:
        for nombre_serie, (ruta_api, serie) in SERIES_EIA.items():
            try:
                agregar(nombre_serie, f"eia:{serie}",
                        con_reintentos(lambda r=ruta_api, se=serie: _eia(s, r, se, ini, fin, api_key),
                                       intentos=2))
            except Exception as e:
                log.warning("combustibles: EIA %s fallo (%s)", serie, e)

    agregar("usd_clp", "mindicador",
            con_reintentos(lambda: _usdclp(s, ini, fin)))

    if not marcos:
        raise RuntimeError("ninguna serie de combustibles descargada")
    return pd.concat(marcos, ignore_index=True)


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        df = _descargar_mes(s, ini, fin)
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas, %d series)",
                 FUENTE, destino.name, len(df), df.serie.nunique())
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
