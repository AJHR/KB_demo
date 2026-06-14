"""Capa compartida para consumir la API SIP del Coordinador Electrico Nacional.

Endpoints documentados en sources/costos_sen/anexos/coordinador.md (seccion 2).
Host: https://sipub.api.coordinador.cl (gateway 3scale). Autenticacion por
`user_key` como query param; se obtiene registrandose en
https://portal.api.coordinador.cl/ y aca se lee del entorno
(COORDINADOR_USER_KEY, secret en GitHub Actions).

ADVERTENCIA: la red del sandbox de desarrollo esta bloqueada, asi que NADA de
este modulo pudo probarse contra los endpoints reales. Por eso todo es
deliberadamente defensivo:

- `get_paginado` soporta los dos patrones de paginacion observados en
  clientes de terceros (URL 'next' estilo DRF, o `page` incremental hasta
  pagina vacia), ademas de respuestas que son una lista cruda sin envoltorio.
- `buscar_columna` / `extraer_fecha_hora` mapean nombres de campo inciertos.
- `filtrar_barras` usa regex laxos (PATRONES_BARRA) porque el nombre exacto
  de cada barra en la API es incierto.

La capa de red queda separada de los parsers: los parsers de cada extractor
se prueban offline con fixtures inline en tests_offline.py.
"""

from __future__ import annotations

import os
import re
import time
import unicodedata
from datetime import date, timedelta
from typing import Iterator
from urllib.parse import urljoin

import pandas as pd

from comun import ErrorCredencial, log

# ---------------------------------------------------------------------------
# Rate limiting conservador.
# Evidencia de terceros (coordinador.md seccion 2): un cliente usa 60 req/hora
# como tasa segura en algunos planes. Default 1.2 s entre requests,
# configurable via la variable de entorno CEN_API_PAUSA_SEG.
# ---------------------------------------------------------------------------
PAUSA_SEG_DEFAULT = 1.2

# Tope de seguridad para no quedar en un loop infinito de paginacion. Es solo
# un backstop: get_paginado ya corta por pagina vacia, pagina repetida o total
# alcanzado. Con 500 un mes pesado de CMg (todas las barras x 24h x ~30d, ~700
# paginas a limit=1000) se TRUNCABA en silencio; 5000 cubre el mes completo y
# deja que la instrumentacion muestre el conteo real de paginas.
MAX_PAGINAS = 5000


def pausa_seg() -> float:
    """Pausa (segundos) entre requests; lee CEN_API_PAUSA_SEG con default 1.2."""
    crudo = os.environ.get("CEN_API_PAUSA_SEG", "")
    try:
        valor = float(crudo) if crudo else PAUSA_SEG_DEFAULT
    except ValueError:
        log.warning("CEN_API_PAUSA_SEG invalido (%r); uso default %.1fs",
                    crudo, PAUSA_SEG_DEFAULT)
        valor = PAUSA_SEG_DEFAULT
    return max(0.0, valor)


def pausar() -> None:
    """Pausa de rate limiting; llamar ANTES de cada request a la API SIP."""
    time.sleep(pausa_seg())


def user_key() -> str:
    """user_key de la API SIP desde el entorno; falla con mensaje accionable."""
    key = os.environ.get("COORDINADOR_USER_KEY", "").strip()
    if not key:
        raise ErrorCredencial(
            "Falta la variable de entorno COORDINADOR_USER_KEY: registrar un "
            "usuario en portal.api.coordinador.cl (plan Consulta de Datos), "
            "obtener el user_key y configurar el secret COORDINADOR_USER_KEY "
            "(en GitHub Actions: Settings > Secrets and variables > Actions).")
    return key


def dias_entre(ini: date, fin: date) -> Iterator[date]:
    """Itera los dias entre dos fechas, ambas inclusive."""
    d = ini
    while d <= fin:
        yield d
        d += timedelta(days=1)


# ---------------------------------------------------------------------------
# Capa de red: GET con paginacion defensiva
# ---------------------------------------------------------------------------

# Claves que sugieren que la respuesta dict esta paginada.
_CLAVES_PAGINACION = {"next", "previous", "prev", "page", "pages", "total_pages",
                      "count", "total", "limit", "offset", "per_page", "size"}


def _get_json(session, url: str, params: dict | None = None):
    """GET + parseo JSON con mensaje de error util (incluye inicio del body)."""
    r = session.get(url, params=params, timeout=120)
    r.raise_for_status()
    try:
        return r.json()
    except ValueError as e:
        raise ValueError(f"respuesta no-JSON de {url}: {r.text[:300]!r}") from e


def extraer_filas(json_obj) -> tuple[list, str | None]:
    """Extrae (filas, url_siguiente) de una respuesta JSON de la API SIP.

    Defensivo ante las formas observadas/posibles:
    - lista cruda -> es la lista de filas, sin paginacion;
    - dict con lista bajo 'data', 'results' o 'items' (en ese orden);
    - 'next' (URL de la pagina siguiente) si existe en la raiz del dict.
    """
    if isinstance(json_obj, list):
        return json_obj, None
    if isinstance(json_obj, dict):
        siguiente = json_obj.get("next")
        for clave in ("data", "results", "items"):
            valor = json_obj.get(clave)
            if isinstance(valor, list):
                return valor, siguiente
        return [], siguiente
    return [], None


def _total_declarado(json_obj) -> int | None:
    """Total de filas declarado por la API, si lo informa (count/total/...)."""
    if not isinstance(json_obj, dict):
        return None
    for clave in ("count", "total", "total_rows", "totalElements"):
        valor = json_obj.get(clave)
        if isinstance(valor, int) and not isinstance(valor, bool):
            return valor
    return None


def get_paginado(session, url: str, params: dict | None = None) -> list:
    """Descarga TODAS las paginas de un endpoint SIP; devuelve la lista de filas.

    Estrategia (defensiva, sin haber visto la API real):
    1. Si la respuesta es una lista cruda -> se asume completa.
    2. Si el dict trae 'next' (URL) -> se sigue 'next' hasta agotarlo
       (reinyectando user_key si la URL 'next' no lo trae).
    3. Si el dict no tiene NINGUNA clave de paginacion -> se asume completa.
    4. Si hay indicios de paginacion sin 'next' -> page+=1 hasta pagina vacia,
       hasta alcanzar el total declarado (count/total), o hasta detectar que
       el servidor ignora 'page' (pagina identica a la anterior).
    Tope de seguridad: MAX_PAGINAS (500) paginas.
    Aplica la pausa de rate limiting entre paginas.
    """
    params = dict(params or {})
    pausa = pausa_seg()
    t0 = time.monotonic()
    estado = {"paginas": 1, "tope": False}

    def _fin(filas: list) -> list:
        # Instrumentacion de diagnostico: cuanto costo y si paginó hasta el
        # tope (señal de truncacion o de filtro de fecha ignorado por la API).
        dt = time.monotonic() - t0
        etiqueta = url.rstrip("/").rsplit("/", 1)[-1] or url
        log.info("get_paginado [%s]: %d filas en %d pagina(s), %.1fs "
                 "(%.2fs/pag)%s", etiqueta, len(filas), estado["paginas"], dt,
                 dt / max(estado["paginas"], 1),
                 " [TOPE MAX_PAGINAS — datos posiblemente truncados]"
                 if estado["tope"] else "")
        return filas

    j = _get_json(session, url, params)
    filas, siguiente = extraer_filas(j)

    # Caso 1: lista cruda, sin envoltorio de paginacion.
    if isinstance(j, list):
        return _fin(filas)

    # Caso 2: paginacion por URL 'next'.
    if isinstance(siguiente, str) and siguiente.strip():
        for _ in range(2, MAX_PAGINAS + 1):
            time.sleep(pausa)
            estado["paginas"] += 1
            url_sig = siguiente if siguiente.startswith("http") else urljoin(url, siguiente)
            extra = ({"user_key": params["user_key"]}
                     if "user_key" in params and "user_key=" not in url_sig else None)
            j = _get_json(session, url_sig, extra)
            nuevas, siguiente = extraer_filas(j)
            if not nuevas:
                break
            filas.extend(nuevas)
            if not (isinstance(siguiente, str) and siguiente.strip()):
                break
        else:
            estado["tope"] = True
            log.warning("get_paginado: tope de %d paginas alcanzado en %s",
                        MAX_PAGINAS, url)
        return _fin(filas)

    # Caso 3: dict sin ningun indicio de paginacion -> respuesta completa.
    if not isinstance(j, dict) or not (_CLAVES_PAGINACION & set(j.keys())):
        return _fin(filas)

    total = _total_declarado(j)
    if not filas or (total is not None and len(filas) >= total):
        return _fin(filas)

    # Caso 4: paginacion por parametro page incremental.
    pagina = int(params.get("page", 1) or 1)
    pagina_previa = filas[:]
    for _ in range(2, MAX_PAGINAS + 1):
        pagina += 1
        time.sleep(pausa)
        estado["paginas"] += 1
        j = _get_json(session, url, dict(params, page=pagina))
        nuevas, _ = extraer_filas(j)
        if not nuevas:
            break
        if nuevas == pagina_previa:
            # El servidor ignora 'page' y repite la misma pagina: cortar
            # aca evita duplicar filas hasta el tope de paginas.
            log.debug("get_paginado: %s ignora 'page'; corto en pagina %d",
                      url, pagina)
            break
        filas.extend(nuevas)
        pagina_previa = nuevas
        if total is not None and len(filas) >= total:
            break
    else:
        estado["tope"] = True
        log.warning("get_paginado: tope de %d paginas alcanzado en %s",
                    MAX_PAGINAS, url)
    return _fin(filas)


# ---------------------------------------------------------------------------
# Mapeo defensivo de columnas (la API SIP no tiene esquema documentado)
# ---------------------------------------------------------------------------

def _sin_acentos(texto: str) -> str:
    """Quita diacriticos: 'CHARRÚA' -> 'CHARRUA' (NFD + drop combining)."""
    nfd = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in nfd if not unicodedata.combining(c))


def _normalizar(nombre: str) -> str:
    """Clave laxa de comparacion: minusculas, sin acentos ni separadores."""
    return re.sub(r"[^a-z0-9]", "", _sin_acentos(str(nombre)).lower())


def buscar_columna(df: pd.DataFrame, candidatos) -> str | None:
    """Primer candidato presente en df.columns; exacto primero, luego laxo.

    La busqueda laxa ignora mayusculas, acentos y separadores, de modo que
    'fecha_hora' encuentra tambien 'FechaHora' o 'fecha-hora'."""
    for c in candidatos:
        if c in df.columns:
            return c
    laxas: dict[str, str] = {}
    for col in df.columns:
        laxas.setdefault(_normalizar(col), str(col))
    for c in candidatos:
        col = laxas.get(_normalizar(c))
        if col is not None:
            return col
    return None


def a_datetime(serie: pd.Series) -> pd.Series:
    """to_datetime defensivo: formatos mixtos, errores -> NaT."""
    try:
        return pd.to_datetime(serie, errors="coerce", format="mixed")
    except (TypeError, ValueError):
        return pd.to_datetime(serie, errors="coerce")


# Variantes de nombre observadas/plausibles para fecha y hora en la API SIP.
CANDIDATOS_FECHA = ["fecha", "fecha_dia", "fecha_operacion", "fecha_medicion",
                    "dia", "date"]
CANDIDATOS_HORA = ["hora", "hra", "hour"]
CANDIDATOS_FECHA_HORA = ["fecha_hora", "fechahora", "fecha_hora_operacion",
                         "datetime", "timestamp"]


def extraer_fecha_hora(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Series (fecha ISO str, hora Int64) desde columnas de nombre incierto.

    Prefiere fecha + hora explicitas; si no, descompone 'fecha_hora'.
    La hora se deja tal cual la entrega la API (sin normalizar 0-23 vs 1-24:
    eso se decide en la tabla maestra con datos reales a la vista)."""
    col_fecha = buscar_columna(df, CANDIDATOS_FECHA)
    col_hora = buscar_columna(df, CANDIDATOS_HORA)
    col_fh = buscar_columna(df, CANDIDATOS_FECHA_HORA)

    if col_fecha is not None:
        fecha = a_datetime(df[col_fecha]).dt.date.astype(str)
    elif col_fh is not None:
        fecha = a_datetime(df[col_fh]).dt.date.astype(str)
    else:
        raise ValueError(
            f"sin columna de fecha reconocible; columnas: {list(df.columns)}")

    if col_hora is not None:
        hora = pd.to_numeric(df[col_hora], errors="coerce").astype("Int64")
    elif col_fh is not None:
        hora = a_datetime(df[col_fh]).dt.hour.astype("Int64")
    else:
        hora = pd.Series(pd.NA, index=df.index, dtype="Int64")
    return fecha, hora


# ---------------------------------------------------------------------------
# Barras de referencia para costos marginales
# ---------------------------------------------------------------------------

# Nombres "oficiales" segun las descargas web del CEN (barras 220 kV de
# referencia historica del SIC/SING). OJO: el nombre exacto que entrega la
# API es incierto -> el filtrado real usa PATRONES_BARRA, no esta lista.
BARRAS_REFERENCIA = [
    "BA S/E QUILLOTA 220KV",
    "BA S/E CRUCERO 220KV",
    "BA S/E CHARRUA 220KV",
    "BA S/E POLPAICO 220KV",
    "BA S/E ALTO JAHUEL 220KV",
]

# Regex laxos (case-insensitive, aplicados sin acentos) para reconocer las
# barras de referencia ante variantes de nombre ('Quillota 220', 'BA S/E
# CHARRÚA 220KV', 'ALTO-JAHUEL 220', etc.).
PATRONES_BARRA = [
    r"QUILLOTA.*220",
    r"CRUCERO.*220",
    r"CHARRUA.*220",
    r"POLPAICO.*220",
    r"ALTO.?JAHUEL.*220",
]

_RE_BARRAS = re.compile("|".join(f"(?:{p})" for p in PATRONES_BARRA),
                        re.IGNORECASE)


def filtrar_barras(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Filtra el DataFrame a las barras de referencia (PATRONES_BARRA).

    Case-insensitive e insensible a acentos. Si la columna no existe devuelve
    un DataFrame vacio (con las mismas columnas) en vez de morir."""
    if col not in df.columns:
        log.warning("filtrar_barras: columna %r inexistente (columnas: %s)",
                    col, list(df.columns))
        return df.head(0).copy()
    if df.empty:
        return df.copy()
    normalizadas = df[col].astype(str).map(_sin_acentos)
    mascara = normalizadas.str.contains(_RE_BARRAS, na=False)
    return df[mascara].copy()


# ---------------------------------------------------------------------------
# Parser base de respuestas de costo marginal (compartido por los extractores
# de CMg real y CMg programado; cada uno expone su propio parsear_respuesta)
# ---------------------------------------------------------------------------

CANDIDATOS_BARRA = ["barra_info", "nmb_barra_info", "barra", "nombre_barra",
                    "barra_mnemotecnico", "nemotecnico_barra",
                    "barra_referencia", "nombre_barra_referencia",
                    "barra_transferencia"]
CANDIDATOS_CMG = ["cmg_usd_mwh_", "cmg_usd_mwh", "cmg", "costo_en_dolares",
                  "cmg_usd", "costo_marginal"]

COLUMNAS_CMG = ["barra", "fecha", "hora", "cmg_usd_mwh"]


def parsear_cmg(json_obj, preservar=()) -> pd.DataFrame:
    """Parser defensivo de respuestas de CMg -> [barra, fecha, hora, cmg_usd_mwh].

    - `json_obj` puede ser la respuesta completa (dict) o la lista de filas.
    - Mapea nombres de campo inciertos (CANDIDATOS_BARRA / CANDIDATOS_CMG).
    - Filtra a las barras de referencia via filtrar_barras.
    - `preservar`: nombres de columnas extra (p.ej. metadatos de publicacion)
      que se copian tal cual si existen en la respuesta.
    """
    filas, _ = extraer_filas(json_obj)
    if not filas:
        return pd.DataFrame(columns=COLUMNAS_CMG)
    df = pd.DataFrame(filas)
    col_barra = buscar_columna(df, CANDIDATOS_BARRA)
    col_cmg = buscar_columna(df, CANDIDATOS_CMG)
    if col_barra is None or col_cmg is None:
        raise ValueError(
            "respuesta CMg sin campos reconocibles de barra/cmg; columnas: "
            f"{list(df.columns)}")
    fecha, hora = extraer_fecha_hora(df)
    out = pd.DataFrame({
        "barra": df[col_barra].astype(str),
        "fecha": fecha,
        "hora": hora,
        "cmg_usd_mwh": pd.to_numeric(df[col_cmg], errors="coerce"),
    })
    for extra in preservar:
        col = buscar_columna(df, [extra])
        if col is not None and extra not in out.columns:
            out[extra] = df[col]
    out = filtrar_barras(out, "barra")
    return out.reset_index(drop=True)
