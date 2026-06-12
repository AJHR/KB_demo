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

Punto de partida: el LightGBM baseline de la fase 3 (models/baselines.py),
sin cambios. MAPE de referencia en autoresearch/log_experimentos.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))
from baselines import ModeloLightGBM  # noqa: E402

NOMBRE_EXPERIMENTO = "exp001_objetivo_l1"
HIPOTESIS = ("El costo diario tiene spikes de escasez; el objetivo L2 del "
             "baseline persigue esos outliers. Cambiar a objetivo L1 "
             "(regression_l1) deberia bajar el MAPE mediano sin tocar nada mas.")


class ModeloLGBM_L1(ModeloLightGBM):
    PARAMS = {**ModeloLightGBM.PARAMS, "objective": "regression_l1"}


def seleccionar_features(columnas_conformes: list[str],
                         df: pd.DataFrame) -> list[str]:
    return columnas_conformes


def crear_modelo(columnas: list[str]):
    return ModeloLGBM_L1(columnas)
