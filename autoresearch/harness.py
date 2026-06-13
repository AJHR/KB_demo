"""Harness del autoresearch: entrena, evalua (via protocolo canonico) y
registra. El agente NO modifica este archivo — solo model.py.

Flujo: carga tabla maestra -> features conformes (verificar_antifuga) ->
model.seleccionar_features -> model.crear_modelo -> evaluar_walk_forward ->
fila append en log_experimentos.md.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "models"))
sys.path.insert(0, str(Path(__file__).parent))

from baselines import columnas_conformes  # noqa: E402
from evaluacion import evaluar_walk_forward, verificar_antifuga  # noqa: E402

import model  # noqa: E402  — el archivo del experimento

RUTA_TABLA = RAIZ / "data" / "processed" / "tabla_maestra.parquet"
RUTA_LOG = Path(__file__).parent / "log_experimentos.md"


COL_OBJETIVO = "costo_op_usd"
DIAS_TRUNCAMIENTO = 60


def _features_del_modelo(df: pd.DataFrame, conformes: list[str]):
    """Ejecuta model.seleccionar_features con las defensas anti-fuga H1/H2
    (auditoria work/auditoria_antifuga_fase3.md):

    - el modelo recibe una COPIA sin la columna objetivo: no puede leer el
      label ni mutar la tabla de evaluacion;
    - las columnas conformes preexistentes deben volver INTACTAS (un
      experimento que sobrescribe costo_lag2 con el label queda rechazado);
    - toda columna NUEVA pasa un test de invarianza a truncamiento: se
      recalcula la seleccion sobre la tabla sin los ultimos N dias y los
      valores del tramo comun deben coincidir; una feature que mira el
      futuro (shift negativo, rolling centrado, estadisticas de muestra
      completa) cambia al truncar y se rechaza.
    """
    df_sel = df.drop(columns=[COL_OBJETIVO]).copy()
    feats = model.seleccionar_features(conformes, df_sel)

    intactas = [c for c in feats if c in conformes]
    verificar_antifuga(intactas)
    for c in intactas:
        if not df_sel[c].equals(df[c]):
            raise ValueError(
                f"FUGA: la columna conforme '{c}' fue modificada por "
                f"seleccionar_features; las conformes son inmutables")

    nuevas = [c for c in feats if c not in conformes]
    if nuevas:
        df_trunc = df.drop(columns=[COL_OBJETIVO]).iloc[:-DIAS_TRUNCAMIENTO].copy()
        model.seleccionar_features(conformes, df_trunc)
        n = len(df_trunc)
        for c in nuevas:
            if c not in df_trunc.columns:
                raise ValueError(f"FUGA: feature nueva '{c}' no reproducible "
                                 f"sobre la tabla truncada")
            a, b = df_sel[c].iloc[:n], df_trunc[c]
            iguales = (a.fillna(-9e18).to_numpy() == b.fillna(-9e18).to_numpy())
            if not iguales.all():
                raise ValueError(
                    f"FUGA: la feature nueva '{c}' cambia al truncar el final "
                    f"de la serie => usa informacion del futuro (shift "
                    f"negativo, rolling centrado o estadisticas de muestra "
                    f"completa). Calcular solo con el pasado.")
        print(f"{len(nuevas)} features derivadas nuevas validadas "
              f"(invarianza a truncamiento): {nuevas[:10]}")

    # tabla de evaluacion: original + nuevas validadas
    df_eval = df.copy()
    for c in nuevas:
        df_eval[c] = df_sel[c]

    # overlay de metadatos: las nuevas validadas se registran para que el
    # gate canonico de evaluar_walk_forward las acepte (no se salta nada)
    ruta_meta = None
    if nuevas:
        import tempfile

        meta = json.loads((RAIZ / "data" / "processed" /
                           "metadatos_features.json").read_text())
        for c in nuevas:
            meta[c] = {"fuente": f"autoresearch:{model.NOMBRE_EXPERIMENTO}",
                       "lag_dias": None, "disponible_a_las": "derivada",
                       "cumple_regla_2000": True,
                       "nota": "derivada de columnas conformes; validada por "
                               "invarianza a truncamiento en harness.py"}
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                          delete=False)
        json.dump(meta, tmp)
        tmp.close()
        ruta_meta = Path(tmp.name)
    return feats, df_eval, ruta_meta


def main() -> int:
    t0 = time.time()
    df = pd.read_parquet(RUTA_TABLA)
    df["fecha"] = pd.to_datetime(df["fecha"])
    origen = df.origen_datos.iloc[0] if "origen_datos" in df.columns else "real"

    conformes = columnas_conformes(df)
    feats, df_eval, ruta_meta = _features_del_modelo(df, conformes)

    res = evaluar_walk_forward(df_eval, feats, lambda: model.crear_modelo(feats),
                               model.NOMBRE_EXPERIMENTO, ruta_metadatos=ruta_meta)
    dur_min = (time.time() - t0) / 60

    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True,
                             cwd=RAIZ).stdout.strip()
    except Exception:
        sha = "?"

    fila = (f"| {datetime.utcnow():%Y-%m-%d %H:%M}Z | {model.NOMBRE_EXPERIMENTO} "
            f"| {model.HIPOTESIS.replace('|', '/')} | {res.mape:.3f} "
            f"| {res.mae:,.0f} | {res.rmse:,.0f} | {res.sesgo:+,.0f} "
            f"| {res.n_folds} | {dur_min:.1f} | {origen} | {sha} | _pendiente_ |")
    with RUTA_LOG.open("a") as f:
        f.write(fila + "\n")

    print(json.dumps({**res.como_dict(), "duracion_min": round(dur_min, 1),
                      "n_features": len(feats), "origen_datos": origen},
                     indent=2, ensure_ascii=False))
    print(f"\nregistrado en {RUTA_LOG.name}; completar columna 'decision' "
          f"(conservar/descartar) tras analizar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
