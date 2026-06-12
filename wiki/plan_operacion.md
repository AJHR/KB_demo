---
title: Plan de operacionalización — predicción diaria de costos SEN
sources:
  - sources/costos_sen/catalogo_fuentes.md
  - models/evaluacion.py
  - .github/workflows/etl_nocturno.yml
last_synthesized: 2026-06-12
---

# Plan de operacionalización (fase 5 — diseño, no implementado)

Cómo pasa el sistema de "baselines evaluados" a "predicción diaria en producción
contra el KPI del CEN". Todo lo descrito aquí se implementa después de que el
backfill real esté validado y el objetivo definitivo (costo PLEXOS del PO +
costo real reconstruido) reemplace al placeholder.

## 1. Predicción diaria conectada al pipeline nocturno

El workflow `etl_nocturno.yml` (02:00 Chile) gana un paso final `predecir`:

1. Tras el incremento de fuentes y la reconstrucción de la tabla maestra,
   ejecuta `python3 models/predecir.py --fecha manana` (módulo a crear), que:
   carga el modelo vigente (artefacto versionado `models/artefactos/modelo_vigente.pkl`
   con hash del experimento de autoresearch que lo produjo), arma la fila de
   features del día D+1 con el **mismo código** de `construir_tabla_maestra.py`
   (cero divergencia train/serve) y emite la predicción.
2. Publica: (a) commit de `data/processed/predicciones.parquet` (histórico
   append-only: fecha_emision, fecha_objetivo, prediccion_usd, modelo, hash);
   (b) artefacto del run con un resumen md; (c) opcional fase 2: issue/Slack
   con la predicción y su intervalo (cuantiles P10/P90 si el modelo vigente
   los produce).
3. Orden de ejecución: ETL → tabla maestra → validadores → predicción. Si los
   validadores marcan rojo (fuente crítica incompleta), la predicción se emite
   igual con flag `degradada=true` y la lista de fuentes faltantes (el CEN
   necesita SIEMPRE un número; un número degradado y marcado vale más que
   ninguno).

Nota de timing: el corte anti-fuga es 20:00 del día D, pero el cron corre
02:00 de D+1. Es coherente: todo insumo usado estaba disponible antes de las
20:00 de D (los extractores no piden nada "del futuro"); correr a las 02:00
solo da margen operativo. Una mejora fase 2 es un segundo cron 21:00 de D para
emitir la predicción 5 horas antes.

## 2. Monitoreo de error acumulado contra el KPI del CEN

- `predicciones.parquet` se cruza cada noche con el costo real ya conocido
  (rezago 2-3 días) → tabla `error_diario` (APE, error con signo).
- Métricas rodantes: MAPE 7/30/90 días, sesgo 30 días, conteo de días con
  APE > 15 %.
- Reporte mensual automático en `wiki/desempeno_operacion.md` (regenerado por
  el workflow, mismo patrón que `calidad_datos.md`): MAPE del mes vs MAPE de
  validación histórica, desglose por condición de calendario, los 5 peores
  días con contexto (¿falla mayor? ¿hidrología extrema? — cruzar ex-post con
  los EAF del CEN, ver catálogo de fuentes §noticias).
- El KPI del CEN se audita comparando programado vs real (Reporte Art. 72-15);
  nuestro reporte replica esa misma comparación para la predicción del modelo,
  más la del propio PO del CEN como benchmark competitivo: **si no le ganamos
  al PO del Coordinador, el modelo no aporta**.

## 3. Política de reentrenamiento

- **Regla base (calendario):** reentrenar el primer lunes de cada mes con la
  ventana expansiva completa (mismo constructor del experimento vigente,
  protocolo de `evaluacion.py`), porque el walk-forward canónico ya simula
  exactamente ese régimen (refit cada 28 días).
- **Regla reactiva (por desempeño):** si MAPE-30d > 1,25 × MAPE de validación
  histórica del modelo vigente durante 5 días consecutivos → reentrenamiento
  inmediato + issue automático para revisión humana.
- **Regla estructural:** ante eventos que cambian el sistema (retiro de una
  central a carbón, entrada de interconexión/BESS grande, cambio normativo del
  despacho como la entrada del PID), se etiqueta la fecha en una tabla de
  `regimenes.md` y se evalúa si la ventana de entrenamiento debe truncarse
  (experimento de autoresearch, no decisión manual ad-hoc).
- Todo reentrenamiento pasa por `evaluacion.py` y queda registrado en
  `autoresearch/log_experimentos.md` (el reentrenamiento es un experimento
  más, con la misma vara).

## 4. Monitoreo de distribution drift

Motivado por la advertencia de `wiki/referencias/ia-en-sistemas-electricos.md`
(la mezcla de generación chilena cambia rápido: ERNC 44 % y subiendo).

- **Drift del error (síntoma):** alerta si MAPE-30d > MAPE_validación × (1+X),
  con **X = 25 %** inicial (calibrar tras 3 meses de operación). Acción:
  reentrenamiento reactivo (§3) + revisión del log.
- **Drift de las features (causa):** test mensual de PSI (Population Stability
  Index) de cada feature contra su distribución en la ventana de entrenamiento;
  PSI > 0,25 en una feature de importancia top-10 → issue automático.
- **Drift del objetivo:** media/varianza móviles 90d del costo diario
  comparadas contra el histórico de entrenamiento (z-score > 3 → alerta).
- Los tres monitores corren en el mismo workflow nocturno (determinístico,
  sin LLMs) y escriben a `wiki/desempeno_operacion.md`.

## 5. Riesgos operativos conocidos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Fuente CEN cambia formato/endpoint (histórico: quiebre 2024-07-15) | Parsers defensivos + validadores de esquema + issue tras 2 fallos consecutivos (ya implementado) |
| Hora de publicación del PO posterior a las 20:00 | El modelo vigente no puede depender del PO de D+1 (bloqueado por anti-fuga hasta verificación); plan B documentado: PO del día D + pronósticos centralizados |
| user_key del CEN revocada/expirada | El estado `omitida_sin_credencial` es visible en `estado_etl.json`; alerta si persiste > 3 días |
| Feriado decretado con < 48 h de aviso | Actualización manual de la tabla de eventos + reentrenamiento no requerido (el modelo ya conoce el efecto "feriado") |
| Predicción no emitida (fallo total del pipeline) | El último modelo y la última tabla viven en git: re-ejecución manual vía workflow_dispatch en < 10 min |
