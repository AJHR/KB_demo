"""Extractor de cotas de embalses (hidrologia) via API SIP del CEN.

Endpoints candidatos (sources/costos_sen/anexos/coordinador.md, seccion 2;
la ruta exacta es incierta — el repo de terceros in-ventures/colbun_pge usa
la base `/api/v2/recursos`, pero otros endpoints v2 documentados cuelgan de
`/sipub/api/v2`). Se prueban ambas variantes y se recuerda la que funciona:

- Principal:   https://sipub.api.coordinador.cl/api/v2/recursos/cotas_embalses/
- Alternativa: https://sipub.api.coordinador.cl/sipub/api/v2/recursos/cotas_embalses/
  (si la principal devuelve 404)

Parametros: ?user_key=...&fecha=YYYY-MM-DD -> UN DIA por request (loop por
dias del mes con pausa de rate limit). Columnas de salida:
[fecha, embalse, cota_msnm, afluente_m3s] con mapeo defensivo de campos.

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

FUENTE = "cen_embalses"

URL_PRINCIPAL = "https://sipub.api.coordinador.cl/api/v2/recursos/cotas_embalses/"
URL_ALTERNATIVA = "https://sipub.api.coordinador.cl/sipub/api/v2/recursos/cotas_embalses/"

COLUMNAS = ["fecha", "embalse", "cota_msnm", "afluente_m3s"]

# Variantes plausibles de los campos en la API SIP.
CANDIDATOS_EMBALSE = ["embalse", "nombre_embalse", "nmb_embalse", "central",
                      "nombre"]
CANDIDATOS_COTA = ["cota_msnm", "cota_m", "cota", "nivel_msnm", "nivel",
                   "cota_embalse"]
CANDIDATOS_AFLUENTE = ["afluente_m3s", "afluente", "caudal_afluente_m3s",
                       "caudal_afluente", "caudal_m3s", "caudal"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON -> DataFrame [fecha, embalse, cota_msnm, afluente_m3s].

    Mapeo defensivo: si la API no trae cota o afluente, la columna queda en
    NA (la serie es diaria; la hora, si viniera, se ignora)."""
    filas, _ = extraer_filas(json_obj)
    if not filas:
        return pd.DataFrame(columns=COLUMNAS)
    df = pd.DataFrame(filas)
    col_emb = buscar_columna(df, CANDIDATOS_EMBALSE)
    if col_emb is None:
        raise ValueError(
            f"respuesta de embalses sin campo de embalse; columnas: {list(df.columns)}")
    col_cota = buscar_columna(df, CANDIDATOS_COTA)
    col_afl = buscar_columna(df, CANDIDATOS_AFLUENTE)
    fecha, _hora = extraer_fecha_hora(df)  # serie diaria: hora ignorada
    out = pd.DataFrame({
        "fecha": fecha,
        "embalse": df[col_emb].astype(str),
        "cota_msnm": (pd.to_numeric(df[col_cota], errors="coerce")
                      if col_cota else pd.NA),
        "afluente_m3s": (pd.to_numeric(df[col_afl], errors="coerce")
                         if col_afl else pd.NA),
    })
    return out[COLUMNAS].reset_index(drop=True)


def _descargar_dia(s, dia: date, urls: list[str]) -> list:
    """Un dia de cotas, probando las variantes de URL en orden.

    `urls` se reordena in-place para recordar la variante que funciono y no
    pagar un 404 extra por cada dia siguiente."""
    # limit=1000: sin el, la API pagina de a ~19 filas (el diagnostico midio 15
    # paginas y 24s para 288 filas de un dia); con un limit holgado cabe en 1
    # pagina -> ~15x menos requests por dia.
    params = {"user_key": user_key(), "fecha": dia.isoformat(), "limit": 1000}
    for url in list(urls):
        try:
            filas = get_paginado(s, url, params)
        except requests.HTTPError as e:
            codigo = e.response.status_code if e.response is not None else None
            if codigo == 404:
                log.info("%s: 404 en %s para %s; pruebo variante", FUENTE, url, dia)
                continue
            raise
        if filas:
            if url != urls[0]:
                urls.remove(url)
                urls.insert(0, url)
            return filas
        # vacio sin error: probar la otra variante por si acaso
    log.warning("%s: ninguna variante de URL entrego datos para %s", FUENTE, dia)
    return []


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    urls = [URL_PRINCIPAL, URL_ALTERNATIVA]
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        filas_mes: list = []
        for dia in dias_entre(ini, fin):
            pausar()  # rate limit: un mes son ~30 requests de un dia c/u
            filas_mes.extend(
                con_reintentos(lambda d=dia: _descargar_dia(s, d, urls)))
        df = parsear_respuesta(filas_mes)
        if df.empty:
            log.warning("%s: 0 filas utiles en %s..%s; particion no escrita",
                        FUENTE, ini, fin)
            continue
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas, %d embalses)",
                 FUENTE, destino.name, len(df), df.embalse.nunique())
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
