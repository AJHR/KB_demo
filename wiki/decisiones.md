---
title: Registro de decisiones — Predicción de costos de operación SEN
sources:
  - sources/regulation-coordinador-operacion-sen/B43-DIN-04-Diccionario-de-Datos-Web-SIP.md
  - sources/costos_sen/catalogo_fuentes.md
last_synthesized: 2026-06-12
---

# Registro de decisiones — Modelo predictivo de costo de operación diario del SEN

Registro append-only de decisiones técnicas y de negocio tomadas durante la construcción del sistema.
Cada decisión: contexto, alternativas, decisión, justificación.

## D-001 — Rama de trabajo: `claude/epic-pasteur-wph10y` en vez de `feature/prediccion-costos-sen`

- **Contexto:** la misión pide trabajar en `feature/prediccion-costos-sen`, pero el entorno de ejecución remota (Claude Code on the web) restringe el push exclusivamente a la rama designada por la sesión (`claude/epic-pasteur-wph10y`); el proxy de git rechaza cualquier otra rama.
- **Decisión:** desarrollar todo en `claude/epic-pasteur-wph10y`. Si se desea el nombre canónico, basta renombrar la rama al mergear o crear `feature/prediccion-costos-sen` desde ella.
- **Impacto:** ninguno en el contenido; solo el nombre de la rama.

## D-002 — Red del sandbox bloqueada: el backfill corre en GitHub Actions, no en la sesión

- **Contexto:** la política de red de este entorno bloquea (HTTP 403 vía proxy) todo tráfico saliente salvo registries de paquetes (PyPI) y GitHub. Verificado empíricamente contra coordinador.cl, datos.energiaabierta.cl, archive-api.open-meteo.com y sipub.api.coordinador.cl, tanto con `curl` como con WebFetch. Sesiones anteriores del repo documentaron el mismo bloqueo (`log.md` 2026-05-14).
- **Alternativas:** (a) bloquearse y pedir cambio de política de red; (b) datos 100 % sintéticos; (c) ejecutar la descarga real en runners de GitHub Actions, que sí tienen salida a internet, y commitear los Parquet a la rama.
- **Decisión:** (c) como vía principal. Los extractores son código real y determinístico; el workflow `backfill.yml` (workflow_dispatch) los ejecuta en un runner con red y commitea los datos. La verificación "muestra descargada y parseable" de la fase 1 queda delegada a la primera corrida del workflow. Como respaldo para no bloquear las fases 3-4, se genera un dataset sintético **explícitamente etiquetado** (`data/processed/SINTETICO.md`) con la misma estructura de la tabla maestra, que se descarta automáticamente cuando llegan datos reales.
- **Riesgo aceptado:** hasta que el workflow corra con éxito, las URLs del catálogo están verificadas solo contra documentación oficial (diccionario SIP B43-DIN-04) y búsqueda web, no contra descargas en vivo.

## D-003 — Documento de referencia de IA en sistemas eléctricos: reconstruido, no copiado

- **Contexto:** la fase 4 pide "copiar el documento de investigación sobre IA en sistemas eléctricos a `wiki/referencias/`". Ese documento no existe en el repo ni se encontró en el Google Drive del usuario (búsquedas por contenido: "Safe RL", "físico-ML", "estabilidad transitoria"+"aprendizaje").
- **Decisión:** se usó como ancla in-repo la presentación `sources/regulation-coordinador-mercados-servicios/2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.pdf` (hoja de ruta I+D+i del CEN, menciona AI-assisted operations y AI-enabled decision support) y se redactó `wiki/referencias/ia-en-sistemas-electricos.md` con investigación web propia cubriendo los temas que la misión menciona (modelos híbridos físico-ML, distribution drift por cambio de mezcla de generación, clasificación de estabilidad transitoria, Safe RL).
- **Reversible:** si el documento original aparece, se ingiere a `sources/` y se actualiza la nota.

## D-004 — Variable objetivo (definición operativa)

- **Contexto:** "costo de operación" tiene al menos dos definiciones en las fuentes del CEN: (1) el costo total de operación **programado** que entrega la Programación Diaria (PCP/PO, resultado del modelo de optimización PLP/PCP del día D para D+1), y (2) el **costo real** de operación que se reconstruye ex-post (valorización de la generación real a costos variables auditados; aparece en informes mensuales/anuales del CEN, ej. USD 1.600 MM/año según `sources/.../2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.md` p.4).
- **Decisión (provisoria hasta validar acceso en la primera corrida del backfill):** la variable objetivo es el **costo total de operación diario real del SEN en USD**. Si la serie oficial diaria real no es descargable programáticamente con historia suficiente, se usa como proxy operativo la **valorización diaria de la generación real por los costos marginales horarios reales en barras de referencia** (∑ₕ demanda_h × CMg_h ponderado), documentando la diferencia. El costo de operación **programado** del PO se usa como *feature* (es la mejor predicción física disponible del propio CEN y se publica antes de las 20:00), no como objetivo.
- **Justificación:** el KPI del CEN compara proyección vs. costo real; el objetivo debe ser el real. Ver detalle en `sources/costos_sen/catalogo_fuentes.md` §1 cuando se complete la fase 1.

## D-005 — Moneda del objetivo: USD

- El CEN publica costos marginales y valorizaciones del mercado spot en USD/MWh (con conversión a CLP informativa). Los informes de costo de operación del CEN se expresan en USD. Se fija USD como moneda del objetivo; el tipo de cambio USD/CLP entra como feature, no como conversión del objetivo.

## D-006 — Regla anti-fuga de las 20:00, implementación

- Toda columna de la tabla maestra lleva metadato `disponible_a_las` (hora Chile del día D en que el dato queda públicamente disponible). El chequeo automático (`models/evaluacion.py::verificar_antifuga`) rechaza cualquier feature cuya disponibilidad declarada sea posterior a las 20:00 del día D o cuyo timestamp de dato sea posterior al día D. Los pronósticos de clima usan la **Historical Forecast API** de Open-Meteo (pronóstico emitido el día D para D+1), nunca el clima observado de D+1.
