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

Base vigente: exp001_objetivo_l1 (LightGBM objetivo L1). Este experimento
agrega SOLO features derivadas fisicas, sin tocar el modelo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))
from baselines import ModeloLightGBM  # noqa: E402

NOMBRE_EXPERIMENTO = "exp002_features_fisicas"
HIPOTESIS = ("El costo sale de un despacho por orden de merito: sequia "
             "encarece el GNL marginal (interaccion precip_hidro_90d x "
             "henry hub), la demanda neta de solar pronosticada define que "
             "tecnologia margina, y el spread brent-carbon mueve el stack. "
             "Tres derivadas fila-a-fila de columnas conformes (sin estado, "
             "invariantes a truncamiento) deberian bajar el MAPE de la base "
             "L1 sin riesgo de fuga.")


class ModeloLGBM_L1(ModeloLightGBM):
    PARAMS = {**ModeloLightGBM.PARAMS, "objective": "regression_l1"}


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
    return ModeloLGBM_L1(columnas)
