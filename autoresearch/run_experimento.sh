#!/usr/bin/env bash
# Corre UN experimento de autoresearch con presupuesto de tiempo duro.
#
# Presupuesto: PRESUPUESTO_MIN minutos (default 20). Racional: la tabla
# maestra tiene ~2.700 filas diarias y el protocolo canonico hace ~65 folds
# de walk-forward; el baseline LightGBM completo tarda ~1-2 min, asi que 20
# min dan margen 10x para modelos mas pesados sin permitir que un TFT mal
# dimensionado consuma la noche. Para cambiarlo: PRESUPUESTO_MIN=40 bash
# autoresearch/run_experimento.sh — y documentar el porque en
# log_experimentos.md.
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRESUPUESTO_MIN="${PRESUPUESTO_MIN:-20}"

if [ ! -f "$DIR/../data/processed/tabla_maestra.parquet" ]; then
  echo "ERROR: falta data/processed/tabla_maestra.parquet"
  echo "  con datos reales : (cd tools/etl && python3 construir_tabla_maestra.py)"
  echo "  con sinteticos   : (cd tools/etl && python3 generar_sintetico.py && \\"
  echo "                      python3 construir_tabla_maestra.py --dir-raw ../../data/raw_sintetico --origen sintetico)"
  exit 1
fi

echo "experimento con presupuesto de ${PRESUPUESTO_MIN} min..."
timeout "${PRESUPUESTO_MIN}m" python3 "$DIR/harness.py"
CODIGO=$?
if [ $CODIGO -eq 124 ]; then
  echo "PRESUPUESTO AGOTADO (${PRESUPUESTO_MIN} min) — experimento abortado."
  echo "Registrar en log_experimentos.md como 'descartar (timeout)'."
fi
exit $CODIGO
