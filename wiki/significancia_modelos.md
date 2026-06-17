---
title: Significancia de modelos — CMg real diario D+1 (historia extendida)
sources:
  - data/processed/tabla_maestra.parquet
  - tools/comparar_modelos_dm.py
  - autoresearch/log_experimentos.md
  - models/evaluacion.py
last_synthesized: 2026-06-17
---

# Significancia de modelos sobre historia extendida (23 meses)

Tras extender el backfill del CMg real al régimen "nuevo" completo
(2024-07-15 → 2026-06-07, **687 días con objetivo, 12 folds, N=328**), ya hay
potencia para testear si las diferencias de MAPE entre modelos son reales o
ruido. Antes (4 folds, N=99) cualquier diferencia <1pp era indistinguible.

## Por qué importó conseguir más historia

Con la ventana corta (4 folds, eval 2026-03→06) la conclusión era:
**exp006 (cuantil 0.60) es el mejor, MAPE 18.77 %**. Esa conclusión **no
sobrevivió** a la historia completa:

| Métrica | Ventana corta (4 folds, eval mar–jun 2026) | Año completo (12 folds, eval jul 2025–jun 2026) |
|---|---|---|
| MAPE del mejor modelo | ~19 % | ~25 % |
| Sesgo del modelo | **negativo** (−4.96): sub-proyecta | **positivo** (+2.08): sobre-proyecta |
| Mejor objetivo | cuantil 0.60 (empuja ↑) | L1 / mediana |

El sesgo **cambió de signo** entre ventanas. La ventana corta caía en un
período de precios bajos donde el modelo sub-proyectaba; el tilt al cuantil
0.60 (exp006) lo corregía. Pero sobre el año completo —que incluye el invierno
2025 con spikes— el modelo **sobre**-proyecta, y ese mismo tilt empuja en la
dirección equivocada. **El 18.77 % era un artefacto de una ventana fácil.**

## Resultados sobre el año completo (12 folds, N=328)

| Modelo | MAPE % | Sesgo | Implementable |
|--------|-------:|------:|:--|
| persistencia_lag1 (usa CMg de ayer) | 22.95 | +0.20 | ❌ fuga operacional (CMg de T−1 no publicado a las 20:00) |
| **exp007_l1 (ensemble L1 + 2 derivadas)** | **24.75** | **+0.20** | ✅ **base vigente** |
| exp006_q60 (ensemble cuantil 0.60) | 26.71 | +2.08 | ✅ |
| estacional_dow (promedio mismo día, 4 sem) | 27.93 | +0.89 | ✅ naive |
| persistencia_lag3 | 31.31 | +0.08 | ✅ |
| lightgbm_baseline (L2, single) | 33.60 | +3.34 | ✅ |

## Test de significancia (Wilcoxon signed-rank sobre APE diario)

`tools/comparar_modelos_dm.py` — comparación pareada día a día (estilo
Diebold-Mariano), p<0.05 = diferencia significativa:

| Comparación | ΔMAPE (a−b) | p-valor | Veredicto |
|---|--:|--:|---|
| exp007_l1 vs lightgbm_baseline_L2 | −8.85 pp | <0.0001 | **exp007 mejor, SIGNIFICATIVO** |
| exp007_l1 vs exp006_q60 | −1.96 pp | 0.0012 | **exp007 mejor, SIGNIFICATIVO** |
| estacional_dow vs lightgbm_baseline_L2 | −5.67 pp | 0.0038 | **el naive le gana al baseline L2, SIGNIFICATIVO** |
| exp007_l1 vs estacional_dow | −3.18 pp | 0.092 | no significativo (gana en media, no día-a-día) |
| exp007_l1 vs persistencia_lag1 (fuga) | +1.80 pp | 0.20 | empate estadístico con la cota con fuga |

## Conclusiones

1. **El baseline LightGBM L2 está mal calibrado**: pierde de forma
   significativa hasta contra un promedio estacional naive (27.93 vs 33.60,
   p=0.0038). Persigue los spikes de invierno y sobre-proyecta (+3.34).
2. **El trabajo de autoresearch sí agregó valor real**: el ensemble L1 +
   derivadas físicas (exp007) le gana al baseline L2 por 8.85 pp con
   p<0.0001 — mejora robusta, no ruido.
3. **exp007 (L1) es la nueva base vigente**, no exp006. Revertir el objetivo
   al de mediana bajó el sesgo a ~0 y mejoró el MAPE de forma significativa
   (p=0.0012). La decisión de exp006 fue revertida por la evidencia.
4. **Techo realista**: exp007 (24.75 %) está estadísticamente **empatado** con
   la persistencia-lag1 que tiene fuga operacional (22.95 %, p=0.20). O sea, el
   mejor modelo implementable ya iguala a una cota que "hace trampa" usando el
   CMg de ayer. Ganar más requiere señal que hoy no está en la tabla.
5. **Honestidad sobre el naive estacional**: exp007 gana 3.2 pp en media pero
   la diferencia NO es significativa día-a-día (p=0.092). Podemos afirmar que
   el ML es *tan bueno o mejor* que el estacional, no que lo supera de forma
   concluyente. Cerrar ese gap es el objetivo de los próximos experimentos.

## Próximos pasos (con esta evidencia)

- El margen de mejora está en los **días de spike** (peores APE), no en los
  días normales. Features de escasez (cota de embalses con pendiente, déficit
  hídrico acumulado) y/o el híbrido físico-ML son la vía de mayor retorno.
- Re-correr exp003 (pesos por recencia) ahora que el drift de régimen es real
  y hay 12 folds para medirlo.
- Cota dura: sin nueva señal, ~24-25 % MAPE parece el techo de esta tabla.
