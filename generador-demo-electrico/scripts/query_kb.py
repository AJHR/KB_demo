#!/usr/bin/env python3
"""CLI para buscar en el vector store del KB.

Uso:
    python query_kb.py "como se calcula la potencia firme"
    python query_kb.py --topk 10 "bloques horarios pmgd con bess"
    python query_kb.py --topic regulation-cne-reglamentos-mercado "que es panel de expertos"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parent.parent.parent
LANCEDB_DIR = REPO / "data" / "vector" / "lancedb"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main() -> int:
    ap = argparse.ArgumentParser(description="Query del vector store del KB.")
    ap.add_argument("query", help="Pregunta en lenguaje natural")
    ap.add_argument("--topk", type=int, default=5, help="Cantidad de resultados (default 5)")
    ap.add_argument("--topic", default=None,
                    help="Filtrar a un topic especifico (ej. regulation-cne-reglamentos-mercado)")
    ap.add_argument("--full", action="store_true",
                    help="Mostrar chunk completo (no recortar a 400 chars)")
    args = ap.parse_args()

    if not LANCEDB_DIR.exists():
        print(f"ERROR: no existe {LANCEDB_DIR}. Corre primero process_sources.py.",
              file=sys.stderr)
        return 1

    import lancedb
    from sentence_transformers import SentenceTransformer

    db = lancedb.connect(str(LANCEDB_DIR))
    if "chunks" not in db.table_names():
        print("ERROR: tabla 'chunks' no existe en LanceDB.", file=sys.stderr)
        return 1

    tbl = db.open_table("chunks")
    model = SentenceTransformer(EMBED_MODEL)
    vec = model.encode(args.query, normalize_embeddings=True).tolist()

    q = tbl.search(vec)
    if args.topic:
        q = q.where(f"topic = '{args.topic}'")
    hits = q.limit(args.topk).to_list()

    print(f"\nQuery: {args.query}")
    if args.topic:
        print(f"Topic: {args.topic}")
    print(f"Resultados: {len(hits)}\n")

    for i, h in enumerate(hits, 1):
        score = h.get("_distance", 0)
        text = h.get("text", "")
        if not args.full and len(text) > 400:
            text = text[:400].rsplit(" ", 1)[0] + "..."
        text = text.replace("\n", " ")
        print(f"{i}. [{score:.3f}] {h.get('file_path')}")
        print(f"   chunk {h.get('chunk_index')}/{h.get('total_chunks')-1}  topic={h.get('topic')}")
        url = h.get("source_url")
        if url:
            print(f"   url: {url}")
        print(f"   > {text}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
