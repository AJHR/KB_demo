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
| 2026-06-12 18:34Z | exp001_objetivo_l1 | El costo diario tiene spikes de escasez; el objetivo L2 del baseline persigue esos outliers. Cambiar a objetivo L1 (regression_l1) deberia bajar el MAPE mediano sin tocar nada mas. | 4.551 | 487,851 | 1,106,352 | -83,737 | 85 | 3.0 | sintetico | 426a85b | verificacion — re-corrida tras parches de auditoria (H1/H2/H3/H6/H7); reproduce 4.551 exacto |
| 2026-06-12 22:25Z | exp002_features_fisicas | El costo sale de un despacho por orden de merito: sequia encarece el GNL marginal (interaccion precip_hidro_90d x henry hub), la demanda neta de solar pronosticada define que tecnologia margina, y el spread brent-carbon mueve el stack. Tres derivadas fila-a-fila de columnas conformes (sin estado, invariantes a truncamiento) deberian bajar el MAPE de la base L1 sin riesgo de fuga. | 4.509 | 484,194 | 1,103,318 | -87,357 | 85 | 2.2 | sintetico | b427de9 | conservar — las 3 derivadas fisicas bajan MAPE 4.551→4.509 y MAE/RMSE; mejora marginal (probablemente no significativa con DM) pero costo cero y direccion fisica correcta; re-validar con datos reales |
| 2026-06-12 22:28Z | exp003_pesos_recientes | La mezcla de generacion deriva rapido (ERNC 44% y subiendo); la historia vieja pertenece a otro regimen. Ponderar las muestras de entrenamiento con decaimiento exponencial (half-life 365 dias) deberia bajar el MAPE al concentrar el ajuste en el regimen vigente sin descartar datos. | 4.542 | 490,401 | 1,105,358 | -86,846 | 85 | 2.0 | sintetico | 57038e2 | descartar — pesos half-life 365d empeoran MAPE 4.509→4.542 y MAE; el sintetico no tiene el drift de regimen que motiva la idea, re-probar con datos reales (alli el drift ERNC es real) o con half-life mas largo |
