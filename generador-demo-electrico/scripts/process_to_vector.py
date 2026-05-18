"""Convierte archivos crudos en data/raw/ a chunks vectoriales en LanceDB."""
from __future__ import annotations

import _bootstrap  # noqa: F401

import json
import sys
import time
import traceback
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator, Optional

import pandas as pd
from loguru import logger

from config import settings as S


# ---- text extraction --------------------------------------------------------

def _read_meta(file_path: Path) -> dict:
    m = file_path.with_suffix(file_path.suffix + ".meta.json")
    if m.exists():
        try:
            return json.loads(m.read_text("utf-8"))
        except Exception:
            pass
    return {}


def extract_pdf(path: Path) -> Optional[str]:
    """Extrae texto con pdfplumber, fallback pypdf. Devuelve None si parece escaneado."""
    text_parts: list[str] = []
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
    except Exception as e:
        logger.warning(f"pdfplumber fail {path.name}: {e}; fallback pypdf")
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            for page in reader.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
        except Exception as e2:
            logger.error(f"pypdf fail {path.name}: {e2}")
            return None
    joined = "\n\n".join(text_parts).strip()
    # Heuristica de escaneo: <50 chars por pagina promedio
    if not joined or len(joined) < 50 * max(1, len(text_parts)):
        logger.warning(f"posible PDF escaneado (requiere OCR): {path.name}")
        return None
    return joined


def extract_csv(path: Path) -> Optional[str]:
    """Convierte CSV en descripcion textual estructurada.

    Para series largas (>500 filas) genera resumen estadistico mensual por barra
    si detecta columnas tipo `fecha`/`barra`/`cmg` o `usd/mwh`.
    """
    try:
        df = pd.read_csv(path)
    except Exception as e:
        try:
            df = pd.read_csv(path, sep=";")
        except Exception as e2:
            logger.warning(f"csv read fail {path.name}: {e} / {e2}")
            return None
    if df.empty:
        return None
    name = path.stem
    parts: list[str] = [f"# Dataset {name}\nFuente: {path.parent.name}.\nColumnas: {list(df.columns)}."]
    if len(df) > 500 and _looks_like_cmg(df):
        # resumen estadistico mensual por barra
        df2 = _normalize_cmg(df)
        if df2 is not None:
            monthly = df2.groupby(["mes", "barra"])["cmg"].agg(["min", "mean", "max", "count"]).reset_index()
            for _, r in monthly.iterrows():
                parts.append(
                    f"Resumen mensual CMg barra {r['barra']} mes {r['mes']}: "
                    f"min {r['min']:.2f}, prom {r['mean']:.2f}, max {r['max']:.2f}, "
                    f"horas {int(r['count'])} USD/MWh. Fuente: CEN."
                )
            # ademas un sample de filas (primeras 50)
            for _, r in df.head(50).iterrows():
                parts.append(_row_to_sentence(r, name))
        else:
            for _, r in df.head(500).iterrows():
                parts.append(_row_to_sentence(r, name))
    else:
        for _, r in df.head(1500).iterrows():
            parts.append(_row_to_sentence(r, name))
    return "\n".join(parts)


def _looks_like_cmg(df: pd.DataFrame) -> bool:
    cols = [c.lower() for c in df.columns]
    has_cmg = any("cmg" in c or "usd" in c or "marginal" in c for c in cols)
    has_date = any("fecha" in c or "date" in c or "timestamp" in c for c in cols)
    has_bar = any("barra" in c or "nodo" in c for c in cols)
    return has_cmg and has_date and has_bar


def _normalize_cmg(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    cols = {c.lower(): c for c in df.columns}
    def pick(*candidates):
        for cand in candidates:
            for k, real in cols.items():
                if cand in k:
                    return real
        return None
    c_date = pick("fecha", "date", "timestamp")
    c_bar = pick("barra", "nodo")
    c_val = pick("cmg", "usd", "marginal")
    if not (c_date and c_bar and c_val):
        return None
    out = pd.DataFrame({
        "fecha": pd.to_datetime(df[c_date], errors="coerce"),
        "barra": df[c_bar].astype(str),
        "cmg": pd.to_numeric(df[c_val], errors="coerce"),
    }).dropna()
    out["mes"] = out["fecha"].dt.strftime("%Y-%m")
    return out


def _row_to_sentence(row: pd.Series, dataset: str) -> str:
    fields = ", ".join(f"{k}={v}" for k, v in row.items() if pd.notna(v))
    return f"Registro {dataset}: {fields}."


def extract_xlsx(path: Path) -> Optional[str]:
    try:
        xls = pd.ExcelFile(path)
        out = []
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            if df.empty:
                continue
            out.append(f"# {path.stem} / hoja {sheet}\nColumnas: {list(df.columns)}.")
            for _, r in df.head(500).iterrows():
                out.append(_row_to_sentence(r, f"{path.stem}/{sheet}"))
        return "\n".join(out) if out else None
    except Exception as e:
        logger.warning(f"xlsx fail {path.name}: {e}")
        return None


def extract_json(path: Path) -> Optional[str]:
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception as e:
        logger.warning(f"json fail {path.name}: {e}")
        return None
    out: list[str] = []
    def walk(prefix, node):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(f"{prefix}.{k}" if prefix else k, v)
        elif isinstance(node, list):
            for i, v in enumerate(node[:200]):
                walk(f"{prefix}[{i}]", v)
        else:
            out.append(f"{prefix}: {node}")
    walk("", data)
    return "\n".join(out) if out else None


def extract_html_md(path: Path) -> Optional[str]:
    text = path.read_text("utf-8", errors="ignore")
    if path.suffix.lower() in (".html", ".htm"):
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(text, "lxml")
            for s in soup(["script", "style", "nav", "footer"]):
                s.decompose()
            return "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
        except Exception as e:
            logger.warning(f"html fail {path.name}: {e}")
            return None
    return text


EXTRACTORS = {
    ".pdf": extract_pdf,
    ".csv": extract_csv,
    ".xlsx": extract_xlsx,
    ".xls": extract_xlsx,
    ".json": extract_json,
    ".html": extract_html_md,
    ".htm": extract_html_md,
    ".md": extract_html_md,
    ".txt": extract_html_md,
}


# ---- chunking ---------------------------------------------------------------

def chunk_text(text: str, max_tokens: int = S.CHUNK_TOKENS, overlap: int = S.CHUNK_OVERLAP) -> list[str]:
    """Chunking por parrafos con tokenizer simple. Tokenizer real via tiktoken si esta."""
    if not text:
        return []
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        def n_tok(s): return len(enc.encode(s))
    except Exception:
        def n_tok(s): return max(1, len(s) // 4)

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    cur: list[str] = []
    cur_tok = 0
    for p in paragraphs:
        pt = n_tok(p)
        if pt > max_tokens:
            # parrafo gigante: cortar por oraciones aprox
            for s in p.split(". "):
                if cur_tok + n_tok(s) > max_tokens and cur:
                    chunks.append("\n\n".join(cur))
                    cur = _tail_overlap(cur, n_tok, overlap)
                    cur_tok = sum(n_tok(x) for x in cur)
                cur.append(s)
                cur_tok += n_tok(s)
            continue
        if cur_tok + pt > max_tokens and cur:
            chunks.append("\n\n".join(cur))
            cur = _tail_overlap(cur, n_tok, overlap)
            cur_tok = sum(n_tok(x) for x in cur)
        cur.append(p)
        cur_tok += pt
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def _tail_overlap(cur: list[str], n_tok, overlap_tokens: int) -> list[str]:
    out: list[str] = []
    tok = 0
    for p in reversed(cur):
        pt = n_tok(p)
        if tok + pt > overlap_tokens:
            break
        out.insert(0, p)
        tok += pt
    return out


# ---- metadata + storage -----------------------------------------------------

@dataclass
class ChunkRow:
    doc_id: str
    source: str
    source_url: str
    fecha_documento: str
    fecha_descarga: str
    tipo: str
    tecnologia: Optional[str]
    barra: Optional[str]
    chunk_index: int
    total_chunks: int
    hash_original: str
    file_path: str
    text: str


def classify_path(path: Path) -> tuple[str, Optional[str], Optional[str]]:
    """Devuelve (tipo, tecnologia, barra) inferidos del path/nombre."""
    s = str(path).lower()
    tipo = "reporte"
    if "regulacion" in s or "ntsycs" in s or "lge" in s or "ciberseguridad" in s:
        tipo = "normativo"
    elif "costos_marginales" in s or "generacion" in s or "demanda" in s or "precipita" in s or "instalaciones" in s:
        tipo = "operacional"
    elif "mercado" in s or "transferencias" in s or "precios_nudo" in s:
        tipo = "mercado"
    tec = None
    for t in ("hidro", "eolico", "solar", "termico"):
        if t in s:
            tec = t
            break
    barra = None
    if "cmg_horario_" in path.name:
        # cmg_horario_<barra>_<yyyy-mm>.csv
        m = path.stem.split("_")
        if len(m) >= 3:
            barra = m[2].replace("-", " ").title()
    return tipo, tec, barra


def fecha_documento_guess(meta: dict, path: Path) -> str:
    if meta.get("fecha_documento"):
        return meta["fecha_documento"]
    import re
    m = re.search(r"(20\d{2})[-_]?(\d{2})", path.stem)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return ""


def iter_raw_files() -> Iterator[Path]:
    for p in S.DATA_RAW.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTRACTORS:
            yield p


# ---- embeddings + lancedb ---------------------------------------------------

def _embed_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(S.EMBED_MODEL)


def _connect_lancedb():
    import lancedb
    return lancedb.connect(str(S.LANCEDB_PATH))


def process_all() -> dict:
    """Procesa todos los archivos raw y los indexa en LanceDB."""
    counts: dict[str, int] = defaultdict(int)
    manifest: list[dict] = []
    stats: dict = {"started_at": datetime.utcnow().isoformat() + "Z"}

    files = list(iter_raw_files())
    if not files:
        logger.warning("No hay archivos raw para procesar.")
        stats["finished_at"] = datetime.utcnow().isoformat() + "Z"
        S.MANIFEST_PATH.write_text(json.dumps({"docs": [], "stats": stats}, indent=2), encoding="utf-8")
        return stats

    logger.info(f"Procesando {len(files)} archivos raw...")

    try:
        model = _embed_model()
        db = _connect_lancedb()
    except Exception as e:
        logger.error(f"setup embeddings/lancedb fail: {e}")
        raise

    rows: list[dict] = []
    requires_ocr: list[str] = []

    for f in files:
        try:
            meta = _read_meta(f)
            ext = f.suffix.lower()
            extractor = EXTRACTORS.get(ext)
            if not extractor:
                continue
            text = extractor(f)
            if text is None:
                if ext == ".pdf":
                    requires_ocr.append(str(f.relative_to(S.ROOT)))
                continue
            chunks = chunk_text(text)
            if not chunks:
                continue
            tipo, tec, barra = classify_path(f)
            doc_id = meta.get("sha256", "")[:16] or f.stem
            embs = model.encode(chunks, batch_size=32, show_progress_bar=False, normalize_embeddings=True)
            for i, (ch, vec) in enumerate(zip(chunks, embs)):
                row = ChunkRow(
                    doc_id=doc_id,
                    source=str(f.parent.relative_to(S.DATA_RAW)),
                    source_url=meta.get("url", ""),
                    fecha_documento=fecha_documento_guess(meta, f),
                    fecha_descarga=meta.get("downloaded_at", ""),
                    tipo=tipo,
                    tecnologia=tec,
                    barra=barra,
                    chunk_index=i,
                    total_chunks=len(chunks),
                    hash_original=meta.get("sha256", ""),
                    file_path=str(f.relative_to(S.ROOT)),
                    text=ch,
                )
                d = asdict(row)
                d["vector"] = vec.tolist()
                rows.append(d)
            manifest.append({
                "doc_id": doc_id,
                "file_path": str(f.relative_to(S.ROOT)),
                "source_url": meta.get("url", ""),
                "hash": meta.get("sha256", ""),
                "chunks": len(chunks),
                "indexed_at": datetime.utcnow().isoformat() + "Z",
            })
            counts["docs_indexed"] += 1
            counts["chunks_total"] += len(chunks)
            logger.info(f"OK {f.name}: {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"FAIL {f.name}: {e}\n{traceback.format_exc()}")
            counts["docs_failed"] += 1

    if rows:
        if "chunks" in db.table_names():
            db.drop_table("chunks")
        db.create_table("chunks", data=rows, mode="overwrite")
        logger.info(f"LanceDB: tabla 'chunks' con {len(rows)} filas en {S.LANCEDB_PATH}")
    else:
        logger.warning("No hubo rows que escribir a LanceDB.")

    stats.update({
        "finished_at": datetime.utcnow().isoformat() + "Z",
        "docs_indexed": counts["docs_indexed"],
        "docs_failed": counts["docs_failed"],
        "chunks_total": counts["chunks_total"],
        "requires_ocr": requires_ocr,
    })
    S.MANIFEST_PATH.write_text(
        json.dumps({"docs": manifest, "stats": stats}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"manifest.json escrito ({len(manifest)} docs)")
    return stats


def main() -> int:
    logger.remove()
    logger.add(sys.stderr, level="INFO",
               format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | {message}")
    logger.add(S.SYNC_LOG, level="DEBUG", rotation="50 MB", retention=10)
    t0 = time.time()
    stats = process_all()
    logger.info(f"process_to_vector done in {(time.time()-t0)/60:.1f} min: {stats}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
