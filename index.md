# Index — Knowledge Base

Catalogo navegable de este repositorio. Para reglas y schema ver [`CLAUDE.md`](./CLAUDE.md). Para historial de cambios ver [`log.md`](./log.md).

## Zonas

### `sources/` — Referencia inmutable

Material importado de afuera que no editamos. Cada subcarpeta tiene un `RESUMEN.md`.

_(vacio — agregar entradas cuando entre contenido)_

| Carpeta | Tema | RESUMEN |
|---------|------|---------|

### `work/` — Documentos vivos

Documentos nuestros que evolucionan: minutas, diagnosticos, decisiones.

_(vacio — agregar entradas cuando entre contenido)_

| Carpeta | Tema | RESUMEN |
|---------|------|---------|

### `wiki/` — Sintesis

Paginas generadas que cruzan fuentes. Ver [`wiki/RESUMEN.md`](./wiki/RESUMEN.md).

| Pagina | Tema | Fuentes | Ultima sintesis |
|--------|------|---------|-----------------|

### `tools/` — Mantenimiento

| Script | Proposito |
|--------|-----------|
| [`tools/lint-kb.sh`](./tools/lint-kb.sh) | Verificar invariantes del KB (ver CLAUDE.md) |

### Subproyectos

| Subproyecto | Proposito |
|-------------|-----------|
| [`spence-demo-electrico/`](./spence-demo-electrico/README.md) | Pipeline de scraping respetuoso CEN+CNE+Energia Abierta+Minenergia + vector store LanceDB. El output de `spence-demo-electrico/data/raw/` se ingiere posteriormente al KB padre bajo `sources/`. Estado: codigo listo, ejecucion bloqueada en sandbox actual (ver `REPORTE_INGESTA.md`). |
