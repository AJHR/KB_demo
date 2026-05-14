# wiki/

## Que contiene
Paginas de sintesis generadas por LLM que cruzan multiples fuentes de `sources/` y `work/`. Cada pagina cita sus origenes via frontmatter YAML y se considera viva: se regenera cuando sus fuentes cambian.

## Archivos clave
| Archivo | Descripcion | Notas |
|---------|-------------|-------|
| _(ninguno todavia)_ | - | Agregar paginas cuando haya fuentes que sintetizar |

## Como agregar una pagina
1. Identifica un tema cross-fuente (no un resumen de una sola carpeta).
2. Crea `wiki/{tema-en-kebab-case}.md` con frontmatter:
   ```yaml
   ---
   title: Nombre legible
   sources:
     - sources/.../archivo.md
     - work/.../otro.md
   last_synthesized: YYYY-MM-DD
   ---
   ```
3. Cita inline los hechos no obvios.
4. Registra en `log.md` y `index.md`.

## Advertencias
- Las paginas son derivadas. La fuente de verdad sigue siendo `sources/` y `work/`.
- `tools/lint-kb.sh` marca como stale las paginas cuyas fuentes cambiaron despues de `last_synthesized`.
