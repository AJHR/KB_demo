#!/usr/bin/env python3
"""Convierte cada PDF en sources/ a un companion .md al lado.

Idempotente: si el .md existe y el hash del PDF no cambio, lo saltea.
Las .md tienen frontmatter con metadata + texto con marcadores de pagina.

Uso:
    python pdf_to_md.py                              # todo sources/
    python pdf_to_md.py --topic regulation-cne-...   # solo un topic
    python pdf_to_md.py --force                      # regenerar todos
    python pdf_to_md.py --root /path/a/sources       # otro root

Solo dep: pypdf.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

SCRIPT = Path(__file__).resolve()
DEFAULT_ROOT = SCRIPT.parent.parent.parent / "sources"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def read_sidecar_sha(pdf: Path) -> Optional[str]:
    """Si hay .meta.json, devuelve el sha256 cacheado (mas rapido que hashing)."""
    m = pdf.with_suffix(pdf.suffix + ".meta.json")
    if m.exists():
        try:
            return json.loads(m.read_text("utf-8")).get("sha256")
        except Exception:
            return None
    return None


def needs_regen(pdf: Path, md: Path) -> bool:
    """True si hay que (re)generar el .md."""
    if not md.exists():
        return True
    try:
        content = md.read_text("utf-8", errors="replace")
    except Exception:
        return True
    # leer frontmatter
    m = re.match(r"^---\n(.+?)\n---\n", content, re.S)
    if not m:
        return True
    fm = m.group(1)
    sha_match = re.search(r"^pdf_sha256:\s*(\S+)", fm, re.M)
    if not sha_match:
        return True
    md_sha = sha_match.group(1)
    pdf_sha = read_sidecar_sha(pdf) or sha256_file(pdf)
    return md_sha != pdf_sha


def clean_text(text: str) -> str:
    """Cleanup minimo: strip trailing whitespace, collapsa blank lines."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    out: list[str] = []
    blank = 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank <= 2:
                out.append(ln)
        else:
            blank = 0
            out.append(ln)
    return "\n".join(out).strip()


def extract_pdf(pdf: Path) -> tuple[Optional[str], dict]:
    """Devuelve (texto_con_marcadores_de_pagina, info_dict).
    info_dict tiene: n_pages, n_pages_extracted, chars_total, needs_ocr (heuristica), errors.
    """
    info = {"n_pages": 0, "n_pages_extracted": 0, "chars_total": 0,
            "needs_ocr": False, "errors": []}
    try:
        from pypdf import PdfReader
    except Exception as e:
        info["errors"].append(f"pypdf-import: {e}")
        return None, info
    try:
        r = PdfReader(str(pdf))
    except Exception as e:
        info["errors"].append(f"open: {e}")
        return None, info
    info["n_pages"] = len(r.pages)
    parts: list[str] = []
    for i, page in enumerate(r.pages, 1):
        try:
            t = page.extract_text() or ""
        except Exception as e:
            t = ""
            info["errors"].append(f"page-{i}: {e}")
        t = t.strip()
        if t:
            info["n_pages_extracted"] += 1
            info["chars_total"] += len(t)
        parts.append(f"<!-- page {i} -->\n\n{t}\n")
    text = "\n".join(parts)
    avg_per_page = info["chars_total"] / max(1, info["n_pages"])
    if avg_per_page < 50:
        info["needs_ocr"] = True
    return clean_text(text), info


def md_path_for(pdf: Path) -> Path:
    """xxx.pdf -> xxx.md (al lado)."""
    return pdf.with_suffix(".md")


def write_md(pdf: Path, text: Optional[str], info: dict, sha: str, repo_root: Path) -> Path:
    md = md_path_for(pdf)
    title = pdf.stem.replace("_", " ").replace("-", " ")
    rel_pdf = pdf.relative_to(repo_root).as_posix()
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines: list[str] = [
        "---",
        f"pdf_source: {rel_pdf}",
        f"pdf_sha256: {sha}",
        f"pdf_pages: {info['n_pages']}",
        f"extracted_pages: {info['n_pages_extracted']}",
        f"extracted_chars: {info['chars_total']}",
        f"extracted_at: {now}",
        "extractor: pypdf",
    ]
    if info["needs_ocr"]:
        lines.append("needs_ocr: true")
    if info["errors"]:
        lines.append("extraction_errors: " + json.dumps(info["errors"][:5], ensure_ascii=False))
    lines += ["---", "", f"# {title}", ""]
    if text is None or info["n_pages_extracted"] == 0:
        lines += ["**No se pudo extraer texto.** Posible PDF escaneado o corrupto.",
                  "Considere OCR (Tesseract / pdf2image)."]
    elif info["needs_ocr"]:
        lines += [f"**ADVERTENCIA**: PDF probablemente escaneado (promedio "
                  f"{info['chars_total']/max(1,info['n_pages']):.0f} chars/pag). "
                  f"Texto extraido puede ser incompleto.\n",
                  text]
    else:
        lines.append(text)
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md


def iter_pdfs(root: Path, topic_filter: Optional[str] = None):
    if topic_filter:
        topics = [root / topic_filter]
    else:
        topics = [d for d in sorted(root.iterdir()) if d.is_dir()]
    for topic in topics:
        if not topic.exists() or not topic.is_dir():
            continue
        for pdf in sorted(topic.rglob("*.pdf")):
            yield pdf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--topic", default=None, help="Solo un topic (ej. regulation-cne-reglamentos-mercado)")
    ap.add_argument("--force", action="store_true", help="Regenerar incluso si el .md esta al dia")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: no existe {root}", file=sys.stderr); return 1
    repo_root = root.parent
    t0 = time.time()
    counts = {"created": 0, "updated": 0, "skipped": 0, "failed": 0, "needs_ocr": 0}
    pdfs = list(iter_pdfs(root, args.topic))
    print(f"Encontrados {len(pdfs)} PDFs en {root}")

    for i, pdf in enumerate(pdfs, 1):
        rel = pdf.relative_to(repo_root).as_posix()
        md = md_path_for(pdf)
        if not args.force and not needs_regen(pdf, md):
            counts["skipped"] += 1
            if i % 50 == 0:
                print(f"  [{i}/{len(pdfs)}] avance...")
            continue
        if args.dry_run:
            print(f"  DRY  [{i}/{len(pdfs)}] {rel}")
            continue
        sha = read_sidecar_sha(pdf) or sha256_file(pdf)
        text, info = extract_pdf(pdf)
        if text is None and info["n_pages_extracted"] == 0:
            # igual escribimos el .md con placeholder
            counts["failed"] += 1
        was_new = not md.exists()
        write_md(pdf, text, info, sha, repo_root)
        if was_new:
            counts["created"] += 1
        else:
            counts["updated"] += 1
        if info["needs_ocr"]:
            counts["needs_ocr"] += 1
        if info["errors"]:
            err = info["errors"][0]
            print(f"  WARN [{i}/{len(pdfs)}] {pdf.name}: {err}")
        else:
            print(f"  OK   [{i}/{len(pdfs)}] {pdf.name}  "
                  f"({info['n_pages']}p, {info['chars_total']//1000}k chars"
                  f"{', OCR?' if info['needs_ocr'] else ''})")

    dt = (time.time() - t0) / 60
    print(f"\n=== RESUMEN ({dt:.1f} min) ===")
    print(f"  Creados:     {counts['created']}")
    print(f"  Actualizados:{counts['updated']}")
    print(f"  Skip cache:  {counts['skipped']}")
    print(f"  Fallaron:    {counts['failed']}")
    print(f"  Needs OCR:   {counts['needs_ocr']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
