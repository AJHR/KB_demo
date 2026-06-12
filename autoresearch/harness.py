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


def main() -> int:
    t0 = time.time()
    df = pd.read_parquet(RUTA_TABLA)
    df["fecha"] = pd.to_datetime(df["fecha"])
    origen = df.origen_datos.iloc[0] if "origen_datos" in df.columns else "real"

    conformes = columnas_conformes(df)
    feats = model.seleccionar_features(conformes, df)

    nuevas = [c for c in feats if c not in conformes]
    # las features nuevas creadas en seleccionar_features deben derivar solo
    # de columnas conformes; verificar_antifuga cubre las preexistentes
    verificar_antifuga([c for c in feats if c in conformes])
    if nuevas:
        print(f"AVISO: {len(nuevas)} features derivadas nuevas: {nuevas[:10]}")

    res = evaluar_walk_forward(df, feats, lambda: model.crear_modelo(feats),
                               model.NOMBRE_EXPERIMENTO)
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
