"""Scraper de la Comision Nacional de Energia (CNE)."""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper


class CNEScraper:
    def __init__(self, base: BaseScraper, page_cfgs: list[dict]):
        self.base = base
        self.cfgs = {p["id"]: p for p in page_cfgs}

    def _list_pdfs(self, page_url: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        out = []
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                out.append(urllib.parse.urljoin(page_url, href))
        return sorted(set(out))

    def _list_matching(self, page_url: str, match: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        pat = re.compile(re.escape(match), re.IGNORECASE)
        out = []
        for a in soup.select("a[href]"):
            text = (a.get_text() or "") + " " + a["href"]
            if pat.search(text) and a["href"].lower().endswith(".pdf"):
                out.append(urllib.parse.urljoin(page_url, a["href"]))
        return sorted(set(out))

    def run_normativa_electrica(self) -> list[Path]:
        cfg = self.cfgs["normativa_electrica"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            urls = self._list_pdfs(cfg["url"])
        except Exception as e:
            logger.error(f"normativa_electrica list: {e}")
            return []
        out = []
        for u in urls[:120]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out

    def run_ntsycs(self) -> list[Path]:
        cfg = self.cfgs["ntsycs"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            urls = self._list_matching(cfg["url"], "NTSyCS")
        except Exception as e:
            logger.error(f"ntsycs: {e}")
            return []
        out = []
        for u in urls[:20]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out

    def run_anexo_sismico(self) -> list[Path]:
        cfg = self.cfgs["anexo_tecnico_sismico"]
        dest = S.DATA_RAW / cfg["category"]
        urls = []
        try:
            for q in ("Resolucion REx", "Anexo Sismico", "sismico", "41-2025"):
                try:
                    urls.extend(self._list_matching(cfg["url"], q))
                except Exception as e:
                    logger.warning(f"anexo_sismico q='{q}': {e}")
        except Exception as e:
            logger.error(f"anexo_sismico: {e}")
            return []
        urls = sorted(set(urls))
        out = []
        for u in urls[:20]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out

    def run_obras_nuevas_urgentes(self) -> list[Path]:
        cfg = self.cfgs["obras_nuevas_urgentes"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            urls = self._list_pdfs(cfg["url"])
        except Exception as e:
            logger.error(f"obras_nuevas_urgentes: {e}")
            return []
        anos = cfg.get("params", {}).get("anos", [2025, 2026])
        pat = re.compile("|".join(str(a) for a in anos))
        urls = [u for u in urls if pat.search(u)]
        out = []
        for u in urls[:60]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out

    def run_precios_nudo(self) -> list[Path]:
        cfg = self.cfgs["precios_nudo"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            urls = self._list_pdfs(cfg["url"])
        except Exception as e:
            logger.error(f"precios_nudo: {e}")
            return []
        out = []
        for u in urls[:30]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out

    def run_informes_tecnicos_art163(self) -> list[Path]:
        cfg = self.cfgs["informes_tecnicos_art163"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            urls = self._list_matching(cfg["url"], "Art. 163")
            urls.extend(self._list_matching(cfg["url"], "163"))
        except Exception as e:
            logger.error(f"informes_tecnicos_art163: {e}")
            return []
        urls = sorted(set(urls))
        out = []
        for u in urls[:20]:
            try:
                out.append(self.base.download(u, dest))
            except Exception as e:
                logger.warning(f"skip {u}: {e}")
        return out
