#!/usr/bin/env python3
"""Procesa sources/regulation-*/*.pdf a vector store LanceDB.

Lee directo del KB (sources/), no de data/raw/. Pensado para correr desde
el Mac despues de regulation_only.py.

Output:
  <repo>/data/vector/lancedb/      (binario, gitignored)
  <repo>/data/vector/manifest.json (committed)
  <repo>/data/vector/README.md     (committed)

Idempotente: skip PDFs cuyo hash ya esta en manifest.json. Re-runs son baratos.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parent.parent.parent
SOURCES = REPO / "sources"
VECTOR_DIR = REPO / "data" / "vector"
LANCEDB_DIR = VECTOR_DIR / "lancedb"
MANIFEST = VECTOR_DIR / "manifest.json"

EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM = 384
CHUNK_TOKENS = 800
CHUNK_OVERLAP = 150


@dataclass
class ChunkRow:
    doc_id: str          # sha256[:16] del PDF
    file_path: str       # ej. sources/regulation-cne-reglamentos-mercado/NTCO-PMGD-2026.pdf
    topic: str           # ej. regulation-cne-reglamentos-mercado
    source_url: str      # URL original (del .meta.json sidecar)
    hash_original: str
    chunk_index: int
    total_chunks: int
    text: str


# ---- text extraction (pypdf) -----------------------------------------------

def extract_pdf_text(path: Path) -> Optional[str]:
    """Devuelve texto completo del PDF o None si parece escaneado."""
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path))
        parts: list[str] = []
        for page in r.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                parts.append("")
        text = "\n\n".join(parts).strip()
        # Heuristica de escaneo: <50 chars/pagina promedio
        if not text or len(text) < 50 * max(1, len(r.pages)):
            return None
        return text
    except Exception as e:
        print(f"  WARN pypdf fail {path.name}: {e}")
        return None


# ---- chunking ---------------------------------------------------------------

def _make_tokenizer():
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return lambda s: len(enc.encode(s))
    except Exception:
        return lambda s: max(1, len(s) // 4)


def chunk_text(text: str, n_tok=None, max_tokens: int = CHUNK_TOKENS,
               overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text:
        return []
    if n_tok is None:
        n_tok = _make_tokenizer()
    paragraphs = [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]
    chunks: list[str] = []
    cur: list[str] = []
    cur_t = 0
    for p in paragraphs:
        pt = n_tok(p)
        if pt > max_tokens:
            # parrafo gigante -> cortar por oraciones
            for s in re.split(r"(?<=[\.!?])\s+", p):
                st = n_tok(s)
                if cur_t + st > max_tokens and cur:
                    chunks.append("\n\n".join(cur))
                    cur = _tail_overlap(cur, n_tok, overlap)
                    cur_t = sum(n_tok(x) for x in cur)
                cur.append(s)
                cur_t += st
            continue
        if cur_t + pt > max_tokens and cur:
            chunks.append("\n\n".join(cur))
            cur = _tail_overlap(cur, n_tok, overlap)
            cur_t = sum(n_tok(x) for x in cur)
        cur.append(p)
        cur_t += pt
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def _tail_overlap(cur: list[str], n_tok, overlap_tokens: int) -> list[str]:
    out: list[str] = []
    tot = 0
    for p in reversed(cur):
        pt = n_tok(p)
        if tot + pt > overlap_tokens:
            break
        out.insert(0, p)
        tot += pt
    return out


# ---- metadata helpers ------------------------------------------------------

def read_sidecar(pdf: Path) -> dict:
    m = pdf.with_suffix(pdf.suffix + ".meta.json")
    if m.exists():
        try:
            return json.loads(m.read_text("utf-8"))
        except Exception:
            return {}
    return {}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            buf = f.read(1 << 20)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text("utf-8"))
        except Exception:
            pass
    return {"docs": [], "stats": {}}


def save_manifest(m: dict) -> None:
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


# ---- main ------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    LANCEDB_DIR.mkdir(parents=True, exist_ok=True)

    # Inputs
    pdfs = sorted(SOURCES.rglob("*.pdf"))
    print(f"Encontrados {len(pdfs)} PDFs en {SOURCES}")
    if not pdfs:
        print("Nada que procesar.")
        return 0

    manifest = load_manifest()
    indexed_hashes = {d["hash"] for d in manifest.get("docs", []) if d.get("hash")}

    # Lazy imports (pesados)
    print("Cargando sentence-transformers...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBED_MODEL)
    print("Cargando lancedb...")
    import lancedb
    db = lancedb.connect(str(LANCEDB_DIR))
    n_tok = _make_tokenizer()

    rows: list[dict] = []
    new_docs: list[dict] = []
    skipped = {"already_indexed": 0, "requires_ocr": 0, "no_text": 0, "errors": 0}
    requires_ocr: list[str] = []

    for i, pdf in enumerate(pdfs, 1):
        try:
            file_hash = sha256_file(pdf)
            if file_hash in indexed_hashes:
                skipped["already_indexed"] += 1
                continue
            text = extract_pdf_text(pdf)
            if text is None:
                rel = str(pdf.relative_to(REPO))
                requires_ocr.append(rel)
                skipped["requires_ocr"] += 1
                print(f"  [{i}/{len(pdfs)}] OCR? {pdf.name}")
                continue
            chunks = chunk_text(text, n_tok=n_tok)
            if not chunks:
                skipped["no_text"] += 1
                continue
            sidecar = read_sidecar(pdf)
            topic = pdf.parent.name
            doc_id = file_hash[:16]
            embs = model.encode(chunks, batch_size=32, show_progress_bar=False,
                                normalize_embeddings=True)
            for ci, (ch, vec) in enumerate(zip(chunks, embs)):
                row = ChunkRow(
                    doc_id=doc_id,
                    file_path=str(pdf.relative_to(REPO)),
                    topic=topic,
                    source_url=sidecar.get("url", ""),
                    hash_original=file_hash,
                    chunk_index=ci,
                    total_chunks=len(chunks),
                    text=ch,
                )
                d = asdict(row)
                d["vector"] = vec.tolist()
                rows.append(d)
            new_docs.append({
                "doc_id": doc_id,
                "file_path": str(pdf.relative_to(REPO)),
                "topic": topic,
                "source_url": sidecar.get("url", ""),
                "hash": file_hash,
                "chunks": len(chunks),
                "indexed_at": datetime.utcnow().isoformat() + "Z",
            })
            print(f"  [{i}/{len(pdfs)}] OK   {pdf.name}: {len(chunks)} chunks")
        except Exception as e:
            skipped["errors"] += 1
            print(f"  [{i}/{len(pdfs)}] FAIL {pdf.name}: {e}")
            traceback.print_exc()

    # Escribir LanceDB
    if rows:
        if "chunks" in db.table_names():
            tbl = db.open_table("chunks")
            tbl.add(rows)
            n_added = len(rows)
            print(f"LanceDB: append {n_added} chunks a tabla existente")
        else:
            db.create_table("chunks", data=rows)
            print(f"LanceDB: tabla 'chunks' creada con {len(rows)} chunks")
    else:
        print("Sin filas nuevas que escribir.")

    # Actualizar manifest
    manifest["docs"].extend(new_docs)
    manifest["stats"] = {
        "last_run": datetime.utcnow().isoformat() + "Z",
        "total_docs_in_index": len(manifest["docs"]),
        "total_chunks_added_this_run": len(rows),
        "embed_model": EMBED_MODEL,
        "embed_dim": EMBED_DIM,
        "chunk_tokens": CHUNK_TOKENS,
        "chunk_overlap": CHUNK_OVERLAP,
        "requires_ocr": requires_ocr,
        "skipped": skipped,
    }
    save_manifest(manifest)

    dt = (time.time() - t0) / 60
    print(f"\n=== RESUMEN ===")
    print(f"  Tiempo: {dt:.1f} min")
    print(f"  PDFs procesados nuevos:  {len(new_docs)}")
    print(f"  Chunks agregados:        {len(rows)}")
    print(f"  Ya indexados (skip):     {skipped['already_indexed']}")
    print(f"  Requieren OCR (skip):    {skipped['requires_ocr']}")
    print(f"  Sin texto extraible:     {skipped['no_text']}")
    print(f"  Errores:                 {skipped['errors']}")
    print(f"  Manifest: {MANIFEST.relative_to(REPO)}")
    print(f"  LanceDB:  {LANCEDB_DIR.relative_to(REPO)}")
    print(f"\nProba el RAG: python generador-demo-electrico/scripts/query_kb.py 'tu pregunta'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
