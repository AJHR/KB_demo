"""Extractor del Costo Marginal PROGRAMADO (PO/PID) via API SIP del CEN.

Endpoint (evidencia en sources/costos_sen/anexos/coordinador.md, seccion 2;
repo de terceros TM3-Corp/pudidi_cmg_prediction):

    https://sipub.api.coordinador.cl/cmg-programado-pid/v4/findByDate
        ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&user_key=...

Mismo patron v4 que costo-marginal-real: tramos de hasta 31 dias (aca,
mensuales), parser defensivo y filtro a barras de referencia.
NO PROBADO contra el endpoint real (red del sandbox bloqueada).

────────────────────────────────────────────────────────────────────────────
NOTA ANTI-FUGA (IMPORTANTE — leer antes de usar esta fuente como feature):

Este dato es el CMg PROGRAMADO para el dia D+1, en principio conocido
durante el dia D (resultado del Programa de Operacion). PERO la hora de
publicacion del PO NO esta confirmada (coordinador.md, seccion 7): si el PO
de D+1 se publica despues de las 20:00 hora Chile del dia D, usar este dato
para predecir D+1 seria fuga de informacion. Ademas, la Programacion
Intradiaria (PID) RE-publica programas varias veces durante el propio dia
D+1: la "ultima version" disponible casi siempre contiene informacion
posterior al corte.

Decision de diseno: ESTE EXTRACTOR SOLO CAPTURA. La tabla maestra
(construir_tabla_maestra.py) decide si esta serie entra al modelo y con que
rezago, cuando se confirme empiricamente la hora de publicacion desde el
runner. Si la API expone metadatos de version/publicacion (claves tipo
'fecha_publicacion', 'version', 'created_at'), se preservan tal cual
(CAMPOS_PUBLICACION) para poder filtrar a la PRIMERA version del programa.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from cen_api import get_paginado, parsear_cmg, pausar, user_key
from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "cen_cmg_programado"

URL = "https://sipub.api.coordinador.cl/cmg-programado-pid/v4/findByDate"

COLUMNAS_BASE = ["barra", "fecha", "hora", "cmg_usd_mwh"]

# Metadatos de version/publicacion a preservar si la API los incluye
# (criticos para el analisis anti-fuga; ver nota en el docstring).
CAMPOS_PUBLICACION = ["fecha_publicacion", "fecha_publicacion_po", "version",
                      "created_at", "updated_at", "fecha_creacion"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON -> DataFrame [barra, fecha, hora, cmg_usd_mwh, *metadatos].

    Mismo mapeo defensivo y filtro de barras que el CMg real
    (cen_api.parsear_cmg); ademas preserva, si existen, las columnas de
    CAMPOS_PUBLICACION con su nombre original."""
    return parsear_cmg(json_obj, preservar=CAMPOS_PUBLICACION)


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
            log.warning("%s: 0 filas utiles en %s..%s (%d filas crudas); "
                        "particion no escrita", FUENTE, ini, fin, len(filas))
            continue
        extras = [c for c in df.columns if c not in COLUMNAS_BASE]
        if extras:
            log.info("%s: la API trae metadatos de publicacion %s (preservados)",
                     FUENTE, extras)
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
