# Log — Registro cronologico del KB

Append-only. Entradas mas recientes arriba. Cada entrada: fecha, accion, contexto.

Formato:

```
## YYYY-MM-DD
- [accion] descripcion breve (origen / autor)
```

---

## 2026-05-14
- [scraping-project] Anadido `spence-demo-electrico/` como subcarpeta: pipeline de scraping respetuoso (httpx + playwright) de CEN, CNE, Energia Abierta y Minenergia con vector store local (lancedb + sentence-transformers). Listo para correr en entorno con red saliente. Sandbox actual bloqueado por 403, ver `spence-demo-electrico/REPORTE_INGESTA.md`. Cuando se corra de verdad, el contenido de `data/raw/` se ingerira al KB padre bajo `sources/{cen-...,cne-...,regulacion-...}/`.
- [scaffold] Estructura inicial creada: `sources/`, `work/`, `wiki/`, `tools/`. CLAUDE.md con gobernanza, index.md, log.md, wiki/RESUMEN.md, tools/lint-kb.sh. Repo vacio, listo para ingestion.
