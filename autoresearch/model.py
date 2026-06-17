"""model.py — EL archivo que el agente experimentador modifica (y solo este).

Interfaz exigida por el harness (autoresearch/harness.py):

  NOMBRE_EXPERIMENTO : str   — identificador unico del experimento
  HIPOTESIS          : str   — que se esta probando y por que (1-3 lineas)
  seleccionar_features(columnas_conformes, df) -> list[str]
      Subconjunto/orden de features a usar. Solo puede devolver columnas del
      argumento `columnas_conformes` (ya filtradas por verificar_antifuga) o
      columnas NUEVAS que agregue a `df` AQUI derivadas exclusivamente de
      columnas conformes (transformaciones sin mirar el futuro).
  crear_modelo(columnas) -> objeto con .fit(X, y) y .predict(X)

Base vigente: exp006_objetivo_cuantil_p60 (mediana de 3 LightGBM cuantil-0.60
+ 2 derivadas fisicas). Este experimento revierte SOLO el objetivo a L1
(mediana): con la historia extendida (23 meses, 12 folds) el sesgo se volvio
POSITIVO (+2.08), o sea el modelo sobre-proyecta; el tilt al cuantil 0.60
(pensado para sub-proyeccion en la ventana corta) ahora empuja en la
direccion equivocada.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))
from baselines import ModeloLightGBM  # noqa: E402

NOMBRE_EXPERIMENTO = "exp007_revertir_l1_mediana"
HIPOTESIS = ("Con la historia extendida a 23 meses (12 folds, evaluacion "
             "2025-07..2026-06 que incluye el invierno con spikes), el sesgo "
             "del modelo se invirtio a POSITIVO (+2.08 en exp006): ahora "
             "sobre-proyecta. El tilt al cuantil 0.60 (exp006) se eligio para "
             "corregir una sub-proyeccion que solo existia en la ventana corta "
             "de 4 folds; sobre el ano completo empuja al alza justo cuando el "
             "modelo ya sobreestima. Revertir el objetivo a L1 (mediana "
             "condicional) deberia bajar el sesgo hacia 0 y el MAPE. Una sola "
             "variable cambia sobre la base vigente (objetivo cuantil->L1).")


class ModeloLGBM_L1(ModeloLightGBM):
    PARAMS = {**ModeloLightGBM.PARAMS, "objective": "regression_l1"}


class EnsambleMedianaSeeds:
    """Mediana de 3 LightGBM L1 identicos salvo random_state."""

    SEEDS = (42, 43, 44)

    def __init__(self, columnas: list[str]):
        self.columnas = columnas
        self._modelos: list = []

    def fit(self, X, y):
        import lightgbm as lgb

        self._modelos = []
        for seed in self.SEEDS:
            params = {**ModeloLGBM_L1.PARAMS, "random_state": seed}
            m = lgb.LGBMRegressor(**params)
            m.fit(X[self.columnas].astype(float), y)
            self._modelos.append(m)

    def predict(self, X):
        import numpy as np

        preds = np.column_stack(
            [m.predict(X[self.columnas].astype(float))
             for m in self._modelos])
        return np.median(preds, axis=1)


_DERIVADAS = ["der_sequia_x_gnl", "der_spread_brent_carbon"]


def seleccionar_features(columnas_conformes: list[str],
                         df: pd.DataFrame) -> list[str]:
    # Derivadas fila-a-fila de columnas conformes: sin shift ni estadisticas
    # de muestra => invariantes a truncamiento por construccion.
    # 1) sequia x combustible: con poca lluvia acumulada (90d) el valor del
    #    agua sube y el GNL margina mas caro.
    df["der_sequia_x_gnl"] = (df["fx_henry_hub_usd_mmbtu"]
                              / (df["precip_hidro_90d"] + 1.0))
    # 2) spread brent - carbon: posicion relativa de tecnologias en el
    #    orden de merito.
    df["der_spread_brent_carbon"] = (df["fx_brent_usd_bbl"]
                                     - df["fx_carbon_api2_usd_t"])
    return list(columnas_conformes) + _DERIVADAS


def crear_modelo(columnas: list[str]):
    return EnsambleMedianaSeeds(columnas)
