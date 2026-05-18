# Log — Registro cronologico del KB

Append-only. Entradas mas recientes arriba. Cada entrada: fecha, accion, contexto.

Formato:

```
## YYYY-MM-DD
- [accion] descripcion breve (origen / autor)
```

---

## 2026-05-15
- [vector] Agregado pipeline RAG: `generador-demo-electrico/scripts/process_sources.py` (sources/*.pdf -> chunks -> embeddings -> LanceDB), `query_kb.py` (CLI de busqueda semantica), `run_vector.sh` (wrapper Mac). Modelo `paraphrase-multilingual-MiniLM-L12-v2` (384d). `data/vector/lancedb/` gitignored, `manifest.json` y `README.md` versionados. Pendiente ejecucion en Mac.
- [gitignore] Anadido `.gitignore` raiz: data/vector/lancedb/, __pycache__, .venv*/, .DS_Store.
- [wiki] Sintetizadas 4 paginas en `wiki/` con frontmatter completo: `mercado-mayorista-chile.md`, `servicios-complementarios-y-transferencias.md`, `conexion-y-transmision.md`, `marco-pmgd-y-distribuida.md`. Cada una cita inline PDFs reales de `sources/regulation-*/`. Texto extraido con `pypdf` de los reglamentos clave (DOC23, NT Coordinacion y Operacion, NTCO-PMGD-2026, DS 144, DS 48, sistemas de medidas).
- [index/RESUMEN] `index.md` y `wiki/RESUMEN.md` actualizados para reflejar el contenido real bajado. Glosario de siglas agregado al index.
- [scraper] Detectadas 2 URLs erradas en la corrida `093393b`: `cne.cl/tarificacion/electrica/precios-nudo/` y `coordinador.cl/normativa/`. Tambien `coordinador.cl/mercados/` y `coordinador.cl/operacion/` entregaron solo 1 archivo cada una. Fix pendiente en `regulation_only.py` con URLs alternativas.

## 2026-05-14
- [ingesta] Corrida `093393b` de `regulation_only.py` desde Mac local. 254 PDFs (207 unicos, ~390 MB) en 9 carpetas `sources/regulation-*/`. RESUMEN.md auto-generado por el script en cada carpeta. CEN y CNE accesibles desde el Mac (no asi desde sandbox).
- [scraping-project] Anadido `generador-demo-electrico/` como subcarpeta: pipeline de scraping respetuoso (httpx + playwright) de CEN, CNE, Energia Abierta y Minenergia con vector store local (lancedb + sentence-transformers). Listo para correr en entorno con red saliente. Sandbox actual bloqueado por 403, ver `generador-demo-electrico/REPORTE_INGESTA.md`. Cuando se corra de verdad, el contenido de `data/raw/` se ingerira al KB padre bajo `sources/{cen-...,cne-...,regulacion-...}/`.
- [scaffold] Estructura inicial creada: `sources/`, `work/`, `wiki/`, `tools/`. CLAUDE.md con gobernanza, index.md, log.md, wiki/RESUMEN.md, tools/lint-kb.sh. Repo vacio, listo para ingestion.
