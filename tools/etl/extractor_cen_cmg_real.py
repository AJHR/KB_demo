"""Extractor del Costo Marginal REAL por barra via API SIP del Coordinador.

Endpoint (evidencia en sources/costos_sen/anexos/coordinador.md, seccion 2):

    https://sipub.api.coordinador.cl/costo-marginal-real/v4/findByDate
        ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&user_key=...

- Maximo ~31 dias por request -> se descarga en tramos mensuales
  (meses_entre garantiza tramos <= 31 dias).
- Requiere COORDINADOR_USER_KEY en el entorno (portal.api.coordinador.cl).
- QUIEBRE DE SERIE documentado (coordinador.md seccion 1.1): desde el
  2024-07-15 rige el "Costo Marginal Real (nuevo)"; lo anterior queda como
  historico "antiguo". La columna `regimen` deja el quiebre explicito para
  que el modelado no mezcle ambos tramos a ciegas.
- NO PROBADO contra el endpoint real (red del sandbox bloqueada): el parser
  es defensivo y se prueba offline con fixtures en tests_offline.py.

Anti-fuga: el CMg real se publica con rezago de dias/semanas (proceso de
transferencias economicas); la tabla maestra solo puede exponerlo como
feature retrospectiva, nunca como informacion disponible el dia D.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pandas as pd

from cen_api import get_paginado, parsear_cmg, pausar, user_key
from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "cen_cmg_real"

URL = "https://sipub.api.coordinador.cl/costo-marginal-real/v4/findByDate"

# Desde esta fecha rige el "Costo Marginal Real (nuevo)" (coordinador.md 1.1).
FECHA_QUIEBRE = date(2024, 7, 15)

COLUMNAS = ["barra", "fecha", "hora", "cmg_usd_mwh", "regimen"]


def _regimen(fecha_iso) -> object:
    """'antiguo' si fecha < 2024-07-15, 'nuevo' desde entonces; NA si invalida."""
    f = str(fecha_iso)
    if not re.match(r"^\d{4}-\d{2}-\d{2}", f):
        return pd.NA
    return "antiguo" if f < FECHA_QUIEBRE.isoformat() else "nuevo"


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON -> DataFrame [barra, fecha, hora, cmg_usd_mwh, regimen].

    Mapeo defensivo de campos (variantes 'barra_info'/'nmb_barra_info'/...,
    'cmg_usd_mwh_'/'cmg'/'costo_en_dolares', 'fecha_hora' o 'fecha'+'hora')
    y filtrado a las barras de referencia: ver cen_api.parsear_cmg."""
    df = parsear_cmg(json_obj)
    df["regimen"] = df["fecha"].map(_regimen)
    return df[COLUMNAS]


def _descargar_tramo(s, ini: date, fin: date) -> list:
    params = {"startDate": ini.isoformat(), "endDate": fin.isoformat(),
              "user_key": user_key(), "limit": 1000}
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
        log.info("%s: particion %s (%d filas, %d barras)",
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
