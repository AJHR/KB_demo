#!/usr/bin/env python3
"""Scraping enfocado: regulacion electrica chilena -> KB sources/.

Deps minimas: httpx, beautifulsoup4, lxml.
Sin Playwright. Sin login. Sin embeddings. Solo PDFs publicos.

Output:
  <repo>/sources/regulation-<topic>/<archivo>.pdf
  <repo>/sources/regulation-<topic>/<archivo>.pdf.meta.json
  <repo>/spence-demo-electrico/logs/regulation.log
"""
from __future__ import annotations

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
KB_ROOT = SCRIPT.parent.parent.parent   # spence-demo-electrico/scripts/ -> KB root
SOURCES_DIR = KB_ROOT / "sources"
LOG_DIR = SCRIPT.parent.parent / "logs"
LOG_PATH = LOG_DIR / "regulation.log"

UA = "SpenceKBDemo/1.0 (research; contacto: demo@spence.local)"
MIN_DELAY = 3.0
JITTER = 1.0
TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_BASE = 3.0

DISCOVERY_KEYWORDS = re.compile(
    r"normativ|regul|decret|reglament|tarific|norma|cibersegur|grid.?form|"
    r"sismic|ntsy|art.?163|reforma|precios.?de.?nudo|obras|"
    r"mercad|servic.?complement|transferenc|pmgd|pliego|procedimient|"
    r"operacion|programa|panel.?expert|coordin|expansion|despacho",
    re.IGNORECASE,
)


@dataclass
class SourcePage:
    topic: str           # subcarpeta sources/regulation-<topic>/ (kebab-case)
    title: str
    url: str
    filter_regex: str = ""
    limit: int = 50
    discover_depth: int = 1   # 0 = solo PDFs de esta pagina


PAGES: list[SourcePage] = [
    SourcePage(
        topic="cne-sector-electrico",
        title="CNE - Normativa sector electrico (LGE, decretos, reglamentos)",
        url="https://www.cne.cl/normativas/electrica/sector-electrico/",
        limit=80,
    ),
    SourcePage(
        topic="cne-precios-nudo",
        title="CNE - Precios de nudo (informes y decretos)",
        url="https://www.cne.cl/tarificacion/electrica/precios-nudo/",
        limit=40,
    ),
    SourcePage(
        topic="cne-obras-nuevas-urgentes",
        title="CNE - Decretos obras nuevas y urgentes",
        url="https://www.cne.cl/tarificacion/electrica/obras-nuevas-y-urgentes/",
        filter_regex=r"(2023|2024|2025|2026)",
        limit=50,
    ),
    SourcePage(
        topic="cne-normas-tecnicas",
        title="CNE - Normas tecnicas (NTSyCS, anexo sismico)",
        url="https://www.cne.cl/normativas/electrica/normas-tecnicas/",
        limit=40,
    ),
    SourcePage(
        topic="coordinador-normativa-tecnica",
        title="Coordinador - Normativa tecnica (ciberseguridad, grid forming, BESS)",
        url="https://www.coordinador.cl/normativa/",
        limit=60,
    ),
    SourcePage(
        topic="coordinador-reportes-estadisticas",
        title="Coordinador - Reportes anuales y desempeno SEN",
        url="https://www.coordinador.cl/reportes-y-estadisticas/",
        limit=40,
    ),
    SourcePage(
        topic="minenergia-marco-regulatorio",
        title="Ministerio de Energia - Marco regulatorio y reforma 2026",
        url="https://energia.gob.cl/",
        limit=30,
    ),
    # --- mercado mayorista: como funciona el mercado para generadores ---
    SourcePage(
        topic="cne-reglamentos-mercado",
        title="CNE - Reglamentos de mercado (coordinacion, servicios complementarios, transferencias economicas)",
        url="https://www.cne.cl/normativas/electrica/sector-electrico/",
        filter_regex=r"reglament|servic.?complement|transferenc|coordin|panel.?expert|pmgd",
        limit=40,
    ),
    SourcePage(
        topic="coordinador-mercados-servicios",
        title="Coordinador - Mercado mayorista (servicios complementarios, transferencias)",
        url="https://www.coordinador.cl/mercados/",
        limit=60,
    ),
    SourcePage(
        topic="coordinador-operacion-sen",
        title="Coordinador - Operacion del SEN (procedimientos DO, programacion, despacho)",
        url="https://www.coordinador.cl/operacion/",
        limit=60,
    ),
    SourcePage(
        topic="coordinador-desarrollo-transmision",
        title="Coordinador - Desarrollo y expansion de transmision",
        url="https://www.coordinador.cl/desarrollo/",
        limit=40,
    ),
]


# Per-domain rate limiting + backoff state
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


def extract_pdfs(html: str, base_url: str, filter_re: Optional[re.Pattern]) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.select("a[href]"):
        href = a["href"]
        if not href.lower().split("?")[0].endswith(".pdf"):
            continue
        full = urllib.parse.urljoin(base_url, href)
        hay = (a.get_text() or "") + " " + href
        if filter_re and not filter_re.search(hay):
            continue
        out.append(full)
    return sorted(set(out))


def discover_subpages(html: str, base_url: str, max_subpages: int = 12) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    base_domain = _domain(base_url)
    out = []
    for a in soup.select("a[href]"):
        href = a["href"]
        text = (a.get_text() or "") + " " + href
        if not DISCOVERY_KEYWORDS.search(text):
            continue
        full = urllib.parse.urljoin(base_url, href)
        if _domain(full) != base_domain:
            continue
        if full.lower().endswith(".pdf"):
            continue
        # evitar mailto, anclas, params raros
        if full.startswith("mailto:") or "#" in full.split("/")[-1]:
            continue
        out.append(full.split("#")[0])
    return sorted(set(out))[:max_subpages]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_filename(url: str) -> str:
    name = Path(urllib.parse.urlparse(url).path).name
    name = urllib.parse.unquote(name)
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", name)
    if not name or name == ".pdf":
        name = "doc.pdf"
    return name


def download_pdf(client: httpx.Client, pdf_url: str, dest_dir: Path, page_meta: dict) -> Optional[Path]:
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
        "scraped_from": page_meta,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"  OK   {target.name} ({len(r.content)//1024} KB)")
    return target


def process_page(client: httpx.Client, page: SourcePage) -> int:
    log(f"\n=== {page.title} ===\n    {page.url}")
    dest = SOURCES_DIR / f"regulation-{page.topic}"
    page_meta = {"page_url": page.url, "page_title": page.title}
    filter_re = re.compile(page.filter_regex, re.IGNORECASE) if page.filter_regex else None
    r = fetch(client, page.url)
    if r is None:
        log("    pagina raiz no accesible; skip")
        return 0
    pdf_urls = set(extract_pdfs(r.text, page.url, filter_re))
    log(f"    {len(pdf_urls)} PDFs en la pagina raiz")
    if page.discover_depth >= 1:
        subpages = discover_subpages(r.text, page.url)
        log(f"    {len(subpages)} subpaginas candidatas para crawl depth-1")
        for sp in subpages:
            sr = fetch(client, sp)
            if sr is None:
                continue
            extra = extract_pdfs(sr.text, sp, filter_re)
            pdf_urls.update(extra)
            log(f"    +{len(extra)} PDFs desde {sp}")
    pdf_urls = sorted(pdf_urls)[: page.limit]
    log(f"    descargando {len(pdf_urls)} (limit {page.limit})")
    n = 0
    for u in pdf_urls:
        if download_pdf(client, u, dest, page_meta) is not None:
            n += 1
    log(f"    -> {n} archivos en sources/regulation-{page.topic}/")
    return n


def write_resumen(topic: str, page: SourcePage, files: list[Path]) -> None:
    dest = SOURCES_DIR / f"regulation-{topic}"
    if not dest.exists() or not files:
        return
    lines = [
        f"# regulation-{topic}",
        "",
        "## Que contiene",
        f"{page.title}. Material descargado automaticamente desde `{page.url}`. INMUTABLE (no editar).",
        "",
        "## Archivos clave",
        "| Archivo | Tamano | Origen |",
        "|---------|--------|--------|",
    ]
    for f in sorted(files):
        size_kb = f.stat().st_size // 1024
        meta_p = f.with_suffix(f.suffix + ".meta.json")
        src = "-"
        if meta_p.exists():
            try:
                src = json.loads(meta_p.read_text("utf-8")).get("url", "-")
            except Exception:
                pass
        lines.append(f"| `{f.name}` | {size_kb} KB | {src} |")
    lines += [
        "",
        "## Advertencias",
        "- Archivos descargados via scraping respetuoso (rate limit 3s, User-Agent identificado).",
        "- Algunos PDFs pueden requerir OCR si son escaneos viejos.",
        "- Para procesamiento del contenido ver `wiki/` de la raiz.",
        "",
    ]
    (dest / "RESUMEN.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    SOURCES_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text("", encoding="utf-8")
    headers = {
        "User-Agent": UA,
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
    }
    counts: dict[str, int] = {}
    log(f"KB_ROOT = {KB_ROOT}")
    log(f"SOURCES = {SOURCES_DIR}")
    with httpx.Client(headers=headers, timeout=TIMEOUT, follow_redirects=True) as client:
        for page in PAGES:
            try:
                n = process_page(client, page)
            except Exception as e:
                log(f"  FATAL {page.topic}: {e}")
                n = 0
            counts[page.topic] = n
            # generar RESUMEN.md por topic
            dest = SOURCES_DIR / f"regulation-{page.topic}"
            files = [p for p in dest.glob("*.pdf")] if dest.exists() else []
            write_resumen(page.topic, page, files)
    log("\n=== RESUMEN ===")
    total = 0
    for topic, n in counts.items():
        log(f"  {n:>3}  regulation-{topic}")
        total += n
    log(f"\nTOTAL: {total} archivos en {SOURCES_DIR}")
    log(f"LOG  : {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
