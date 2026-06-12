# program.md — Org de investigación: predicción del costo de operación diario del SEN

> Patrón adaptado de [karpathy/autoresearch](https://github.com/karpathy/autoresearch):
> un archivo que el agente modifica (`model.py`), un presupuesto fijo, una métrica, un log.
> Este archivo es de SOLO LECTURA para el agente experimentador.

## Misión

Minimizar el **MAPE walk-forward** de la predicción del costo total de operación
diario del SEN con horizonte D+1, medido exclusivamente por
`models/evaluacion.py::evaluar_walk_forward` sobre
`data/processed/tabla_maestra.parquet`.

Métricas secundarias (se registran, no se optimizan directamente): MAE, RMSE y
**sesgo** (error medio con signo — al CEN no le da lo mismo sub-proyectar que
sobre-proyectar).

## Arranque (sesiones nocturnas)

```bash
cd /ruta/al/repo/KB_demo
bash autoresearch/run_experimento.sh        # corre el experimento actual de model.py
```

Loop de trabajo del agente, por experimento:

1. Lee `log_experimentos.md` (qué se probó, qué quedó vigente, qué ideas hay en cola).
2. Formula UNA hipótesis falsable. Escríbela en `model.py` (`HIPOTESIS = "..."`)
   y dale un nombre nuevo (`NOMBRE_EXPERIMENTO`).
3. Modifica SOLO `model.py` para implementarla.
4. `bash autoresearch/run_experimento.sh` — entrena, evalúa y agrega la fila de
   resultados al log automáticamente.
5. Decide: **conservar** (el nuevo `model.py` queda como base) o **descartar**
   (revierte `model.py` con git al último estado conservado). Registra la
   decisión y una línea de aprendizaje en el log, columna `decision`.
6. Commit: `git commit -am "autoresearch: <NOMBRE_EXPERIMENTO> MAPE=X.XX <conservar|descartar>"`.
7. Repite mientras quede presupuesto de la sesión.

## Reglas (violarlas invalida el experimento)

- **Solo se modifica `autoresearch/model.py`.** Nada más. Ni datos, ni
  `models/evaluacion.py`, ni la tabla maestra, ni este archivo.
- **Evaluación únicamente vía `models/evaluacion.py`** con sus parámetros
  canónicos (refit 28 días, mínimo 365 días de train). Reportar números
  obtenidos de otra forma está prohibido.
- **Presupuesto: 20 minutos por experimento** (timeout duro en
  `run_experimento.sh`; cambiarlo = editar `PRESUPUESTO_MIN` en ese script y
  documentar por qué en el log). Si tu modelo no entrena+evalúa en 20 min con
  ~2.700 filas, la idea es demasiado cara: simplifica.
- **Anti-fuga**: solo features que `verificar_antifuga` acepte (declaradas
  conformes a la regla de las 20:00 en `metadatos_features.json`). Está
  prohibido usar `saltar_antifuga=True`, `costo_lag1`, `cmg_programado_d1`
  (mientras esté marcada no conforme) o construir features nuevas a partir de
  la columna objetivo sin lag >= 2.
- **Defensas automáticas del harness** (no intentes rodearlas; tras la
  auditoría de fase 3 están testeadas): `seleccionar_features` recibe la tabla
  SIN la columna objetivo y en copia; las columnas conformes deben volver
  intactas; toda feature nueva pasa un test de invarianza a truncamiento —
  shift negativo, rolling centrado o normalización con estadísticas de la
  muestra completa la rechazan. Si necesitas normalizar, usa estadísticas
  expansivas del pasado (`expanding()`), no globales.
- **Todo experimento queda en el log**, también (especialmente) los fallidos.
- Semillas fijas (`random_state=42`) — resultados reproducibles o no cuentan.

## Líneas de investigación sugeridas (en orden de retorno esperado)

1. **Variantes de gradient boosting**: tuning de LightGBM (num_leaves,
   learning_rate, feature_fraction), XGBoost, CatBoost; objetivo MAE vs MSE vs
   Tweedie; transformación log del objetivo.
2. **Features derivadas** (la vía más barata de mejorar): interacciones
   hidrología×combustibles (años secos amplifican el efecto del precio GNL),
   anomalías vs climatología (radiación relativa a la media del mes), spreads
   de combustibles, pendiente de la cota del Laja (7/30 días), demanda neta
   pronosticada (demanda − solar − eólica estimadas con el pronóstico de clima).
3. **Ensambles**: promedio/mediana de GBM con distinto seed u objetivo;
   stacking ligero con regresión lineal regularizada.
4. **Modelos híbridos físico-ML** (ver `wiki/referencias/ia-en-sistemas-electricos.md`):
   descomponer costo ≈ Σ(generación_térmica_esperada × costo_variable_proxy) +
   residual ML; o predecir CMg medio y demanda por separado y componer.
5. **Redes para series (TFT, N-HiTS)**: con ~2.700 observaciones diarias son
   candidatas débiles — exigir regularización fuerte y justificar contra el
   costo de presupuesto. Probar solo después de agotar 1-4.
6. **Cuantiles** (P10/P50/P90 con objetivo quantile) — útil para el KPI
   asimétrico del CEN; evaluar el P50 con el protocolo canónico.

## Advertencia de drift (de la referencia de IA en sistemas eléctricos)

La mezcla de generación chilena cambia rápido (ERNC 44 % en 2025 y subiendo;
duck curve creciente). Ventanas de entrenamiento muy largas pueden aprender
regímenes muertos (carbón pre-descarbonización). Experimentos legítimos:
ponderar muestras recientes, ventana móvil vs expansiva (cambiar la ventana
del MODELO es legítimo; cambiar la del PROTOCOLO de evaluación no).

## Registro

`autoresearch/log_experimentos.md` — append-only. El harness agrega la fila de
resultados; el agente agrega hipótesis (antes) y decisión (después).
