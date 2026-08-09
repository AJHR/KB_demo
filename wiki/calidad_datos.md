---
title: Calidad de datos del pipeline de costos SEN
sources:
  - data/processed/tabla_maestra.parquet
last_synthesized: 2026-08-09
---

# Calidad de datos — pipeline de costos SEN

> Generado automaticamente por `tools/etl/validadores.py --reporte` el 2026-08-09.
> Directorio analizado: `/home/runner/work/KB_demo/KB_demo/data/raw`.

## Completitud por fuente

| fuente | fecha_min | fecha_max | dias_presentes | dias_esperados | pct_completitud | n_huecos | huecos |
|---|---|---|---|---|---|---|---|
| calendario | 2019-01-01 | 2026-12-31 | 2892 | 2922 | 99.0 | 1 | 2026-06-01..2026-06-30 |
| clima_observado | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| clima_pronostico | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| combustibles | 2019-01-02 | 2026-06-12 | 1915 | 2719 | 70.4 | 396 | 2019-01-05..2019-01-06; 2019-01-12..2019-01-13; 2019-01-19..2019-01-20; 2019-01-26..2019-01-27; 2019-02-02..2019-02-03; 2019-02-09..2019-02-10; 2019-02-16..2019-02-17; 2019-02-23..2019-02-24; 2019-03-02..2019-03-03; 2019-03-09..2019-03-10; 2019-03-16..2019-03-17; 2019-03-23..2019-03-24; 2019-03-30..2019-03-31; 2019-04-06..2019-04-07; 2019-04-13..2019-04-14; 2019-04-19..2019-04-21; 2019-04-27..2019-04-28; 2019-05-04..2019-05-05; 2019-05-11..2019-05-12; 2019-05-18..2019-05-19 ... |

## Outliers (|x - mediana| > 4 · MAD escalado)

_(ninguna fuente con columnas numericas conocidas todavia)_

## Consistencia cruzada: generacion vs demanda (diario)

Sin violaciones (tolerancia 12%: perdidas + autoconsumo).

