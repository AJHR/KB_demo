---
title: Calidad de datos del pipeline de costos SEN
sources:
  - data/processed/tabla_maestra.parquet
last_synthesized: 2026-06-17
---

# Calidad de datos — pipeline de costos SEN

> Generado automaticamente por `tools/etl/validadores.py --reporte` el 2026-06-17.
> Directorio analizado: `/home/runner/work/KB_demo/KB_demo/data/raw`.

## Completitud por fuente

| fuente | fecha_min | fecha_max | dias_presentes | dias_esperados | pct_completitud | n_huecos | huecos |
|---|---|---|---|---|---|---|---|
| calendario | 2019-01-01 | 2026-12-31 | 2904 | 2922 | 99.4 | 1 | 2026-06-13..2026-06-30 |
| cen_cmg_programado | 2024-01-01 | 2026-06-14 | 772 | 896 | 86.2 | 21 | 2024-02-06..2024-02-06; 2024-02-12..2024-02-14; 2024-03-01..2024-05-31; 2024-07-04..2024-07-04; 2024-07-25..2024-07-25; 2024-08-14..2024-08-14; 2024-09-01..2024-09-03; 2024-09-11..2024-09-12; 2024-09-16..2024-09-17; 2024-09-21..2024-09-21; 2024-09-26..2024-09-26; 2024-09-30..2024-09-30; 2024-10-27..2024-10-27; 2024-11-11..2024-11-11; 2024-11-16..2024-11-17; 2024-12-15..2024-12-20; 2025-01-14..2025-01-14; 2025-02-27..2025-02-27; 2025-03-03..2025-03-03; 2025-03-06..2025-03-06 ... |
| cen_cmg_real | 2025-03-01 | 2026-06-07 | 462 | 464 | 99.6 | 1 | 2025-06-01..2025-06-02 |
| cen_embalses | 2024-01-01 | 2026-05-08 | 761 | 859 | 88.6 | 5 | 2024-03-01..2024-05-31; 2025-11-28..2025-11-30; 2025-12-02..2025-12-02; 2026-02-09..2026-02-09; 2026-03-02..2026-03-02 |
| clima_observado | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| clima_pronostico | 2019-01-01 | 2026-06-13 | 2721 | 2721 | 100.0 | 0 |  |
| combustibles | 2019-01-02 | 2026-06-12 | 1915 | 2719 | 70.4 | 396 | 2019-01-05..2019-01-06; 2019-01-12..2019-01-13; 2019-01-19..2019-01-20; 2019-01-26..2019-01-27; 2019-02-02..2019-02-03; 2019-02-09..2019-02-10; 2019-02-16..2019-02-17; 2019-02-23..2019-02-24; 2019-03-02..2019-03-03; 2019-03-09..2019-03-10; 2019-03-16..2019-03-17; 2019-03-23..2019-03-24; 2019-03-30..2019-03-31; 2019-04-06..2019-04-07; 2019-04-13..2019-04-14; 2019-04-19..2019-04-21; 2019-04-27..2019-04-28; 2019-05-04..2019-05-05; 2019-05-11..2019-05-12; 2019-05-18..2019-05-19 ... |

## Outliers (|x - mediana| > 4 · MAD escalado)

- `cen_cmg_real.cmg_usd_mwh`: 2145 filas sospechosas de 75408 (2.84%)

| fecha | barra | cmg_usd_mwh | _desviacion_robusta |
|---|---|---|---|
| 2025-03-13 | BA S/E CRUCERO 220KV BP1 | 188.16851 | 4.2 |
| 2025-03-14 | BA S/E ALTO JAHUEL 220KV BP1 | 216.4691975 | 5.1 |
| 2025-03-14 | BA S/E ALTO JAHUEL 220KV BP2 | 212.123015 | 5.0 |
| 2025-03-14 | BA S/E CHARRUA 220KV BP1-1 | 207.62363249999999 | 4.9 |
| 2025-03-14 | BA S/E CRUCERO 220KV BP1 | 229.2619775 | 5.6 |

- `cen_cmg_programado.cmg_usd_mwh`: 3574 filas sospechosas de 249955 (1.43%)

| fecha | barra | cmg_usd_mwh | _desviacion_robusta |
|---|---|---|---|
| 2024-01-01 | BA S/E CHARRUA 220KV BP1-1 | 435.06 | 16.9 |
| 2024-01-01 | BA S/E POLPAICO (TRANSELEC) 220KV BP1 | 435.06 | 16.9 |
| 2024-01-01 | BA S/E QUILLOTA 220KV BP1-1 | 435.06 | 16.9 |
| 2024-01-01 | BA S/E ALTO JAHUEL 220KV BP1 | 435.06 | 16.9 |
| 2024-01-01 | BA S/E CRUCERO 220KV BP1 | 435.06 | 16.9 |

- `cen_embalses.cota_msnm`: 18266 filas sospechosas de 219191 (8.33%)

| fecha | embalse | cota_msnm | _desviacion_robusta |
|---|---|---|---|
| 2024-01-01 | MAULE | 2164.2 | 4.4 |
| 2024-01-01 | MAULE | 2164.2 | 4.4 |
| 2024-01-01 | MAULE | 2164.2 | 4.4 |
| 2024-01-01 | MAULE | 2164.2 | 4.4 |
| 2024-01-01 | MAULE | 2164.2 | 4.4 |


## Consistencia cruzada: generacion vs demanda (diario)

Sin violaciones (tolerancia 12%: perdidas + autoconsumo).

