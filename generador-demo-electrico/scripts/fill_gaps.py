#!/usr/bin/env python3
"""Llena los huecos del KB: SSCC (DS 113), Grid Forming, modelos dinamicos, NTCO anexos.

Mas agresivo que regulation_only.py:
- Depth-2 crawl desde varios seed URLs por gap
- Keyword matching tanto en links como en nombre de PDF
- Cada gap tiene un target folder y limites propios

Modo "completar lo que falta" — no toca PDFs ya bajados.

Uso (mismo venv que regulation_only):
    python fill_gaps.py
    python fill_gaps.py --gap sscc       # solo un gap especifico
    python fill_gaps.py --list           # listar gaps disponibles
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from bs4 import BeautifulSoup

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parent.parent.parent
SOURCES = REPO / "sources"
LOG_DIR = SCRIPT.parent.parent / "logs"
LOG_PATH = LOG_DIR / "fill_gaps.log"

UA = "GeneradorKBDemo/1.0 (research; contacto: demo@generador.local)"
MIN_DELAY = 3.0
JITTER = 1.0
TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_BASE = 3.0


@dataclass
class Gap:
    id: str                       # identificador corto (cli flag)
    target_folder: str            # ej. "regulation-coordinador-normativa-tecnica"
    title: str
    seed_urls: list[str]
    keyword_regex: str            # regex case-insensitive
    max_subpages: int = 15
    max_subsubpages: int = 5      # depth-2 budget por subpagina
    max_pdfs: int = 30
    note: str = ""


GAPS: list[Gap] = [
    Gap(
        id="sscc",
        target_folder="regulation-cne-reglamentos-mercado",
        title="SSCC: DS 113, reglamento de Servicios Complementarios + NTCO anexos",
        seed_urls=[
            "https://www.cne.cl/normativas/electrica/sector-electrico/",
            "https://www.cne.cl/normativas/electrica/normas-tecnicas/",
            "https://www.coordinador.cl/mercados/",
            "https://www.coordinador.cl/mercados/servicios-complementarios/",
            "https://energia.gob.cl/",
        ],
        keyword_regex=(r"(\bDS[\s\.-]*113\b|servicios[\s_-]?complement|"
                       r"\bSSCC\b|control.?de.?frecuencia|reserva.*giro|"
                       r"partida.*negro|inercia|primario.*frecuencia)"),
        max_pdfs=40,
        note="DS 113/2020 = reglamento maestro de SSCC + anexos NTCO especificos.",
    ),
    Gap(
        id="grid-forming",
        target_folder="regulation-coordinador-normativa-tecnica",
        title="Grid Forming + ciberseguridad CEN + estandares tecnicos",
        seed_urls=[
            "https://www.coordinador.cl/",
            "https://www.coordinador.cl/normativa-tecnica/",
            "https://www.coordinador.cl/documentos-tecnicos/",
            "https://www.coordinador.cl/sistema-electrico/",
            "https://www.coordinador.cl/sistema-electrico/documentos-tecnicos/",
            "https://www.coordinador.cl/operacion/documentos-tecnicos/",
        ],
        keyword_regex=(r"(grid.?form|cibersegur|protocolo.*ciber|"
                       r"estandar.*ciber|bess.*norm|guia.*bess|"
                       r"inercia.*sintetic|inversor.*form)"),
        max_pdfs=30,
        note="Guia Grid Forming + Estandar Ciberseguridad + Protocolo Notificacion Ciberincidentes.",
    ),
    Gap(
        id="modelos-dinamicos",
        target_folder="regulation-coordinador-operacion-sen",
        title="Procedimientos DO + modelos dinamicos + programa de operacion",
        seed_urls=[
            "https://www.coordinador.cl/operacion/",
            "https://www.coordinador.cl/operacion/documentos-tecnicos/",
            "https://www.coordinador.cl/operacion/procedimientos-do/",
            "https://www.coordinador.cl/operacion/programa-de-operacion/",
            "https://www.coordinador.cl/sistema-electrico/operacion-real/",
        ],
        keyword_regex=(r"(procedimiento.*DO|programa.*operaci|"
                       r"modelo.*dinamic|homologac.*modelo|powerfactory|"
                       r"despacho|reserva.*tecnica|deslast)"),
        max_pdfs=30,
        note="Algunos pueden estar detras de login (REUC/InfoTecnica) — esos se saltan.",
    ),
    Gap(
        id="pliego-tecnico",
        target_folder="regulation-coordinador-normativa-tecnica",
        title="Pliego Tecnico Normalizado (PTN) del CEN",
        seed_urls=[
            "https://www.coordinador.cl/normativa-tecnica/",
            "https://www.coordinador.cl/sistema-electrico/",
            "https://www.coordinador.cl/sistema-electrico/conexion-al-sen/",
            "https://www.coordinador.cl/conexion/",
        ],
        keyword_regex=r"(pliego.*tecnico|PTN|PRTD|requisito.*tecnico|conexion.*SEN)",
        max_pdfs=30,
        note="Pliego Tecnico Normalizado = especs tecnicas oficiales para conectarse al SEN.",
    ),
]


# Per-domain rate limiting state
_state: dict[str, dict] = {}


def _domain(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def _wait(url: str) -> None:
    dom = _domain(url)
    st = _state.setdefault(dom, {"last": 0.0, "delay": MIN_DELAY})
    elapsed = time.monotonic() - st["last"]
    delay = st["delay"] + random.uniform(-JITTER, JITTER)
    if st["last"] > 0 and elapsed < delay:
        time.sleep(max(0.0, delay - elapsed))
    st["last"] = time.monotonic()


def _throttle_up(url: str) -> None:
    st = _state.setdefault(_domain(url), {"last": 0.0, "delay": MIN_DELAY})
    st["delay"] = min(st["delay"] * 2, 60.0)


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch(client: httpx.Client, url: str) -> Optional[httpx.Response]:
    delay = RETRY_BASE
    for attempt in range(1, MAX_RETRIES + 1):
        _wait(url)
        try:
            r = client.get(url)
        except httpx.HTTPError as e:
            log(f"  ERR  attempt {attempt}/{MAX_RETRIES} {url}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(delay); delay *= 3
                continue
            return None
        if r.status_code in (429, 503):
            log(f"  WARN {r.status_code} (throttle) {url}")
            _throttle_up(url)
            time.sleep(delay); delay *= 3
            continue
        if r.status_code in (401, 403):
            log(f"  AUTH {r.status_code} {url} (skip; sin bypass)")
            return None
        if r.status_code == 404:
            log(f"  404  {url}")
            return None
        if r.status_code >= 400:
            log(f"  WARN {r.status_code} {url}")
            if attempt < MAX_RETRIES:
                time.sleep(delay); delay *= 3
                continue
            return None
        return r
    return None


def extract_pdfs(html: str, base_url: str, kw_re: re.Pattern) -> list[str]:
    """PDFs cuyo href O texto del link matchea el keyword regex."""
    soup = BeautifulSoup(html, "lxml")
    out: list[str] = []
    for a in soup.select("a[href]"):
        href = a["href"]
        if not href.lower().split("?")[0].endswith(".pdf"):
            continue
        full = urllib.parse.urljoin(base_url, href)
        hay = (a.get_text() or "") + " " + href
        if kw_re.search(hay):
            out.append(full)
    return sorted(set(out))


def discover_subpages(html: str, base_url: str, kw_re: re.Pattern,
                      max_results: int = 20) -> list[str]:
    """Subpaginas same-domain cuyo link matchea el keyword regex."""
    soup = BeautifulSoup(html, "lxml")
    base_dom = _domain(base_url)
    out: list[str] = []
    for a in soup.select("a[href]"):
        href = a["href"]
        text = (a.get_text() or "") + " " + href
        if not kw_re.search(text):
            continue
        full = urllib.parse.urljoin(base_url, href)
        if _domain(full) != base_dom:
            continue
        if full.lower().split("?")[0].endswith(".pdf"):
            continue
        if full.startswith("mailto:"):
            continue
        # Quita anchors
        full = full.split("#")[0]
        if full == base_url:
            continue
        out.append(full)
    return sorted(set(out))[:max_results]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_filename(url: str) -> str:
    name = Path(urllib.parse.urlparse(url).path).name
    name = urllib.parse.unquote(name)
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", name)
    if not name or name == ".pdf":
        name = "doc.pdf"
    return name


def download_pdf(client: httpx.Client, pdf_url: str, dest_dir: Path,
                 gap: Gap, found_on: str) -> Optional[Path]:
    target = dest_dir / safe_filename(pdf_url)
    meta_path = target.with_suffix(target.suffix + ".meta.json")
    if target.exists() and meta_path.exists():
        log(f"  CACHE {target.name}")
        return target
    r = fetch(client, pdf_url)
    if r is None:
        return None
    if not r.content or r.content[:4] != b"%PDF":
        log(f"  SKIP not-a-pdf {pdf_url}")
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(r.content)
    meta = {
        "url": pdf_url,
        "fetched_url": str(r.url),
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "sha256": sha256(r.content),
        "size_bytes": len(r.content),
        "content_type": r.headers.get("content-type"),
        "scraped_from": {
            "found_on": found_on,
            "gap": gap.id,
            "gap_title": gap.title,
        },
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"  OK   {target.name} ({len(r.content)//1024} KB)  via {urllib.parse.urlparse(found_on).path}")
    return target


def process_gap(client: httpx.Client, gap: Gap) -> int:
    log(f"\n{'='*78}\n## {gap.title}\n{'='*78}")
    log(f"   target: sources/{gap.target_folder}")
    log(f"   keyword: {gap.keyword_regex}")
    if gap.note:
        log(f"   nota: {gap.note}")
    kw_re = re.compile(gap.keyword_regex, re.IGNORECASE)
    dest = SOURCES / gap.target_folder
    pdf_urls: dict[str, str] = {}  # url -> found_on
    visited: set[str] = set()

    def visit(page_url: str, depth: int):
        if page_url in visited:
            return
        visited.add(page_url)
        r = fetch(client, page_url)
        if r is None:
            return
        # PDFs en esta pagina
        for pdf in extract_pdfs(r.text, page_url, kw_re):
            if pdf not in pdf_urls:
                pdf_urls[pdf] = page_url
        # Subpaginas
        if depth > 0:
            limit = gap.max_subpages if depth == gap_depth else gap.max_subsubpages
            subs = discover_subpages(r.text, page_url, kw_re, max_results=limit)
            for sp in subs:
                if len(pdf_urls) >= gap.max_pdfs:
                    return
                visit(sp, depth - 1)

    gap_depth = 2  # depth-2 desde cada seed
    for seed in gap.seed_urls:
        if len(pdf_urls) >= gap.max_pdfs:
            log(f"   ya alcanzamos max_pdfs={gap.max_pdfs}, paro")
            break
        log(f"   seed: {seed}")
        visit(seed, gap_depth)

    log(f"   PDFs candidatos: {len(pdf_urls)}")
    n_ok = 0
    for url, found_on in sorted(pdf_urls.items())[: gap.max_pdfs]:
        if download_pdf(client, url, dest, gap, found_on) is not None:
            n_ok += 1
    log(f"   -> {n_ok} archivos descargados a sources/{gap.target_folder}")
    return n_ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", action="append", default=None,
                    help="ID del gap a procesar (puede usarse varias veces). Default: todos.")
    ap.add_argument("--list", action="store_true", help="Listar gaps disponibles y salir.")
    args = ap.parse_args()

    if args.list:
        for g in GAPS:
            print(f"  {g.id:18s}  -> sources/{g.target_folder}")
            print(f"  {'':18s}     {g.title}")
            print(f"  {'':18s}     {len(g.seed_urls)} seeds, max {g.max_pdfs} PDFs")
            print()
        return 0

    gaps_to_run = GAPS
    if args.gap:
        wanted = set(args.gap)
        gaps_to_run = [g for g in GAPS if g.id in wanted]
        missing = wanted - {g.id for g in gaps_to_run}
        if missing:
            print(f"ERROR: gaps no encontrados: {missing}", file=sys.stderr)
            print("Disponibles: " + ", ".join(g.id for g in GAPS), file=sys.stderr)
            return 1

    SOURCES.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text("", encoding="utf-8")

    headers = {
        "User-Agent": UA,
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
    }
    t0 = time.time()
    counts: dict[str, int] = {}
    with httpx.Client(headers=headers, timeout=TIMEOUT, follow_redirects=True) as client:
        for gap in gaps_to_run:
            try:
                n = process_gap(client, gap)
            except Exception as e:
                log(f"  FATAL {gap.id}: {e}")
                import traceback; log(traceback.format_exc())
                n = 0
            counts[gap.id] = n

    dt = (time.time() - t0) / 60
    log(f"\n=== RESUMEN ({dt:.1f} min) ===")
    for gid, n in counts.items():
        log(f"  {n:>3}  {gid}")
    log(f"  total: {sum(counts.values())}")
    log(f"  log:   {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
