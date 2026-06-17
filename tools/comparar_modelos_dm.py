"""Comparacion pareada de modelos (estilo Diebold-Mariano) sobre el APE diario.

Con la historia extendida (23 meses, 12 folds, N=328) ya hay potencia para
testear si las diferencias de MAPE entre modelos son significativas o ruido.
Test no parametrico de Wilcoxon de rangos con signo sobre el APE por dia
(pareado por fecha): H0 = misma distribucion de error; p<0.05 = diferencia
significativa. Reporta tambien la diferencia media de MAPE (pp).

NO toca el protocolo canonico: cada modelo se evalua con evaluar_walk_forward.
Uso: python3 tools/comparar_modelos_dm.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "models"))

from baselines import (ModeloColumna, ModeloEstacional, ModeloLightGBM,  # noqa: E402
                       columnas_conformes)
from evaluacion import evaluar_walk_forward  # noqa: E402

df = pd.read_parquet(RAIZ / "data/processed/tabla_maestra.parquet")
df["fecha"] = pd.to_datetime(df["fecha"])

# derivadas fisicas (identicas a autoresearch/model.py)
df["der_sequia_x_gnl"] = df["fx_henry_hub_usd_mmbtu"] / (df["precip_hidro_90d"] + 1.0)
df["der_spread_brent_carbon"] = df["fx_brent_usd_bbl"] - df["fx_carbon_api2_usd_t"]

conf = columnas_conformes(df)
feats_ml = conf + ["der_sequia_x_gnl", "der_spread_brent_carbon"]

# overlay de metadatos para que el gate acepte las 2 derivadas
meta = json.loads((RAIZ / "data/processed/metadatos_features.json").read_text())
for c in ("der_sequia_x_gnl", "der_spread_brent_carbon"):
    meta[c] = {"cumple_regla_2000": True, "fuente": "derivada",
               "lag_dias": None, "disponible_a_las": "derivada", "nota": "cmp"}
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
json.dump(meta, tmp)
tmp.close()
overlay = Path(tmp.name)

import lightgbm as lgb  # noqa: E402


class Ensamble:
    SEEDS = (42, 43, 44)

    def __init__(self, cols, objective, alpha=None):
        self.cols, self.obj, self.alpha, self.ms = cols, objective, alpha, []

    def fit(self, X, y):
        self.ms = []
        for s in self.SEEDS:
            p = dict(ModeloLightGBM.PARAMS)
            p["random_state"] = s
            p["objective"] = self.obj
            if self.alpha is not None:
                p["alpha"] = self.alpha
            m = lgb.LGBMRegressor(**p)
            m.fit(X[self.cols].astype(float), y)
            self.ms.append(m)

    def predict(self, X):
        P = np.column_stack([m.predict(X[self.cols].astype(float)) for m in self.ms])
        return np.median(P, axis=1)


modelos = {
    "estacional_dow":           (ModeloEstacional.COLS, lambda: ModeloEstacional(), None),
    "lightgbm_baseline_L2":     (conf, lambda: ModeloLightGBM(conf), None),
    "exp006_q60":               (feats_ml, lambda: Ensamble(feats_ml, "quantile", 0.60), overlay),
    "exp007_l1":                (feats_ml, lambda: Ensamble(feats_ml, "regression_l1"), overlay),
    "persistencia_lag1_FUGA":   (["cmg_lag1"], lambda: ModeloColumna("cmg_lag1"), "SALTAR"),
}

preds = {}
print(f"{'modelo':28s} {'MAPE%':>7} {'sesgo':>7} {'N':>5}")
for name, (cols, ctor, meta_arg) in modelos.items():
    kw = {}
    if meta_arg == "SALTAR":
        kw["saltar_antifuga"] = True
    elif meta_arg is not None:
        kw["ruta_metadatos"] = meta_arg
    r = evaluar_walk_forward(df, cols, ctor, name, **kw)
    p = r.predicciones.copy()
    p["fecha"] = pd.to_datetime(p["fecha"])
    p["ape"] = (p.prediccion - p.real).abs() / p.real * 100
    preds[name] = p.set_index("fecha")["ape"].rename(name)
    print(f"{name:28s} {r.mape:7.2f} {r.sesgo:+7.2f} {r.n_predicciones:5d}")

A = pd.concat(preds.values(), axis=1).dropna()
print(f"\nN comun (dias con prediccion de todos): {len(A)}")
print("\nComparaciones pareadas (Wilcoxon signed-rank sobre APE diario):")
print("  dMAPE(a-b) < 0  => 'a' tiene menor APE medio que 'b'")
pares = [("exp007_l1", "estacional_dow"),
         ("exp007_l1", "lightgbm_baseline_L2"),
         ("exp007_l1", "exp006_q60"),
         ("exp007_l1", "persistencia_lag1_FUGA"),
         ("estacional_dow", "lightgbm_baseline_L2")]
for a, b in pares:
    d = (A[a] - A[b])
    w = stats.wilcoxon(A[a], A[b])
    sig = "SIGNIFICATIVO" if w.pvalue < 0.05 else "no significativo"
    print(f"  {a:22s} vs {b:22s}: dMAPE={d.mean():+6.2f}pp  "
          f"mediana_dif={d.median():+6.2f}  p={w.pvalue:.4f}  [{sig}]")
