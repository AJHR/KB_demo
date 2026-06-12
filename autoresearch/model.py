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

Base vigente: exp002_features_fisicas (LightGBM L1 + 3 derivadas fisicas).
Este experimento cambia SOLO el predictor: mediana de 3 LightGBM L1 con
seeds distintos, sin tocar features ni hiperparametros.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))
from baselines import ModeloLightGBM  # noqa: E402

NOMBRE_EXPERIMENTO = "exp005_ensamble_seeds"
HIPOTESIS = ("Parte del error del LightGBM L1 es varianza del muestreo "
             "interno (subsample/colsample por seed). La mediana de 3 "
             "modelos identicos con seeds 42/43/44 promedia esa varianza "
             "sin tocar el sesgo del modelo, y deberia bajar el MAPE de la "
             "base vigente a costo 3x de entrenamiento (cabe en "
             "presupuesto).")


class ModeloLGBM_L1(ModeloLightGBM):
    PARAMS = {**ModeloLightGBM.PARAMS, "objective": "regression_l1"}


class EnsambleMedianaSeeds:
    """Mediana de 3 LightGBM L1 identicos salvo random_state (42/43/44)."""

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


_RAD_SOLAR = ["pron_radiacion_media_solar_diego_almagro",
              "pron_radiacion_media_solar_maria_elena"]

_DERIVADAS = ["der_sequia_x_gnl", "der_demanda_neta_solar",
              "der_spread_brent_carbon"]


def seleccionar_features(columnas_conformes: list[str],
                         df: pd.DataFrame) -> list[str]:
    # Todas las derivadas son funciones FILA-A-FILA de columnas conformes:
    # no usan shift, rolling ni estadisticas de muestra => invariantes a
    # truncamiento por construccion.
    # 1) sequia x combustible: con poca lluvia acumulada (90d) el valor del
    #    agua sube y el GNL margina mas caro.
    df["der_sequia_x_gnl"] = (df["fx_henry_hub_usd_mmbtu"]
                              / (df["precip_hidro_90d"] + 1.0))
    # 2) proxy de demanda neta: demanda menos radiacion solar pronosticada
    #    (promedio de los puntos solar_*) escalada por el share solar
    #    reciente. NaN pre-2021 en pron_* los maneja LightGBM nativo.
    rad_solar = df[_RAD_SOLAR].mean(axis=1)
    df["der_demanda_neta_solar"] = (df["demanda_total_mwh"]
                                    - rad_solar * df["share_solar"])
    # 3) spread brent - carbon: posicion relativa de tecnologias en el
    #    orden de merito.
    df["der_spread_brent_carbon"] = (df["fx_brent_usd_bbl"]
                                     - df["fx_carbon_api2_usd_t"])
    return list(columnas_conformes) + _DERIVADAS


def crear_modelo(columnas: list[str]):
    return EnsambleMedianaSeeds(columnas)
