# generador-demo-electrico

KB de demo para el sector electrico chileno: scraping respetuoso de fuentes publicas (CEN, CNE, Energia Abierta, Ministerio de Energia) + vector store local con embeddings multilingues.

> Vive como subcarpeta del KB principal. Los archivos crudos descargados a `data/raw/` se ingieren posteriormente al KB padre en `sources/{topic}/` siguiendo el flujo de `CLAUDE.md` de la raiz.

## Stack
- Python 3.11+
- `httpx` + `beautifulsoup4` (estatico), `playwright` chromium headless (JS / formularios)
- `pandas`, `pdfplumber` (fallback `pypdf`)
- `lancedb` + `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
- `apscheduler`, `loguru`, `tenacity`

## Setup

```bash
cd generador-demo-electrico
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Reglas de scraping (no negociable)

- Rate limit: 3s + jitter +-1s entre requests al mismo dominio. 429/503 dobla el delay.
- User-Agent: `GeneradorKBDemo/1.0 (research; contacto: demo@generador.local)`. No mentir.
- robots.txt: chequear al inicio, registrar Disallow en `logs/skipped_by_robots.txt`.
- Reintentos: 3 maximo, backoff exponencial 3s/9s/27s.
- Concurrencia: 1 request simultaneo por dominio.
- Sin bypass de auth. Login -> `logs/auth_required.txt` y seguir.
- Caching por hash de contenido.

## Comandos

```bash
python scripts/initial_load.py        # carga inicial (6-8 horas esperadas)
python scripts/process_to_vector.py   # raw -> embeddings -> lancedb
python scripts/update_daily.py        # delta 7 dias (programar 06:00 CL)
python scripts/update_weekly.py       # normativa + informe mensual (lun 07:00 CL)
```

## Estructura

```
generador-demo-electrico/
├── config/{sources.yaml, settings.py}
├── scrapers/{base_scraper, cen_scraper, cne_scraper, energia_abierta, regulation_scraper}.py
├── scripts/{initial_load, process_to_vector, update_daily, update_weekly}.py
├── data/
│   ├── raw/{cen,cne,regulacion,reportes,mercado}/...
│   └── vector/{lancedb/, manifest.json}
└── logs/{sync.log, skipped_by_robots.txt, auth_required.txt, failed_downloads.txt}
```

## Salidas

- `data/raw/` — archivos originales (CSV/PDF/JSON/MD) con metadatos en sidecars `.meta.json`.
- `data/vector/lancedb/` — base vectorial RAG con citas trazables al chunk de origen.
- `data/vector/manifest.json` — inventario indexado: doc_id, hash, fecha.
- `logs/` — auditoria verbosa.
- `REPORTE_INGESTA.md` (raiz del proyecto) — reporte de la corrida con counts, cobertura temporal, fallos y 5 queries demo contra el vector store.
