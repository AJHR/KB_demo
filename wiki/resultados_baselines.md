---
title: Resultados de baselines — CMg real diario D+1
sources:
  - data/processed/tabla_maestra.parquet
  - models/evaluacion.py
last_synthesized: 2026-06-17
---

# Resultados de baselines

Protocolo: walk-forward ventana expansiva, refit cada 28 días,
mínimo 365 días de entrenamiento inicial — única vía:
`models/evaluacion.py`. Métrica principal: MAPE.

| Modelo | MAPE % | MAE USD/MWh | RMSE USD/MWh | Sesgo USD/MWh | Folds | N |
|--------|-------:|------------:|-------------:|--------------:|------:|--:|
| persistencia_lag1 (teorica, fuga operacional) | 22.95 | 10.52 | 15.35 | +0.20 | 12 | 328 |
| persistencia_lag3 (implementable, primer lag publicado) | 31.31 | 14.23 | 21.51 | +0.08 | 12 | 328 |
| estacional_dow_4sem | 27.93 | 13.01 | 19.53 | +0.89 | 12 | 328 |
| lightgbm_baseline | 33.60 | 14.08 | 19.57 | +3.34 | 12 | 328 |

**Mejor baseline: `persistencia_lag1 (teorica, fuga operacional)` (MAPE 22.95 %).**
Evaluado 2025-07-15 00:00:00 → 2026-06-07 00:00:00.
LightGBM usa 106 features conformes a la regla 20:00
(verificación automática `verificar_antifuga`; `cmg_lag1`, `cmg_lag2` y
`cmg_programado_d1` rechazadas por declaración de no conformidad).

## Análisis de errores (mejor modelo)

### MAPE por condición de calendario

| Condición | False | True |
|-----------|------:|-----:|
| es_feriado | 22.70 | 28.55 |
| es_finde | 21.59 | 26.34 |
| es_sandwich | 23.00 | 17.73 |
| semana_18sept | 23.12 | 15.42 |
| es_eleccion | 22.78 | 50.90 |

### MAPE por día de semana

| lun | mar | mie | jue | vie | sab | dom |
|---:|---:|---:|---:|---:|---:|---:|
| 19.82 | 18.06 | 23.75 | 20.67 | 25.62 | 32.49 | 20.18 |

### MAPE por mes

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 23.78 | 17.51 | 19.87 | 23.20 | 24.15 | 36.19 | 28.64 | 22.00 | 20.07 | 16.66 | 28.91 | 26.84 |

### 15 peores días

| fecha               |    real |   prediccion |      ape | es_feriado   | es_finde   | es_sandwich   | semana_18sept   | es_eleccion   |
|:--------------------|--------:|-------------:|---------:|:-------------|:-----------|:--------------|:----------------|:--------------|
| 2025-11-29 00:00:00 | 26.4034 |      57.1601 | 116.488  | False        | True       | False         | False           | False         |
| 2026-01-06 00:00:00 | 24.8712 |      53.1151 | 113.561  | False        | False      | False         | False           | False         |
| 2025-08-23 00:00:00 | 45.9637 |      97.7863 | 112.747  | False        | True       | False         | False           | False         |
| 2026-01-31 00:00:00 | 32.7359 |      68.3027 | 108.648  | False        | True       | False         | False           | False         |
| 2026-03-21 00:00:00 | 32.9741 |      68.6481 | 108.188  | False        | True       | False         | False           | False         |
| 2025-07-16 00:00:00 | 75.9697 |     152.666  | 100.957  | True         | False      | False         | False           | False         |
| 2025-12-12 00:00:00 | 32.4281 |      62.7731 |  93.5765 | False        | False      | False         | False           | False         |
| 2025-09-27 00:00:00 | 27.8223 |      52.8144 |  89.8278 | False        | True       | False         | False           | False         |
| 2026-06-03 00:00:00 | 62.4331 |     115.221  |  84.5503 | False        | False      | False         | False           | False         |
| 2026-05-28 00:00:00 | 76.6294 |     139.632  |  82.2166 | False        | False      | False         | False           | False         |
| 2025-11-07 00:00:00 | 28.3785 |      51.6004 |  81.8293 | False        | False      | False         | False           | False         |
| 2025-12-27 00:00:00 | 24.7004 |      44.5917 |  80.5301 | False        | True       | False         | False           | False         |
| 2026-01-24 00:00:00 | 31.7609 |      56.5503 |  78.0498 | False        | True       | False         | False           | False         |
| 2025-07-27 00:00:00 | 49.1139 |      86.2311 |  75.5736 | False        | True       | False         | False           | False         |
| 2025-12-14 00:00:00 | 22.6506 |      39.1023 |  72.6324 | False        | True       | False         | False           | True          |
