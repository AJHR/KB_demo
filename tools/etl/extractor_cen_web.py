"""Sonda de descarga KEYLESS del Coordinador (sin user_key).

Decision del usuario (2026-06-13): antes de asumir que se necesita user_key,
PROBAR en vivo en el runner de GitHub (que si tiene red) los candidatos de
descarga sin credencial que la investigacion dejo marcados como "inferido /
no verificado" (sources/costos_sen/anexos/descarga_publica_cen.md):

  - endpoint WordPress historico  /wp-json/costo-marginal/v1/data
  - patrones export.csv?from=&to=  de las paginas de graficos
  - subdominio cmgreal.coordinador.cl
  - (control) API SIP v4 SIN user_key -> se espera 401/403, confirma que la
    key es realmente obligatoria

Este modulo NO asume que algo funciona: prueba cada candidato, registra el
resultado HTTP real (status, content-type, si parsea como datos tabulares,
muestra) en data/raw/cen_web/sonda_keyless.parquet, y SI algun candidato
entrega datos reales de CMg/demanda, los guarda en data/raw/cen_web_{serie}/.

El veredicto se lee en el log del job y en el parquet de la sonda. Es un
extractor de diagnostico: siempre "tiene exito" (escribe el reporte) aunque
todos los candidatos fallen, para no disparar el issue automatico de fallos.
"""

from __future__ import annotations

import io
import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from comun import (DIR_RAW, escribir_parquet_atomico, log,
                   registrar_manifiesto)

FUENTE = "cen_web"

# Headers de navegador: varios endpoints WP/Highcharts validan UA y Referer.
HEADERS_NAVEGADOR = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    "Accept": "text/csv,application/json,text/plain,*/*",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
}


def _candidatos(ini: date, fin: date) -> list[dict]:
    f, t = ini.isoformat(), fin.isoformat()
    base = "https://www.coordinador.cl"
    g = f"{base}/mercados/graficos/costos-marginales"
    o = f"{base}/operacion/graficos/operacion-real"
    return [
        # --- CMg real (variable objetivo) ---
        {"serie": "cmg_real", "nombre": "wp_json_costo_marginal",
         "url": f"{base}/wp-json/costo-marginal/v1/data",
         "referer": f"{g}/costo-marginal-real/"},
        {"serie": "cmg_real", "nombre": "export_csv_cmg_real_nuevo",
         "url": f"{g}/costo-marginal-real-nuevo/export.csv?from={f}&to={t}",
         "referer": f"{g}/costo-marginal-real-nuevo/"},
        {"serie": "cmg_real", "nombre": "export_csv_cmg_real",
         "url": f"{g}/costo-marginal-real/export.csv?from={f}&to={t}",
         "referer": f"{g}/costo-marginal-real/"},
        {"serie": "cmg_real", "nombre": "cmgreal_subdominio",
         "url": "https://cmgreal.coordinador.cl/",
         "referer": None},
        # --- demanda real ---
        {"serie": "demanda", "nombre": "export_csv_demanda_real",
         "url": f"{o}/demanda-real/export.csv?from={f}&to={t}",
         "referer": f"{o}/demanda-real/"},
        # --- generacion real ---
        {"serie": "generacion", "nombre": "export_csv_generacion_real",
         "url": f"{o}/generacion-real/export.csv?from={f}&to={t}",
         "referer": f"{o}/generacion-real/"},
        # --- control: API SIP v4 SIN user_key (se espera 401/403) ---
        {"serie": "control", "nombre": "sip_v4_sin_key",
         "url": ("https://sipub.api.coordinador.cl/costo-marginal-real/"
                 f"v4/findByDate?startDate={f}&endDate={t}&page=1&limit=10"),
         "referer": None},
    ]


def _clasificar(texto: str, content_type: str) -> tuple[str, int]:
    """Devuelve (clase, n_filas_estimadas). clase en:
    datos_csv / datos_json / html_spa / vacio / no_tabular."""
    s = texto.lstrip()
    if not s:
        return "vacio", 0
    bajo = s[:2000].lower()
    if s[:1] in "{[" or "application/json" in content_type:
        try:
            j = json.loads(texto)
            n = len(j) if isinstance(j, list) else len(
                j.get("data", j.get("results", j.get("items", []))))
            return ("datos_json", n) if n else ("no_tabular", 0)
        except Exception:
            pass
    if "<html" in bajo or "<!doctype html" in bajo:
        return "html_spa", 0
    # CSV/TSV: >=2 lineas y delimitador consistente
    lineas = [ln for ln in s.splitlines() if ln.strip()][:50]
    if len(lineas) >= 2:
        for delim in (";", ",", "\t"):
            if all(delim in ln for ln in lineas[:3]):
                return "datos_csv", len(lineas)
    return "no_tabular", 0


def _probar(s, cand: dict) -> dict:
    headers = dict(HEADERS_NAVEGADOR)
    if cand["referer"]:
        headers["Referer"] = cand["referer"]
    res = {"serie": cand["serie"], "candidato": cand["nombre"],
           "url": cand["url"].split("?")[0]}
    try:
        r = s.get(cand["url"], headers=headers, timeout=30,
                  allow_redirects=True)
        ct = r.headers.get("Content-Type", "")
        clase, nfilas = _clasificar(r.text, ct)
        res.update(status=r.status_code, content_type=ct[:80],
                   bytes=len(r.content), url_final=r.url.split("?")[0],
                   clase=clase, filas_estimadas=nfilas,
                   keyless_ok=bool(r.ok and clase in ("datos_csv", "datos_json")),
                   muestra=r.text[:300].replace("\n", " ⏎ "))
    except Exception as e:  # noqa: BLE001 - sonda: registrar, no morir
        res.update(status=None, content_type=None, bytes=0,
                   url_final=None, clase="error", filas_estimadas=0,
                   keyless_ok=False, muestra=f"{type(e).__name__}: {e}"[:300])
    estado = "OK-DATOS" if res["keyless_ok"] else (
        f"{res.get('clase')}/{res.get('status')}")
    log.info("sonda keyless [%s] %s -> %s", cand["serie"], cand["nombre"], estado)
    return res


def _guardar_datos_keyless(s, cand: dict, dir_datos: Path) -> None:
    """Si un candidato CSV/JSON dio datos, los persiste crudos para inspeccion
    (parser dedicado se construye despues, cuando sepamos el esquema real)."""
    try:
        headers = dict(HEADERS_NAVEGADOR)
        if cand["referer"]:
            headers["Referer"] = cand["referer"]
        r = s.get(cand["url"], headers=headers, timeout=60)
        crudo = (dir_datos or DIR_RAW) / f"cen_web_{cand['serie']}"
        crudo.mkdir(parents=True, exist_ok=True)
        ext = "json" if cand["clase"] == "datos_json" else "csv"
        (crudo / f"{cand['nombre']}.{ext}").write_text(r.text)
        log.info("sonda keyless: datos crudos guardados en %s", crudo)
    except Exception as e:  # noqa: BLE001
        log.warning("sonda keyless: no se pudo guardar crudo de %s (%s)",
                    cand["nombre"], e)


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    # Ventana reciente y corta para los export.csv (rango grande puede fallar
    # distinto); el objetivo es detectar si el endpoint responde con datos.
    fin = fecha_fin
    ini = max(fecha_inicio, fin - timedelta(days=7))
    from comun import sesion_http

    s = sesion_http()
    s.headers.update(HEADERS_NAVEGADOR)

    resultados = [_probar(s, c) for c in _candidatos(ini, fin)]
    df = pd.DataFrame(resultados)

    destino = (dir_datos or DIR_RAW) / FUENTE / "sonda_keyless.parquet"
    escribir_parquet_atomico(df, destino)

    ganadores = df[df.keyless_ok]
    if not ganadores.empty:
        log.info("sonda keyless: %d candidato(s) con DATOS sin key: %s",
                 len(ganadores), list(ganadores.candidato))
        cands = {c["nombre"]: c for c in _candidatos(ini, fin)}
        for _, fila in ganadores.iterrows():
            cand = cands[fila.candidato]
            cand["clase"] = fila.clase
            _guardar_datos_keyless(s, cand, dir_datos or DIR_RAW)
    else:
        log.warning("sonda keyless: NINGUN candidato entrego datos sin key; "
                    "la API SIP v4 con user_key es el camino robusto. "
                    "Ver data/raw/cen_web/sonda_keyless.parquet")

    registrar_manifiesto(FUENTE, [destino], dir_datos,
                         candidatos=len(resultados),
                         keyless_ok=int(ganadores.shape[0]))
    return [destino]


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inicio", type=date.fromisoformat, required=True)
    p.add_argument("--fin", type=date.fromisoformat, required=True)
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()
    for r in extract(a.inicio, a.fin, forzar=a.forzar):
        print(r)
