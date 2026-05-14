#!/usr/bin/env bash
# lint-kb.sh — Verifica invariantes del KB descritos en CLAUDE.md.
# Exit code 0 = ok. Exit code != 0 = hay problemas.

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0
WARNINGS=0

err()  { echo "ERROR: $*"   >&2; ERRORS=$((ERRORS+1)); }
warn() { echo "WARN:  $*"   >&2; WARNINGS=$((WARNINGS+1)); }
info() { echo "INFO:  $*"; }

is_kebab_case() {
  # acepta solo a-z, 0-9 y guiones; no espacios, no mayusculas, no underscore
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]
}

# -----------------------------------------------------------------------------
# Check 1: RESUMEN.md existe en cada subcarpeta directa de sources/, work/, wiki/
# -----------------------------------------------------------------------------
info "Check 1: RESUMEN.md en cada subcarpeta de sources/, work/, wiki/"
for zone in sources work wiki; do
  [ -d "$zone" ] || continue
  while IFS= read -r -d '' dir; do
    if [ ! -f "$dir/RESUMEN.md" ]; then
      err "Falta RESUMEN.md en $dir"
    fi
  done < <(find "$zone" -mindepth 1 -maxdepth 1 -type d -print0)
done

# -----------------------------------------------------------------------------
# Check 2: Nombres de carpetas kebab-case
# -----------------------------------------------------------------------------
info "Check 2: Carpetas en kebab-case"
for zone in sources work wiki; do
  [ -d "$zone" ] || continue
  while IFS= read -r -d '' dir; do
    base="$(basename "$dir")"
    if ! is_kebab_case "$base"; then
      err "Carpeta no kebab-case: $dir"
    fi
  done < <(find "$zone" -mindepth 1 -type d -print0)
done

# -----------------------------------------------------------------------------
# Check 3: Wiki pages stale (sources modificados despues de last_synthesized)
# -----------------------------------------------------------------------------
info "Check 3: Wiki pages stale"
if [ -d wiki ]; then
  while IFS= read -r -d '' page; do
    [ "$(basename "$page")" = "RESUMEN.md" ] && continue
    last_syn=$(awk '/^---$/{f=!f; next} f && /^last_synthesized:/ {print $2; exit}' "$page")
    if [ -z "$last_syn" ]; then
      warn "Wiki page sin last_synthesized: $page"
      continue
    fi
    last_syn_ts=$(date -d "$last_syn" +%s 2>/dev/null || echo "")
    if [ -z "$last_syn_ts" ]; then
      warn "last_synthesized invalido en $page: $last_syn"
      continue
    fi
    # extraer lista de sources del frontmatter
    sources_list=$(awk '
      /^---$/{f=!f; next}
      f && /^sources:/{in_s=1; next}
      f && in_s && /^[[:space:]]*-/ {sub(/^[[:space:]]*-[[:space:]]*/,""); print; next}
      f && in_s && !/^[[:space:]]/ {in_s=0}
    ' "$page")
    while IFS= read -r src; do
      [ -z "$src" ] && continue
      if [ ! -f "$src" ]; then
        err "Wiki $page referencia source inexistente: $src"
        continue
      fi
      src_ts=$(stat -c %Y "$src" 2>/dev/null || stat -f %m "$src" 2>/dev/null)
      if [ -n "$src_ts" ] && [ "$src_ts" -gt "$last_syn_ts" ]; then
        warn "Stale: $page (source $src modificado despues de last_synthesized=$last_syn)"
      fi
    done <<< "$sources_list"
  done < <(find wiki -type f -name '*.md' -print0)
fi

# -----------------------------------------------------------------------------
# Check 4: Archivos > 500KB
# -----------------------------------------------------------------------------
info "Check 4: Archivos grandes (>500KB)"
while IFS= read -r -d '' f; do
  warn "Archivo grande (>500KB): $f"
done < <(find sources work wiki -type f -size +500k -print0 2>/dev/null)

# -----------------------------------------------------------------------------
# Check 5: Archivos raw sin companion .md
# -----------------------------------------------------------------------------
info "Check 5: Archivos raw (PDF/HTML/XLSX/PPTX/DOCX) sin companion .md"
while IFS= read -r -d '' raw; do
  base="${raw%.*}"
  if [ ! -f "${base}.md" ]; then
    warn "Raw sin companion .md: $raw (esperado ${base}.md)"
  fi
done < <(find sources work -type f \( -iname '*.pdf' -o -iname '*.html' -o -iname '*.htm' -o -iname '*.xlsx' -o -iname '*.pptx' -o -iname '*.docx' \) -print0 2>/dev/null)

# -----------------------------------------------------------------------------
# Check 6: Links relativos en index.md apuntan a archivos existentes
# -----------------------------------------------------------------------------
info "Check 6: Links validos en index.md"
if [ -f index.md ]; then
  # extrae rutas markdown tipo [text](./path) o [text](path)
  while IFS= read -r link; do
    # quita ./ inicial y posibles anclas #...
    path="${link#./}"
    path="${path%%#*}"
    [ -z "$path" ] && continue
    # ignora urls http(s)
    [[ "$path" =~ ^https?:// ]] && continue
    if [ ! -e "$path" ]; then
      err "index.md: link roto -> $link"
    fi
  done < <(grep -oE '\]\(([^)]+)\)' index.md | sed 's/^](//; s/)$//')
fi

# -----------------------------------------------------------------------------
# Check 7: Archivos en sources/ no modificados despues de su import
# -----------------------------------------------------------------------------
# Estrategia: se considera la fecha del primer commit que toco el archivo como
# "fecha de import". Si mtime/ultimo commit > primer commit, advertir.
info "Check 7: Inmutabilidad de sources/"
if [ -d sources ] && git rev-parse --git-dir > /dev/null 2>&1; then
  while IFS= read -r -d '' f; do
    first_commit=$(git log --diff-filter=A --follow --format=%H -- "$f" 2>/dev/null | tail -1)
    last_commit=$(git log -1 --format=%H -- "$f" 2>/dev/null)
    if [ -n "$first_commit" ] && [ -n "$last_commit" ] && [ "$first_commit" != "$last_commit" ]; then
      err "sources/ no inmutable: $f modificado despues del import"
    fi
  done < <(find sources -type f ! -name 'RESUMEN.md' ! -name '.gitkeep' -print0)
fi

# -----------------------------------------------------------------------------
# Resumen
# -----------------------------------------------------------------------------
echo ""
echo "===================="
echo " Errores:    $ERRORS"
echo " Warnings:   $WARNINGS"
echo "===================="

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi
exit 0
