"""Extractor del Costo Marginal Real del SEN via API SIP (endpoint
costo-marginal-real, regimen "nuevo"), a resolucion horaria.

Decision de fuente (D-012, usuario 2026-06-14), tomada tras medir en vivo la
cobertura real de la API SIP v4 (no asumida):

  - `costo-marginal-real/v4/findByDate` SOLO entrega el regimen "nuevo"
    (>=2024-07-15): agosto 2024 trajo datos; enero 2024 -> 0 filas.
  - `costo-marginal-online/v4/findByDate` resulto ser SOLO-RECIENTE (ventana
    movil): mayo 2026 trajo datos; febrero 2024 -> 0 filas. NO sirve para
    historia profunda.
  - El CMg real anterior al 2024-07-15 ("antiguo") NO esta en la API v4; vive
    en open data de la CNE (datos.energiaabierta.cl) o en CSV legacy del CEN.

El usuario opto por usar SOLO el SIP "nuevo" (>=2024-07-15): historia mas corta
(~2 anos) pero una sola fuente que ya funciona, sin credenciales nuevas. La
historia multi-ano queda como extension futura (extractor de Energia Abierta).

    https://sipub.api.coordinador.cl/costo-marginal-real/v4/findByDate
        ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&limit=&user_key=...

- Hasta ~31 dias por request -> tramos mensuales (meses_entre).
- Se ignoran los meses anteriores a FECHA_INICIO_DATOS (no estan en este
  endpoint): evita pagar requests vacios en un backfill largo.
- Requiere COORDINADOR_USER_KEY (portal.api.coordinador.cl).

Anti-fuga: el CMg real se publica con rezago (proceso de transferencias); la
tabla maestra lo incorpora con LAG_CMG, nunca como dato del propio dia D+1.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from cen_api import dias_entre, get_paginado, parsear_cmg, pausar, user_key
from comun import (con_reintentos, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion,
                   sesion_http)

FUENTE = "cen_cmg_real"

URL = "https://sipub.api.coordinador.cl/costo-marginal-real/v4/findByDate"

# El endpoint solo sirve el regimen "nuevo" (verificado en runner): antes de
# esta fecha devuelve 0 filas. Se evita iterar esos meses en un backfill largo.
FECHA_INICIO_DATOS = date(2024, 7, 1)

# La API respeta `limit` PERO con un techo: 4000/pagina funciona (D-012);
# limit=20000 hace que el gateway devuelva 502 en la PRIMERA pagina del dia
# (run #27561362926: los 6 meses que corrieron fallaron con "too many 502").
# 4000 es el maximo probado-seguro. Un dia trae ~96k filas (todas las barras x
# 96 intervalos de 15min) => ~24 paginas/dia a limit=4000.
#
# El gateway ademas limita REQUESTS por user_key (~530 req/h medido en el unico
# mes que completo): con varios jobs en paralelo se gatillan 429 sostenidos.
# Por eso el workflow corre cen_cmg_real con max-parallel=1: el cuello de
# botella es el limite por key, que la concurrencia no puede superar.
LIMIT = 4000

COLUMNAS = ["barra", "fecha", "hora", "cmg_usd_mwh"]


def parsear_respuesta(json_obj) -> pd.DataFrame:
    """Respuesta JSON -> DataFrame horario [barra, fecha, hora, cmg_usd_mwh].

    Mapeo defensivo via cen_api.parsear_cmg (filtra a barras de referencia) y
    consolidacion a horario: media por (barra, fecha, hora). Es no-op si la
    serie ya viene horaria (un registro por hora) y correcta si trajera
    sub-horario."""
    df = parsear_cmg(json_obj)
    if df.empty:
        return df[COLUMNAS] if set(COLUMNAS).issubset(df.columns) else \
            pd.DataFrame(columns=COLUMNAS)
    horario = (df.groupby(["barra", "fecha", "hora"], as_index=False)
                 .agg(cmg_usd_mwh=("cmg_usd_mwh", "mean")))
    horario = horario.sort_values(["fecha", "hora", "barra"]).reset_index(drop=True)
    return horario[COLUMNAS]


def _descargar_dia(s, dia: date) -> list:
    params = {"startDate": dia.isoformat(), "endDate": dia.isoformat(),
              "user_key": user_key(), "limit": LIMIT}
    return get_paginado(s, URL, params)


def _descargar_mes(s, ini: date, fin: date) -> list:
    """Descarga el mes DIA POR DIA. El CMg real-nuevo trae todas las barras en
    15-min (~2-4 millones de filas/mes); paginar un mes completo llega a
    offsets profundos (page 500+) donde el gateway devuelve 502 masivos. Pedir
    dia por dia mantiene la paginacion somera (~decenas de paginas) -> estable
    y mas rapido en neto. La pausa de rate-limit va por dia.

    Tolerancia a dias irrecuperables: si un dia agota los reintentos (racha
    sostenida de 429/502 del gateway), se SALTA con aviso en vez de tumbar el
    mes entero. Antes, un solo dia malo hacia fallar todo el mes -> 0 datos
    (run #27563427333: 2025-01/02 cayeron asi). Un mes con 1-2 dias faltantes
    sigue siendo util: la tabla maestra reindexa a calendario y esos dias
    quedan NaN (se excluyen del walk-forward). Si fallan demasiados dias, el
    mes queda escaso pero no se pierde lo descargado."""
    filas: list = []
    saltados: list = []
    for dia in dias_entre(ini, fin):
        pausar()
        try:
            filas.extend(con_reintentos(lambda d=dia: _descargar_dia(s, d)))
        except Exception as e:  # noqa: BLE001 - dia irrecuperable: saltar, no abortar el mes
            saltados.append(dia)
            log.warning("%s: dia %s irrecuperable (%s); se salta", FUENTE, dia, e)
    if saltados:
        log.warning("%s: %d/%d dias saltados en %s..%s: %s", FUENTE,
                    len(saltados), (fin - ini).days + 1, ini, fin,
                    ", ".join(d.isoformat() for d in saltados))
    return filas


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    inicio = max(fecha_inicio, FECHA_INICIO_DATOS)
    if inicio > fecha_fin:
        log.info("%s: rango %s..%s anterior al inicio de datos (%s); nada que "
                 "descargar", FUENTE, fecha_inicio, fecha_fin, FECHA_INICIO_DATOS)
        registrar_manifiesto(FUENTE, [], dir_datos)
        return []
    s = sesion_http()
    rutas = []
    for ini, fin in meses_entre(inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        filas = _descargar_mes(s, ini, fin)
        df = parsear_respuesta(filas)
        if df.empty:
            # No se escribe particion vacia: la proxima corrida reintenta en
            # vez de dar el mes por cerrado con cero datos.
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
