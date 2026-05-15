#!/usr/bin/env bash
# Scrapea regulacion electrica chilena directo al KB (sources/regulation-*).
# Idempotente: podes relanzarlo sin problema.
#
# Uso (desde la raiz del repo, en la branch claude/create-kb-prompt-3hYLl):
#   bash run_regulation.sh
#
# Variables opcionales:
#   PUSH=0 bash run_regulation.sh   # solo descarga, no hace git commit/push
#   BRANCH=otra-branch bash run_regulation.sh

set -euo pipefail

cd "$(dirname "$0")"
ROOT="$PWD"
BRANCH="${BRANCH:-claude/create-kb-prompt-3hYLl}"
PUSH="${PUSH:-1}"

log() { printf "\n==> %s\n" "$*"; }

# 1. Python: probamos en orden hasta encontrar uno que ande
PYBIN=""
for cand in python3.11 python3.12 python3.10 python3.13 python3; do
  if command -v "$cand" >/dev/null 2>&1; then
    PYBIN="$cand"
    break
  fi
done
if [ -z "$PYBIN" ]; then
  if command -v brew >/dev/null 2>&1; then
    log "Instalando python@3.11 (brew)..."
    brew install python@3.11
    PYBIN="python3.11"
  else
    echo "ERROR: no encuentro python3.x. Instalalo con: brew install python@3.11" >&2
    exit 1
  fi
fi
log "Usando: $PYBIN ($($PYBIN --version 2>&1))"

# 2. Branch correcta (no falla si ya estamos ahi)
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
  log "Cambiando a branch $BRANCH..."
  git fetch origin "$BRANCH"
  git checkout "$BRANCH"
fi
git pull --ff-only origin "$BRANCH" || true

# 3. venv ligero (sin Playwright, sin sentence-transformers)
VENV="$ROOT/spence-demo-electrico/.venv-reg"
# Verificamos que el venv este COMPLETO (no solo que exista el directorio)
if [ ! -f "$VENV/bin/activate" ]; then
  if [ -d "$VENV" ]; then
    log "venv anterior incompleto; lo borro y recreo..."
    rm -rf "$VENV"
  fi
  log "Creando venv ligero con $PYBIN en $VENV..."
  if ! "$PYBIN" -m venv "$VENV"; then
    log "venv standard fallo; reintento con --without-pip y bootstrap manual..."
    "$PYBIN" -m venv --without-pip "$VENV"
    # bootstrap pip via get-pip
    "$VENV/bin/python" -m ensurepip --upgrade 2>/dev/null || {
      curl -sSL https://bootstrap.pypa.io/get-pip.py | "$VENV/bin/python"
    }
  fi
  if [ ! -f "$VENV/bin/activate" ]; then
    echo "ERROR: no pude crear el venv en $VENV. Probemos manualmente:" >&2
    echo "  rm -rf $VENV && $PYBIN -m venv $VENV" >&2
    exit 1
  fi
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet httpx beautifulsoup4 lxml

# 4. Scrapear
log "Ejecutando regulation_only.py (10-30 min esperados)..."
python spence-demo-electrico/scripts/regulation_only.py

# 5. Commit + push (opcional)
if [ "$PUSH" = "1" ]; then
  git add sources/regulation-* 2>/dev/null || true
  if git diff --cached --quiet; then
    log "Nada nuevo para commitear."
  else
    log "Commiteando + pusheando a $BRANCH..."
    git commit -m "ingesta: regulacion electrica chilena ($(date +%F))"
    git push -u origin "$BRANCH"
    log "PUSH OK. Avisame en el chat y desde mi sandbox sintetizo wiki/ + RESUMEN.md."
  fi
else
  log "PUSH=0: archivos en sources/regulation-* sin commit."
fi
