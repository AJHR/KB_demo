#!/usr/bin/env python3
"""Ingesta manual de PDFs al KB: copia + genera .meta.json + actualiza RESUMEN.md.

Casos de uso:
1. PDF unico:
     python ingest_manual.py /path/al/DS_113_2020.pdf \\
       --topic cne-reglamentos-mercado \\
       --url https://www.diariooficial.interior.gob.cl/...

2. Carpeta inbox/ (drag and drop, interactivo):
     mkdir -p inbox && cp ~/Downloads/*.pdf inbox/
     python ingest_manual.py --inbox inbox/

3. Reparar orfanatos en sources/ (PDFs sin .meta.json):
     python ingest_manual.py --fix-orphans

4. Listar topics:
     python ingest_manual.py --list-topics

Sin deps externas (solo stdlib).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parent.parent.parent
SOURCES = REPO / "sources"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def is_pdf(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(4) == b"%PDF"
    except Exception:
        return False


def list_topics() -> list[str]:
    if not SOURCES.exists():
        return []
    return sorted(d.name for d in SOURCES.iterdir()
                  if d.is_dir() and d.name.startswith("regulation-"))


def normalize_topic(topic: str) -> str:
    """Acepta 'cne-reglamentos-mercado' o 'regulation-cne-reglamentos-mercado'."""
    return topic if topic.startswith("regulation-") else f"regulation-{topic}"


def safe_filename(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", name)
    if not name.lower().endswith(".pdf"):
        name = name + ".pdf"
    return name


def find_existing_by_hash(target_dir: Path, sha: str) -> Optional[Path]:
    for m in target_dir.glob("*.meta.json"):
        try:
            d = json.loads(m.read_text("utf-8"))
            if d.get("sha256") == sha:
                # m es xxx.pdf.meta.json -> queremos xxx.pdf
                return m.with_name(m.name[: -len(".meta.json")])
        except Exception:
            continue
    return None


def write_meta(pdf_target: Path, url: str, source_path: Path, sha: str,
               title: str = "", note: str = "", method: str = "manual") -> Path:
    meta_path = pdf_target.with_suffix(pdf_target.suffix + ".meta.json")
    meta = {
        "url": url,
        "fetched_url": url,
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "sha256": sha,
        "size_bytes": pdf_target.stat().st_size,
        "content_type": "application/pdf",
        "scraped_from": {
            "method": method,
            "original_path": str(source_path),
            "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "title": title,
            "note": note,
        },
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta_path


def regenerate_resumen(topic_dir: Path) -> None:
    """Regenera RESUMEN.md con listado de PDFs reales en la carpeta."""
    pdfs = sorted(topic_dir.glob("*.pdf"))
    if not pdfs:
        return
    name = topic_dir.name
    lines = [
        f"# {name}",
        "",
        "## Que contiene",
        "Material regulatorio publico del sector electrico chileno.",
        "INMUTABLE: no editar PDFs aqui. Ediciones / anotaciones van a `work/` o `wiki/`.",
        "",
        "## Archivos clave",
        "| Archivo | Tamano | Origen |",
        "|---------|--------|--------|",
    ]
    for pdf in pdfs:
        size_kb = pdf.stat().st_size // 1024
        meta_p = pdf.with_suffix(pdf.suffix + ".meta.json")
        src = "-"
        if meta_p.exists():
            try:
                d = json.loads(meta_p.read_text("utf-8"))
                src = d.get("url") or d.get("scraped_from", {}).get("note") or "-"
            except Exception:
                pass
        # truncar URL larga para legibilidad
        if isinstance(src, str) and len(src) > 80:
            src = src[:77] + "..."
        lines.append(f"| `{pdf.name}` | {size_kb} KB | {src} |")
    lines += [
        "",
        "## Advertencias",
        "- Archivos descargados via scraping o ingesta manual.",
        "- Algunos PDFs pueden requerir OCR si son escaneos viejos.",
        "- Para procesamiento del contenido ver `wiki/` de la raiz.",
        "",
    ]
    (topic_dir / "RESUMEN.md").write_text("\n".join(lines), encoding="utf-8")


def ingest_one(source: Path, topic: str, url: str = "", title: str = "",
               note: str = "", rename: Optional[str] = None,
               dry_run: bool = False) -> Optional[Path]:
    if not source.exists():
        print(f"  ERROR: no existe {source}", file=sys.stderr)
        return None
    if not is_pdf(source):
        print(f"  ERROR: {source.name} no parece PDF (no empieza con %PDF)", file=sys.stderr)
        return None

    topic_full = normalize_topic(topic)
    target_dir = SOURCES / topic_full
    if not target_dir.exists():
        print(f"  WARN: topic '{topic_full}' no existe todavia. La creo.", file=sys.stderr)

    sha = sha256_file(source)
    existing = find_existing_by_hash(target_dir, sha) if target_dir.exists() else None
    if existing:
        print(f"  SKIP: ya existe con mismo hash -> {existing.relative_to(REPO)}")
        return existing

    filename = safe_filename(rename or source.name)
    target = target_dir / filename
    if target.exists() and not existing:
        # mismo nombre pero hash distinto -> sufijo
        stem = target.stem
        n = 2
        while True:
            cand = target_dir / f"{stem}_v{n}.pdf"
            if not cand.exists():
                target = cand
                break
            n += 1

    if dry_run:
        print(f"  DRY: copiaria {source.name} -> {target.relative_to(REPO)}")
        print(f"  DRY: meta sha256={sha[:16]}... url={url or '(empty)'}")
        return target

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    write_meta(target, url=url, source_path=source, sha=sha, title=title, note=note)
    regenerate_resumen(target_dir)
    print(f"  OK: {target.relative_to(REPO)}  ({target.stat().st_size//1024} KB)  sha256={sha[:16]}...")
    return target


def prompt(s: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        v = input(f"{s}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(1)
    return v or default


def cmd_inbox(inbox_dir: Path, dry_run: bool) -> int:
    topics = list_topics()
    if not topics:
        print(f"ERROR: no hay topics en {SOURCES}. Corre regulation_only.py primero o crea una carpeta manualmente.", file=sys.stderr)
        return 1
    pdfs = sorted(inbox_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No hay PDFs en {inbox_dir}/")
        return 0
    print(f"\n{len(pdfs)} PDF(s) en {inbox_dir}/\nTopics disponibles:")
    for i, t in enumerate(topics, 1):
        print(f"  {i:2d}. {t}")
    print()

    ingested = []
    for pdf in pdfs:
        print(f"\n--- {pdf.name} ({pdf.stat().st_size//1024} KB) ---")
        # topic
        choice = prompt("Topic (numero o nombre)", default="skip")
        if choice == "skip":
            print("  (saltado)")
            continue
        if choice.isdigit():
            idx = int(choice) - 1
            if not (0 <= idx < len(topics)):
                print("  numero invalido, salto"); continue
            topic = topics[idx]
        else:
            topic = choice
        url = prompt("URL original (opcional, Enter para saltar)")
        title = prompt("Titulo / descripcion corta (opcional)")
        note = prompt("Nota interna (opcional)")
        rename = prompt("Renombrar archivo? (Enter = mantener nombre original)")
        rename = rename or None
        result = ingest_one(pdf, topic, url=url, title=title, note=note,
                            rename=rename, dry_run=dry_run)
        if result and not dry_run:
            try:
                pdf.unlink()
                print(f"  (removido de {inbox_dir.name}/)")
            except Exception:
                pass
            ingested.append(result)
    print(f"\n=== {len(ingested)} archivo(s) ingestado(s) ===")
    return 0


def cmd_fix_orphans(dry_run: bool) -> int:
    """PDFs sin .meta.json: pide URL y genera la meta."""
    orphans = []
    for pdf in SOURCES.rglob("*.pdf"):
        meta = pdf.with_suffix(pdf.suffix + ".meta.json")
        if not meta.exists():
            orphans.append(pdf)
    if not orphans:
        print("No hay orfanatos (todos los PDFs tienen .meta.json).")
        return 0
    print(f"\n{len(orphans)} PDF(s) sin .meta.json:\n")
    for pdf in orphans:
        print(f"--- {pdf.relative_to(REPO)} ---")
        url = prompt("URL original (Enter = vacio)")
        note = prompt("Nota interna (opcional)")
        if dry_run:
            print(f"  DRY: generaria meta para {pdf.name}")
            continue
        sha = sha256_file(pdf)
        write_meta(pdf, url=url, source_path=pdf, sha=sha, note=note, method="manual-fix")
        regenerate_resumen(pdf.parent)
        print(f"  OK meta generada")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingesta manual de PDFs al KB.")
    ap.add_argument("file", nargs="?", help="Path al PDF a ingerir")
    ap.add_argument("--topic", help="Topic destino (con o sin prefijo 'regulation-')")
    ap.add_argument("--url", default="", help="URL original")
    ap.add_argument("--title", default="", help="Titulo opcional")
    ap.add_argument("--note", default="", help="Nota interna opcional")
    ap.add_argument("--rename", default=None, help="Nombre final del archivo (opcional)")
    ap.add_argument("--inbox", help="Carpeta con PDFs para ingesta interactiva batch")
    ap.add_argument("--fix-orphans", action="store_true",
                    help="Buscar PDFs sin .meta.json y generarles uno")
    ap.add_argument("--list-topics", action="store_true", help="Listar topics y salir")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.list_topics:
        for t in list_topics():
            print(t)
        return 0
    if args.fix_orphans:
        return cmd_fix_orphans(args.dry_run)
    if args.inbox:
        return cmd_inbox(Path(args.inbox), args.dry_run)
    if not args.file:
        ap.print_help()
        return 1
    if not args.topic:
        topics = list_topics()
        print("Topics disponibles:")
        for i, t in enumerate(topics, 1):
            print(f"  {i:2d}. {t}")
        choice = prompt("Topic (numero o nombre)")
        if choice.isdigit():
            idx = int(choice) - 1
            if not (0 <= idx < len(topics)):
                print("Invalido", file=sys.stderr); return 1
            args.topic = topics[idx]
        else:
            args.topic = choice
    if not args.url:
        args.url = prompt("URL original (opcional, Enter para saltar)")

    result = ingest_one(Path(args.file), args.topic, url=args.url, title=args.title,
                        note=args.note, rename=args.rename, dry_run=args.dry_run)
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
