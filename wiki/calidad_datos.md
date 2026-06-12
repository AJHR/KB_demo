---
title: Calidad de datos del pipeline de costos SEN
sources:
  - data/processed/tabla_maestra.parquet
last_synthesized: 2026-06-12
---

# Calidad de datos — pipeline de costos SEN

> Generado automaticamente por `tools/etl/validadores.py --reporte` el 2026-06-12.
> Directorio analizado: `/home/user/KB_demo/data/raw`.

## Completitud por fuente

| fuente | fecha_min | fecha_max | dias_presentes | dias_esperados | pct_completitud | n_huecos | huecos |
|---|---|---|---|---|---|---|---|
| calendario | 2020-01-01 | 2026-12-31 | 2557 | 2557 | 100.0 | 0 |  |

## Outliers (|x - mediana| > 4 · MAD escalado)

_(ninguna fuente con columnas numericas conocidas todavia)_

## Consistencia cruzada: generacion vs demanda (diario)

_No evaluable: faltan `cen_demanda` y/o `cen_generacion`._

