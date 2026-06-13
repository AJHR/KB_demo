"""Validadores de calidad sobre data/raw y data/processed.

Tres validaciones + un reporte en wiki/:

- `validar_completitud(dir_raw)`: por fuente, % de dias presentes entre la
  primera y la ultima fecha observada, y lista de huecos (gaps > 1 dia).
- `validar_outliers(df, col, k=4.0)`: filas sospechosas por desviacion
  robusta (|x - mediana| > k * 1.4826 * MAD).
- `validar_consistencia_cruzada(dir_raw)`: si existen cen_demanda y
  cen_generacion, verifica a nivel diario que
  |suma_generacion - demanda| / demanda <= 12% (perdidas + autoconsumo).
- `generar_reporte(dir_raw, ruta_salida)`: escribe wiki/calidad_datos.md
  (frontmatter YAML segun CLAUDE.md) con los resultados; si aun no hay
  datos lo dice explicitamente (estado: esperando primer backfill).

CLI:
    python3 validadores.py --reporte            # escribe wiki/calidad_datos.md
    python3 validadores.py                      # imprime completitud por stdout
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from cen_api import a_datetime, buscar_columna
from comun import DIR_RAW, RAIZ_REPO, log

# Variantes de columna de fecha en las particiones crudas.
CANDIDATOS_FECHA = ["fecha", "fecha_po", "fecha_hora", "date", "dia"]

COLUMNAS_COMPLETITUD = ["fuente", "fecha_min", "fecha_max", "dias_presentes",
                        "dias_esperados", "pct_completitud", "n_huecos", "huecos"]

# Fuente -> columna numerica a auditar por outliers en el reporte.
OUTLIERS_POR_FUENTE = {
    "cen_cmg_real": "cmg_usd_mwh",
    "cen_cmg_programado": "cmg_usd_mwh",
    "cen_demanda": "demanda_mwh",
    "cen_generacion": "generacion_mwh",
    "cen_embalses": "cota_msnm",
}


def _cargar_fuente(dir_raw: Path, fuente: str) -> pd.DataFrame | None:
    """Concatena todas las particiones parquet de una fuente; None si no hay."""
    base = Path(dir_raw) / fuente
    if not base.is_dir():
        return None
    partes = []
    for ruta in sorted(base.rglob("*.parquet")):
        try:
            partes.append(pd.read_parquet(ruta))
        except Exception as e:  # noqa: BLE001 - una particion corrupta no mata el reporte
            log.warning("validadores: no se pudo leer %s (%s)", ruta, e)
    if not partes:
        return None
    return pd.concat(partes, ignore_index=True)


def validar_completitud(dir_raw: Path | None = None) -> pd.DataFrame:
    """Completitud diaria por fuente bajo dir_raw.

    Devuelve un DataFrame [fuente, fecha_min, fecha_max, dias_presentes,
    dias_esperados, pct_completitud, n_huecos, huecos] donde `huecos` lista
    los rangos faltantes (gaps de mas de 1 dia entre fechas consecutivas)."""
    dir_raw = Path(dir_raw) if dir_raw else DIR_RAW
    filas = []
    if not dir_raw.is_dir():
        return pd.DataFrame(columns=COLUMNAS_COMPLETITUD)
    for sub in sorted(p for p in dir_raw.iterdir() if p.is_dir()):
        fuente = sub.name
        df = _cargar_fuente(dir_raw, fuente)
        if df is None or df.empty:
            continue
        col = buscar_columna(df, CANDIDATOS_FECHA)
        if col is None:
            log.warning("validar_completitud: %s sin columna de fecha "
                        "reconocible (columnas: %s)", fuente, list(df.columns))
            continue
        fechas = sorted(set(a_datetime(df[col]).dt.date.dropna()))
        if not fechas:
            continue
        f_min, f_max = fechas[0], fechas[-1]
        esperados = (f_max - f_min).days + 1
        presentes = len(fechas)
        huecos = []
        for a, b in zip(fechas, fechas[1:]):
            if (b - a).days > 1:
                huecos.append(f"{(a + timedelta(days=1)).isoformat()}.."
                              f"{(b - timedelta(days=1)).isoformat()}")
        filas.append({
            "fuente": fuente,
            "fecha_min": f_min.isoformat(),
            "fecha_max": f_max.isoformat(),
            "dias_presentes": presentes,
            "dias_esperados": esperados,
            "pct_completitud": round(100.0 * presentes / esperados, 1),
            "n_huecos": len(huecos),
            "huecos": "; ".join(huecos[:20]) + (" ..." if len(huecos) > 20 else ""),
        })
    return pd.DataFrame(filas, columns=COLUMNAS_COMPLETITUD)


def validar_outliers(df: pd.DataFrame, col: str, k: float = 4.0) -> pd.DataFrame:
    """Filas sospechosas por desviacion robusta: |x - mediana| > k * MAD escalado.

    MAD escalado = 1.4826 * mediana(|x - mediana|) (consistente con sigma
    para distribucion normal). Si la serie es constante (MAD = 0), cualquier
    desviacion no nula se marca sospechosa. Devuelve las filas originales
    con columnas extra _mediana y _desviacion_robusta."""
    if col not in df.columns or df.empty:
        return df.head(0).copy()
    serie = pd.to_numeric(df[col], errors="coerce")
    mediana = serie.median()
    mad = (serie - mediana).abs().median()
    escala = 1.4826 * mad
    if pd.isna(escala) or escala == 0:
        desv = (serie - mediana).abs()
        mascara = serie.notna() & (desv > 0)
    else:
        desv = (serie - mediana).abs() / escala
        mascara = serie.notna() & (desv > k)
    sospechosas = df.loc[mascara].copy()
    sospechosas["_mediana"] = mediana
    sospechosas["_desviacion_robusta"] = desv.loc[mascara].round(1)
    return sospechosas


def _agregado_diario(df: pd.DataFrame, candidatos_valor: list[str]) -> pd.Series | None:
    """Suma diaria de la primera columna candidata; indice = fecha ISO str."""
    col_f = buscar_columna(df, CANDIDATOS_FECHA)
    col_v = buscar_columna(df, candidatos_valor)
    if col_f is None or col_v is None:
        return None
    fechas = a_datetime(df[col_f]).dt.date.astype(str)
    valores = pd.to_numeric(df[col_v], errors="coerce")
    return valores.groupby(fechas).sum()


def validar_consistencia_cruzada(dir_raw: Path | None = None,
                                 tolerancia: float = 0.12) -> list[str]:
    """Chequeo fisico diario: |suma_generacion - demanda| / demanda <= 12%.

    El 12% absorbe perdidas de transmision + autoconsumo (y diferencias de
    convencion horaria). Solo evaluable si existen cen_demanda y
    cen_generacion bajo dir_raw; si falta alguna devuelve []. Devuelve un
    string descriptivo por cada dia que viola la tolerancia."""
    dir_raw = Path(dir_raw) if dir_raw else DIR_RAW
    dem = _cargar_fuente(dir_raw, "cen_demanda")
    gen = _cargar_fuente(dir_raw, "cen_generacion")
    if dem is None or gen is None or dem.empty or gen.empty:
        log.info("consistencia cruzada: faltan cen_demanda y/o cen_generacion; "
                 "no evaluable")
        return []
    serie_dem = _agregado_diario(dem, ["demanda_mwh", "demanda"])
    serie_gen = _agregado_diario(gen, ["generacion_mwh", "generacion", "mwh"])
    if serie_dem is None or serie_gen is None:
        log.warning("consistencia cruzada: columnas no reconocibles")
        return []
    violaciones = []
    for fecha in sorted(set(serie_dem.index) & set(serie_gen.index)):
        d, g = serie_dem[fecha], serie_gen[fecha]
        if pd.isna(d) or pd.isna(g) or d == 0:
            continue
        desvio = abs(g - d) / abs(d)
        if desvio > tolerancia:
            violaciones.append(
                f"{fecha}: generacion {g:,.0f} MWh vs demanda {d:,.0f} MWh "
                f"(desvio {desvio:.1%} > {tolerancia:.0%})")
    return violaciones


def _tabla_md(df: pd.DataFrame) -> str:
    """Tabla markdown sin depender de tabulate (df.to_markdown lo requiere)."""
    if df.empty:
        return "_(sin datos)_"
    cols = [str(c) for c in df.columns]
    lineas = ["| " + " | ".join(cols) + " |",
              "|" + "|".join("---" for _ in cols) + "|"]
    for _, fila in df.iterrows():
        celdas = [str(v).replace("|", "\\|").replace("\n", " ") for v in fila]
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas)


def generar_reporte(dir_raw: Path | None = None,
                    ruta_salida: Path | None = None) -> Path:
    """Escribe wiki/calidad_datos.md con completitud, outliers y consistencia.

    Frontmatter YAML segun la gobernanza del KB (CLAUDE.md). Si no hay datos
    el reporte lo dice explicitamente en vez de fingir tablas vacias."""
    dir_raw = Path(dir_raw) if dir_raw else DIR_RAW
    ruta_salida = (Path(ruta_salida) if ruta_salida
                   else RAIZ_REPO / "wiki" / "calidad_datos.md")
    hoy = date.today().isoformat()
    completitud = validar_completitud(dir_raw)

    L = [
        "---",
        "title: Calidad de datos del pipeline de costos SEN",
        "sources:",
        "  - data/processed/tabla_maestra.parquet",
        f"last_synthesized: {hoy}",
        "---",
        "",
        "# Calidad de datos — pipeline de costos SEN",
        "",
        f"> Generado automaticamente por `tools/etl/validadores.py --reporte` el {hoy}.",
        f"> Directorio analizado: `{dir_raw}`.",
        "",
    ]

    if completitud.empty:
        L += [
            "**Estado: esperando primer backfill.**",
            "",
            "No se encontraron particiones de datos en el directorio raw. "
            "Correr los extractores (backfill historico) y regenerar este "
            "reporte.",
            "",
        ]
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        ruta_salida.write_text("\n".join(L) + "\n", encoding="utf-8")
        log.info("reporte de calidad (sin datos) escrito en %s", ruta_salida)
        return ruta_salida

    L += ["## Completitud por fuente", "", _tabla_md(completitud), ""]

    L += ["## Outliers (|x - mediana| > 4 · MAD escalado)", ""]
    alguna = False
    for fuente, col in OUTLIERS_POR_FUENTE.items():
        df = _cargar_fuente(dir_raw, fuente)
        if df is None or df.empty or col not in df.columns:
            continue
        alguna = True
        sosp = validar_outliers(df, col)
        L.append(f"- `{fuente}.{col}`: {len(sosp)} filas sospechosas de "
                 f"{len(df)} ({100.0 * len(sosp) / len(df):.2f}%)")
        if not sosp.empty:
            cols_muestra = [c for c in ("fecha", "barra", "tecnologia", "embalse",
                                        col, "_desviacion_robusta")
                            if c in sosp.columns]
            L += ["", _tabla_md(sosp[cols_muestra].head(5)), ""]
    if not alguna:
        L.append("_(ninguna fuente con columnas numericas conocidas todavia)_")
    L.append("")

    L += ["## Consistencia cruzada: generacion vs demanda (diario)", ""]
    evaluable = ((dir_raw / "cen_demanda").is_dir()
                 and (dir_raw / "cen_generacion").is_dir())
    if not evaluable:
        L.append("_No evaluable: faltan `cen_demanda` y/o `cen_generacion`._")
    else:
        violaciones = validar_consistencia_cruzada(dir_raw)
        if violaciones:
            L += [f"{len(violaciones)} dia(s) violan "
                  "|suma_generacion - demanda| / demanda <= 12%:", ""]
            L += [f"- {v}" for v in violaciones]
        else:
            L.append("Sin violaciones (tolerancia 12%: perdidas + autoconsumo).")
    L.append("")

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    ruta_salida.write_text("\n".join(L) + "\n", encoding="utf-8")
    log.info("reporte de calidad escrito en %s", ruta_salida)
    return ruta_salida


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reporte", action="store_true",
                   help="escribe wiki/calidad_datos.md")
    p.add_argument("--dir-raw", type=Path, default=None,
                   help="directorio raw alternativo (default data/raw)")
    p.add_argument("--salida", type=Path, default=None,
                   help="ruta alternativa del reporte")
    a = p.parse_args()
    if a.reporte:
        ruta = generar_reporte(a.dir_raw, a.salida)
        print(f"reporte escrito en {ruta}")
    else:
        print(validar_completitud(a.dir_raw).to_string(index=False))
