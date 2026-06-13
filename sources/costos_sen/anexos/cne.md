# Fuentes de datos públicas — CNE Chile / Energía Abierta

**Objetivo:** insumos para modelo predictivo del costo total de operación diario del SEN.
**Fecha de investigación:** 2026-06-12. Método: solo WebSearch + búsqueda de código en GitHub (la red saliente del sandbox está bloqueada: curl/WebFetch devuelven 403).
**Estado de verificación global: pendiente — red del sandbox bloqueada.** Ningún endpoint fue invocado en vivo; todo lo aquí descrito proviene de resultados de búsqueda, documentación indexada y código de terceros en GitHub.

**Regla anti-fuga (recordatorio):** nada publicado después de las 20:00 hora Chile del día D sirve para predecir D+1. Las horas exactas de publicación NO pudieron confirmarse en vivo; se anotan las mejores evidencias encontradas y quedan como tarea de verificación.

---

## Tabla resumen de fuentes

| # | Fuente | URL / endpoint exacto | Acceso | Autenticación | Formato | Granularidad | Profundidad histórica | Frecuencia | Hora de publicación | Verificación |
|---|--------|----------------------|--------|---------------|---------|--------------|----------------------|------------|---------------------|--------------|
| 1 | API Energía Abierta (Junar) — catálogo de datasets | Portal: `http://datos.energiaabierta.cl/` (alias histórico `datos.energiaabierta.cne.cl`). API: `http://cne.cloudapi.junar.com/api/v2/datastreams/{GUID}/data.json/?auth_key=KEY` | REST GET | `auth_key` gratuita (registro en `/developers/`); claves públicas = solo lectura | JSON, CSV (`data.csv`), AJSON, XML, HTML | Según dataset (mensual, anual, semanal) | Variable por dataset (capacidad instalada: serie larga, visualización "desde 1898") | Según dataset | No documentada | pendiente — red del sandbox bloqueada |
| 2 | API Energía Desarrolladores (v2 de la API CNE) | Portal: `https://desarrolladores.energiaabierta.cl/`. Base: `https://api.desarrolladores.energiaabierta.cl/{tema}/v1/{recurso}.json?auth_key=KEY` | REST GET | `auth_key` gratuita (registro) | JSON / AJSON | Según servicio (horaria para costos marginales, mensual para capacidad/generación, diaria para indicadores) | No documentada en búsquedas | Según servicio | No documentada | pendiente — red del sandbox bloqueada |
| 3 | Capacidad instalada de generación por tecnología | Dataviews Junar: `datos.energiaabierta.cl/dataviews/245691/capacidad-instalada-de-generacion-sen/` (también 240266 total Chile, 245692 SEA, 245695 Los Lagos). API: `api.desarrolladores.energiaabierta.cl/capacidad-instalada/v1/convencional.json?auth_key=KEY` | REST GET o descarga web | `auth_key` para API; descarga web abierta | JSON/CSV/XLSX | Mensual, por sistema y tecnología | Serie histórica larga (visualización oficial menciona evolución desde 1898) | Mensual | No documentada (probable rezago de semanas tras cierre de mes) | pendiente — red del sandbox bloqueada |
| 4 | Costos marginales (reales, por barra) | Visualización: `energiaabierta.cl/visualizaciones/sic-sing-marginal-costs/`. API: `api.desarrolladores.energiaabierta.cl/costos-marginales/v1/barras.json?auth_key=KEY` | REST GET | `auth_key` | JSON | Horaria (USD/MWh) por barra: Atacama, Cardones, Charrúa, Crucero, Pan de Azúcar, Puerto Montt, Quillota, Tarapacá; promedio diario por barra | Visualización cubre ~3 años hacia atrás | Diaria/continua (dato origen: Coordinador) | No documentada; rezago desconocido | pendiente — red del sandbox bloqueada |
| 5 | Precios de paridad de combustibles (MEPCO) | Página: `https://www.cne.cl/tarificacion/hidrocarburos/mecanismo-de-estabilizacion-de-precios-de-los-combustibles-mepco/`. Informes PDF: `https://www.cne.cl/wp-content/uploads/{YYYY}/{MM}/{YYYY_MM_DD}_MEPCO.pdf`. Datos abiertos relacionados en `energiaabierta.cl/categorias-estadistica/hydrocarbons/` | Descarga web (PDF/Excel); posible dataset Junar | Sin autenticación (web) | PDF (informe) + tablas; Diario Oficial | Semanal | Desde 2014 (Ley 20.765) | Semanal: cálculo CNE, se conoce el miércoles, vigencia jueves. Desde marzo 2026 la paridad se calcula con ventana de 4 semanas | Miércoles (hora exacta no confirmada); vigencia jueves madrugada | pendiente — red del sandbox bloqueada |
| 6 | Informes de Precio de Nudo de Corto Plazo (PNCP) — incluye proyecciones de precios de combustibles (carbón, GNL, diésel) | `https://www.cne.cl/tarificacion/electrica/precio-nudo-corto-plazo/`. Ej.: ITP jun-2024 `https://www.cne.cl/wp-content/uploads/2024/06/ITP-PNCP-Jun-2024.pdf`; indexación mensual ej. `Rex-CNE-05-indexacion-PNCP-Ene-25.pdf`. Informe de proyecciones de precios de combustibles 2024–2044 (Res. Ex. CNE N°317, 19-jun-2024) | Descarga web | Ninguna | PDF + anexos (planillas) | Fijación semestral; indexación mensual (reajuste si variación acumulada >10%); CNE publica la variación de indexadores dentro de los primeros 5 días de cada mes | Informes disponibles online al menos desde ~2014; proyecciones de combustibles a 20 años | Semestral (ITP ~jun y ~dic; ITD ~ene y ~jul) + resoluciones mensuales de indexación | No documentada (primeros 5 días del mes para indexadores) | pendiente — red del sandbox bloqueada |
| 7 | Informes de Precio de Nudo Promedio (PNP) | `https://www.cne.cl/tarificacion/electrica/precio-nudo-promedio/` | Descarga web | Ninguna | PDF + anexos | Semestral (componente tarifario regulado) | Años de informes archivados | Semestral (ciclos con informes preliminar/definitivo; fijaciones asociadas a abril y octubre, con decretos posteriores en Diario Oficial) | No documentada | pendiente — red del sandbox bloqueada |
| 8 | Reporte Mensual del Sector Energético (CNE) | `https://www.cne.cl/wp-content/uploads/{YYYY}/{MM}/RMensual_v{YYYYMM}.pdf` (ej. `RMensual_v202601.pdf`); índice en `https://www.cne.cl/nuestros-servicios/reportes/informacion-y-estadisticas/` | Descarga web | Ninguna | PDF | Mensual: capacidad instalada, generación SEN, demanda máxima horaria, costos marginales, precio medio de mercado, hidrología | Varios años | Mensual, con rezago (reporte de mes M sale en M+1) | No documentada | pendiente — red del sandbox bloqueada |
| 9 | Reporte/boletín diario CNE (energía eléctrica) | Pista encontrada en código: `http://server.reportediario.cne.cl/server/Boletin/Lista/InfoElectricaCostoMarginal?fecha={fecha}`; además `http://reportes.cne.cl/reportes?c=` (reporte precios combustibles en estaciones) | HTTP GET (aparenta API interna sin documentación pública) | Aparentemente ninguna | JSON (presumible) | Diaria (costo marginal) | Desconocida | Diaria | No documentada — CRÍTICO verificar vs. regla 20:00 | pendiente — red del sandbox bloqueada |
| 10 | api.cne.cl — "API Combustibles" | `https://api.cne.cl/` (asociada a Bencina en Línea: `appbencinaenlinea.cne.cl`) | REST | Registro/token en el portal | JSON | Precios en estaciones de servicio (vehicular), por estación | — | Continua | — | pendiente — red del sandbox bloqueada |

---

## Detalle por punto de la misión

### 1. API REST de Energía Abierta (plataforma Junar)

- La documentación oficial vive en `http://datos.energiaabierta.cl/developers/`. La API es RESTful sobre la nube de Junar: host `cne.cloudapi.junar.com`.
- **Patrón de invocación (v2):** `http://cne.cloudapi.junar.com/api/v2/datastreams/{GUID}/data.json/?auth_key=TU_KEY` — el `{GUID}` es el identificador del dataview (ej. `VENTA-NACIO-POR-PRODU-Y`, `FACTO-DE-EMISI-PROME-MENSU`, `CAPAC-INSTA-...`). Sufijos alternativos: `data.csv`, `data.ajson`, `data.xml`, `data.html`.
- **Descubrimiento de recursos:** `GET /api/v2/resources.json?auth_key=KEY&query={texto}&limit=&offset=&order=top` (confirmado en la documentación de Junar en GitHub, repo `Junar/docs`).
- **Patrón legacy (v1):** `http://cne.cloudapi.junar.com/datastreams/invoke/{GUID}?auth_key=KEY&output=json_array`.
- **Autenticación:** requiere `auth_key`. Es **gratuita**: se obtiene registrándose en la ruta `/developers/` del portal. Hay claves públicas (solo lectura, suficiente para este proyecto) y privadas (se piden al equipo Junar).
- **Advertencia:** el listado comunitario `juanbrujo/listado-apis-publicas-en-chile` marca la API original de `datos.energiaabierta.cl` como **deprecada** y apunta a `api.cne.cl` como vigente (aunque api.cne.cl cubre solo combustibles vehiculares). Sin acceso de red no se pudo confirmar si Junar sigue respondiendo; el portal `datos.energiaabierta.cl` sigue indexado y activo en buscadores. **Verificar en vivo es la primera tarea cuando haya red.**
- La capa más moderna es **Energía Desarrolladores** (`desarrolladores.energiaabierta.cl`): API REST con métodos agrupados por tema, también con `auth_key`, respuestas JSON. Servicios confirmados en código de terceros: `capacidad-instalada/v1/convencional.json`, `generacion-bruta/v1/ernc.json`, `costos-marginales/v1/barras.json`, `indicadores-diarios/v1/utm.ajson`, `indicadores-diarios/v1/euro.ajson` (estos dos últimos útiles para indexadores cambiarios).

### 2. Precios de combustibles (CNE)

- **Paridad semanal (MEPCO, Ley 20.765):** la CNE calcula semanalmente precios de paridad de importación (cotizaciones Costa del Golfo de EE.UU., FOB + flete + seguros + internación) para gasolinas 93/97, diésel, GLP y kerosene (Ley 19.030). El informe se conoce el **miércoles** y los precios rigen desde el **jueves**. Publicación formal vía Diario Oficial; PDFs históricos en `cne.cl/wp-content/uploads/`. Desde marzo 2026, Hacienda amplió la ventana de cálculo de paridad a 4 semanas.
- **Limitación importante para el modelo:** la paridad MEPCO cubre combustibles vehiculares/domésticos (incluye diésel, el único compartido con generación térmica). Los precios de **carbón, GNL y fuel oil para generación** NO salen del MEPCO: aparecen en (a) los **informes PNCP** (proyecciones de carbón y GNL, ej. Tablas 6 y 7 del ITP; costos térmicos basados en lo informado por el Coordinador en los 2 meses previos) y (b) el **Informe de proyecciones de Precios de Combustibles 2024–2044** (Res. Ex. CNE N°317, 19-jun-2024). Los costos de combustibles efectivamente declarados día a día son dato del Coordinador (fuera del alcance CNE, documentar en ficha aparte).
- Estadísticas de hidrocarburos descargables en `energiaabierta.cl/categorias-estadistica/hydrocarbons/` (incluye metodología de paridad de derivados del petróleo).

### 3. Capacidad instalada por tecnología

- Datasets Junar identificados: **245691** (SEN), **240266** (total Chile), **245692** (SEA), **245695** (Los Lagos); búsqueda completa en `datos.energiaabierta.cl/search/?q=Capacidad+Instalada&resource=ds&category=Electricidad`.
- Granularidad mensual por sistema y tecnología; la visualización oficial (`energiaabierta.cl/visualizaciones/installed-capacity/`) muestra la serie de capacidad neta "desde 1898".
- Vía API Desarrolladores: `capacidad-instalada/v1/convencional.json` (presumiblemente existe el espejo ERNC; verificar catálogo).

### 4. Precios de nudo

- **PNCP:** fijación semestral con Informe Técnico Preliminar (~jun y ~dic) e Informe Técnico Definitivo (~ene y ~jul), aprobados por resolución exenta; PDFs en `cne.cl`. Entre fijaciones hay **indexación mensual**: reajuste cuando los indexadores acumulan variación >10%; la CNE publica la variación de indexadores en su web dentro de los **primeros 5 días de cada mes** (ej. Rex CNE N°05 ene-2025). Formato: PDF con anexos/planillas.
- **PNP (precio nudo promedio):** semestral, informe preliminar → observaciones de empresas → informe definitivo → decreto del Ministerio de Energía en Diario Oficial; fijaciones asociadas a abril y octubre.

### 5. ¿Publica la CNE series de costo de operación del SEN?

- **No se encontró una serie CNE de "costo total de operación diario del SEN".** Ese dato lo produce el Coordinador Eléctrico Nacional. Lo más cercano en la CNE:
  - Costos marginales horarios/diarios por barra (Energía Abierta, origen Coordinador).
  - **Reporte Mensual del Sector Energético** (PDF mensual): generación, demanda máxima, costos marginales, precio medio de mercado, hidrología.
  - Boletín diario `reportediario.cne.cl` (endpoint `InfoElectricaCostoMarginal?fecha=`, hallado en código del repo `JSCEG/NSIE`), sin documentación pública: candidato a fuente diaria, verificar existencia y hora de corte.
  - Anuario Estadístico de Energía (anual, certificado en blockchain).
- Conclusión: la **variable objetivo** del modelo deberá construirse con datos del Coordinador; la CNE aporta sobre todo **features** (combustibles, capacidad, precios regulados, indexadores).

### 6. Evidencia de viabilidad (código que consume la API)

| Repo | Qué hace |
|------|----------|
| `wri/global-power-plant-database` | Usó `cne.cloudapi.junar.com/api/v2/datastreams/{GUID}/data.csv/` como fuente oficial de plantas de Chile |
| `Dhauzur/admetricks` | Axios (JS) contra `api/v2/datastreams/VALOR-DOLAR-OBSER/data.json/` con `auth_key` |
| `aaizemberg/infovis` | jQuery contra `datastreams/invoke/{GUID}?auth_key=...&output=json_array` (patrón legacy) |
| `JSCEG/NSIE` | Consume `api.desarrolladores.energiaabierta.cl/indicadores-diarios/v1/...` y `reportediario.cne.cl` |
| `fuad-onate-evs/poc-data-engineering-data-architecture-2026` | Python; documenta endpoints `capacidad-instalada/v1/`, `generacion-bruta/v1/ernc`, `costos-marginales/v1/barras` |
| `FvD/junr` | Paquete R genérico para la API Junar (aplicable a CNE) |
| `Junar/docs` | Documentación oficial API v2 usando `cne.cloudapi.junar.com` como ejemplo |

La API fue real y ampliamente consumida; el riesgo es su **posible deprecación** (flag en `listado-apis-publicas-en-chile`). Mitigación: API Desarrolladores + descargas CSV del portal.

---

## Relevancia para el modelo de costo de operación diario del SEN

| Fuente | Relevancia | Por qué |
|--------|-----------|---------|
| Informes PNCP + proyecciones de combustibles (fila 6) | **Alta** | Única fuente CNE con precios proyectados de carbón, GNL y diésel para generación — driver directo del costo térmico de operación. Frecuencia semestral + indexadores mensuales: sin riesgo de fuga, pero feature de baja frecuencia (escalón). |
| Precios de paridad / MEPCO (fila 5) | **Alta** | Señal semanal del precio del diésel (combustible marginal frecuente en el SEN) con vínculo directo a mercados internacionales. Publicado miércoles → usable para D+1 si se captura antes de 20:00 (verificar hora exacta). No cubre carbón/GNL. |
| Costos marginales por barra (fila 4) | **Alta** | Proxy más cercano al costo de operación disponible vía API CNE; útil como feature autorregresiva. RIESGO: el rezago de carga en Energía Abierta es desconocido — si supera horas, consumir el dato directo del Coordinador y dejar esta fuente como respaldo. |
| Capacidad instalada mensual por tecnología (fila 3) | **Media** | Define la estructura de oferta (entrada de renovables baja el costo de operación estructuralmente). Cambia lento; feature mensual sin riesgo de fuga. |
| Reporte Mensual del Sector Energético (fila 8) | **Media** | Consolidado mensual (generación, demanda, hidrología, costos marginales) útil para validación cruzada y features mensuales; rezago de semanas lo hace inútil para señal diaria. |
| API Junar / Desarrolladores como mecanismo (filas 1–2) | **Media-Alta (instrumental)** | No es un dato sino el canal: gratuito, JSON/CSV, key de registro simple. Condiciona la ingesta de las filas 3–4. Verificar vigencia (flag de deprecación). |
| Boletín diario reportediario.cne.cl (fila 9) | **Media (potencial alta)** | Si existe y publica costo marginal diario temprano, sería la fuente diaria CNE más valiosa; hoy es solo una pista de código sin documentación. Verificar primero. |
| Precio Nudo Promedio (fila 7) | **Baja** | Tarifa regulada a clientes finales; refleja contratos y estabilizaciones, no el costo de operación físico del sistema. Solo útil como contexto. |
| api.cne.cl combustibles vehiculares (fila 10) | **Baja** | Precios en bombas de bencina: aguas abajo del MEPCO, redundante y con ruido de márgenes minoristas. Preferir paridad CNE directamente. |

### Próximos pasos de verificación (cuando haya red)
1. Probar `http://cne.cloudapi.junar.com/api/v2/resources.json?auth_key=...` con una key de registro (confirmar que Junar sigue vivo).
2. Listar catálogo de `api.desarrolladores.energiaabierta.cl` y confirmar granularidad/rezago de `costos-marginales/v1/barras.json`.
3. Confirmar existencia y hora de corte de `reportediario.cne.cl` (regla 20:00).
4. Medir hora real de publicación del informe semanal de paridad (miércoles, ¿AM o PM?).
