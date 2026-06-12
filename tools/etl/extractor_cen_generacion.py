"""Extractor de generacion real horaria por tecnologia via API SIP del CEN.

Endpoint (sources/costos_sen/anexos/coordinador.md, seccion 2; evidencia en
repo de terceros alo-ngh/iea_scraper_limited):

    https://sipub.api.coordinador.cl/sipub/api/v1/recursos/
        generacion_centrales_tecnologia_horario?user_key=...&fecha=YYYY-MM-DD

UN DIA por request (loop por dias del mes con pausa de rate limit: un mes
son ~30 requests). El detalle por central es enorme (cientos de centrales x
24 horas), asi que ANTES de guardar se agrega por (fecha, hora, tecnologia)
sumando MWh -> columnas [fecha, hora, tecnologia, generacion_mwh]. El
detalle por central no se persiste: si mas adelante hace falta (p.ej. para
el proxy de costo real = generacion x costo variable por central), se
cambia la agregacion aqui y se re-extrae con forzar=True.

Requiere COORDINADOR_USER_KEY. NO PROBADO contra el endpoint real (sandbox
sin red); el parser se prueba offline en tests_offline.py.
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

FUENTE = "cen_generacion"

URL = ("https://sipub.api.coordinador.cl/sipub/api/v1/recursos/"
       "generacion_centrales_tecnologia_horario")

COLUMNAS = ["fecha", "hora", "tecnologia", "generacion_mwh"]

# Variantes plausibles de los campos en la API SIP.
CANDIDATOS_TECNOLOGIA = ["tipo_central", "tecnologia", "central_tipo", "tipo",
                         "tipo_tecnologia", "combustible"]
CANDIDATOS_GENERACION = ["generacion_real_mwh", "generacion_mwh", "mwh",
                         "generacion", "energia_mwh", "valor"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON -> DataFrame agregado [fecha, hora, tecnologia, generacion_mwh].

    Mapeo defensivo de campos y agregacion por (fecha, hora, tecnologia)
    sumando MWh: el detalle por central no se conserva (ver docstring)."""
    filas, _ = extraer_filas(json_obj)
    if not filas:
        return pd.DataFrame(columns=COLUMNAS)
    df = pd.DataFrame(filas)
    col_tec = buscar_columna(df, CANDIDATOS_TECNOLOGIA)
    col_gen = buscar_columna(df, CANDIDATOS_GENERACION)
    if col_tec is None or col_gen is None:
        raise ValueError(
            "respuesta de generacion sin campos reconocibles de "
            f"tecnologia/MWh; columnas: {list(df.columns)}")
    fecha, hora = extraer_fecha_hora(df)
    detalle = pd.DataFrame({
        "fecha": fecha,
        "hora": hora,
        "tecnologia": df[col_tec].astype(str),
        "generacion_mwh": pd.to_numeric(df[col_gen], errors="coerce"),
    })
    agregado = (detalle
                .groupby(["fecha", "hora", "tecnologia"], as_index=False,
                         dropna=False)["generacion_mwh"]
                .sum())
    return agregado[COLUMNAS]


def _descargar_dia(s, dia: date) -> list:
    params = {"user_key": user_key(), "fecha": dia.isoformat()}
    try:
        return get_paginado(s, URL, params)
    except requests.HTTPError as e:
        codigo = e.response.status_code if e.response is not None else None
        if codigo == 404:
            log.warning("%s: 404 para %s (dia sin publicar aun?)", FUENTE, dia)
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
        log.info("%s: particion %s (%d filas agregadas, %d tecnologias)",
                 FUENTE, destino.name, len(df), df.tecnologia.nunique())
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
