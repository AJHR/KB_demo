"""Genera REPORTE_INGESTA.md a partir de data/raw + LanceDB + logs."""
from __future__ import annotations

import _bootstrap  # noqa: F401

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from config import settings as S


DEMO_QUERIES = [
    "Costo marginal promedio en Quillota ultimo mes",
    "Que dice el anexo sismico sobre BESS",
    "Cambios propuestos por la reforma 2026",
    "Como se reportan ciberincidentes en el sector electrico chileno",
    "Capacidad instalada de generacion solar en Chile 2026",
]


def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def counts_by_category() -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for sub in sorted(S.DATA_RAW.rglob("*")):
        if not sub.is_file() or sub.name.endswith(".meta.json") or sub.name == ".gitkeep":
            continue
        cat = "/".join(sub.parent.relative_to(S.DATA_RAW).parts)
        n, sz = out.get(cat, (0, 0))
        out[cat] = (n + 1, sz + sub.stat().st_size)
    return out


def fechas_cobertura(category_prefix: str) -> tuple[str, str]:
    import re
    rng_min: str | None = None
    rng_max: str | None = None
    for meta in (S.DATA_RAW / category_prefix).rglob("*.meta.json") if (S.DATA_RAW / category_prefix).exists() else []:
        try:
            d = json.loads(meta.read_text("utf-8"))
        except Exception:
            continue
        for src in (d.get("url", ""), meta.stem):
            m = re.search(r"(20\d{2})[-_]?(\d{2})", src)
            if m:
                k = f"{m.group(1)}-{m.group(2)}"
                rng_min = k if (rng_min is None or k < rng_min) else rng_min
                rng_max = k if (rng_max is None or k > rng_max) else rng_max
    return rng_min or "-", rng_max or "-"


def read_log(path: Path, label: str) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text("utf-8").splitlines()
    return lines[-100:]


def run_demo_queries() -> list[dict]:
    """Ejecuta las 5 demo queries contra LanceDB; si no hay datos, devuelve nota."""
    out = []
    try:
        import lancedb
        from sentence_transformers import SentenceTransformer
        db = lancedb.connect(str(S.LANCEDB_PATH))
        if "chunks" not in db.table_names():
            return [{"query": q, "results": [], "note": "Tabla 'chunks' no existe"} for q in DEMO_QUERIES]
        tbl = db.open_table("chunks")
        model = SentenceTransformer(S.EMBED_MODEL)
        for q in DEMO_QUERIES:
            v = model.encode(q, normalize_embeddings=True).tolist()
            hits = tbl.search(v).limit(3).to_list()
            out.append({"query": q, "results": [
                {"file": h.get("file_path"), "source_url": h.get("source_url"),
                 "chunk_index": h.get("chunk_index"),
                 "snippet": (h.get("text", "") or "")[:240].replace("\n", " ")}
                for h in hits
            ], "note": ""})
    except Exception as e:
        for q in DEMO_QUERIES:
            out.append({"query": q, "results": [], "note": f"error: {e}"})
    return out


def main() -> int:
    cats = counts_by_category()
    total_files = sum(n for n, _ in cats.values())
    total_size = sum(sz for _, sz in cats.values())

    manifest = {"docs": [], "stats": {}}
    if S.MANIFEST_PATH.exists():
        try:
            manifest = json.loads(S.MANIFEST_PATH.read_text("utf-8"))
        except Exception:
            pass
    chunks_total = manifest.get("stats", {}).get("chunks_total", 0)
    requires_ocr = manifest.get("stats", {}).get("requires_ocr", [])

    failed = read_log(S.FAILED_DOWNLOADS, "failed_downloads.txt")
    auth = read_log(S.AUTH_REQUIRED, "auth_required.txt")
    robots = read_log(S.SKIPPED_BY_ROBOTS, "skipped_by_robots.txt")

    cmg_min, cmg_max = fechas_cobertura("cen/costos_marginales")
    gen_min, gen_max = fechas_cobertura("cen/generacion_real")
    dem_min, dem_max = fechas_cobertura("cen/demanda")

    demo = run_demo_queries()

    lines: list[str] = []
    A = lines.append
    A(f"# Reporte de Ingesta — {datetime.utcnow().strftime('%Y-%m-%d %H:%MZ')}")
    A("")
    A("## Resumen")
    A(f"- Archivos descargados: **{total_files}** ({_human(total_size)})")
    A(f"- Chunks en vector store: **{chunks_total}**")
    A(f"- Docs PDF que requieren OCR: **{len(requires_ocr)}**")
    A(f"- Rutas saltadas por robots.txt: **{len(robots)}**")
    A(f"- Descargas fallidas: **{len(failed)}**")
    A(f"- Recursos que requieren auth: **{len(auth)}**")
    A("")
    A("## Archivos por categoria")
    A("")
    A("| Categoria | Archivos | Tamano |")
    A("|-----------|----------|--------|")
    for cat in sorted(cats):
        n, sz = cats[cat]
        A(f"| {cat} | {n} | {_human(sz)} |")
    A("")
    A("## Cobertura temporal")
    A("")
    A("| Serie | Min | Max |")
    A("|-------|-----|-----|")
    A(f"| CEN CMg horario | {cmg_min} | {cmg_max} |")
    A(f"| CEN generacion real | {gen_min} | {gen_max} |")
    A(f"| CEN demanda | {dem_min} | {dem_max} |")
    A("")
    A("## Documentos que requieren OCR (escaneados)")
    if requires_ocr:
        for r in requires_ocr:
            A(f"- `{r}`")
    else:
        A("_(ninguno)_")
    A("")
    A("## Rutas saltadas por robots.txt (ultimas 100)")
    if robots:
        A("```")
        A("\n".join(robots))
        A("```")
    else:
        A("_(ninguna)_")
    A("")
    A("## Descargas fallidas (ultimas 100)")
    if failed:
        A("```")
        A("\n".join(failed))
        A("```")
    else:
        A("_(ninguna)_")
    A("")
    A("## Recursos que requirieron auth (ultimas 100)")
    if auth:
        A("```")
        A("\n".join(auth))
        A("```")
    else:
        A("_(ninguno)_")
    A("")
    A("## 5 queries de prueba contra el vector store")
    for entry in demo:
        A("")
        A(f"### Q: {entry['query']}")
        if not entry["results"]:
            A(f"_Sin resultados._ {entry.get('note','')}")
            continue
        for i, r in enumerate(entry["results"], 1):
            A(f"{i}. `{r.get('file')}` (chunk #{r.get('chunk_index')}) — {r.get('source_url') or 'sin url'}")
            A(f"   > {r.get('snippet')}")
    out_path = S.ROOT / "REPORTE_INGESTA.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"escrito: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
