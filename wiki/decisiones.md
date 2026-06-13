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
- **Limitación de activación (verificada empíricamente):** GitHub solo registra workflows dispatchables vía API cuando el archivo existe en la **rama default** del repo; con los workflows solo en la rama del PR, `actions_list` devuelve 0 y el dispatch da 404. Esta sesión no puede pushear a la rama default (regla de la sesión). En su lugar se ejecutó un **dry-run local fiel** de cada step del workflow nocturno (guard de tz, deps, run_etl incremental, tabla maestra condicional, validadores, detección de fallos, commit simulado) — todos OK, y destapó y corrigió un bug real de sobreescritura de particiones mensuales en modo incremental. **El dry-run en GitHub queda a un clic:** al mergear el PR (o copiar los dos YAML a la rama default), disparar `backfill.yml` y `etl_nocturno.yml` vía workflow_dispatch.

## D-003 — Documento de referencia de IA en sistemas eléctricos: reconstruido, no copiado

- **Contexto:** la fase 4 pide "copiar el documento de investigación sobre IA en sistemas eléctricos a `wiki/referencias/`". Ese documento no existe en el repo ni se encontró en el Google Drive del usuario (búsquedas por contenido: "Safe RL", "físico-ML", "estabilidad transitoria"+"aprendizaje").
- **Decisión:** se usó como ancla in-repo la presentación `sources/regulation-coordinador-mercados-servicios/2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.pdf` (hoja de ruta I+D+i del CEN, menciona AI-assisted operations y AI-enabled decision support) y se redactó `wiki/referencias/ia-en-sistemas-electricos.md` con investigación web propia cubriendo los temas que la misión menciona (modelos híbridos físico-ML, distribution drift por cambio de mezcla de generación, clasificación de estabilidad transitoria, Safe RL).
- **Reversible:** si el documento original aparece, se ingiere a `sources/` y se actualiza la nota.

## D-004 — Variable objetivo (definición operativa)

- **Contexto:** "costo de operación" tiene al menos dos definiciones en las fuentes del CEN: (1) el costo total de operación **programado** que entrega la Programación Diaria (PCP/PO, resultado del modelo de optimización PLP/PCP del día D para D+1), y (2) el **costo real** de operación que se reconstruye ex-post (valorización de la generación real a costos variables auditados; aparece en informes mensuales/anuales del CEN, ej. USD 1.600 MM/año según `sources/.../2026-04-21-PPT-CEN-MINISTERIO-DE-CIENCIAS-Y-TECNOLOGIA.md` p.4).
- **Decisión (actualizada tras fase 1 + revisión adversarial):** la variable objetivo definitiva es el **costo total de operación diario real del SEN en USD**, construido como Σ(generación real horaria por central × costo variable declarado), validado contra los agregados mensuales del Informe Mensual SEN y el Reporte Anual Art. 72-15 — que es exactamente la comparación con que se audita el desempeño del CEN. El **costo programado** diario (función objetivo PLEXOS del ZIP del Programa de Operación, público, histórico ≥2017-2019) se captura como serie hermana: sirve de feature si su hora de publicación resulta anterior a las 20:00 (riesgo nº1, sin confirmar) y de benchmark del propio CEN.
- **Placeholder técnico transitorio:** mientras el parser del PO no esté validado contra muestras reales (imposible desde este sandbox sin red), la tabla maestra usa la **valorización de retiros a CMg** (Σₕ demanda_h × CMg_h en barras de referencia) como columna objetivo. La revisión adversarial (`sources/costos_sen/anexos/revision_adversarial.md`, C1) demostró que esta valorización NO aproxima el costo de operación (rentas inframarginales; colapso en horas de vertimiento solar; ignora encendidos/SSCC; sesgo no estacionario). Se acepta únicamente para validar la maquinaria de extremo a extremo; el reemplazo es prioridad 1 post-backfill y NO se reportará al CEN ningún número basado en el placeholder.
- **Justificación:** el KPI del CEN compara proyección vs. costo real; el objetivo debe ser el real. Detalle en `sources/costos_sen/catalogo_fuentes.md` §"La variable objetivo".

## D-005 — Moneda del objetivo: USD

- El CEN publica costos marginales y valorizaciones del mercado spot en USD/MWh (con conversión a CLP informativa). Los informes de costo de operación del CEN se expresan en USD. Se fija USD como moneda del objetivo; el tipo de cambio USD/CLP entra como feature, no como conversión del objetivo.

## D-006 — Regla anti-fuga de las 20:00, implementación

- Toda columna de la tabla maestra lleva metadato `disponible_a_las` (hora Chile del día D en que el dato queda públicamente disponible). El chequeo automático (`models/evaluacion.py::verificar_antifuga`) rechaza cualquier feature cuya disponibilidad declarada sea posterior a las 20:00 del día D o cuyo timestamp de dato sea posterior al día D. Los pronósticos de clima usan la **Historical Forecast API** de Open-Meteo (pronóstico emitido el día D para D+1), nunca el clima observado de D+1.

## D-007 — Stack de combustibles sin credenciales por defecto

- **Contexto:** las series spot oficiales (EIA) y FRED requieren API key (gratuita pero exige registro del usuario); bloquear el backfill en eso violaría las reglas de autonomía.
- **Decisión:** el extractor de combustibles funciona sin credenciales vía stooq.com (CSV directo) con yfinance de respaldo (futuros front-month Brent/HH/HO/API2) y mindicador.cl para USD/CLP. Si `EIA_API_KEY` existe en el entorno, agrega además las series spot oficiales (lag 7 por rezago de publicación). JKM y carbón spot no tienen fuente gratuita (Platts/Argus de pago): proxy documentado en el catálogo, anexo combustibles.
- **Trade-off aceptado:** futuros ≠ spot (base risk); para el MVP la señal direccional es suficiente y el settlement de 14:28-14:30 ET cumple la regla 20:00 con holgura.

## D-008 — Carpeta `sources/costos_sen`: nombre e inmutabilidad

- La misión especifica literalmente `sources/costos_sen/` como ubicación del catálogo; la convención del repo (CLAUDE.md) pide kebab-case y `tools/lint-kb.sh` lo marca. Se respeta el nombre de la misión.
- El catálogo además es un documento de trabajo (se corrigió tras la revisión adversarial), lo que dispara el check de inmutabilidad de `sources/`. Ambas advertencias del linter para esta carpeta quedan aceptadas y documentadas aquí; el resto de los errores de inmutabilidad del linter son falsos positivos de mtime por el clone fresco del contenedor (preexistentes a esta misión).

## D-009 — Datos sintéticos etiquetados como puente hasta el primer backfill real

- **Contexto:** sin red en el sandbox, las fases 3-4 no podían validarse de extremo a extremo con datos reales en esta sesión.
- **Decisión:** `tools/etl/generar_sintetico.py` (seed=42, física plausible: duck curve, años secos/húmedos, spike de combustibles 2022, quiebre 2024-07-15) puebla `data/raw_sintetico/` con los mismos esquemas del pipeline real; la tabla maestra y todos los reportes marcan `origen_datos=sintetico` de forma prominente. **Ningún MAPE sobre datos sintéticos es una métrica del problema real** y los reportes lo declaran. El workflow `backfill.yml` reemplaza esto con datos reales al correr con `COORDINADOR_USER_KEY` configurada; las fuentes sin credenciales (clima, combustibles, calendario) se llenan con datos reales desde la primera corrida.

## D-010 — Descarga keyless del CEN: descartada por prueba empírica en el runner

- **Contexto:** a pedido del usuario se evaluó si la data del Coordinador (CMg real, demanda) se puede bajar sin `user_key`, en vez de asumirlo. Se construyó `tools/etl/extractor_cen_web.py` (sonda) y se ejecutó **en vivo en GitHub Actions** (run #27454055998), donde sí hay red.
- **Resultado (evidencia dura, no inferencia):**
  - Los patrones `export.csv?from=&to=` de las páginas de gráficos → **404** (no existen; eran inferidos).
  - La API SIP v4 sin `user_key` → **403** (confirma que la key es obligatoria).
  - El subdominio `cmgreal.coordinador.cl` → 200 pero es la SPA (HTML), no datos.
  - El endpoint `https://www.coordinador.cl/wp-json/costo-marginal/v1/data` → **sí devuelve JSON de CMg por barra**, pero es un **snapshot demo congelado**: un solo día (2024-12-05), 192 registros, 555 días de antigüedad, sin parámetros de fecha. Inútil para backfill o D+1.
- **Decisión:** la descarga keyless **no es una fuente usable** para la variable objetivo. El camino robusto es la **API SIP v4 con `user_key`** gratuito (los 6 extractores `cen_*` ya lo soportan y se auto-omiten con gracia sin él, ver D-002/fix). La sonda `cen_web` queda como **monitor**: corregida para exigir cobertura multi-día y frescura (≤30 días) antes de declarar un endpoint "usable", de modo que detecte automáticamente si el CEN llegara a exponer un keyless real. No se construye extractor keyless de producción.
- **Recomendación al usuario:** registrar el `user_key` gratuito en portal.api.coordinador.cl (~2 min, no es login) y cargarlo como secret `COORDINADOR_USER_KEY` en GitHub (Settings → Secrets → Actions; nunca pegarlo en el chat).
