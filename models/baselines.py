"""Baselines obligatorios de la fase 3 — evaluados SOLO via evaluacion.py.

1. Persistencia: costo de manana = costo de hoy (definicion de la mision).
   Matiz operacional: a las 20:00 del dia D el costo de D aun no cierra, asi
   que la persistencia "de hoy" (lag 1) tiene fuga operacional leve. Se
   reportan ambas variantes:
     - persistencia_lag1 (definicion literal; usa saltar_antifuga, referencia)
     - persistencia_lag2 (implementable en produccion)
2. Estacional: promedio del mismo dia de semana de las ultimas 4 semanas
   (lags 7/14/21/28 — conforme regla 20:00).
3. LightGBM: features de calendario, clima, hidrologia, combustibles y
   lags/rolling del costo — solo columnas declaradas conformes en
   metadatos_features.json (verificacion anti-fuga automatica).

Uso: python3 baselines.py [--tabla ../data/processed/tabla_maestra.parquet]
                          [--reporte ../wiki/resultados_baselines.md]
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from evaluacion import (RUTA_METADATOS, ResultadoEvaluacion,
                        evaluar_walk_forward)

RAIZ = Path(__file__).resolve().parents[1]


class ModeloColumna:
    """Baseline que devuelve directamente una columna de la tabla."""

    def __init__(self, columna: str):
        self.columna = columna
        self._mediana = None

    def fit(self, X, y):
        self._mediana = float(np.nanmedian(y))

    def predict(self, X):
        pred = X[self.columna].to_numpy(dtype=float)
        return np.where(np.isnan(pred), self._mediana, pred)


class ModeloEstacional:
    """Promedio del mismo dia de semana de las ultimas 4 semanas."""

    COLS = ["costo_lag7", "costo_lag14", "costo_lag21", "costo_lag28"]

    def fit(self, X, y):
        self._mediana = float(np.nanmedian(y))

    def predict(self, X):
        pred = X[self.COLS].mean(axis=1).to_numpy(dtype=float)
        return np.where(np.isnan(pred), self._mediana, pred)


class ModeloLightGBM:
    """LightGBM con hiperparametros fijos (los experimentos van en
    autoresearch/, no aqui)."""

    PARAMS = dict(n_estimators=600, learning_rate=0.03, num_leaves=31,
                  min_child_samples=20, subsample=0.9, subsample_freq=1,
                  colsample_bytree=0.9, random_state=42, verbosity=-1)

    def __init__(self, columnas: list[str]):
        self.columnas = columnas
        self._m = None

    def fit(self, X, y):
        import lightgbm as lgb

        self._m = lgb.LGBMRegressor(**self.PARAMS)
        self._m.fit(X[self.columnas].astype(float), y)

    def predict(self, X):
        return self._m.predict(X[self.columnas].astype(float))


def columnas_conformes(df: pd.DataFrame, ruta_metadatos: Path | None = None) -> list[str]:
    """Features declaradas conformes a la regla 20:00, presentes en la tabla."""
    meta = json.loads((ruta_metadatos or RUTA_METADATOS).read_text())
    return [c for c, info in meta.items()
            if c in df.columns and not c.startswith("_")
            and isinstance(info, dict) and info.get("cumple_regla_2000")]


def correr_baselines(ruta_tabla: Path) -> list[ResultadoEvaluacion]:
    df = pd.read_parquet(ruta_tabla)
    df["fecha"] = pd.to_datetime(df["fecha"])

    resultados = [
        evaluar_walk_forward(df, ["costo_lag1"], lambda: ModeloColumna("costo_lag1"),
                             "persistencia_lag1 (teorica, fuga operacional)",
                             saltar_antifuga=True),
        evaluar_walk_forward(df, ["costo_lag2"], lambda: ModeloColumna("costo_lag2"),
                             "persistencia_lag2 (implementable)"),
        evaluar_walk_forward(df, ModeloEstacional.COLS, ModeloEstacional,
                             "estacional_dow_4sem"),
    ]

    feats = columnas_conformes(df)
    resultados.append(
        evaluar_walk_forward(df, feats, lambda: ModeloLightGBM(feats),
                             "lightgbm_baseline"))
    return resultados, df, feats


def _analisis_errores(res: ResultadoEvaluacion, df: pd.DataFrame) -> dict:
    p = res.predicciones.copy()
    p["fecha"] = pd.to_datetime(p["fecha"])
    p["ape"] = (p.prediccion - p.real).abs() / p.real * 100
    cal_cols = [c for c in ("es_feriado", "es_finde", "es_sandwich",
                            "semana_18sept", "es_eleccion") if c in df.columns]
    m = p.merge(df[["fecha"] + cal_cols], on="fecha", how="left")
    grupos = {}
    for c in cal_cols:
        grupos[c] = m.groupby(m[c].astype(bool)).ape.mean().to_dict()
    por_mes = m.groupby(m.fecha.dt.month).ape.mean().round(2).to_dict()
    por_dow = m.groupby(m.fecha.dt.dayofweek).ape.mean().round(2).to_dict()
    peores = m.nlargest(15, "ape")[["fecha", "real", "prediccion", "ape"]
                                   + cal_cols]
    return {"grupos": grupos, "por_mes": por_mes, "por_dow": por_dow,
            "peores": peores}


def escribir_reporte(resultados, df, feats, ruta_salida: Path,
                     origen_datos: str) -> None:
    mejor = min(resultados, key=lambda r: r.mape)
    lineas = [
        "---",
        "title: Resultados de baselines — costo de operacion D+1",
        "sources:",
        "  - data/processed/tabla_maestra.parquet",
        "  - models/evaluacion.py",
        f"last_synthesized: {date.today().isoformat()}",
        "---",
        "",
        "# Resultados de baselines",
        "",
    ]
    if origen_datos == "sintetico":
        lineas += [
            "> ⚠️ **DATOS SINTÉTICOS.** Estos números validan la maquinaria",
            "> (protocolo walk-forward, anti-fuga, pipeline) sobre",
            "> `data/raw_sintetico/`. **NO son métricas del problema real.**",
            "> Se regeneran automáticamente cuando el backfill real",
            "> (workflow `backfill.yml`) puebla `data/raw/`.",
            "",
        ]
    lineas += [
        "Protocolo: walk-forward ventana expansiva, refit cada 28 días,",
        "mínimo 365 días de entrenamiento inicial — única vía:",
        "`models/evaluacion.py`. Métrica principal: MAPE.",
        "",
        "| Modelo | MAPE % | MAE USD | RMSE USD | Sesgo USD | Folds | N |",
        "|--------|-------:|--------:|---------:|----------:|------:|--:|",
    ]
    for r in resultados:
        lineas.append(
            f"| {r.nombre_modelo} | {r.mape:.2f} | {r.mae:,.0f} "
            f"| {r.rmse:,.0f} | {r.sesgo:+,.0f} | {r.n_folds} "
            f"| {r.n_predicciones} |")
    lineas += [
        "",
        f"**Mejor baseline: `{mejor.nombre_modelo}` (MAPE {mejor.mape:.2f} %).**",
        f"Evaluado {mejor.fecha_inicio_eval} → {mejor.fecha_fin_eval}.",
        f"LightGBM usa {len(feats)} features conformes a la regla 20:00",
        "(verificación automática `verificar_antifuga`; `costo_lag1` y",
        "`cmg_programado_d1` rechazadas por declaración de no conformidad).",
        "",
        "## Análisis de errores (mejor modelo)",
        "",
    ]
    an = _analisis_errores(mejor, df)
    lineas.append("### MAPE por condición de calendario")
    lineas.append("")
    lineas.append("| Condición | False | True |")
    lineas.append("|-----------|------:|-----:|")
    for c, v in an["grupos"].items():
        lineas.append(f"| {c} | {v.get(False, float('nan')):.2f} "
                      f"| {v.get(True, float('nan')):.2f} |")
    dows = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
    lineas += ["", "### MAPE por día de semana", "",
               "| " + " | ".join(dows) + " |",
               "|" + "---:|" * 7,
               "| " + " | ".join(f"{an['por_dow'].get(i, float('nan')):.2f}"
                                 for i in range(7)) + " |",
               "", "### MAPE por mes", "",
               "| " + " | ".join(str(m) for m in range(1, 13)) + " |",
               "|" + "---:|" * 12,
               "| " + " | ".join(f"{an['por_mes'].get(m, float('nan')):.2f}"
                                 for m in range(1, 13)) + " |",
               "", "### 15 peores días", "",
               an["peores"].to_markdown(index=False), ""]
    ruta_salida.write_text("\n".join(lineas))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tabla", type=Path,
                   default=RAIZ / "data/processed/tabla_maestra.parquet")
    p.add_argument("--reporte", type=Path,
                   default=RAIZ / "wiki/resultados_baselines.md")
    a = p.parse_args()

    resultados, df, feats = correr_baselines(a.tabla)
    origen = df.origen_datos.iloc[0] if "origen_datos" in df.columns else "real"
    for r in resultados:
        print(f"{r.nombre_modelo:48s} MAPE={r.mape:6.2f}%  MAE={r.mae:12,.0f}  "
              f"RMSE={r.rmse:12,.0f}  sesgo={r.sesgo:+12,.0f}")
    escribir_reporte(resultados, df, feats, a.reporte, origen)
    print(f"\nreporte: {a.reporte} (origen datos: {origen})")


if __name__ == "__main__":
    main()
