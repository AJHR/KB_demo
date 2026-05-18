# data/vector/

Vector store del KB para busqueda semantica sobre `sources/`.

## Contenido

| Archivo | Versionado | Que es |
|---------|------------|--------|
| `manifest.json` | Si | Inventario JSON: doc_id, file_path, hash, chunks, indexed_at por PDF indexado. Util para humanos y para procesos delta. |
| `lancedb/` | **No** (gitignored) | Base vectorial binaria LanceDB. Se regenera localmente con `python generador-demo-electrico/scripts/process_sources.py`. |
| `README.md` | Si | Este archivo. |

## Como se genera

Desde la raiz del repo, despues de tener `sources/regulation-*/*.pdf`:

```bash
bash run_vector.sh
```

O manualmente:

```bash
source generador-demo-electrico/.venv-reg/bin/activate
pip install pypdf sentence-transformers lancedb pyarrow tiktoken
python generador-demo-electrico/scripts/process_sources.py
```

## Como se consulta

```bash
python generador-demo-electrico/scripts/query_kb.py "tu pregunta"
python generador-demo-electrico/scripts/query_kb.py --topic regulation-cne-reglamentos-mercado "potencia firme"
python generador-demo-electrico/scripts/query_kb.py --topk 10 "bess y grid forming"
```

## Schema de la tabla `chunks`

| Campo | Tipo | Para que |
|-------|------|----------|
| `doc_id` | str (sha256[:16]) | Identidad del PDF |
| `file_path` | str | Path relativo al repo (e.g. `sources/regulation-cne-reglamentos-mercado/NTCO-PMGD-2026.pdf`) |
| `topic` | str | Carpeta padre (`regulation-cne-reglamentos-mercado`) |
| `source_url` | str | URL original de descarga (del .meta.json sidecar) |
| `hash_original` | str | sha256 completo del PDF |
| `chunk_index` | int | 0-indexed |
| `total_chunks` | int | Total para el doc |
| `text` | str | Contenido del chunk |
| `vector` | list[float] (384) | Embedding (paraphrase-multilingual-MiniLM-L12-v2, normalized) |

## Parametros del indexado

| Parametro | Valor |
|-----------|-------|
| Modelo de embeddings | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (gratis, local, multilingue) |
| Dimension | 384 |
| Tokens por chunk | 800 |
| Overlap | 150 tokens |
| Tokenizer | tiktoken `cl100k_base` con fallback heuristico |

## Por que no commiteamos LanceDB

- Es binario (parquet + indices) — diff inutil
- ~10-50MB por cada 100k chunks
- Se reconstruye determinista desde `sources/` + manifest.json
- Cambios al modelo de embeddings invalidan toda la base; mejor regenerar
