---
title: IA en sistemas eléctricos — nota de referencia para el forecasting de costos de operación del SEN
sources:
  - sources/regulation-coordinador-mercados-servicios/2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.md
last_synthesized: 2026-06-12
---

# IA en sistemas eléctricos — nota de referencia

> **Nota de procedencia.** El documento original "investigación sobre IA en sistemas eléctricos" que la fase 4 de la misión pedía copiar no existe en el repo (ver `wiki/decisiones.md`, D-003). Esta nota lo reconstruye combinando (a) la única fuente in-repo relacionada — la hoja de ruta I+D+i del CEN presentada al Ministerio de Ciencias (`sources/regulation-coordinador-mercados-servicios/2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.md`) — y (b) investigación web sobre la literatura de ML aplicado a sistemas de potencia (11 búsquedas, 2026-06-12). Su propósito es práctico: separar qué partes de esa literatura sirven para predecir el costo de operación diario del SEN (D+1, MAPE walk-forward) y cuáles no.

**Términos usados en esta nota** (complementa el glosario de `index.md`):

| Término | Significado |
|---|---|
| EPF | Electricity price forecasting, la literatura de pronóstico de precios spot |
| ERV / ERNC | Energía renovable variable (solar+eólica) / ERNC incluye además mini-hidro, biomasa, etc. |
| PO / PCP / PLP | Programa de Operación diario del CEN y sus modelos de optimización de corto/largo plazo |
| Walk-forward | Evaluación con reentrenamiento secuencial: solo datos pasados disponibles en cada predicción |
| PSI | Population Stability Index, métrica estándar de drift en la distribución de una feature |
| Orden de mérito | Despacho de centrales de menor a mayor costo variable hasta cubrir la demanda |

## 1. Panorama: IA aplicada a sistemas eléctricos

Los surveys del área (p. ej. [A Survey of Machine Learning Applications for Power System Analytics](https://ieeexplore.ieee.org/document/8783340/), [Advances in the Application of ML Techniques for Power System Analytics](https://doi.org/10.3390/en14164776)) agrupan las aplicaciones en cinco familias:

| Familia | Problema típico | Escala temporal | Datos típicos |
|---|---|---|---|
| **Forecasting** | Demanda, generación renovable, precios/costos | Horas–días | Series temporales + exógenas (clima, combustibles) |
| **Evaluación de seguridad** | Estabilidad transitoria/dinámica (TSA/DSA) | Milisegundos–segundos | PMU, simulaciones dinámicas |
| **Control** | Regulación de frecuencia/voltaje, despacho de BESS/DER (RL) | Tiempo real | Estado de la red + acciones |
| **Mantenimiento y fallas** | Detección de anomalías de equipos, protecciones | Continuo | Sensores, SCADA |
| **Planificación** | Expansión, escenarios probabilísticos | Años | Escenarios simulados |

Dos advertencias transversales de la literatura:

- Gran parte de los resultados publicados se valida sobre datos simulados o benchmarks pequeños; la transferencia a condiciones reales de operación es el cuello de botella, con inconsistencias de rigor metodológico y métricas que dificultan comparar resultados (ver el [scoping review de ML en protecciones](https://www.sciencedirect.com/science/article/pii/S0142061525008051)).
- El término "IA en sistemas eléctricos" mezcla problemas con objetivos, datos y escalas temporales incompatibles entre sí. Importar técnicas de una familia a otra sin revisar esos tres ejes es el error de diseño más común.

**Dónde se ubica el CEN.** La hoja de ruta I+D+i del Coordinador (PPT al Ministerio de Ciencias, 2026-04-21) cubre las cinco familias:

- "AI-assisted operations": analítica avanzada e IA como soporte a la operación en tiempo real (p. 13).
- "AI-enabled decision support": IA + computación de alto desempeño (HPC) para simulación, pronóstico y soporte a decisiones, dentro de la dimensión Digitalización (p. 16).
- Evaluación de seguridad dinámica y monitoreo (p. 13), planificación probabilística y por escenarios (p. 14), simulación de mercados (p. 15).

El driver declarado es el aumento de complejidad operacional por la transición energética: mayor variabilidad e incertidumbre renovable, menor inercia, nuevos recursos (BESS, DER, H2V, electromovilidad, data centers) y digitalización (pp. 7–8). **Nuestra misión cae exclusivamente en la primera familia (forecasting)**, alineada con la línea "AI-enabled decision support": pronóstico para soporte de decisiones, no control.

## 2. Qué aplica al forecasting de costos de operación del SEN

### 2.a Modelos híbridos físico-ML: usar la estructura del problema

El costo de operación diario no es una serie temporal arbitraria: es el resultado de un despacho de mínimo costo por orden de mérito, resuelto cada día por los modelos PCP/PLP del propio CEN. La literatura de electricity price forecasting (EPF) — el problema hermano más estudiado — es explícita en que los modelos que incorporan esa estructura superan a los puramente estadísticos:

- La taxonomía canónica es [Weron (2014), "Electricity price forecasting: A review of the state-of-the-art with a look into the future"](https://www.sciencedirect.com/science/article/pii/S0169207014001083), IJF 30(4): modelos fundamentales (simulan el despacho), de forma reducida, estadísticos y de ML/IA computacional, con la conclusión de que los híbridos que combinan información fundamental con corrección estadística son consistentemente competitivos.
- El **X-model** (Ziel & Steinert) modela el precio como la intersección de las curvas de oferta y demanda de la subasta. Trabajos recientes aprenden el **orden de mérito directamente de los datos** ([A data-driven merit order: Learning a fundamental electricity price model](https://arxiv.org/abs/2501.02963), Energy Economics 2025) o usan la curva de mérito como serie temporal de entrada ([Day-Ahead EPF Using Merit-Order Curves Time Series](https://arxiv.org/pdf/2512.17758)), superando tanto a fundamentales clásicos como a modelos data-driven de complejidad comparable.
- [Lago, Marcjasz, De Schutter & Weron (2021)](https://arxiv.org/abs/2008.08004), Applied Energy, establecen las buenas prácticas del campo: benchmark abierto ([epftoolbox](https://github.com/jeslago/epftoolbox)), ventanas de test largas (años, no semanas), comparación contra baselines fuertes, y el hallazgo incómodo de que un lineal bien regularizado (LEAR) es difícil de batir.
- En el flanco físico-ML más formal, la literatura de physics-informed ML para energía ([revisión de híbridos física+ML en PV](https://www.sciencedirect.com/science/article/pii/S0038092X24007394)) distingue tres vías de hibridación: restricciones físicas en la función de pérdida, arquitectura informada por física, y modelos grey-box. Para un objetivo agregado diario como el nuestro, la vía pragmática es la tercera: la física entra como **features y priors**, no como PINNs.

Traducción al SEN — cómo entra la estructura del despacho al modelo:

| Mecanismo físico | Feature / decisión de diseño | Por qué importa |
|---|---|---|
| El PCP/PO ya resuelve el despacho de D+1 | **Costo programado del PO como regresor ancla**, o directamente predecir el residuo real − programado | Es la mejor predicción física disponible; se publica antes de las 20:00 (compatible con regla anti-fuga D-006). El ML corrige su sesgo sistemático, no reinventa el despacho |
| Stack por orden de mérito | Precios de combustibles (GNL, carbón, diésel), disponibilidad térmica, ERV pronosticada (entra a costo ~0 y desplaza el stack) | El costo es no lineal en la demanda neta: depende de qué tecnología queda marginal. Esa no linealidad "a saltos" es terreno natural de los árboles |
| Valor del agua (acople hidrológico intertemporal) | Cotas de embalses, energía afluente, estacionalidad hidrológica | En un sistema hidrotérmico el costo de oportunidad del agua mueve el nivel de toda la serie; la hidro cayó a 24% de participación en 2025, −23% c/r 2024 (PPT CEN, p. 5). La literatura de scheduling hidrotérmico usa ML para inflows y funciones de producción ([revisión sistemática](https://www.mdpi.com/2673-2688/3/1/6), [ML en scheduling de largo plazo](https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/rpg2.12985)) |
| Restricciones de transmisión | Horas de desacople, spread de CMg entre barras de referencia, vertimiento ERV | La congestión encarece el despacho (vertimiento + térmica forzada aguas abajo); es uno de los desafíos operacionales que el propio CEN lista (p. 8) |

### 2.b Distribution drift: el riesgo dominante en el caso chileno

La mezcla de generación del SEN cambió más rápido que la de la mayoría de los sistemas sobre los que se publica. Según el PPT del CEN:

- Participación solar **~11% en 2018** (p. 6, "Chile ha ido avanzando aceleradamente en esta transición energética").
- **ERNC 44%** de participación en 2025, con **ERV (solar+eólica) en 38%, +20,6% c/r 2024**; hidráulica 24% (−23%), GNL+carbón 33% (p. 5).

Un modelo entrenado sobre la historia completa aprende un sistema que ya no existe: la relación demanda→costo de 2019 (carbón marginal casi siempre) no es la de 2025 (solar desplazando térmica a mediodía, BESS desplazando puntas, ducks curves y vertimientos).

La literatura de concept drift en forecasting energético ([Concept Drift Scenarios in Electrical Load Forecasting](https://www.researchgate.net/publication/368435298_Concept_Drift_Scenarios_in_Electrical_Load_Forecasting_with_Different_Generation_Modalities), [Forecasting online adaptation methods for energy domain](https://www.sciencedirect.com/science/article/abs/pii/S0952197623006838)) distingue dos tipos que aquí operan simultáneamente:

- **Shift temporal / de marginales:** cambia la distribución de los inputs (más días de alta penetración solar, más capacidad BESS) aunque la relación input→costo se mantenga.
- **Concept drift propiamente tal:** la misma demanda neta produce otro costo porque cambió el stack subyacente (retiro de carbón, entrada de BESS).

Implicancias operativas para la misión:

1. **Ventanas de entrenamiento:** no maximizar historia a ciegas. Comparar bajo walk-forward: ventana expansiva vs. rodante (~2–3 años) vs. ponderación temporal decreciente. Hipótesis a priori: la ventana rodante o la ponderación reciente ganan, porque el primer tercio de la muestra pertenece a otro régimen.
2. **Features que absorben el drift:** codificar la mezcla explícitamente (participación ERV del día, capacidad instalada solar/BESS acumulada, dummy post-retiro de centrales relevantes) convierte parte del drift en señal: el modelo interpola sobre la mezcla en lugar de memorizar una época.
3. **Reentrenamiento:** programado (mensual o trimestral) como mínimo. Los métodos de adaptación online reportan mejoras de ~8–34% bajo drift, pero con ~1500–2000 obs. el reentrenamiento batch frecuente es más simple, auditable y suficiente.
4. **Monitoreo de drift en producción:**
   - error walk-forward por sub-período (no solo el agregado: una degradación localizada en el último tramo es drift, no mala suerte);
   - sesgo del residuo vs. costo programado del PO (si el PO mismo deriva, el residuo lo delata primero);
   - distribución de features clave (PSI o test de población similar) entre ventana de entrenamiento y datos recientes.

### 2.c Arquitecturas razonables para ~1500–2000 observaciones diarias

Honestidad muestral primero: ~5 años de datos diarios son ~1.800 puntos, de los cuales el último tercio pertenece a un régimen distinto (sección 2.b). La muestra **efectiva** para el régimen vigente es aún menor. Eso descarta de partida las arquitecturas data-hungry como apuesta principal.

| Opción | Veredicto | Evidencia |
|---|---|---|
| **Gradient boosting (LightGBM/XGBoost)** | Candidato por defecto | Domina en tabular con muestras chicas y relaciones no suaves: ganó M5 ([solución ganadora M5 Uncertainty](https://www.sciencedirect.com/science/article/abs/pii/S0169207021002090)) y ASHRAE GEPIII ([lessons learned](https://arxiv.org/abs/2202.02898)); las fronteras irregulares del despacho (saltos de tecnología marginal) son su terreno ([por qué los árboles siguen ganando en tabular](https://forecastegy.com/posts/gradient-boosting-vs-deep-learning-tabular-data/)). Cuantiles nativos para salida probabilística |
| **Lineal regularizado (tipo LEAR)** | Baseline obligatorio | En EPF es notoriamente difícil de batir ([Lago et al. 2021](https://arxiv.org/abs/2008.08004)); con esta muestra su varianza baja es ventaja real. Si el boosting no le gana en walk-forward, la complejidad extra no se justifica |
| **TFT** | Solo experimento controlado | El [Temporal Fusion Transformer](https://www.sciencedirect.com/science/article/pii/S0169207021000637) aporta multi-horizonte, covariables e interpretabilidad, pero es un modelo grande: con <2.000 obs. exige dropout agresivo, capacidad mínima y early stopping, y aun así el riesgo de overfitting es alto |
| **N-HiTS** | Solo experimento controlado | Más liviano que los transformers (sus autores reportan ~20% mejor con 50× menos cómputo), pero su ventaja aparece en horizontes largos y muestras mayores |
| **Foundation models de forecasting / DL sin regularización** | No | Con esta muestra son varianza pura; la evidencia tabular general va en contra |

Reglas de juego:

- Ninguna arquitectura se adopta sin batir al boosting y al lineal bajo el protocolo canónico de `models/evaluacion.py::evaluar_walk_forward` (única fuente de verdad de MAPE/MAE/RMSE/sesgo en este repo).
- **Ensembles y residuos** son la mejora barata: promedio simple boosting+lineal, o boosting sobre el residuo del costo programado del PO (híbrido físico-ML de 2.a).
- Salida probabilística (cuantiles del boosting o conformal prediction) antes que arquitecturas más grandes: para decisiones de operación, un intervalo honesto vale más que un punto marginalmente mejor.

### 2.d Protocolo de evaluación: las trampas que la literatura ya pagó

La razón por la que EPF tiene un paper de "best practices" ([Lago et al. 2021](https://arxiv.org/abs/2008.08004)) es que durante una década el campo publicó mejoras irreproducibles: tests cortos, períodos elegidos a conveniencia, baselines débiles. Lecciones directamente aplicables a esta misión:

- **Ventana de test larga y contigua.** Un año mínimo de walk-forward; con drift activo (2.b), reportar además el error por sub-período. Esto ya es ley en el repo: `models/evaluacion.py::evaluar_walk_forward` es la única fuente de verdad de métricas.
- **Fuga de datos como riesgo número uno.** En EPF la fuga típica es usar exógenas conocidas solo ex-post. Aquí la regla anti-fuga de las 20:00 (D-006, metadato `disponible_a_las` por columna) ataca exactamente eso; los pronósticos de clima deben ser los emitidos el día D, no el clima observado de D+1.
- **MAPE con cuidado.** El MAPE explota cuando el denominador se acerca a cero y penaliza asimétricamente sobre/sub-predicción. Para un costo de operación diario del SEN (decenas de millones de USD al año, nunca cercano a cero) es utilizable, pero conviene reportar MAE y sesgo junto al MAPE — como ya hace el protocolo canónico — y vigilar los días atípicos (festivos, fallas mayores) que dominan el promedio.
- **Significancia, no solo ranking.** Dos modelos con MAPE 6,1% y 6,3% sobre 365 días probablemente no son distinguibles. La práctica estándar en EPF es el test de Diebold-Mariano sobre las pérdidas diarias antes de declarar un ganador.
- **Baselines ingenuos siempre en la tabla.** Persistencia (costo de hoy), persistencia estacional (mismo día semana anterior) y el costo programado del PO sin corrección. Si un modelo no bate al PO crudo, no aporta nada sobre lo que el CEN ya publica.

## 3. Qué NO aplica y por qué

Estas líneas dominan la literatura de "IA en sistemas eléctricos" y la hoja de ruta del CEN, pero **no** son herramientas para este problema. Queda escrito para no desviar el autoresearch:

- **Clasificación de estabilidad transitoria (TSA/DSA).** Problema de seguridad dinámica: clasificar en milisegundos–segundos si el sistema sobrevive a una contingencia, con datos PMU o simulaciones dinámicas; los modelos típicos son CNN/LSTM/GNN sobre trayectorias post-falta ([critical review de TSA data-driven](https://arxiv.org/abs/2111.00978)). Es la línea "Dynamic security assessment" del CEN (p. 13) — relevante para un sistema con menor inercia — pero su variable objetivo (estable/inestable), escala temporal y datos no tienen intersección con un costo diario agregado. Lo único exportable es una lección metodológica: su problema crónico de generalización ante cambios de topología y condición operativa es el mismo distribution shift de la sección 2.b.
- **Safe RL para control de red.** Regulación de frecuencia y voltaje, gestión de BESS/DER con garantías de seguridad durante exploración y despliegue ([review de Safe RL para control de sistemas de potencia](https://arxiv.org/abs/2407.00681); [critical review en smart grids](https://arxiv.org/abs/2409.16256)). RL presupone una **acción de control** y una política a optimizar bajo restricciones; nuestro problema es predicción pura: no controlamos nada, solo estimamos un escalar D+1. Adoptar RL aquí sería un error de planteamiento, no de implementación.
- **Detección de fallas y mantenimiento predictivo.** Anomalías de equipos, protecciones, gestión de perturbaciones: datos de sensores por activo, objetivo de clasificación/detección. Sin conexión con el costo agregado — salvo indirectamente, como causa de indisponibilidad térmica, que ya entra como feature de disponibilidad, no como problema de ML propio.
- **Computer vision para inspección de infraestructura.** Drones sobre líneas, termografía, vegetación. Otra familia de datos y otro objetivo; cero intersección con la misión.

Criterio general: la misión es **regresión escalar diaria con exógenas, horizonte D+1 y evaluación MAPE walk-forward**. Toda técnica cuya unidad de trabajo sea milisegundos, acciones de control o imágenes queda fuera por construcción.

## 4. Referencias clave y conexión con el autoresearch

| # | Referencia | Conexión con líneas del autoresearch |
|---|---|---|
| 1 | Weron (2014), *Electricity price forecasting: a review of the state-of-the-art*, IJF — [sciencedirect](https://www.sciencedirect.com/science/article/pii/S0169207014001083) | Taxonomía base para la línea de **selección de familia de modelos**; justifica partir por híbridos fundamental+estadístico en vez de series de tiempo puras |
| 2 | Lago, Marcjasz, De Schutter, Weron (2021), *Forecasting day-ahead electricity prices: best practices and an open-access benchmark*, Applied Energy — [arXiv:2008.08004](https://arxiv.org/abs/2008.08004), [epftoolbox](https://github.com/jeslago/epftoolbox) | Protocolo de evaluación (test largo, sin cherry-picking, baselines fuertes) que `models/evaluacion.py::evaluar_walk_forward` replica; baseline LEAR para la línea de **baselines obligatorios** |
| 3 | *A data-driven merit order: learning a fundamental electricity price model*, Energy Economics (2025) — [arXiv:2501.02963](https://arxiv.org/abs/2501.02963) | Plantilla para la línea **híbrido físico-ML**: aprender el stack de despacho del SEN (combustibles, ERV, hidro) en vez de simularlo |
| 4 | *Forecasting with gradient boosted trees: winning solution to the M5 Uncertainty competition*, IJF (2022) — [sciencedirect](https://www.sciencedirect.com/science/article/abs/pii/S0169207021002090); complemento: *ASHRAE GEPIII lessons learned* — [arXiv:2202.02898](https://arxiv.org/abs/2202.02898) | Evidencia empírica para la línea **modelo principal = gradient boosting** con muestra chica y features tabulares; recetas de tuning y validación temporal |
| 5 | *Forecasting online adaptation methods for energy domain*, Engineering Applications of AI (2023) — [sciencedirect](https://www.sciencedirect.com/science/article/abs/pii/S0952197623006838) | Línea de **drift**: diseño de ventanas, frecuencia de reentrenamiento y monitoreo; cuantifica cuánto se gana adaptando bajo drift (~8–34%) |
| 6 | *A critical review of data-driven transient stability assessment* — [arXiv:2111.00978](https://arxiv.org/abs/2111.00978) | Documenta por qué TSA queda **fuera de alcance**; su discusión de generalización ante cambios de condición operativa informa la línea de drift |
| 7 | *Safe Reinforcement Learning for Power System Control: A Review* — [arXiv:2407.00681](https://arxiv.org/abs/2407.00681) | Documenta por qué RL queda **fuera de alcance**: sin acción de control no hay política que aprender |

Y la fuente in-repo: hoja de ruta I+D+i del CEN (`sources/regulation-coordinador-mercados-servicios/2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.md`) — contexto institucional (mandato Art. 72-13 LGSE, p. 9), cifras de la transición (pp. 4–6), desafíos operacionales (pp. 7–8) y el encuadre "AI-enabled decision support" (p. 16) en el que esta misión se inscribe.

## 5. Resumen ejecutable

Lo que esta nota fundamenta, en una lista:

1. Plantear el problema como **regresión tabular diaria**, no como serie de tiempo pura ni como problema de control.
2. La física entra como features: **costo programado del PO, combustibles, hidrología/valor del agua, ERV pronosticada, congestión**. Considerar predecir el residuo real − programado.
3. Modelo principal: **gradient boosting con cuantiles**; baseline obligatorio: **lineal regularizado**; baselines ingenuos: persistencia y PO crudo.
4. TFT/N-HiTS solo como experimento controlado y con la carga de la prueba: deben batir al boosting bajo `evaluar_walk_forward`.
5. Asumir **drift estructural** (solar ~11% en 2018 → ERNC 44% en 2025, PPT CEN pp. 5–6): comparar ventanas de entrenamiento, codificar la mezcla como feature, reentrenar en calendario y monitorear error por sub-período + PSI.
6. **No** invertir en TSA, Safe RL, detección de fallas ni computer vision: otras familias de problema, sin intersección con el objetivo.
