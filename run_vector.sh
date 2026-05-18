#!/usr/bin/env bash
# Procesa sources/ a vector store LanceDB + descarga modelo de embeddings.
# Esperado: 10-30 min primera vez (descarga modelo ~500MB de HuggingFace), <5 min en re-runs.
#
# Uso: bash run_vector.sh

set -euo pipefail

cd "$(dirname "$0")"
ROOT="$PWD"
BRANCH="${BRANCH:-claude/create-kb-prompt-3hYLl}"

log() { printf "\n==> %s\n" "$*"; }

# Branch
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
  log "Cambiando a branch $BRANCH..."
  git fetch origin "$BRANCH"
  git checkout "$BRANCH"
fi
git pull --ff-only origin "$BRANCH" || true

# Reusa el mismo venv que regulation_only (.venv-reg), o lo crea si no existe
VENV="$ROOT/generador-demo-electrico/.venv-reg"
if [ ! -f "$VENV/bin/activate" ]; then
  if [ -d "$VENV" ]; then
    log "venv anterior incompleto; lo borro y recreo..."
    rm -rf "$VENV"
  fi
  # Buscar un python disponible (mismo orden que run_regulation.sh)
  PYBIN=""
  for cand in python3.11 python3.12 python3.10 python3.13 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
      PYBIN="$cand"; break
    fi
  done
  if [ -z "$PYBIN" ]; then
    echo "ERROR: no encuentro python3.x. Instala con: brew install python@3.11" >&2
    exit 1
  fi
  log "Creando venv en $VENV con $PYBIN ($($PYBIN --version 2>&1))..."
  if ! "$PYBIN" -m venv "$VENV"; then
    log "venv standard fallo; reintento con --without-pip + get-pip..."
    "$PYBIN" -m venv --without-pip "$VENV"
    curl -sSL https://bootstrap.pypa.io/get-pip.py | "$VENV/bin/python"
  fi
  if [ ! -f "$VENV/bin/activate" ]; then
    echo "ERROR: no pude crear el venv. Pruebalo manual:" >&2
    echo "  rm -rf $VENV && $PYBIN -m venv $VENV" >&2
    exit 1
  fi
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

log "Instalando deps de vector store (~1GB total con torch)..."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet pypdf tiktoken sentence-transformers lancedb pyarrow

log "Procesando sources/ a vector store (puede tardar)..."
python generador-demo-electrico/scripts/process_sources.py

log "Commit + push del manifest.json (no se commitea LanceDB, es binario)"
git add data/vector/manifest.json data/vector/README.md 2>/dev/null || true
if git diff --cached --quiet; then
  log "Nada nuevo en manifest."
else
  git commit -m "vector: indexar sources/ a LanceDB ($(date +%F))"
  git push origin "$BRANCH"
fi

cat <<'EOF'

LISTO. Proba el RAG con preguntas en lenguaje natural:

  source generador-demo-electrico/.venv-reg/bin/activate
  python generador-demo-electrico/scripts/query_kb.py "como se calcula la potencia firme"
  python generador-demo-electrico/scripts/query_kb.py "bloques horarios pmgd con bess"
  python generador-demo-electrico/scripts/query_kb.py "panel de expertos"
  python generador-demo-electrico/scripts/query_kb.py --topk 10 "ciberseguridad sistema electrico"

Para limitar a un topic:
  python generador-demo-electrico/scripts/query_kb.py --topic regulation-cne-reglamentos-mercado "transferencias economicas"

EOF
