---
title: Resultados de baselines — costo de operacion D+1
sources:
  - data/processed/tabla_maestra.parquet
  - models/evaluacion.py
last_synthesized: 2026-06-12
---

# Resultados de baselines

> ⚠️ **DATOS SINTÉTICOS.** Estos números validan la maquinaria
> (protocolo walk-forward, anti-fuga, pipeline) sobre
> `data/raw_sintetico/`. **NO son métricas del problema real.**
> Se regeneran automáticamente cuando el backfill real
> (workflow `backfill.yml`) puebla `data/raw/`.

Protocolo: walk-forward ventana expansiva, refit cada 28 días,
mínimo 365 días de entrenamiento inicial — única vía:
`models/evaluacion.py`. Métrica principal: MAPE.

| Modelo | MAPE % | MAE USD | RMSE USD | Sesgo USD | Folds | N |
|--------|-------:|--------:|---------:|----------:|------:|--:|
| persistencia_lag1 (teorica, fuga operacional) | 7.00 | 745,888 | 1,506,095 | -514 | 85 | 2353 |
| persistencia_lag2 (implementable) | 8.87 | 923,621 | 1,630,842 | -951 | 85 | 2353 |
| estacional_dow_4sem | 6.59 | 694,811 | 1,264,153 | -10,549 | 85 | 2353 |
| lightgbm_baseline | 6.85 | 717,547 | 1,225,060 | +265,772 | 85 | 2353 |

**Mejor baseline: `estacional_dow_4sem` (MAPE 6.59 %).**
Evaluado 2020-01-01 00:00:00 → 2026-06-10 00:00:00.
LightGBM usa 122 features conformes a la regla 20:00
(verificación automática `verificar_antifuga`; `costo_lag1` y
`cmg_programado_d1` rechazadas por declaración de no conformidad).

## Análisis de errores (mejor modelo)

### MAPE por condición de calendario

| Condición | False | True |
|-----------|------:|-----:|
| es_feriado | 6.24 | 14.07 |
| es_finde | 6.68 | 6.36 |
| es_sandwich | 6.59 | 5.83 |
| semana_18sept | 6.52 | 10.30 |
| es_eleccion | 6.58 | 7.89 |

### MAPE por día de semana

| lun | mar | mie | jue | vie | sab | dom |
|---:|---:|---:|---:|---:|---:|---:|
| 7.00 | 5.88 | 6.26 | 6.96 | 7.28 | 5.38 | 7.33 |

### MAPE por mes

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 6.51 | 6.01 | 5.99 | 6.98 | 6.56 | 6.24 | 6.93 | 5.08 | 7.22 | 7.59 | 6.22 | 7.82 |

### 15 peores días

| fecha               |        real |   prediccion |     ape | es_feriado   | es_finde   | es_sandwich   | semana_18sept   | es_eleccion   |
|:--------------------|------------:|-------------:|--------:|:-------------|:-----------|:--------------|:----------------|:--------------|
| 2025-02-25 00:00:00 | 1.6478e+07  |  6.62949e+06 | 59.7676 | False        | False      | False         | False           | False         |
| 2026-06-07 00:00:00 | 2.3482e+07  |  1.01766e+07 | 56.6622 | False        | True       | False         | False           | False         |
| 2026-01-18 00:00:00 | 1.48534e+07 |  6.55619e+06 | 55.8606 | False        | True       | False         | False           | False         |
| 2021-07-05 00:00:00 | 2.74858e+07 |  1.22014e+07 | 55.6084 | False        | False      | False         | False           | False         |
| 2024-03-14 00:00:00 | 1.58221e+07 |  7.33244e+06 | 53.657  | False        | False      | False         | False           | False         |
| 2024-07-05 00:00:00 | 2.12585e+07 |  1.05555e+07 | 50.347  | False        | False      | False         | False           | False         |
| 2021-06-17 00:00:00 | 2.53872e+07 |  1.29857e+07 | 48.8494 | False        | False      | False         | False           | False         |
| 2024-10-05 00:00:00 | 1.72925e+07 |  8.97251e+06 | 48.1134 | False        | True       | False         | False           | False         |
| 2026-01-15 00:00:00 | 1.28862e+07 |  6.81235e+06 | 47.1344 | False        | False      | False         | False           | False         |
| 2020-01-15 00:00:00 | 1.8911e+07  |  1.01559e+07 | 46.2964 | False        | False      | False         | False           | False         |
| 2022-04-22 00:00:00 | 1.96241e+07 |  1.07004e+07 | 45.473  | False        | False      | False         | False           | False         |
| 2025-03-28 00:00:00 | 1.29429e+07 |  7.11232e+06 | 45.0485 | False        | False      | False         | False           | False         |
| 2022-05-06 00:00:00 | 2.31988e+07 |  1.31313e+07 | 43.3967 | False        | False      | False         | False           | False         |
| 2025-08-17 00:00:00 | 1.72118e+07 |  9.77035e+06 | 43.2345 | False        | True       | False         | False           | False         |
| 2023-05-13 00:00:00 | 1.47258e+07 |  8.59523e+06 | 41.6313 | False        | True       | False         | False           | False         |
