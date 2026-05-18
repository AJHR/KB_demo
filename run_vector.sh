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

# Smoke test: verifica que un python tenga stdlib completo (pyexpat, ssl, etc).
# Hay versiones de brew python@3.11 con libexpat roto que cascadea en pip.
python_works() {
  "$1" -c "import xml.parsers.expat, ssl, ctypes, zlib, hashlib, sqlite3" 2>/dev/null
}

VENV="$ROOT/generador-demo-electrico/.venv-reg"

# Si el venv existe pero su python esta roto, lo nukeamos
if [ -f "$VENV/bin/python" ] && ! python_works "$VENV/bin/python"; then
  log "venv existente tiene stdlib roto (libexpat/pyexpat); recreando..."
  rm -rf "$VENV"
fi

if [ ! -f "$VENV/bin/activate" ]; then
  if [ -d "$VENV" ]; then
    log "venv anterior incompleto; lo borro y recreo..."
    rm -rf "$VENV"
  fi
  # Buscar un python disponible Y funcional (salteamos los con stdlib roto)
  PYBIN=""
  for cand in python3.12 python3.13 python3.11 python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
      if python_works "$cand"; then
        PYBIN="$cand"; break
      else
        log "  $cand: stdlib roto (pyexpat), saltando"
      fi
    fi
  done
  if [ -z "$PYBIN" ]; then
    echo "ERROR: no encuentro un python3.x funcional. Probar:" >&2
    echo "  brew reinstall expat python@3.11" >&2
    exit 1
  fi
  log "Creando venv en $VENV con $PYBIN ($($PYBIN --version 2>&1))..."
  if ! "$PYBIN" -m venv "$VENV"; then
    log "venv standard fallo; reintento con --without-pip + get-pip..."
    "$PYBIN" -m venv --without-pip "$VENV"
    curl -sSL https://bootstrap.pypa.io/get-pip.py | "$VENV/bin/python"
  fi
  if [ ! -f "$VENV/bin/activate" ] || ! python_works "$VENV/bin/python"; then
    echo "ERROR: el venv no quedo funcional. Pruebalo manual:" >&2
    echo "  rm -rf $VENV && /usr/bin/python3 -m venv $VENV" >&2
    exit 1
  fi
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
log "venv listo: $(python --version 2>&1)"

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
