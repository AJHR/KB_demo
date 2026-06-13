# Fuentes de datos públicas — Coordinador Eléctrico Nacional (coordinador.cl)

> **Objetivo**: inventario de fuentes para un modelo predictivo del **costo total de operación diario del SEN, horizonte D+1**.
> **Fecha de investigación**: 2026-06-12. Método: WebSearch + búsqueda de código en GitHub (la red saliente del sandbox está bloqueada: curl/WebFetch devuelven 403, intento único de WebFetch sobre `cne.cl` falló con 403).
> **Estado de verificación de TODAS las filas**: `pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner`.
> **Regla anti-fuga**: para predecir el día D+1 solo puede usarse información publicada **antes de las 20:00 hora Chile del día D**. Cada fuente indica lo que se sabe (y lo que falta verificar) sobre su hora de publicación.

---

## 1. Costo de operación (VARIABLE OBJETIVO)

### 1.1 Definiciones distintas de "costo de operación" encontradas

| Concepto | Definición encontrada | Unidad | Frecuencia | Dónde se publica |
|---|---|---|---|---|
| **Costo de operación programado (del PO diario)** | Costo total de operación que arroja el proceso de Programación Diaria (modelo PCP/PLEXOS): combustible + costos de encendido/detención + costo de falla, según función objetivo del despacho. El Reporte Anual Art. 72-15 compara explícitamente "el costo de operación determinado en el proceso de programación diaria" contra "el costo real de operación". | USD (resultados PLEXOS) | Diaria (1 PO por día + reprogramaciones intradiarias PID) | ZIP del Programa de Operación (ver 1.2) |
| **Costo real de operación del SEN** | Costo efectivo de operar el sistema; el CEN lo reporta agregado: 2024 = 1.670 MMUSD vs 2023 = 2.745 MMUSD (−39,1%). | MM USD | Mensual (Informe Mensual) y anual (Reporte Art. 72-15) | Informe Mensual SEN; Reporte Anual de Desempeño Art. 72-15 |
| **Costo marginal en línea (CMg online)** | "Costo en que incurre el sistema para abastecer la energía durante un intervalo de quince minutos"; se determina a más tardar 15 min después del período de cálculo. | USD/MWh | 15 minutos, casi tiempo real | API SIP v4 + página de descarga (ver §3) |
| **CMg real / preliminar** | CMg definitivo del proceso de transferencias económicas (versión preliminar y luego real). Desde el 15-07-2024 rige el "Costo Marginal Real (nuevo)"; lo anterior queda en histórico. | USD/MWh | Horaria (publicación con rezago de días/semanas para la versión real) | Páginas de descarga + API |
| **CMg programado (PO/PID)** | CMg resultante de la programación diaria/intradiaria por barra. | USD/MWh | Horaria, para el día siguiente | Gráficos operación programada + API `cmg-programado-pid` |
| **Costos de SSCC** | Costos de Servicios Complementarios (no incluidos en el CMg; remuneración separada). | USD | Informe anual + procesos de subasta | Informe SSCC del CEN |

Documentos que sustentan las definiciones:
- Reporte Anual de Desempeño Art. 72-15 (año 2023): https://www.coordinador.cl/wp-content/uploads/2024/04/CEN-ReporteArt72-15ano2023v2.pdf — contiene tabla de costos de operación del SEN y **desviaciones entre costo programado y costo real de operación**.
- Reporte Anual de Desempeño Art. 72-15 (año 2024): https://www.coordinador.cl/wp-content/uploads/2025/04/CEN-Reporte-Art-72-15-ano-2024.pdf
- Informe SSCC 2022: https://www.coordinador.cl/wp-content/uploads/2022/04/2022.03.11-Informe_SSCC_2022.pdf
- Norma Técnica de Coordinación y Operación, capítulo "Programación de la Operación" (CNE, marzo 2025): https://www.cne.cl/wp-content/uploads/2025/04/2025.03-PROGRAMACION-DE-LA-OPERACION.pdf (403 desde sandbox; **aquí debe estar la hora regulatoria de publicación del Programa Diario — verificar**).

### 1.2 Programa de Operación diario (fuente primaria del costo programado)

| Campo | Detalle |
|---|---|
| Nombre | Programas de Operación (PO) — "Programa de Operación y Lista de Prioridades", "Base de datos y resultados Plexos", archivo "COSTOSVARIABLES" |
| URL | https://www.coordinador.cl/operacion/documentos/programas-de-operacion/ (histórico) · https://www.coordinador.cl/operacion/documentos/programas-de-operacion-2021/ (histórico desde 2021) · https://programa.coordinador.cl/ (plataforma nueva) |
| Método de acceso | Descarga de ZIP diarios desde la web (scraping de listado); la página limita descargas a rangos de **máx. 30 días** por consulta |
| Autenticación | Ninguna (público) |
| Formato | ZIP con resultados PLEXOS (CSV/Excel), bases de datos del modelo PCP, costos variables declarados |
| Granularidad | Horaria, por central/barra; el costo total de operación del día es la función objetivo del PLEXOS |
| Profundidad histórica | Listados históricos al menos desde 2021 en la página "desde 2021"; histórico anterior en la página principal (verificar inicio exacto, probablemente 2017-2019) |
| Frecuencia | Diaria + reprogramaciones (Programación Intradiaria PID: marcha blanca 30-12-2022, operación regular desde 15-07-2024: https://www.coordinador.cl/operacion/documentos/programacion-intradiaria/) |
| **Hora de publicación** | **NO CONFIRMADA por búsqueda** (crítico). Manual MP-12 del programa diario: https://gdc.coordinador.cl/anexos/manuales/16Manual_Programa_Diario.pdf (verificar). La página de PO lista fecha/hora de cada publicación → **verificar empíricamente desde el runner qué versión del PO de D+1 existe antes de las 20:00 del día D**. Riesgo de fuga: las versiones PID se publican varias veces al día siguiente. |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner |

### 1.3 Informes con costo de operación real (agregado)

| Campo | Detalle |
|---|---|
| Nombre | Informe Mensual del SEN (incluye "Costos de operación del SEN" en MM USD) |
| URL (patrón) | `https://www.coordinador.cl/wp-content/uploads/{AAAA}/{MM}/CEN_Informe_Mensual_SEN_{mes}{aa}.pdf` — ej.: https://www.coordinador.cl/wp-content/uploads/2026/02/CEN_Informe_Mensual_SEN_Feb26.pdf · https://www.coordinador.cl/wp-content/uploads/2025/12/CEN_Informe_Mensual_SEN_Dic25.pdf · https://www.coordinador.cl/wp-content/uploads/2024/12/CEN_Informe_Mensual_SEN_dic24.pdf · índice en https://www.coordinador.cl/reportes-y-estadisticas/ |
| Método | Descarga PDF (scraping del patrón de URL) |
| Autenticación | Ninguna |
| Formato | PDF (no machine-friendly) |
| Granularidad | Mensual (sirve para validar el agregado del target, no como target diario) |
| Frecuencia / hora | Mensual, días después del cierre del mes; hora irrelevante para D+1 |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner |

| Campo | Detalle |
|---|---|
| Nombre | Resumen Ejecutivo de Operación (diario) e Informe Diario de la Operación |
| URL | índice: https://www.coordinador.cl/operacion/documentos/novedades-cdc/ · ejemplo: https://www.coordinador.cl/wp-content/uploads/2025/06/Resumen-Ejecutivo-de-Operacion-07-06-2025.pdf (patrón `Resumen-Ejecutivo-de-Operacion-DD-MM-AAAA.pdf`) |
| Método | Descarga PDF diaria |
| Contenido | CMg real preliminar por barras (Quillota, Crucero), demanda, generación; **verificar si incluye costo total de operación del día** |
| Frecuencia / hora | Diario, ex-post (describe el día anterior); hora de publicación a verificar |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner |

---

## 2. API pública del Coordinador (SIP)

| Campo | Detalle |
|---|---|
| Nombre | Portal del Desarrollador / API SIP (Sistema de Información Pública), servicio `sipubv2` |
| URLs | Portal: https://portal.api.coordinador.cl/ · Login: https://portal.api.coordinador.cl/login · Planes: https://portal.api.coordinador.cl/planes · Lista de APIs: https://portal.api.coordinador.cl/lista · Doc SIP: https://portal.api.coordinador.cl/documentacion?service=sipubv2 · Doc operaciones: https://portal.api.coordinador.cl/documentacion?service=operaciones · Doc medidas: https://portal.api.coordinador.cl/documentacion?service=medidas · Doc planificación: https://portal.api.coordinador.cl/documentacion?service=planificacion · Solicitud de acceso: https://www.coordinador.cl/api-del-sistema-de-informacion-publica/ · PDF de uso: https://www.coordinador.cl/wp-content/uploads/2019/01/Uso-Api-SIP-Sistema-Informacion-Publica-v1.1.pdf · Manual API desarrolladores: https://medidas.coordinador.cl/public/DOCUMENTACION/INSTRUCTIVOS%20Y%20MANUALES/Manual%20Procedimientos%20Usuarios-Desarrolladores%20API%C2%B4s.pdf |
| Base URL de datos | `https://sipub.api.coordinador.cl` (gateway 3scale). Otros hosts: `operacion.api.coordinador.cl`, `medidas.api.coordinador.cl/medidas-v2` |
| Autenticación | **`user_key` como query param** (token por desarrollador, se obtiene registrándose en el portal). Registro gratuito; "Plan Consulta de Datos" — los planes marcados con asterisco requieren aprobación del CEN (hay que indicar la razón social del Coordinado, lo que sugiere que algunos planes son solo para coordinados; el plan básico de consulta parece abierto — verificar). |
| Formato | JSON, **paginado** (cada página enlaza prev/next; tamaño de página configurable) |
| Parámetro obligatorio | `fecha=YYYY-MM-DD` (v1/v2) o `startDate`/`endDate` (v4); cada llamada cubre típicamente 1 día |
| Profundidad histórica | El PDF oficial ejemplifica con `fecha=2018-01-01` → profundidad ≥ 2018 (verificar por endpoint) |
| Rate limit | Un cliente de terceros usa 60 req/hora como tasa segura (verificar límites del plan) |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner |

### Endpoints confirmados (extraídos de código de terceros en GitHub — evidencia de acceso real)

| Endpoint | Contenido | Versión | Fuente de evidencia |
|---|---|---|---|
| `https://sipub.api.coordinador.cl/costo-marginal-online/v4/findByDate?startDate=&endDate=&limit=&user_key=` | CMg en línea, 15 min | v4 | repos `bess-solutions/open-bess-edge`, `TM3-Corp/pudidi_cmg_prediction` |
| `https://sipub.api.coordinador.cl/costo-marginal-real/v4/findByDate` | CMg real | v4 | repo `FelipeCabelloE/CoordinadorAPI` |
| `https://sipub.api.coordinador.cl/cmg-programado-pid/v4/findByDate` | CMg programado (PID) — pronóstico oficial | v4 | repo `TM3-Corp/pudidi_cmg_prediction` |
| `https://sipub.api.coordinador.cl/sipub/api/v2/demanda_sistema_real/?user_key=&fecha=` | Demanda real del sistema, horaria | v2 | PDF oficial + repo `marcelomatus/gtopt` |
| `https://sipub.api.coordinador.cl/sipub/api/v1/recursos/costo_marginal_programado` | CMg programado | v1 | repo `alo-ngh/iea_scraper_limited` |
| `https://sipub.api.coordinador.cl/sipub/api/v1/recursos/demandasistemareal` | Demanda real | v1 | ídem |
| `https://sipub.api.coordinador.cl/sipub/api/v1/recursos/generacion_centrales_tecnologia_horario` | **Generación horaria por central/tecnología** | v1 | ídem |
| `https://sipub.api.coordinador.cl/api/v2/recursos` (base) | recursos v2 | v2 | repo `in-ventures/colbun_pge` |

> No se encontró ningún endpoint de **costo total de operación** en la API SIP: el costo total hay que extraerlo del ZIP del PO o construirlo (ver Hallazgos).

---

## 3. Costos marginales (reales y programados) — descargas web

| Fuente | URL | Método/Formato | Granularidad | Notas |
|---|---|---|---|---|
| Landing costos marginales | https://www.coordinador.cl/costos-marginales/ | Web | — | Punto de entrada con diccionario de datos |
| CMg en línea — descarga | https://www.coordinador.cl/mercados/graficos/descarga-datos-costos-marginales/costo-marginal-en-linea-descarga-datos-costo-marginal/ | Botón "Exportar" → CSV | 15 min | Casi tiempo real |
| CMg preliminar/real — descarga | https://www.coordinador.cl/mercados/graficos/descarga-datos-costos-marginales/costo-marginal-preliminar-real/ | CSV | Horaria | Archivos diarios, barras 220 kV |
| CMg real (nuevo, ≥15-07-2024) | https://www.coordinador.cl/mercados/graficos/costos-marginales/costo-marginal-real-nuevo/ · doc: https://www.coordinador.cl/mercados/documentos/transferencias-economicas/costo-marginal-real/ | CSV/web | Horaria | El histórico "antiguo" llega solo hasta 14-07-2024 |
| CMg programado | https://www.coordinador.cl/operacion/graficos/operacion-programada/costo-marginal-programado/ | CSV (export) | Horaria, D+1 | Resultado del PO — insumo clave D+1 |
| Desviación CMg programado vs real | https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-los-costos-marginales-programados/ | CSV/web | Horaria | Feature útil de error histórico del PO |
| Histórico CMg real SIC (legacy) | https://www.coordinador.cl/mercados/documentos/transferencias-economicas/costos-marginales-de-energia/historico-costo-marginal-real-sic/ (y subpáginas por año, ej. `costos-marginales-reales-2017/`) | Excel/CSV | Horaria | Pre-2017/legacy CDEC-SIC |
| Portales legacy | https://cmgreal.coordinador.cl/ · https://cmg-sic.coordinador.cl/ · http://cdec2.cdec-sing.cl/ | Web | — | Sistemas antiguos SIC/SING |
| CNE Energía Abierta — CMg horarios | http://datos.energiaabierta.cl/datasets/179804/costos-marginales-horarios/ · API: http://datos.energiaabierta.cl/developers/ (junar v2, `auth_key`) · https://api.cne.cl/ · `api.energiaabierta.cl` | API REST JSON/CSV/XML | Horaria/diaria | Fuente alternativa/espejo de CNE |

Estado de todas: pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner.

---

## 4. Demanda y generación (real y proyectada)

| Fuente | URL | Método/Formato | Granularidad | Hora de publicación |
|---|---|---|---|---|
| Operación Real (hub de gráficos) | https://www.coordinador.cl/operacion/graficos/operacion-real/ | Export CSV | Horaria | Continua/ex-post (verificar rezago) |
| Demanda real | https://www.coordinador.cl/operacion/graficos/demanda/demanda-real-demanda/ · https://www.coordinador.cl/operacion/graficos/operacion-real/demanda-real/ | Export CSV | Horaria, por barra | Verificar |
| Generación programada | https://www.coordinador.cl/operacion/graficos/operacion-programada/generacion-programada/ | Export CSV | Horaria D+1 | Junto al PO (verificar hora) |
| Programa diario de generación | https://www.coordinador.cl/operacion/graficos/operacion-programada/programa-diario-de-generacion/ | Export CSV | Horaria D+1 | ídem |
| Generación real por tecnología (API) | `sipub/api/v1/recursos/generacion_centrales_tecnologia_horario` | API JSON | Horaria por central/tecnología | Verificar rezago |
| Guía plataforma OpReal | https://www.coordinador.cl/wp-content/uploads/2025/07/E21-DEX-01-OpReal-Guia-Usuario-Coordinado_v1.0.pdf | PDF | — | Documentación |
| Pronóstico centralizado de demanda | https://www.coordinador.cl/mercados/documentos/pronostico-centralizado-de-generacion-y-demanda-2/pronostico-centralizado-de-demanda/ | Web/PDF/datos | Corto plazo | Insumo D+1 — verificar hora |
| Pronóstico centralizado de generación (eólica/solar) | https://www.coordinador.cl/mercados/documentos/pronostico-centralizado-de-generacion-y-demanda-2/pronostico-centralizado-de-generacion/ | Web/datos por año | Horaria | Insumo D+1 — verificar hora |
| Pronóstico de caudales | https://www.coordinador.cl/mercados/documentos/pronostico-centralizado-de-generacion-y-demanda-2/pronostico-de-caudales/ | Web | — | Hidrología |
| Reporte mensual pronóstico de demanda | https://www.coordinador.cl/wp-content/uploads/2025/03/Reporte_mensual_demanda_202412.pdf | PDF (Power BI) | Mensual | Diagnóstico de error del pronóstico |
| Cotas de embalses / hidrología | https://www.coordinador.cl/operacion/graficos/operacion-real/cotas-de-embalses-reales/ · https://www.coordinador.cl/operacion/graficos/operacion-real/informacion-condicion-hidrologica/ | Export CSV | Diaria | Feature hidro |

Estado: pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner.

---

## 5. Mantenimientos programados e indisponibilidades

| Fuente | URL | Método/Formato | Notas |
|---|---|---|---|
| Estados Operativos — Indisponibilidades | https://estadosoperativos.coordinador.cl/estados-operativos/indisponibilidades | Web app (posible API interna a inspeccionar) | Indisponibilidades de unidades — feature clave D+1 |
| Índices de Indisponibilidad | https://www.coordinador.cl/operacion/documentos/indices-de-indisponibilidad/ | Documentos | Índices normativos, ex-post |
| Programas de mantenimiento | https://www.coordinador.cl/operacion/documentos/ (sección "Mantenimientos") | Documentos/planillas | Programa mensual/anual de mantenimiento mayor |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner | | |

---

## 6. Transferencias económicas (balances mensuales)

| Fuente | URL | Método/Formato | Granularidad | Notas |
|---|---|---|---|---|
| Hub transferencias económicas | https://www.coordinador.cl/mercados/documentos/transferencias-economicas/ | Web/descargas | Mensual | Balances energía/potencia/SSCC |
| Informe de Valorización de TE | https://www.coordinador.cl/mercados/documentos/transferencias-economicas/informe-de-valorizacion-de-transferencias-economicas/ | Descarga; desde mayo 2025 migró a plataforma **Plabacom** | Mensual | Balance valorizado: ruta "01 Resultados > 01 Balance de Energía > 01 Balance Valorizado", archivo `Balance_MMAA_BD01` |
| Guía Plabacom | https://www.coordinador.cl/wp-content/uploads/2024/11/B43-DIN-GUA26-Plataforma-Balance-Comercial-rev01-2024-11-06.pdf | PDF | — | Puede requerir login para secciones de coordinados (verificar) |
| Gráficos TE | Energía: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/energia/ · Potencia: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/potencia/ · Transmisión: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/transmision/ | Export CSV | Mensual | Publicación con rezago ~1-2 meses → **no usable para D+1**, sí para validación |
| Estado | pendiente — red del sandbox bloqueada, verificar desde GitHub Actions runner | | | |

---

## 7. Programación diaria — hora de publicación (CRÍTICO, sin confirmar)

- Páginas: https://www.coordinador.cl/operacion/documentos/programas-de-operacion/ · https://programa.coordinador.cl/ · PID: https://www.coordinador.cl/operacion/documentos/programacion-intradiaria/
- Manual de procedimientos del Programa Diario (MP-12): https://gdc.coordinador.cl/anexos/manuales/16Manual_Programa_Diario.pdf
- Normativa que regula plazos: NT de Coordinación y Operación, capítulo Programación de la Operación (marzo 2025): https://www.cne.cl/wp-content/uploads/2025/04/2025.03-PROGRAMACION-DE-LA-OPERACION.pdf · NTSyCS: https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf
- **Ninguna búsqueda devolvió la hora exacta de publicación del PO del día siguiente.** La NTSyCS sí confirma que la información detallada de la operación real (CMg horarios por barra, producción, flujos) se publica "al segundo día hábil siguiente" de la operación real.
- **Acción requerida desde el runner**: (1) leer el capítulo de Programación de la Operación y el manual MP-12 para la hora regulatoria; (2) scrapear el listado de POs y registrar el timestamp real de publicación de cada PO durante ~2 semanas; (3) decidir si el PO de D+1 cumple el corte de las 20:00 — si la publicación es posterior, usar como insumo el PO vigente del día D y el CMg programado disponible antes del corte.
- Riesgo adicional de fuga: la **Programación Intradiaria** re-publica programas durante el propio día D+1; siempre usar la **primera** versión del PO, nunca la última disponible.

---

## 8. Ecosistema de terceros (evidencia de viabilidad de acceso programático)

| Repo | Qué hace | Evidencia clave |
|---|---|---|
| https://github.com/TM3-Corp/pudidi_cmg_prediction | Pipeline productivo de **predicción de CMg** (nodo Chiloé 220) | Usa `costo-marginal-online/v4/findByDate` y `cmg-programado-pid/v4/findByDate` con `SIP_API_KEY`; ETL documentado en `docs/ETL_WORKFLOW.md` (~2-5 min por corrida) |
| https://github.com/marcelomatus/gtopt | Cliente Python `cen2gtopt` + `cen_demanda` | Mapea hosts `sipub`, `operacion.api.coordinador.cl`, `medidas.api.coordinador.cl/medidas-v2`; usa `demanda_sistema_real` v2; tasa 60 req/h; fixtures capturados en vivo el 2026-05-06 |
| https://github.com/bess-solutions/open-bess-edge | Scraper BESS con **GitHub Actions** (`.github/workflows/data-pipeline.yml`) | Consume CMg online v4 + `api.energiaabierta.cl` desde runners de GitHub → confirma que la API responde desde GitHub Actions |
| https://github.com/FelipeCabelloE/CoordinadorAPI | Pipeline dlt (data load tool) | Base `https://sipub.api.coordinador.cl:443/costo-marginal-real/v4/` |
| https://github.com/alo-ngh/iea_scraper_limited | Scraper de la IEA para estadísticas chilenas | Endpoints v1: `costo_marginal_programado`, `demandasistemareal`, `generacion_centrales_tecnologia_horario` |
| https://github.com/in-ventures/colbun_pge | DAGs Airflow (Colbún/PGE) | Base `https://sipub.api.coordinador.cl/api/v2/recursos` |
| https://github.com/cjjouanne/Coordinador-Electrico | Notificaciones del **programa diario de operación** | Confirma monitoreo automatizable de la publicación del PO |
| https://github.com/victorcanejan/Costos-marginales | Dataset CMg horario + generación por tecnología | Dataset derivado de datos CEN |
| https://github.com/juanbrujo/listado-apis-publicas-en-chile | Catálogo de APIs públicas chilenas | Lista la API del CEN y la de Energía Abierta (CNE) |
| Tesis U. de Chile (web scraping CEN/CNE, código Python público) | https://repositorio.uchile.cl/bitstream/handle/2250/181581/Web-Scraping-visualizacion-y-analisis-bases-de-datos-de-la-operacion-del-sistema-electrico-chileno.pdf?sequence=1 | Metodología de scraping documentada |

No existe librería PyPI consolidada tipo "pySEN"; el patrón dominante es scripts propios contra la API SIP con `user_key`.

---

## Hallazgos clave para la variable objetivo

1. **No existe un endpoint API ni un CSV oficial con la serie "costo total de operación diario del SEN"**. El concepto existe y el propio CEN lo usa (el Reporte Art. 72-15 compara "costo de operación determinado en la programación diaria" vs "costo real de operación": https://www.coordinador.cl/wp-content/uploads/2024/04/CEN-ReporteArt72-15ano2023v2.pdf), pero las publicaciones agregadas son mensuales (Informe Mensual, MM USD) y anuales (2024: 1.670 MM USD; 2023: 2.745 MM USD).

2. **Recomendación de serie objetivo**: construir el target diario desde el **costo total de operación del Programa de Operación diario (resultados PLEXOS del ZIP del PO)** — https://www.coordinador.cl/operacion/documentos/programas-de-operacion/ y https://programa.coordinador.cl/. Razones: (a) es la única magnitud "costo total de operación" con frecuencia diaria publicada por el CEN; (b) es exactamente la definición que el CEN audita contra el costo real; (c) hay histórico descargable desde al menos 2021 (en tramos de 30 días). Como variante "real", construir un **proxy de costo real diario** = Σ(generación real horaria por central, vía `generacion_centrales_tecnologia_horario` u OpReal) × (costos variables declarados, archivo COSTOSVARIABLES del PO), validándolo contra el Informe Mensual (agregado mensual) y el Reporte Art. 72-15 (anual). Si el PO de D+1 se publica después de las 20:00, el modelo deberá predecir usando el PO del día D y los pronósticos de demanda/generación disponibles antes del corte.

3. **Acceso programático viable y probado**: API SIP (`https://sipub.api.coordinador.cl`, registro gratuito en https://portal.api.coordinador.cl/, auth por `user_key`) es consumida hoy desde GitHub Actions por terceros (repo `bess-solutions/open-bess-edge`), con profundidad histórica ≥2018 según la documentación oficial (https://www.coordinador.cl/wp-content/uploads/2019/01/Uso-Api-SIP-Sistema-Informacion-Publica-v1.1.pdf).

4. **Brechas a cerrar desde el runner** (todas marcadas "pendiente"): hora exacta de publicación del PO D+1 (manual MP-12 + NT Programación de la Operación + observación empírica del listado); contenido exacto del ZIP del PO (nombre del archivo con el costo total); rezago de OpReal y del CMg real; condiciones del "Plan Consulta de Datos" del portal API.
