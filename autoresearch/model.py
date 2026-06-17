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

Base vigente: exp005_ensamble_seeds (mediana de 3 LightGBM L1 + 2 derivadas
fisicas). Este experimento cambia SOLO el objetivo del predictor: de L1
(mediana condicional) a cuantil 0.60, para corregir la sub-proyeccion
sistematica observada en datos reales.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))
from baselines import ModeloLightGBM  # noqa: E402

NOMBRE_EXPERIMENTO = "exp006_objetivo_cuantil_p60"
HIPOTESIS = ("El objetivo L1 predice la mediana condicional; como el CMg "
             "diario real es asimetrico a la derecha (spikes de escasez), la "
             "mediana queda sistematicamente bajo la media y el modelo "
             "sub-proyecta (sesgo -4.96 en exp005, peor que el baseline). "
             "Cambiar el objetivo a cuantil 0.60 desplaza la prediccion hacia "
             "arriba: deberia reducir el sesgo negativo y capturar mejor los "
             "dias de precio alto, bajando el MAPE. Una sola variable cambia "
             "sobre la base vigente (el objetivo del LightGBM del ensemble).")


class ModeloLGBM_Q60(ModeloLightGBM):
    PARAMS = {**ModeloLightGBM.PARAMS, "objective": "quantile", "alpha": 0.60}


class EnsambleMedianaSeeds:
    """Mediana de 3 LightGBM cuantil-0.60 identicos salvo random_state."""

    SEEDS = (42, 43, 44)

    def __init__(self, columnas: list[str]):
        self.columnas = columnas
        self._modelos: list = []

    def fit(self, X, y):
        import lightgbm as lgb

        self._modelos = []
        for seed in self.SEEDS:
            params = {**ModeloLGBM_Q60.PARAMS, "random_state": seed}
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
