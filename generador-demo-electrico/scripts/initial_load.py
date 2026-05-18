"""Orquesta la carga inicial completa.

Esperado: 6-8 horas. No optimizar para velocidad. Logs verbosos en logs/sync.log.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401

import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path

import yaml
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper
from scrapers.cen_scraper import CENScraper
from scrapers.cne_scraper import CNEScraper
from scrapers.energia_abierta import EnergiaAbiertaScraper
from scrapers.regulation_scraper import RegulationScraper


def _setup_logging():
    logger.remove()
    logger.add(sys.stderr, level="INFO",
               format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | {message}")
    logger.add(S.SYNC_LOG, level="DEBUG", rotation="50 MB", retention=10,
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | {name}:{function}:{line} | {message}")


def _load_sources() -> dict:
    with S.SOURCES_YAML.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    _setup_logging()
    t0 = time.time()
    logger.info("=== initial_load: start ===")
    cfg = _load_sources()

    base = BaseScraper()
    counts: dict[str, int] = defaultdict(int)

    try:
        cen = CENScraper(base, cfg["cen"]["pages"])
        cne = CNEScraper(base, cfg["cne"]["pages"])
        ea = EnergiaAbiertaScraper(base, cfg["energia_abierta"]["pages"])
        reg = RegulationScraper(base, cfg["ministerio_energia"]["pages"])

        steps = [
            ("CEN: reportes y estadisticas", cen.run_reportes_y_estadisticas),
            ("CEN: costos marginales (dashboard)", cen.run_cmg_dashboard),
            ("CEN: operacion real (PDF fallback)", cen.run_operacion_real),
            ("CEN: demanda", cen.run_demanda),
            ("CEN: capacidad instalada", cen.run_capacidad_instalada),
            ("CEN: precipitaciones", cen.run_precipitaciones),
            ("CEN: instalaciones en operacion", cen.run_instalaciones_en_operacion),
            ("CEN: documentos tecnicos", cen.run_documentos_tecnicos),
            ("CNE: normativa electrica", cne.run_normativa_electrica),
            ("CNE: NTSyCS", cne.run_ntsycs),
            ("CNE: anexo sismico", cne.run_anexo_sismico),
            ("CNE: obras nuevas y urgentes", cne.run_obras_nuevas_urgentes),
            ("CNE: precios de nudo", cne.run_precios_nudo),
            ("CNE: informes tecnicos Art.163", cne.run_informes_tecnicos_art163),
            ("Energia Abierta: estadisticas electricidad", ea.run_estadisticas_electricidad),
            ("Energia Abierta: listado empresas", ea.run_listado_empresas),
            ("Minenergia: reforma 2026", reg.run_reforma_2026),
        ]

        for name, fn in steps:
            logger.info(f"[step] {name}")
            try:
                files = fn() or []
                counts[name] = len(files)
                logger.info(f"[step] {name}: {len(files)} archivo(s)")
            except Exception as e:
                logger.error(f"[step-error] {name}: {e}\n{traceback.format_exc()}")
                base._log_failed(name, f"step-fatal:{e}")
                counts[name] = 0
    finally:
        base.close()

    dt = time.time() - t0
    logger.info(f"=== initial_load: done in {dt/60:.1f} min ===")
    total = sum(counts.values())
    logger.info(f"total archivos descargados: {total}")
    for k, v in counts.items():
        logger.info(f"  {v:>5}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
