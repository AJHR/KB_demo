"""Extractor de la demanda real horaria del sistema via API SIP del CEN.

Endpoints (sources/costos_sen/anexos/coordinador.md, seccion 2):

- v2 (principal):
    https://sipub.api.coordinador.cl/sipub/api/v2/demanda_sistema_real/
        ?user_key=...&fecha=YYYY-MM-DD
- v1 (fallback si v2 devuelve vacio o 404):
    https://sipub.api.coordinador.cl/sipub/api/v1/recursos/demandasistemareal

La API exige `fecha=YYYY-MM-DD`: UN DIA por request. Eso significa que un
mes son ~30 requests, por lo que cada request va precedido de la pausa de
rate limiting de cen_api (default 1.2 s, configurable via CEN_API_PAUSA_SEG;
evidencia de terceros: 60 req/h en algunos planes). Requiere
COORDINADOR_USER_KEY. NO PROBADO contra el endpoint real (sandbox sin red);
el parser se prueba offline en tests_offline.py.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import requests

from cen_api import (buscar_columna, dias_entre, extraer_fecha_hora,
                     extraer_filas, get_paginado, pausar, user_key)
from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "cen_demanda"

URL_V2 = "https://sipub.api.coordinador.cl/sipub/api/v2/demanda_sistema_real/"
URL_V1 = "https://sipub.api.coordinador.cl/sipub/api/v1/recursos/demandasistemareal"

COLUMNAS = ["fecha", "hora", "demanda_mwh"]

# Variantes plausibles del campo de demanda en la API SIP.
CANDIDATOS_DEMANDA = ["demanda_mwh", "demanda_real_mwh", "demanda",
                      "demanda_real", "demanda_sistema", "dda", "mwh", "valor"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON (o lista de filas) -> DataFrame [fecha, hora, demanda_mwh].

    Mapeo defensivo: demanda via CANDIDATOS_DEMANDA; fecha/hora via
    cen_api.extraer_fecha_hora ('fecha'+'hora' o 'fecha_hora')."""
    filas, _ = extraer_filas(json_obj)
    if not filas:
        return pd.DataFrame(columns=COLUMNAS)
    df = pd.DataFrame(filas)
    col_dem = buscar_columna(df, CANDIDATOS_DEMANDA)
    if col_dem is None:
        raise ValueError(
            f"respuesta de demanda sin campo reconocible; columnas: {list(df.columns)}")
    fecha, hora = extraer_fecha_hora(df)
    out = pd.DataFrame({
        "fecha": fecha,
        "hora": hora,
        "demanda_mwh": pd.to_numeric(df[col_dem], errors="coerce"),
    })
    return out[COLUMNAS].reset_index(drop=True)


def _codigo_http(e: requests.HTTPError) -> int | None:
    return e.response.status_code if e.response is not None else None


def _descargar_dia(s, dia: date) -> list:
    """Un dia de demanda: v2 primero; si da vacio o 404, fallback a v1."""
    params = {"user_key": user_key(), "fecha": dia.isoformat()}
    filas = []
    try:
        filas = get_paginado(s, URL_V2, params)
    except requests.HTTPError as e:
        if _codigo_http(e) != 404:
            raise
        log.info("%s: v2 devolvio 404 para %s; pruebo v1", FUENTE, dia)
    if filas:
        return filas
    try:
        return get_paginado(s, URL_V1, params)
    except requests.HTTPError as e:
        if _codigo_http(e) == 404:
            log.warning("%s: ni v2 ni v1 tienen datos para %s (404)", FUENTE, dia)
            return []
        raise


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        filas_mes: list = []
        for dia in dias_entre(ini, fin):
            pausar()  # rate limit: un mes son ~30 requests de un dia c/u
            filas_mes.extend(con_reintentos(lambda d=dia: _descargar_dia(s, d)))
        df = parsear_respuesta(filas_mes)
        if df.empty:
            log.warning("%s: 0 filas utiles en %s..%s; particion no escrita",
                        FUENTE, ini, fin)
            continue
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas, %d dias)",
                 FUENTE, destino.name, len(df), df.fecha.nunique())
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
