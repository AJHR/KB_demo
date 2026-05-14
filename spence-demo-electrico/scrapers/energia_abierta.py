"""Scraper del portal Energia Abierta (datos abiertos del sector energetico CL)."""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper


class EnergiaAbiertaScraper:
    def __init__(self, base: BaseScraper, page_cfgs: list[dict]):
        self.base = base
        self.cfgs = {p["id"]: p for p in page_cfgs}

    def _list_datasets(self, page_url: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        urls = []
        for a in soup.select("a[href]"):
            href = a["href"].lower()
            if href.endswith((".csv", ".xls", ".xlsx", ".zip", ".json")):
                urls.append(urllib.parse.urljoin(page_url, a["href"]))
        return sorted(set(urls))

    def _list_estadistica_pages(self, page_url: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        out = []
        for a in soup.select(".dataset-card a, .estadistica-item a, article a, .post a"):
            href = a.get("href")
            if href and "energiaabierta" in urllib.parse.urljoin(page_url, href):
                out.append(urllib.parse.urljoin(page_url, href))
        return sorted(set(out))[:50]

    def run_estadisticas_electricidad(self) -> list[Path]:
        cfg = self.cfgs["estadisticas_electricidad_cen"]
        dest = S.DATA_RAW / cfg["category"]
        out: list[Path] = []
        try:
            datasets = self._list_estadistica_pages(cfg["url"])
        except Exception as e:
            logger.error(f"estadisticas_electricidad list: {e}")
            return []
        for ds_page in datasets:
            try:
                files = self._list_datasets(ds_page)
                for f in files:
                    try:
                        out.append(self.base.download(f, dest))
                    except Exception as e:
                        logger.warning(f"skip {f}: {e}")
            except Exception as e:
                logger.warning(f"skip dataset {ds_page}: {e}")
        return out

    def run_listado_empresas(self) -> list[Path]:
        cfg = self.cfgs["listado_empresas"]
        dest = S.DATA_RAW / cfg["category"]
        try:
            res = self.base.get(cfg["url"])
        except Exception as e:
            logger.error(f"listado_empresas: {e}")
            return []
        # guarda el HTML como referencia
        target = dest / "listado_empresas.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(res.content)
        out = [target]
        # ademas, buscar CSV/XLS si los hay
        try:
            for u in self._list_datasets(cfg["url"]):
                try:
                    out.append(self.base.download(u, dest))
                except Exception as e:
                    logger.warning(f"skip {u}: {e}")
        except Exception as e:
            logger.warning(f"listado_empresas datasets: {e}")
        return out
