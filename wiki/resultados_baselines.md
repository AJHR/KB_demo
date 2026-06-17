---
title: Resultados de baselines — CMg real diario D+1
sources:
  - data/processed/tabla_maestra.parquet
  - models/evaluacion.py
  - autoresearch/log_experimentos.md
last_synthesized: 2026-06-17
---

# Resultados de baselines

Protocolo: walk-forward ventana expansiva, refit cada 28 días,
mínimo 365 días de entrenamiento inicial — única vía:
`models/evaluacion.py`. Métrica principal: MAPE.

| Modelo | MAPE % | MAE USD/MWh | RMSE USD/MWh | Sesgo USD/MWh | Folds | N |
|--------|-------:|------------:|-------------:|--------------:|------:|--:|
| persistencia_lag1 (teorica, fuga operacional) | 23.37 | 12.42 | 17.51 | -0.23 | 4 | 99 |
| persistencia_lag3 (implementable, primer lag publicado) | 31.18 | 16.84 | 24.42 | -1.02 | 4 | 99 |
| estacional_dow_4sem | 20.19 | 12.86 | 21.05 | -7.79 | 4 | 99 |
| lightgbm_baseline | 20.02 | 10.88 | 16.23 | -2.10 | 4 | 99 |

**Mejor baseline: `lightgbm_baseline` (MAPE 20.02 %).**
Evaluado 2026-03-01 00:00:00 → 2026-06-07 00:00:00.
LightGBM usa 106 features conformes a la regla 20:00
(verificación automática `verificar_antifuga`; `cmg_lag1`, `cmg_lag2` y
`cmg_programado_d1` rechazadas por declaración de no conformidad).

## Análisis de errores (mejor modelo)

### MAPE por condición de calendario

| Condición | False | True |
|-----------|------:|-----:|
| es_feriado | 19.63 | 29.33 |
| es_finde | 21.51 | 16.40 |
| es_sandwich | 19.82 | 39.20 |
| semana_18sept | 20.02 | nan |
| es_eleccion | 20.02 | nan |

### MAPE por día de semana

| lun | mar | mie | jue | vie | sab | dom |
|---:|---:|---:|---:|---:|---:|---:|
| 20.16 | 19.35 | 22.11 | 24.45 | 21.50 | 18.86 | 14.11 |

### MAPE por mes

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| nan | nan | 23.50 | 14.58 | 21.29 | 22.25 | nan | nan | nan | nan | nan | nan |

### 15 peores días

| fecha               |     real |   prediccion |     ape | es_feriado   | es_finde   | es_sandwich   | semana_18sept   | es_eleccion   |
|:--------------------|---------:|-------------:|--------:|:-------------|:-----------|:--------------|:----------------|:--------------|
| 2026-05-07 00:00:00 |  36.7775 |      62.9282 | 71.1052 | False        | False      | False         | False           | False         |
| 2026-03-07 00:00:00 |  29.8881 |      46.9017 | 56.9241 | False        | True       | False         | False           | False         |
| 2026-05-16 00:00:00 |  35.0373 |      54.9364 | 56.7939 | False        | True       | False         | False           | False         |
| 2026-05-21 00:00:00 | 116.041  |      53.4414 | 53.9463 | True         | False      | False         | False           | False         |
| 2026-05-27 00:00:00 | 139.632  |      66.7229 | 52.215  | False        | False      | False         | False           | False         |
| 2026-03-05 00:00:00 |  31.807  |      47.7972 | 50.2724 | False        | False      | False         | False           | False         |
| 2026-03-08 00:00:00 |  27.8038 |      39.9344 | 43.6291 | False        | True       | False         | False           | False         |
| 2026-03-12 00:00:00 |  30.373  |      43.1304 | 42.0022 | False        | False      | False         | False           | False         |
| 2026-03-02 00:00:00 |  34.6051 |      49.0192 | 41.6529 | False        | False      | False         | False           | False         |
| 2026-04-27 00:00:00 |  71.0996 |      41.7345 | 41.3014 | False        | False      | False         | False           | False         |
| 2026-03-09 00:00:00 |  31.1102 |      43.8917 | 41.0847 | False        | False      | False         | False           | False         |
| 2026-05-22 00:00:00 | 108.978  |      66.2637 | 39.1953 | False        | False      | True          | False           | False         |
| 2026-03-13 00:00:00 |  29.985  |      41.0747 | 36.984  | False        | False      | False         | False           | False         |
| 2026-06-02 00:00:00 | 115.221  |      73.9187 | 35.8459 | False        | False      | False         | False           | False         |
| 2026-03-29 00:00:00 |  30.7061 |      41.6537 | 35.6529 | False        | True       | False         | False           | False         |

## Experimentos de autoresearch en datos reales

| Modelo | MAPE % | MAE USD/MWh | RMSE USD/MWh | Sesgo USD/MWh | Folds | N |
|--------|-------:|------------:|-------------:|--------------:|------:|--:|
| lightgbm_baseline | 20.02 | 10.88 | 16.23 | -2.10 | 4 | 99 |
| exp005_ensamble_seeds | 19.20 | 11.10 | 16.69 | -4.96 | 4 | 99 |
| **exp006_cuantil_p60** | **18.77** | **10.59** | **15.99** | **-3.76** | 4 | 99 |

- **exp005_ensamble_seeds**: mediana de 3 LightGBM L1 (seeds 42/43/44) + 2 derivadas físicas (`der_sequia_x_gnl`, `der_spread_brent_carbon`). Baja MAPE 0.82 pp pero **empeora el sesgo** (-2.10 → -4.96): la mediana del ensemble centraliza aún más sobre un objetivo asimétrico. Conservado provisionalmente.
- **exp006_cuantil_p60** (base vigente): cambia el objetivo del ensemble de L1 (mediana condicional) a cuantil 0.60. **Mejora las cuatro métricas a la vez** y corrige el sesgo hacia cero (-4.96 → -3.76), confirmando el mecanismo: la mediana sub-proyecta una distribución con cola derecha; el cuantil 0.60 desplaza la predicción hacia arriba.

## Interpretación

El CMg real tiene una distribución asimétrica con cola derecha: spikes de escasez (CMg >100 USD/MWh en eventos de déficit hídrico o demanda invernal) que un objetivo de mediana subestima sistemáticamente. Por eso el objetivo cuantil-0.60 (exp006) gana: ataca directamente la sub-proyección. El MAPE de ~19 % en datos reales vs ~4.5 % en sintético refleja la dificultad real de estos spikes.

**Caveat estadístico**: la evaluación real tiene solo **99 puntos en 4 folds**. Diferencias de <1 pp en MAPE no son distinguibles del ruido sin un test Diebold-Mariano (que aún no tiene potencia con esta muestra). exp006 es más creíble que exp005 no por su MAPE marginalmente menor sino porque **las cuatro métricas se mueven de forma coherente con el mecanismo predicho**. Confirmar magnitudes requiere extender el histórico (backfill 2024-07..2025-02 + más historia futura).
