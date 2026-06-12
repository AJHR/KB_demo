"""Extractor EXPLORATORIO del Programa de Operacion (PO) diario del CEN.

El costo total de operacion PROGRAMADO (funcion objetivo del modelo
PCP/PLEXOS) es el candidato a variable objetivo del proyecto
(sources/costos_sen/anexos/coordinador.md, secciones 1.2 y Hallazgos). No
hay API: se publica como ZIPs diarios en

    https://www.coordinador.cl/operacion/documentos/programas-de-operacion/

SIN user_key (descarga web publica). La pagina limita los listados a rangos
de ~30 dias por consulta, y es posible que el listado real se construya con
un POST AJAX de WordPress (admin-ajax.php) en vez de links estaticos.

Comportamiento EXPLORATORIO (la red del sandbox esta bloqueada, nada de esto
pudo verificarse):

1. `listar_pos()` hace GET al listado y busca con regex los href .zip que
   contengan una fecha o 'PO'/'Programa'. Si no encuentra ninguno, loggea un
   WARNING con los primeros 2000 caracteres del HTML (diagnostico desde el
   runner de GitHub Actions) y devuelve lista vacia SIN abortar.
2. Por cada ZIP del rango: descarga a un tmpdir, lista el contenido interno
   (namelist) y extrae SOLO los archivos candidatos a contener el costo
   total — nombres con 'costo', 'objetivo', 'resumen' o 'costosvariables'
   (case-insensitive) y extension .csv/.xlsx — hacia
   data/raw/cen_po/extraidos/{fecha}/.
3. La particion mensual Parquet es un INVENTARIO:
   [fecha_po, zip_url, archivo_interno, tamano, es_candidato]
   (es_candidato marca lo que ademas se extrajo a disco). El parser del
   costo total queda como TODO (abajo): se necesita ver una muestra real de
   un ZIP antes de escribirlo. Este extractor cumple capturando la materia
   prima de forma trazable.

Anti-fuga: la PID re-publica programas durante el propio dia; cuando exista
el parser, usar SIEMPRE la primera version del PO del dia (el inventario
preserva la URL exacta para auditarlo).
"""

from __future__ import annotations

import re
import tempfile
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd

from cen_api import pausar
from comun import (DIR_RAW, con_reintentos, escribir_parquet_atomico, log,
                   meses_entre, particion_completa, registrar_manifiesto,
                   ruta_particion, sesion_http)

FUENTE = "cen_po"

URL_LISTADO = "https://www.coordinador.cl/operacion/documentos/programas-de-operacion/"

COLUMNAS_INVENTARIO = ["fecha_po", "zip_url", "archivo_interno", "tamano",
                       "es_candidato"]

# href que terminan en .zip (con o sin querystring no se contempla: los POs
# observados en terceros son archivos directos).
RE_ZIP = re.compile(r"href=[\"']([^\"']+?\.zip)[\"']", re.IGNORECASE)

# Un ZIP es relevante si su URL menciona PO/Programa (ademas del filtro por
# fecha reconocible en la URL).
RE_RELEVANTE = re.compile(r"(?:\bpo\b|programa)", re.IGNORECASE)

# Fechas dentro de la URL: 2025-06-07 / 20250607 / 07-06-2025, etc.
RE_FECHA_AMD = re.compile(r"(?<!\d)(20\d{2})[-_./]?(\d{2})[-_./]?(\d{2})(?!\d)")
RE_FECHA_DMA = re.compile(r"(?<!\d)(\d{2})[-_./](\d{2})[-_./](20\d{2})(?!\d)")

# Archivos internos candidatos a contener el costo total de operacion.
RE_CANDIDATO = re.compile(r"(costo|objetivo|resumen|costosvariables)",
                          re.IGNORECASE)
EXTENSIONES_CANDIDATO = (".csv", ".xlsx")


def _fecha_de_url(url: str) -> date | None:
    """Intenta extraer la fecha del PO desde la URL del ZIP; None si no hay."""
    m = RE_FECHA_AMD.search(url)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    m = RE_FECHA_DMA.search(url)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    return None


def _es_candidato(nombre_interno: str) -> bool:
    """True si el archivo interno del ZIP puede contener el costo total."""
    return (nombre_interno.lower().endswith(EXTENSIONES_CANDIDATO)
            and bool(RE_CANDIDATO.search(nombre_interno)))


def listar_pos(session, fecha_inicio: date, fecha_fin: date) -> list[tuple[date, str]]:
    """Devuelve [(fecha_po, url_zip)] de los POs listados dentro del rango.

    EXPLORATORIO: si el HTML no contiene links .zip (listado cargado por
    AJAX), se loggea WARNING con el inicio del HTML y se devuelve [] sin
    lanzar excepcion — el pipeline sigue y el runner deja el diagnostico."""
    r = session.get(URL_LISTADO, timeout=120)
    r.raise_for_status()
    html = r.text
    hrefs = [m.group(1) for m in RE_ZIP.finditer(html)]
    if not hrefs:
        log.warning(
            "%s: el HTML de %s no contiene links .zip — el listado "
            "probablemente se carga via POST AJAX de WordPress "
            "(admin-ajax.php); hay que inspeccionarlo desde el runner. "
            "Primeros 2000 caracteres del HTML para diagnostico:\n%s",
            FUENTE, URL_LISTADO, html[:2000])
        return []
    encontrados: set[tuple[date, str]] = set()
    sin_fecha = 0
    for href in hrefs:
        url_zip = urljoin(URL_LISTADO, href)
        fecha_po = _fecha_de_url(url_zip)
        if fecha_po is None and not RE_RELEVANTE.search(url_zip):
            continue  # .zip ajeno a los POs
        if fecha_po is None:
            sin_fecha += 1
            continue
        if fecha_inicio <= fecha_po <= fecha_fin:
            encontrados.add((fecha_po, url_zip))
    if sin_fecha:
        log.info("%s: %d ZIP(s) tipo PO sin fecha reconocible en la URL "
                 "(omitidos; revisar patron desde el runner)", FUENTE, sin_fecha)
    log.info("%s: %d ZIP(s) en rango %s..%s (de %d links .zip en la pagina)",
             FUENTE, len(encontrados), fecha_inicio, fecha_fin, len(hrefs))
    return sorted(encontrados)


def _procesar_zip(session, fecha_po: date, url_zip: str,
                  dir_extraidos: Path) -> list[dict]:
    """Descarga un ZIP de PO, inventaria su contenido y extrae candidatos.

    Devuelve las filas de inventario; los archivos candidatos quedan en
    dir_extraidos/{fecha}/. Un ZIP corrupto loggea WARNING y devuelve []."""
    filas: list[dict] = []
    with tempfile.TemporaryDirectory() as tmp:
        ruta_zip = Path(tmp) / "po.zip"
        r = session.get(url_zip, timeout=600)
        r.raise_for_status()
        ruta_zip.write_bytes(r.content)
        try:
            zf = zipfile.ZipFile(ruta_zip)
        except zipfile.BadZipFile:
            log.warning("%s: contenido no-ZIP o corrupto en %s", FUENTE, url_zip)
            return []
        with zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                candidato = _es_candidato(info.filename)
                filas.append({
                    "fecha_po": fecha_po.isoformat(),
                    "zip_url": url_zip,
                    "archivo_interno": info.filename,
                    "tamano": info.file_size,
                    "es_candidato": candidato,
                })
                if candidato:
                    destino_dir = dir_extraidos / fecha_po.isoformat()
                    destino_dir.mkdir(parents=True, exist_ok=True)
                    # solo el nombre base: evita zip-slip y rutas profundas
                    destino = destino_dir / Path(info.filename).name
                    with zf.open(info) as fh:
                        destino.write_bytes(fh.read())
    n_cand = sum(1 for f in filas if f["es_candidato"])
    log.info("%s: %s -> %d archivos internos, %d candidatos extraidos",
             FUENTE, url_zip, len(filas), n_cand)
    return filas


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    s = sesion_http()
    base = dir_datos or DIR_RAW
    dir_extraidos = base / FUENTE / "extraidos"
    rutas = []
    pos: list[tuple[date, str]] | None = None  # listado perezoso
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        if pos is None:
            pos = con_reintentos(
                lambda: listar_pos(s, fecha_inicio, fecha_fin), intentos=2)
        del_mes = [(f, u) for f, u in pos if ini <= f <= fin]
        if not del_mes:
            log.warning("%s: sin POs listados para %s..%s; particion no escrita",
                        FUENTE, ini, fin)
            continue
        filas: list[dict] = []
        for fecha_po, url_zip in del_mes:
            pausar()
            try:
                filas.extend(con_reintentos(
                    lambda f=fecha_po, u=url_zip: _procesar_zip(s, f, u, dir_extraidos),
                    intentos=2))
            except Exception as e:  # noqa: BLE001 - un ZIP malo no mata el mes
                log.warning("%s: fallo procesando %s (%s); continuo con el resto",
                            FUENTE, url_zip, e)
        if not filas:
            log.warning("%s: ningun ZIP procesable en %s..%s; particion no escrita",
                        FUENTE, ini, fin)
            continue
        df = pd.DataFrame(filas, columns=COLUMNAS_INVENTARIO)
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d archivos inventariados de %d ZIPs)",
                 FUENTE, destino.name, len(df), df.zip_url.nunique())
    registrar_manifiesto(FUENTE, rutas, dir_datos)
    return rutas


# ---------------------------------------------------------------------------
# TODO(parser del costo total) — pendiente de una muestra real:
# 1. Correr este extractor desde el runner para un rango corto (~7 dias) y
#    revisar el inventario parquet + data/raw/cen_po/extraidos/{fecha}/.
# 2. Identificar que archivo interno trae el costo total de operacion
#    (funcion objetivo PLEXOS). Candidatos tipicos: resumen del PO, salida
#    de costos del modelo, 'COSTOSVARIABLES' (ese trae costos variables POR
#    CENTRAL: serviria para RECONSTRUIR el costo multiplicando por
#    generacion, no para leerlo directo).
# 3. Implementar aqui `parsear_costo_total(ruta: Path) -> pd.DataFrame` con
#    columnas [fecha, costo_op_programado_usd] e integrarla a extract()
#    escribiendo una segunda familia de particiones (fuente 'cen_po_costo').
# 4. OJO anti-fuga: usar SIEMPRE la primera version del PO de cada dia (la
#    PID re-publica durante el dia); el inventario preserva zip_url para
#    poder auditar que version se uso.
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inicio", type=date.fromisoformat, required=True)
    p.add_argument("--fin", type=date.fromisoformat, required=True)
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()
    extract(a.inicio, a.fin, forzar=a.forzar)
