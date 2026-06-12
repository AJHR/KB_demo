# Fase 1 — Evaluación: Noticias y Eventos del SEN como señal para modelo de costo de operación

**Fecha de investigación:** 2026-06-12
**Método:** Solo WebSearch (red saliente del sandbox bloqueada: curl/WebFetch → 403). Ninguna URL fue fetcheada directamente; toda verificación de formato queda **pendiente**.
**Pregunta:** ¿Aporta la familia "noticias/eventos" señal procesable determinísticamente (sin LLM en pipeline nocturno) para predicción D+1?

---

## 1. Tabla de fuentes

| # | Fuente | URL | Método de acceso | Formato | Rezago de publicación | Estado verificación |
|---|--------|-----|------------------|---------|----------------------|---------------------|
| 1 | Coordinador — Novedades (sala de prensa) | https://www.coordinador.cl/novedades/ | Scraping HTML; sitio es WordPress (paths `wp-content/uploads` confirmados), por lo que `https://www.coordinador.cl/feed/` (RSS por defecto de WP) **probablemente existe** | HTML / RSS probable | Horas–días tras el evento; texto libre, sin estructura | pendiente — red sandbox bloqueada |
| 2 | Coordinador — EAF (Estudios para Análisis de Fallas) | https://www.coordinador.cl/operacion/documentos/estudios-operacionales/estudios-de-analisis-de-falla/ (índice por año) | Scraping del índice HTML + descarga de PDFs (`/wp-content/uploads/AAAA/MM/EAF-NNN-AAAA.pdf`) | PDF (cientos de páginas en fallas mayores) | **Semanas**: ej. EAF 551/2023 — falla 30-12-2023, publicado 22-01-2024 (~3 semanas); EAF del apagón 25F-2025 entregado a la SEC al límite del plazo legal (~20 días) | pendiente — red sandbox bloqueada |
| 3 | Coordinador — IRF (Informe de Resumen de Falla) | https://www.coordinador.cl/operacion/documentos/informe-de-resumen-de-falla-irf/ | Scraping HTML / repositorio de documentos | Documentos por evento (Anexo Técnico N°3 NTSyCS, art. 10) | Coordinados reportan IF a 48 h y a 5 días del evento; publicación pública posterior | pendiente — red sandbox bloqueada |
| 4 | Coordinador — Desconexiones e Intervenciones / Informes de Falla / Limitaciones | https://www.coordinador.cl/operacion/graficos/desconexiones-e-intervenciones/ | Sección "gráficos": dashboards con datos mensuales (solicitudes de trabajo, limitaciones, informes de falla); posible API/JSON subyacente | HTML/JS; granularidad mensual aparente | Mensual (no D+1) | pendiente — red sandbox bloqueada |
| 5 | Coordinador — Índices de Indisponibilidad (forzada y programada) | https://www.coordinador.cl/operacion/documentos/indices-de-indisponibilidad/ | Descarga de documentos/planillas (cálculo según Título 5-12 NTSyCS) | Documentos/planillas | Consolidación periódica (mensual/anual), retrospectiva | pendiente — red sandbox bloqueada |
| 6 | Coordinador — Programa de Mantenimiento Preventivo Mayor + Programación mensual 12 meses | https://www.coordinador.cl/operacion/documentos/programa-mantenimiento-preventivo-mayor-2/ y https://www.coordinador.cl/operacion/documentos/estudios-de-la-programacion-de-la-operacion/programacion-mensual/ | Descarga directa de archivos (Excel/PDF) | Excel/PDF estructurado | **Prospectivo** (programado a futuro) — esto NO es "noticias", es dato operacional estructurado | pendiente — red sandbox bloqueada |
| 7 | Coordinador — Puesta en Servicio / Entrada en Operación / Infotécnica | https://www.coordinador.cl/desarrollo/documentos/gestion-de-proyectos/.../documentos-entrada-en-operacion/ ; https://infotecnica.coordinador.cl/instalaciones/unidades-generadoras (1.479 unidades registradas) ; https://www.coordinador.cl/mercados/documentos/potencia-de-suficiencia/estados-operativos-de-centrales/ | Infotécnica es un portal estructurado consultable; cartas/declaraciones juradas en cartas.coordinador.cl | Portal estructurado + documentos | El proceso de conexión tiene hitos formales (autorización PES ≤ 20 días); el registro se actualiza con cada interconexión | pendiente — red sandbox bloqueada |
| 8 | Coordinador — Reporte de Novedades del CDC (bitácora diaria) | Referenciado en la Guía Técnica de Elaboración de Informes de Falla (sitio del Coordinador); plataforma Neomante para extracción de eventos | A confirmar: si es descargable, sería la fuente "eventos" más cercana a D+1 | Bitácora / reporte extraíble | Diario | pendiente — red sandbox bloqueada |
| 9 | CNE — Reporte Mensual del Sector Energético + Energía Abierta | https://www.cne.cl/.../RMensual_vAAAAMM.pdf ; http://energiaabierta.cl/ — tiene página explícita de feeds: http://energiaabierta.cl/feed-rss-atom/ | PDF mensual + portal con API/RSS-Atom declarado | PDF / RSS-Atom / datos abiertos | Mensual (capacidad instalada, nuevas centrales) | pendiente — red sandbox bloqueada |
| 10 | Revista Electricidad (revistaei.cl) | https://www.revistaei.cl/ — sitio WordPress; `https://www.revistaei.cl/feed/` probable | RSS probable / scraping | HTML/RSS, texto libre | Horas–días; cobertura editorial, sin datos estructurados | pendiente — red sandbox bloqueada |
| 11 | Energía News (energianews.cl) | No apareció en resultados de búsqueda; posiblemente inactivo o de bajo perfil | — | — | — | pendiente — no localizado vía WebSearch |
| 12 | Reporte Minero (reporteminero.cl) | https://www.reporteminero.cl/noticias/noticias — foco minería, energía secundaria; RSS no confirmado | Scraping / RSS a confirmar | HTML texto libre | Horas–días | pendiente — red sandbox bloqueada |
| 13 | Ministerio de Energía — Noticias | https://energia.gob.cl/noticias | Scraping; sitio Drupal (los Drupal suelen exponer `/rss.xml`) | HTML/RSS probable | Días; comunicacional/político | pendiente — red sandbox bloqueada |

---

## 2. Hallazgos clave

### 2.1 EAF: confirmado que NO sirve para D+1, SÍ para etiquetado retrospectivo
- Rezago documentado: EAF 551/2023 (falla 30-12-2023) publicado 22-01-2024 → **~23 días**. El EAF del apagón total del 25-02-2025 (EAF 089/2025, ~399 páginas) se entregó a la SEC al límite del plazo legal (~20 días).
- Son PDFs largos, no estructurados → extraer features requeriría parsing pesado o LLM.
- **Uso recomendado:** el *índice* de EAFs (número, fecha de la falla, título con instalación afectada) sí es scrapeable determinísticamente y permite etiquetar días anómalos históricos para el análisis de errores del modelo (excluir/ponderar días con falla mayor en entrenamiento y evaluación). Para eso el rezago no importa.

### 2.2 La señal "útil" de las noticias ya existe estructurada en otras fuentes del Coordinador
- **Indisponibilidades/mantenimientos:** Programa de Mantenimiento Preventivo Mayor y programación mensual de 12 meses (descargables, prospectivos) + Índices de Indisponibilidad (Título 5-12 NTSyCS). Además, los **Programas de Operación diarios** (PO/PCP) ya incorporan las indisponibilidades vigentes — el modelo las recibe implícitamente si consume el programa diario.
- **Nuevas centrales:** Infotécnica (registro estructurado de 1.479 unidades generadoras), Estados Operativos de Centrales (plataforma consolidada desde nov-2021), documentos formales de Puesta en Servicio / Entrada en Operación, y el reporte mensual CNE. Un job mensual contra Infotécnica/CNE cubre esto sin leer ninguna noticia.
- **Fallas recientes:** IRF a 48 h / 5 días y el Reporte de Novedades del CDC (bitácora diaria) son más rápidos que cualquier comunicado de prensa y provienen de la fuente primaria.

### 2.3 Medios especializados: redundantes y no determinísticos
- revistaei.cl y similares publican *después* y *a partir de* la información del Coordinador/CNE. Texto libre → procesarlo de forma determinística (keywords/regex) da señal ruidosa; procesarlo bien exige LLM, lo que viola la restricción del pipeline nocturno.
- Único feed RSS confirmado explícitamente por búsqueda: **Energía Abierta (CNE)** tiene página dedicada de RSS/Atom. Los demás (coordinador.cl/feed, revistaei.cl/feed) son inferencia por WordPress, sin verificar.

### 2.4 Único candidato "evento" con potencial D+1
- El **Reporte de Novedades del CDC** (bitácora diaria de eventos del SEN) es la única pieza de esta familia con cadencia diaria y origen primario. Si resulta descargable en formato tabular (vía Neomante o sección de documentos), pertenecería conceptualmente a la familia "datos operacionales del Coordinador", no a "noticias". Verificarlo cuando haya red.

---

## 3. Veredicto

**DESCARTAR del MVP. Fase 2 solo en dos usos acotados y no-noticiosos:**

| Uso | Fase | Justificación |
|-----|------|---------------|
| Noticias/comunicados (Coordinador novedades, revistaei, medios) como feature del modelo | **Descartar** | Texto libre → no procesable determinísticamente sin LLM; redundante (la señal dura ya está en programas de operación, mantenimientos, Infotécnica); llega tarde respecto a las fuentes primarias. |
| Índice de EAF/IRF para **etiquetar días anómalos históricos** | **Fase 2** | Scraping determinístico del índice (fecha de falla + instalación). Mejora el análisis de errores y la limpieza del set de entrenamiento. Rezago de semanas irrelevante para uso retrospectivo. |
| Monitoreo de nuevas centrales vía **Infotécnica/CNE mensual** (no vía noticias) | **Fase 2** | Estructurado y determinístico, pero de baja frecuencia; el efecto de una central nueva entra solo al modelo vía los datos de generación/programas que ya consume el MVP. |
| RSS de novedades del Coordinador como **alerta para humanos** (no feature) | **Opcional** | Útil para que el operador del modelo sepa por qué un día salió raro; cero impacto en el pipeline. |

**Hipótesis del usuario: CONFIRMADA.** La señal predictiva útil para D+1 (indisponibilidades, mantenimientos, parque generador) ya está estructurada en fuentes operacionales del Coordinador que el modelo debe consumir de todos modos; las noticias son redundantes o llegan con semanas de rezago. La única excepción a explorar (fase 2, bajo costo) es el Reporte de Novedades del CDC, que en rigor es dato operacional, no noticia.

---

## 4. Pendientes cuando haya red
1. Verificar existencia de `https://www.coordinador.cl/feed/` y `https://www.revistaei.cl/feed/` (RSS WordPress por defecto).
2. Confirmar si el Reporte de Novedades del CDC es descargable en formato tabular y con qué cadencia/URL estable.
3. Inspeccionar la sección "Desconexiones e Intervenciones" en busca de API/JSON subyacente (granularidad real: ¿mensual o por evento?).
4. Confirmar formato del índice de EAF por año (HTML parseable: número, fecha falla, fecha publicación, título).

## Fuentes principales (de resultados de WebSearch, sin fetch directo)
- https://www.coordinador.cl/novedades/
- https://www.coordinador.cl/operacion/documentos/estudios-operacionales/estudios-de-analisis-de-falla/
- https://www.coordinador.cl/operacion/documentos/informe-de-resumen-de-falla-irf/
- https://www.coordinador.cl/operacion/graficos/desconexiones-e-intervenciones/
- https://www.coordinador.cl/operacion/documentos/indices-de-indisponibilidad/
- https://www.coordinador.cl/operacion/documentos/programa-mantenimiento-preventivo-mayor-2/
- https://infotecnica.coordinador.cl/instalaciones/unidades-generadoras
- https://www.coordinador.cl/mercados/documentos/potencia-de-suficiencia/estados-operativos-de-centrales/
- http://energiaabierta.cl/feed-rss-atom/
- https://www.cne.cl/wp-content/uploads/2025/10/RMensual_v202510.pdf
- https://www.revistaei.cl/
- https://www.reporteminero.cl/noticias/noticias
- https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf
