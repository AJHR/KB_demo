# Log de experimentos — autoresearch costo de operación SEN D+1

Append-only. El harness agrega la fila de métricas; el agente completa la
columna `decision` (conservar/descartar + 1 línea de aprendizaje). Reglas en
[`program.md`](./program.md). Métrica canónica: MAPE walk-forward
(`models/evaluacion.py`).

La columna `origen` distingue corridas sobre datos reales vs sintéticos
(`data/raw_sintetico/`) — **los MAPE no son comparables entre orígenes**.

| fecha (UTC) | experimento | hipótesis | MAPE % | MAE | RMSE | sesgo | folds | min | origen | git | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
