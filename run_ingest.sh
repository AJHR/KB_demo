#!/usr/bin/env bash
# Wrapper para ingest_manual.py. Sin deps externas — usa el python del sistema.
#
# Casos:
#   bash run_ingest.sh /path/al/DS_113_2020.pdf   # uno solo, pregunta topic+url
#   bash run_ingest.sh                            # modo inbox/ batch interactivo
#   bash run_ingest.sh --fix-orphans              # repara PDFs sin .meta.json
#   bash run_ingest.sh --list-topics              # ver topics disponibles

set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
BRANCH="${BRANCH:-claude/create-kb-prompt-3hYLl}"
PUSH="${PUSH:-1}"

log() { printf "\n==> %s\n" "$*"; }

# Pull primero
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$CURRENT_BRANCH" = "$BRANCH" ]; then
  git pull --ff-only origin "$BRANCH" || true
fi

# Buscar python funcional (mismo smoke test que los otros wrappers)
PYBIN=""
for cand in python3.12 python3.13 python3.11 python3.10 python3; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import json, hashlib, shutil" 2>/dev/null; then
    PYBIN="$cand"; break
  fi
done
[ -z "$PYBIN" ] && { echo "ERROR: no encuentro python3" >&2; exit 1; }

# Caso default: si no hay args y existe inbox/, modo inbox
if [ "$#" -eq 0 ]; then
  if [ -d "inbox" ] && [ -n "$(ls inbox/*.pdf 2>/dev/null || true)" ]; then
    log "Modo inbox (encontre PDFs en inbox/)"
    "$PYBIN" generador-demo-electrico/scripts/ingest_manual.py --inbox inbox/
  else
    log "Crea inbox/ con PDFs adentro, o pasa un PDF como argumento."
    echo ""
    "$PYBIN" generador-demo-electrico/scripts/ingest_manual.py --list-topics
    echo ""
    echo "Usos:"
    echo "  mkdir inbox && cp ~/Downloads/*.pdf inbox/ && bash run_ingest.sh"
    echo "  bash run_ingest.sh /path/al/DS_113.pdf"
    echo "  bash run_ingest.sh --fix-orphans"
    exit 0
  fi
else
  "$PYBIN" generador-demo-electrico/scripts/ingest_manual.py "$@"
fi

# Generar .md companions de los PDFs nuevos. Usa .venv-reg si esta (tiene pypdf).
log "Generando .md companions (pdf_to_md, idempotente)..."
VENV="$ROOT/generador-demo-electrico/.venv-reg"
if [ -f "$VENV/bin/python" ] && "$VENV/bin/python" -c "import pypdf" 2>/dev/null; then
  "$VENV/bin/python" generador-demo-electrico/scripts/pdf_to_md.py \
    || log "WARN: pdf_to_md fallo; sigo con commit igual"
elif "$PYBIN" -c "import pypdf" 2>/dev/null; then
  "$PYBIN" generador-demo-electrico/scripts/pdf_to_md.py \
    || log "WARN: pdf_to_md fallo; sigo con commit igual"
else
  log "SKIP pdf_to_md: pypdf no instalado. Para activarlo:"
  log "  $VENV/bin/pip install pypdf  (o)  $PYBIN -m pip install --user pypdf"
fi

# Commit + push si PUSH=1 y hubo cambios
if [ "$PUSH" = "1" ]; then
  git add sources/regulation-* 2>/dev/null || true
  if git diff --cached --quiet; then
    log "Nada nuevo para commitear."
  else
    git commit -m "ingesta manual + md companions ($(date +%F))"
    git push origin "$BRANCH"
    log "PUSH OK. Avisame para re-sintetizar wiki/ con los nuevos PDFs."
  fi
fi
