"""Protocolo CANONICO de evaluacion — UNICA fuente de verdad para comparar modelos.

Reglas no negociables (ver CLAUDE.md de autoresearch/ y wiki/decisiones.md D-006):

1. Nadie evalua de otra forma: ni humanos ni agentes. Cualquier numero de
   MAPE/MAE/RMSE/sesgo reportado en este repo sale de `evaluar_walk_forward`.
2. Validacion walk-forward con ventana EXPANSIVA, sin shuffle, sin acceso al
   futuro: para cada fold se entrena con [inicio, corte) y se predice
   [corte, corte + paso). El modelo se re-instancia en cada fold.
3. Convencion de la tabla maestra: cada fila esta indexada por la fecha
   objetivo T; TODAS las features de esa fila fueron computadas solo con
   informacion disponible hasta las 20:00 (hora Chile) del dia T-1
   (los lags los aplica construir_tabla_maestra.py, no este modulo).
4. Chequeo automatico anti-fuga: `verificar_antifuga` valida contra
   data/processed/metadatos_features.json que cada feature usada declare
   disponibilidad <= 20:00 del dia D. Falla = no se evalua.

Metricas:
- MAPE (principal), MAE, RMSE
- sesgo = error medio con signo (prediccion - real); para el KPI del CEN
  sub-proyectar y sobre-proyectar no son simetricos.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol

import numpy as np
import pandas as pd

RAIZ_REPO = Path(__file__).resolve().parents[1]
RUTA_METADATOS = RAIZ_REPO / "data" / "processed" / "metadatos_features.json"

HORA_CORTE = "20:00"  # hora Chile del dia D; limite duro de disponibilidad

# Parametros canonicos del protocolo. Cambiarlos invalida toda comparacion
# historica: requiere decision documentada en wiki/decisiones.md.
MIN_TRAIN_DIAS = 365
PASO_REFIT_DIAS = 28


class Modelo(Protocol):
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None: ...
    def predict(self, X: pd.DataFrame) -> np.ndarray: ...


@dataclass
class ResultadoEvaluacion:
    nombre_modelo: str
    mape: float
    mae: float
    rmse: float
    sesgo: float
    n_predicciones: int
    n_folds: int
    fecha_inicio_eval: str
    fecha_fin_eval: str
    predicciones: pd.DataFrame = field(repr=False)  # fecha, real, prediccion, fold
    metricas_por_fold: pd.DataFrame = field(repr=False)

    def como_dict(self) -> dict:
        return {k: getattr(self, k) for k in
                ("nombre_modelo", "mape", "mae", "rmse", "sesgo",
                 "n_predicciones", "n_folds", "fecha_inicio_eval",
                 "fecha_fin_eval")}


def _metricas(real: np.ndarray, pred: np.ndarray) -> dict:
    """MAPE excluye dias con real == 0 (indefinido); MAE/RMSE/sesgo usan
    todos los dias. Si la exclusion no es marginal (hallazgo H4 de la
    auditoria: el proxy real puede acercarse a 0 en vertimiento solar), se
    advierte — las poblaciones de MAPE y MAE dejan de ser comparables."""
    err = pred - real
    con_base = real != 0
    n_excluidos = int((~con_base).sum())
    if n_excluidos:
        import logging
        logging.getLogger("evaluacion").warning(
            "MAPE excluye %d dias con objetivo == 0 (de %d); MAE/RMSE los "
            "incluyen", n_excluidos, len(real))
    return {
        "mape": float(np.mean(np.abs(err[con_base] / real[con_base])) * 100),
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "sesgo": float(np.mean(err)),
    }


def verificar_antifuga(columnas_features: list[str],
                       ruta_metadatos: Path | None = None) -> None:
    """Valida que cada feature declare cumplimiento de la regla de las 20:00.

    Cada feature de la tabla maestra debe estar registrada en
    metadatos_features.json con `cumple_regla_2000: true` y una justificacion
    (`disponible_a_las` + `lag_dias` aplicado). Feature no registrada o no
    conforme => ValueError, y el experimento NO se evalua.
    """
    ruta = ruta_metadatos or RUTA_METADATOS
    if not ruta.exists():
        raise FileNotFoundError(
            f"falta {ruta}; construir_tabla_maestra.py debe generarlo")
    meta = json.loads(ruta.read_text())
    problemas = []
    for col in columnas_features:
        info = meta.get(col)
        if info is None:
            problemas.append(f"{col}: sin metadatos de disponibilidad")
        elif not info.get("cumple_regla_2000", False):
            problemas.append(f"{col}: declarada como NO conforme "
                             f"(disponible_a_las={info.get('disponible_a_las')}, "
                             f"lag_dias={info.get('lag_dias')})")
    if problemas:
        raise ValueError("FUGA DE DATOS POTENCIAL — features rechazadas:\n  "
                         + "\n  ".join(problemas))


def evaluar_walk_forward(
    df: pd.DataFrame,
    columnas_features: list[str],
    constructor_modelo: Callable[[], Modelo],
    nombre_modelo: str,
    col_objetivo: str = "cmg_medio_diario",
    col_fecha: str = "fecha",
    min_train_dias: int = MIN_TRAIN_DIAS,
    paso_refit_dias: int = PASO_REFIT_DIAS,
    ruta_metadatos: Path | None = None,
    saltar_antifuga: bool = False,
) -> ResultadoEvaluacion:
    """Evaluacion walk-forward canonica.

    `saltar_antifuga` existe SOLO para los baselines de persistencia y
    estacional, cuyas unicas "features" son la propia serie objetivo con lag
    >= 1 dia (conformidad trivial). Restriccion dura (hallazgo H3 de la
    auditoria): con el flag activo solo se aceptan columnas de lag puro del
    objetivo — cualquier otra columna lanza ValueError.
    """
    if not saltar_antifuga:
        verificar_antifuga(columnas_features, ruta_metadatos)
    else:
        permitidas = {f"cmg_lag{k}" for k in (1, 2, 3, 7, 14, 21, 28)}
        fuera = set(columnas_features) - permitidas
        if fuera:
            raise ValueError(
                f"saltar_antifuga solo admite lags puros del objetivo "
                f"({sorted(permitidas)}); rechazadas: {sorted(fuera)}")

    df = df.sort_values(col_fecha).reset_index(drop=True)
    df = df.dropna(subset=[col_objetivo])
    if df[col_fecha].duplicated().any():
        raise ValueError("fechas duplicadas en la tabla maestra")
    fechas = pd.to_datetime(df[col_fecha])
    if not fechas.is_monotonic_increasing:
        raise AssertionError("orden temporal roto tras sort — imposible")

    inicio = fechas.iloc[0]
    primer_corte = inicio + pd.Timedelta(days=min_train_dias)
    if primer_corte >= fechas.iloc[-1]:
        raise ValueError(
            f"datos insuficientes: se requieren > {min_train_dias} dias de "
            f"entrenamiento inicial y hay {(fechas.iloc[-1]-inicio).days}")

    predicciones, filas_fold = [], []
    corte = primer_corte
    fold = 0
    while corte <= fechas.iloc[-1]:
        fin_fold = corte + pd.Timedelta(days=paso_refit_dias)
        m_train = fechas < corte
        m_test = (fechas >= corte) & (fechas < fin_fold)
        if m_test.sum() == 0:
            corte = fin_fold
            continue
        # garantia estructural: nada del fold de test entra al train
        assert fechas[m_train].max() < fechas[m_test].min()

        modelo = constructor_modelo()  # instancia fresca: sin estado heredado
        modelo.fit(df.loc[m_train, columnas_features],
                   df.loc[m_train, col_objetivo])
        pred = np.asarray(modelo.predict(df.loc[m_test, columnas_features]),
                          dtype=float)
        real = df.loc[m_test, col_objetivo].to_numpy(dtype=float)

        predicciones.append(pd.DataFrame({
            "fecha": df.loc[m_test, col_fecha].to_numpy(),
            "real": real, "prediccion": pred, "fold": fold,
        }))
        filas_fold.append({"fold": fold, "corte": corte.date().isoformat(),
                           "n_train": int(m_train.sum()),
                           "n_test": int(m_test.sum()),
                           **_metricas(real, pred)})
        corte = fin_fold
        fold += 1

    df_pred = pd.concat(predicciones, ignore_index=True)
    glob = _metricas(df_pred.real.to_numpy(), df_pred.prediccion.to_numpy())
    return ResultadoEvaluacion(
        nombre_modelo=nombre_modelo,
        n_predicciones=len(df_pred), n_folds=fold,
        fecha_inicio_eval=str(df_pred.fecha.min()),
        fecha_fin_eval=str(df_pred.fecha.max()),
        predicciones=df_pred,
        metricas_por_fold=pd.DataFrame(filas_fold),
        **glob,
    )
