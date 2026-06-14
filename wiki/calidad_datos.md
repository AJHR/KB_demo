---
title: Calidad de datos del pipeline de costos SEN
sources:
  - data/processed/tabla_maestra.parquet
last_synthesized: 2026-06-14
---

# Calidad de datos — pipeline de costos SEN

> Generado automaticamente por `tools/etl/validadores.py --reporte` el 2026-06-14.
> Directorio analizado: `/home/runner/work/KB_demo/KB_demo/data/raw`.

## Completitud por fuente

| fuente | fecha_min | fecha_max | dias_presentes | dias_esperados | pct_completitud | n_huecos | huecos |
|---|---|---|---|---|---|---|---|
| calendario | 2019-01-01 | 2026-12-31 | 2904 | 2922 | 99.4 | 1 | 2026-06-13..2026-06-30 |
| cen_cmg_programado | 2024-01-01 | 2024-02-29 | 56 | 60 | 93.3 | 2 | 2024-02-06..2024-02-06; 2024-02-12..2024-02-14 |
| cen_embalses | 2024-01-01 | 2024-02-29 | 60 | 60 | 100.0 | 0 |  |
| clima_observado | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| clima_pronostico | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| combustibles | 2019-01-02 | 2026-06-12 | 1915 | 2719 | 70.4 | 396 | 2019-01-05..2019-01-06; 2019-01-12..2019-01-13; 2019-01-19..2019-01-20; 2019-01-26..2019-01-27; 2019-02-02..2019-02-03; 2019-02-09..2019-02-10; 2019-02-16..2019-02-17; 2019-02-23..2019-02-24; 2019-03-02..2019-03-03; 2019-03-09..2019-03-10; 2019-03-16..2019-03-17; 2019-03-23..2019-03-24; 2019-03-30..2019-03-31; 2019-04-06..2019-04-07; 2019-04-13..2019-04-14; 2019-04-19..2019-04-21; 2019-04-27..2019-04-28; 2019-05-04..2019-05-05; 2019-05-11..2019-05-12; 2019-05-18..2019-05-19 ... |

## Outliers (|x - mediana| > 4 · MAD escalado)

- `cen_cmg_programado.cmg_usd_mwh`: 222 filas sospechosas de 10275 (2.16%)

| fecha | barra | cmg_usd_mwh | _desviacion_robusta |
|---|---|---|---|
| 2024-01-01 | BA S/E CHARRUA 220KV BP1-1 | 435.06 | 12.3 |
| 2024-01-01 | BA S/E POLPAICO (TRANSELEC) 220KV BP1 | 435.06 | 12.3 |
| 2024-01-01 | BA S/E QUILLOTA 220KV BP1-1 | 435.06 | 12.3 |
| 2024-01-01 | BA S/E ALTO JAHUEL 220KV BP1 | 435.06 | 12.3 |
| 2024-01-01 | BA S/E CRUCERO 220KV BP1 | 435.06 | 12.3 |

- `cen_embalses.cota_msnm`: 0 filas sospechosas de 17280 (0.00%)

## Consistencia cruzada: generacion vs demanda (diario)

Sin violaciones (tolerancia 12%: perdidas + autoconsumo).

