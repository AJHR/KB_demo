"""Scraper del Coordinador Electrico Nacional."""
from __future__ import annotations

import re
import urllib.parse
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from loguru import logger

from config import settings as S
from scrapers.base_scraper import (
    AuthRequiredError, BaseScraper, CaptchaDetected, RobotsDisallowed,
)


class CENScraper:
    def __init__(self, base: BaseScraper, page_cfgs: list[dict]):
        self.base = base
        self.cfgs = {p["id"]: p for p in page_cfgs}

    # ---- listado generico --------------------------------------------------
    def list_pdfs(self, page_url: str) -> list[str]:
        """Lista PDFs linkeados desde una pagina estatica."""
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        urls = []
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                urls.append(urllib.parse.urljoin(page_url, href))
        return sorted(set(urls))

    def list_links_matching(self, page_url: str, pattern: str) -> list[str]:
        res = self.base.get(page_url)
        soup = BeautifulSoup(res.text(), "lxml")
        pat = re.compile(pattern, re.IGNORECASE)
        urls = []
        for a in soup.select("a[href]"):
            text = (a.get_text() or "") + " " + a["href"]
            if pat.search(text):
                urls.append(urllib.parse.urljoin(page_url, a["href"]))
        return sorted(set(urls))

    # ---- secciones ---------------------------------------------------------
    def run_reportes_y_estadisticas(self) -> list[Path]:
        cfg = self.cfgs["reportes_y_estadisticas"]
        out_dir = S.DATA_RAW / cfg["category"]
        try:
            pdfs = self.list_pdfs(cfg["url"])
        except (AuthRequiredError, RobotsDisallowed, Exception) as e:
            logger.error(f"reportes_y_estadisticas list error: {e}")
            return []
        downloaded = []
        for url in pdfs[:60]:  # limite defensivo
            try:
                p = self.base.download(url, out_dir)
                downloaded.append(p)
            except Exception as e:
                logger.warning(f"skip {url}: {e}")
        return downloaded

    def run_cmg_dashboard(self) -> list[Path]:
        cfg = self.cfgs["cmg_dashboard"]
        out_dir = S.DATA_RAW / cfg["category"]
        meses = cfg["params"]["meses_atras"]
        barras = cfg["params"]["barras"]
        downloaded = []
        try:
            ctx = self.base.playwright_page()
            page = ctx.new_page()
            page.goto(cfg["url"], wait_until="networkidle", timeout=S.PLAYWRIGHT_TIMEOUT_MS)
        except (AuthRequiredError, RobotsDisallowed, CaptchaDetected) as e:
            logger.error(f"cmg_dashboard abort: {e}")
            return []
        except Exception as e:
            logger.error(f"cmg_dashboard playwright open error: {e}")
            self.base._log_failed(cfg["url"], f"playwright-open:{e}")
            return []
        try:
            today = date.today()
            months: list[tuple[int, int]] = []
            cursor = today.replace(day=1)
            for _ in range(meses):
                months.append((cursor.year, cursor.month))
                # mes anterior
                prev = cursor - timedelta(days=1)
                cursor = prev.replace(day=1)
            for barra in barras:
                for (y, m) in months:
                    target_name = f"cmg_horario_{self._slug(barra)}_{y:04d}-{m:02d}.csv"
                    target = out_dir / target_name
                    if target.exists():
                        logger.info(f"CACHE hit {target_name}")
                        downloaded.append(target)
                        continue
                    try:
                        self._cmg_dashboard_select_and_download(page, barra, y, m, target)
                        if target.exists():
                            downloaded.append(target)
                    except Exception as e:
                        logger.warning(f"cmg {barra} {y}-{m:02d}: {e}")
                        self.base._log_failed(cfg["url"], f"cmg {barra} {y}-{m:02d}: {e}")
        finally:
            try:
                ctx.close()
            except Exception:
                pass
        return downloaded

    def _cmg_dashboard_select_and_download(self, page, barra: str, year: int, month: int, target: Path):
        """Intento generico: setear selects/inputs por etiqueta y atrapar el download.

        Como el dashboard real puede cambiar selectores, este metodo encapsula
        la operacion en un try/except amplio para no inventar selectores. Si la
        descarga no ocurre en <30s, registra fail.
        """
        # Estrategia: buscar inputs label-y por nombre de barra y dispatch.
        # NO inventar selectores: si no encontramos, registramos.
        sel_barra = f"select:has-text('{barra}')"
        try:
            page.locator(sel_barra).first.select_option(label=barra, timeout=5000)
        except Exception:
            # fallback: no seleccionable -> registrar
            raise RuntimeError(f"selector barra no encontrado para {barra}")
        # rango de fechas
        date_from = f"{year:04d}-{month:02d}-01"
        # ultimo dia del mes aproximado: dia 28 funciona para todos
        date_to = f"{year:04d}-{month:02d}-28"
        for ph, val in (("Desde", date_from), ("Hasta", date_to)):
            try:
                page.get_by_label(ph).first.fill(val, timeout=5000)
            except Exception:
                pass
        with page.expect_download(timeout=30_000) as dl_info:
            try:
                page.get_by_role("button", name=re.compile("descargar|exportar|csv", re.I)).first.click()
            except Exception as e:
                raise RuntimeError(f"boton descarga no encontrado: {e}")
        dl = dl_info.value
        dl.save_as(str(target))

    def run_operacion_real(self) -> list[Path]:
        """Operacion real: intenta extraer CSVs; si falla, fallback a PDFs Informe Mensual."""
        cfg = self.cfgs["operacion_real_graficos"]
        out_dir = S.DATA_RAW / cfg["category"]
        try:
            self.base.playwright_get_html(cfg["url"], wait_selector="canvas, table, .dashboard")
            # Sin selectores conocidos para CSV: fallback inmediato a PDF mensual.
            logger.info("operacion_real_graficos: fallback a Informes Mensuales del Coordinador")
        except (AuthRequiredError, RobotsDisallowed, CaptchaDetected) as e:
            logger.error(f"operacion_real abort: {e}")
        except Exception as e:
            logger.warning(f"operacion_real playwright: {e}; cae a fallback PDF")
        # Fallback PDF Informe Mensual (ultimos 6)
        try:
            pdfs = self.list_links_matching(
                "https://www.coordinador.cl/reportes-y-estadisticas/",
                r"informe.*mensual",
            )
        except Exception as e:
            logger.error(f"fallback list pdfs: {e}")
            return []
        downloaded = []
        for url in pdfs[:6]:
            try:
                p = self.base.download(url, S.DATA_RAW / "cen/informes_mensuales")
                downloaded.append(p)
            except Exception as e:
                logger.warning(f"skip {url}: {e}")
        return downloaded

    def run_demanda(self) -> list[Path]:
        cfg = self.cfgs["demanda"]
        out_dir = S.DATA_RAW / cfg["category"]
        try:
            self.base.playwright_get_html(cfg["url"])
            logger.info("demanda: dashboard cargado pero sin estrategia de export tabular conocida")
            self.base._log_failed(cfg["url"], "demanda-no-extractor")
        except (AuthRequiredError, RobotsDisallowed, CaptchaDetected) as e:
            logger.error(f"demanda abort: {e}")
        except Exception as e:
            logger.error(f"demanda playwright: {e}")
        return []

    def run_capacidad_instalada(self) -> list[Path]:
        return self._search_and_download("capacidad_instalada", S.DATA_RAW / "cen/capacidad_instalada")

    def run_precipitaciones(self) -> list[Path]:
        return self._search_and_download("precipitaciones", S.DATA_RAW / "cen/precipitaciones")

    def run_instalaciones_en_operacion(self) -> list[Path]:
        return self._search_and_download("instalaciones_en_operacion", S.DATA_RAW / "cen/instalaciones",
                                         extra_exts=(".xlsx", ".xls", ".zip"))

    def run_documentos_tecnicos(self) -> list[Path]:
        out = []
        for key in ("doc_ciberseguridad_estandar", "doc_ciberseguridad_protocolo",
                    "doc_grid_forming_bess", "reporte_anual_desempeno_sen"):
            if key not in self.cfgs:
                continue
            cfg = self.cfgs[key]
            out.extend(self._search_and_download(key, S.DATA_RAW / cfg["category"]))
        return out

    # ---- generico search_in_page ------------------------------------------
    def _search_and_download(self, cfg_id: str, dest: Path,
                             extra_exts: Iterable[str] = (".pdf",)) -> list[Path]:
        cfg = self.cfgs[cfg_id]
        match = cfg.get("params", {}).get("match", "")
        try:
            res = self.base.get(cfg["url"])
        except Exception as e:
            logger.error(f"{cfg_id} list error: {e}")
            return []
        soup = BeautifulSoup(res.text(), "lxml")
        pat = re.compile(re.escape(match), re.IGNORECASE) if match else re.compile(".")
        candidates = []
        for a in soup.select("a[href]"):
            href = a["href"]
            text = (a.get_text() or "")
            haystack = text + " " + href
            if not pat.search(haystack):
                continue
            if not any(href.lower().endswith(ext) for ext in extra_exts):
                continue
            candidates.append(urllib.parse.urljoin(cfg["url"], href))
        candidates = sorted(set(candidates))
        out = []
        for url in candidates[:40]:
            try:
                p = self.base.download(url, dest)
                out.append(p)
            except Exception as e:
                logger.warning(f"skip {url}: {e}")
        return out

    # ---- utils -------------------------------------------------------------
    @staticmethod
    def _slug(s: str) -> str:
        s2 = (s.lower()
              .replace("a", "a").replace("e", "e").replace("i", "i")
              .replace("o", "o").replace("u", "u").replace("n", "n")
              .replace(" ", "-"))
        return re.sub(r"[^a-z0-9\-]", "", s2)
