"""Scraper de regulacion: descarga PDFs del Ministerio de Energia y otros."""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper


class RegulationScraper:
    def __init__(self, base: BaseScraper, page_cfgs: list[dict]):
        self.base = base
        self.cfgs = {p["id"]: p for p in page_cfgs}

    def _list_pdfs(self, page_url: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        urls = []
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                urls.append(urllib.parse.urljoin(page_url, href))
        return sorted(set(urls))

    def _list_matching(self, page_url: str, match: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        pat = re.compile(re.escape(match), re.IGNORECASE)
        urls = []
        for a in soup.select("a[href]"):
            text = (a.get_text() or "") + " " + a["href"]
            if pat.search(text):
                href = a["href"]
                if href.lower().endswith(".pdf") or "noticia" in href.lower():
                    urls.append(urllib.parse.urljoin(page_url, href))
        return sorted(set(urls))

    def run_reforma_2026(self) -> list[Path]:
        out: list[Path] = []
        # comunicados de prensa
        if "reforma_2026_comunicados" in self.cfgs:
            cfg = self.cfgs["reforma_2026_comunicados"]
            dest = S.DATA_RAW / cfg["category"]
            try:
                urls = self._list_matching(cfg["url"], "Reforma 2026")
                for u in urls[:20]:
                    try:
                        if u.lower().endswith(".pdf"):
                            out.append(self.base.download(u, dest))
                        else:
                            # bajar HTML de la noticia
                            res = self.base.get(u)
                            name = urllib.parse.urlparse(u).path.strip("/").replace("/", "_") + ".html"
                            target = dest / name
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(res.content)
                            out.append(target)
                    except Exception as e:
                        logger.warning(f"skip {u}: {e}")
            except Exception as e:
                logger.error(f"reforma_2026_comunicados: {e}")
        # documento completo
        if "reforma_2026_documento" in self.cfgs:
            cfg = self.cfgs["reforma_2026_documento"]
            dest = S.DATA_RAW / cfg["category"]
            try:
                urls = self._list_pdfs(cfg["url"])
                for u in urls[:10]:
                    try:
                        out.append(self.base.download(u, dest))
                    except Exception as e:
                        logger.warning(f"skip {u}: {e}")
            except Exception as e:
                logger.error(f"reforma_2026_documento: {e}")
        return out
