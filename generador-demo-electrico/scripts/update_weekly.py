"""Update semanal: chequea nuevas versiones de normativa + ultimo Informe Mensual.

Programar lunes 07:00 hora Chile.
"""
from __future__ import annotations

import _bootstrap  # noqa: F401

import json
import sys
from datetime import date

import yaml
from loguru import logger

from config import settings as S
from scrapers.base_scraper import BaseScraper
from scrapers.cen_scraper import CENScraper
from scrapers.cne_scraper import CNEScraper
from scripts.process_to_vector import process_all


def _setup_logging():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(S.SYNC_LOG, level="DEBUG", rotation="50 MB")


def _snapshot_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    for meta_path in S.DATA_RAW.rglob("*.meta.json"):
        try:
            d = json.loads(meta_path.read_text("utf-8"))
            key = str(meta_path.with_suffix("").relative_to(S.DATA_RAW))
            out[key] = d.get("sha256", "")
        except Exception:
            continue
    return out


def main() -> int:
    _setup_logging()
    with S.SOURCES_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    pre = _snapshot_hashes()
    base = BaseScraper()
    try:
        cen = CENScraper(base, cfg["cen"]["pages"])
        cne = CNEScraper(base, cfg["cne"]["pages"])
        cne.run_normativa_electrica()
        cne.run_ntsycs()
        cne.run_anexo_sismico()
        cne.run_obras_nuevas_urgentes()
        cne.run_informes_tecnicos_art163()
        cen.run_documentos_tecnicos()
        cen.run_reportes_y_estadisticas()
    finally:
        base.close()
    post = _snapshot_hashes()
    changed = sorted(k for k in post if pre.get(k) != post.get(k))
    added = sorted(k for k in post.keys() - pre.keys())
    if changed or added:
        logger.info("update_weekly: re-indexando delta...")
        stats = process_all()
    else:
        logger.info("update_weekly: sin cambios; skip reindex.")
        stats = {}
    cl_path = S.DATA_VECTOR / f"changelog_{date.today().isoformat()}.md"
    lines = [f"# Changelog {date.today().isoformat()}", ""]
    if added:
        lines.append("## Nuevos")
        lines += [f"- {a}" for a in added]
    if changed:
        lines.append("\n## Modificados")
        lines += [f"- {c}" for c in changed]
    if not added and not changed:
        lines.append("Sin cambios.")
    cl_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"update_weekly done: changelog={cl_path}; stats={stats}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
