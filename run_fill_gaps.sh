#!/usr/bin/env bash
# Completa los huecos del KB: SSCC, Grid Forming, modelos dinamicos, PTN.
# Reusa .venv-reg (httpx + bs4 + lxml, sin embeddings).
#
# Uso:
#   bash run_fill_gaps.sh                  # corre todos los gaps
#   bash run_fill_gaps.sh --gap sscc       # solo el gap "sscc"
#   bash run_fill_gaps.sh --list           # ver gaps disponibles
#   PUSH=0 bash run_fill_gaps.sh           # no commitea
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$PWD"
BRANCH="${BRANCH:-claude/create-kb-prompt-3hYLl}"
PUSH="${PUSH:-1}"
log() { printf "\n==> %s\n" "$*"; }

python_works() {
  "$1" -c "import xml.parsers.expat, ssl, ctypes, zlib, hashlib, sqlite3" 2>/dev/null
}

# Branch
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
  log "Cambiando a branch $BRANCH..."
  git fetch origin "$BRANCH"
  git checkout "$BRANCH"
fi
git pull --ff-only origin "$BRANCH" || true

# venv (reusa o crea con smoke test)
VENV="$ROOT/generador-demo-electrico/.venv-reg"
if [ -f "$VENV/bin/python" ] && ! python_works "$VENV/bin/python"; then
  log "venv existente tiene stdlib roto (pyexpat); recreando..."
  rm -rf "$VENV"
fi
if [ ! -f "$VENV/bin/activate" ]; then
  [ -d "$VENV" ] && rm -rf "$VENV"
  PYBIN=""
  for cand in python3.12 python3.13 python3.11 python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1 && python_works "$cand"; then
      PYBIN="$cand"; break
    fi
  done
  if [ -z "$PYBIN" ]; then
    echo "ERROR: no encuentro python3.x funcional. Probar: brew reinstall expat python@3.11" >&2
    exit 1
  fi
  log "Creando venv con $PYBIN ($($PYBIN --version 2>&1))..."
  "$PYBIN" -m venv "$VENV" || {
    "$PYBIN" -m venv --without-pip "$VENV"
    curl -sSL https://bootstrap.pypa.io/get-pip.py | "$VENV/bin/python"
  }
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

log "Instalando deps (idempotente)..."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet httpx beautifulsoup4 lxml

log "Ejecutando fill_gaps.py (10-20 min esperados)..."
python generador-demo-electrico/scripts/fill_gaps.py "$@"

if [ "$PUSH" = "1" ]; then
  git add sources/regulation-* 2>/dev/null || true
  if git diff --cached --quiet; then
    log "Nada nuevo para commitear."
  else
    git commit -m "ingesta: fill_gaps (SSCC/grid forming/modelos dinamicos/PTN) $(date +%F)"
    git push origin "$BRANCH"
    log "PUSH OK. Avisame para re-sintetizar wiki/ con los nuevos PDFs."
  fi
fi
