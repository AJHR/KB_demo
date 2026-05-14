"""Update diario: ultimos 7 dias de CMg horario y generacion/demanda.

Programar 06:00 hora Chile via apscheduler (cron) o cron del SO.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401

import sys
from datetime import date, timedelta

import yaml
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper
from scrapers.cen_scraper import CENScraper
from scripts.process_to_vector import process_all


def _setup_logging():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(S.SYNC_LOG, level="DEBUG", rotation="50 MB")


def main() -> int:
    _setup_logging()
    with S.SOURCES_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    base = BaseScraper()
    try:
        cen = CENScraper(base, cfg["cen"]["pages"])
        # ultimos 7 dias = mes en curso (y mes anterior si cruza fin de mes)
        today = date.today()
        meses = [(today.year, today.month)]
        first_of_month = today.replace(day=1)
        if (today - first_of_month).days < 7:
            prev = first_of_month - timedelta(days=1)
            meses.append((prev.year, prev.month))
        # forzar override del rango: monkeypatch del config
        cen.cfgs["cmg_dashboard"]["params"]["meses_atras"] = len(meses)
        logger.info(f"update_daily: meses {meses}")
        cen.run_cmg_dashboard()
        cen.run_operacion_real()
        cen.run_demanda()
    finally:
        base.close()
    logger.info("update_daily: re-indexando delta...")
    stats = process_all()
    logger.info(f"update_daily done: {stats}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
