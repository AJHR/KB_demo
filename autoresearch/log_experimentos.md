# Log de experimentos — autoresearch costo de operación SEN D+1

Append-only. El harness agrega la fila de métricas; el agente completa la
columna `decision` (conservar/descartar + 1 línea de aprendizaje). Reglas en
[`program.md`](./program.md). Métrica canónica: MAPE walk-forward
(`models/evaluacion.py`).

La columna `origen` distingue corridas sobre datos reales vs sintéticos
(`data/raw_sintetico/`) — **los MAPE no son comparables entre orígenes**.

| fecha (UTC) | experimento | hipótesis | MAPE % | MAE | RMSE | sesgo | folds | min | origen | git | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 2026-06-12 14:18Z | exp000_baseline_lgbm | Punto de partida: LightGBM baseline de fase 3 sin cambios. Establece la marca a batir. | 6.847 | 717,547 | 1,225,060 | +265,772 | 85 | 3.4 | sintetico | 2ccedf3 | referencia — marca base del loop (= lightgbm_baseline fase 3) |
| 2026-06-12 18:11Z | exp001_objetivo_l1 | El costo diario tiene spikes de escasez; el objetivo L2 del baseline persigue esos outliers. Cambiar a objetivo L1 (regression_l1) deberia bajar el MAPE mediano sin tocar nada mas. | 4.551 | 487,851 | 1,106,352 | -83,737 | 85 | 3.3 | sintetico | 2ccedf3 | conservar — L1 baja MAPE 6.85→4.55 y reduce el sesgo absoluto 3x; queda como base vigente |
