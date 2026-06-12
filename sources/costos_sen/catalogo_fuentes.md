# Catálogo de fuentes — Modelo predictivo de costo de operación diario del SEN

> **Misión**: predecir el costo total de operación diario del SEN con horizonte D+1.
> **Fecha de investigación**: 2026-06-12. Método: 7 agentes de investigación en paralelo (WebSearch + búsqueda de código en GitHub + validación local donde fue posible). Detalle completo por familia en [`anexos/`](./anexos/).
> **Estado de verificación**: la red saliente de este entorno está bloqueada (403 del proxy, ver `wiki/decisiones.md` D-002), por lo que "verificada" significa aquí *documentación oficial + evidencia de código de terceros que la consume*. La verificación en vivo (descargar muestra y parsearla) la ejecuta el workflow `backfill.yml` en runners de GitHub Actions, que sí tienen red. Única excepción: **calendario**, verificada localmente ejecutando código (es offline).

## Tabla maestra de fuentes

| # | Fuente | Endpoint / URL | Acceso | Auth | Formato | Granularidad | Historia | Actualización | Hora publicación (regla 20:00) | Verificación |
|---|--------|----------------|--------|------|---------|--------------|----------|---------------|-------------------------------|--------------|
| 1 | **CEN — Programa de Operación diario (costo programado, objetivo-insumo)** | coordinador.cl/operacion/documentos/programas-de-operacion/ · programa.coordinador.cl | Descarga ZIP (tramos ≤30 días) | No | ZIP (PLEXOS CSV/XLSX, COSTOSVARIABLES) | Diaria (horaria por central) | ≥2021 | Diaria + PID intradiaria | **SIN CONFIRMAR** — riesgo nº1 del proyecto; verificar empíricamente y vía manual MP-12 / NT Programación de la Operación. Usar siempre la *primera* versión del PO, nunca re-publicaciones PID | pendiente (runner) |
| 2 | **CEN — CMg real / preliminar** | sipub.api.coordinador.cl `costo-marginal-real/v4/findByDate` · descarga CSV web | API JSON / CSV | `user_key` (gratis) / No | JSON/CSV | Horaria por barra | ≥2018 (API) | Diaria ex-post | Real definitivo con rezago de días; **preliminar** disponible D+2 hábil. Para D+1 solo sirven con lag ≥2 días | pendiente (runner) |
| 3 | **CEN — CMg online** | `costo-marginal-online/v4/findByDate` | API JSON | `user_key` | JSON | 15 min | ≥2020 aprox | Casi tiempo real (≤15 min) | ✅ usable hasta las 20:00 del día D | pendiente (runner) |
| 4 | **CEN — CMg programado (PO/PID)** | `cmg-programado-pid/v4/findByDate` · CSV web | API JSON / CSV | `user_key` / No | JSON/CSV | Horaria, D+1 | ≥2019 aprox | Diaria | Hereda la hora del PO (ver #1) | pendiente (runner) |
| 5 | **CEN — Demanda real** | `sipub/api/v2/demanda_sistema_real` · CSV web | API JSON / CSV | `user_key` / No | JSON/TSV | Horaria | ≥2018 | Continua ex-post | Día D disponible parcial hasta 20:00; completo D+1 → usar con lag 1 día | pendiente (runner) |
| 6 | **CEN — Generación real por central/tecnología** | `sipub/api/v1/recursos/generacion_centrales_tecnologia_horario` · CSV web (OpReal) | API JSON / TSV | `user_key` / No | JSON/TSV | Horaria por central | ≥2018 | Diaria ex-post | Rezago a verificar (OpReal D+1, medidas validadas D+2 hábil) | pendiente (runner) |
| 7 | **CEN — Pronóstico centralizado de demanda y de generación ERV** | coordinador.cl/mercados/documentos/pronostico-centralizado-de-generacion-y-demanda-2/ | Descarga | No | Datos/PDF | Horaria, corto plazo | A verificar | Diaria | A verificar — candidato a mejor feature D+1 | pendiente (runner) |
| 8 | **CEN — Cotas/afluentes de embalses reales** | API SIP `recursos/cotas_embalses` · CSV web cotas-de-embalses-reales | API JSON / TSV | `user_key` / No | JSON/TSV | Diaria/horaria por embalse | ≥2018 aprox | Diaria | A verificar; cota del día D-1 siempre disponible → lag 1 día | pendiente (runner) |
| 9 | **CEN — Energía afluente y prob. de excedencia** | informacion-condicion-hidrologica (XLSX) | Descarga | No | XLSX | Semanal/mensual | Varios años | Mensual | Sin riesgo (rezago natural) | pendiente (runner) |
| 10 | **CEN — Indisponibilidades / mantenimientos** | estadosoperativos.coordinador.cl · programas de mantenimiento | Web app / planillas | A verificar | Web/XLSX | Diaria / mensual | A verificar | Diaria | A verificar API interna | pendiente (runner) |
| 11 | **CEN — Informe Mensual SEN / Reporte Art. 72-15** (validación del target) | patrón `CEN_Informe_Mensual_SEN_{mes}{aa}.pdf` | Descarga PDF | No | PDF | Mensual/anual | ≥2017 | Mensual | Irrelevante (validación, no feature) | pendiente (runner) |
| 12 | **CNE Energía Abierta — API REST** | `api.desarrolladores.energiaabierta.cl` (capa nueva) · `cne.cloudapi.junar.com/api/v2` (legacy, posible deprecación) | API REST | `auth_key` (gratis) | JSON/CSV/XML | Variada | Larga (capacidad instalada mensual ≥2000s) | Mensual/diaria | Sin riesgo para series mensuales | pendiente (runner) |
| 13 | **Combustibles — futuros (sin key)** | stooq.com CSV (`cb.f`, `ng.f`, `ho.f`) · yfinance (`BZ=F`, `NG=F`, `HO=F`, `MTF=F`, `TTF=F`) | CSV directo / lib | No | CSV/JSON | Diaria (cierre) | >10 años | Diaria | Cierre ~17:00 ET = 18-19h Chile → ✅ usable mismo día; carbón `MTF=F` con huecos por iliquidez | pendiente (runner) |
| 14 | **Combustibles — spot oficiales EIA** (opcional) | api.eia.gov v2: `RNGWHHD`, `RBRTE`, diésel USGC | API JSON | `EIA_API_KEY` (gratis) | JSON | Diaria | Brent ≥1987, HH ≥1997 | Semanal (rezago) | Rezago días→semana: usar con lag ≥7 días | pendiente (runner) |
| 15 | **JKM / carbón API2 spot** | No existe fuente gratuita programática (Platts/Argus de pago) | — | — | — | — | — | — | Proxy: TTF=F + Henry Hub/Brent (indexadores reales de contratos GNL chilenos) | documentado |
| 16 | **USD/CLP** | mindicador.cl/api/dolar/{año} (MVP) · API BDE BCCh `F073.TCO.PRE.Z.D` (producción) | API JSON | No / credenciales gratis | JSON | Diaria | >20 años | Diaria AM | Dólar observado del día D se publica en la mañana de D → ✅ | pendiente (runner) |
| 17 | **Clima observado — Open-Meteo Archive (ERA5)** | archive-api.open-meteo.com/v1/archive | API JSON | No | JSON | Horaria/diaria, 11 puntos | Desde 1940 | Diaria (rezago 2-5 días) | Usar con lag ≥5 días | pendiente (runner) |
| 18 | **Clima pronóstico D+1 sin fuga — Open-Meteo Previous Runs** | previous-runs-api.open-meteo.com (`*_previous_day2`) | API JSON | No | JSON | Horaria | Desde ~2024-01 (GFS temp 2021) | Continua | `previous_day2` garantiza emisión pre-20:00 para todo D+1 (day1 filtra info post-corte en horas tardías). Corrida segura pre-cierre: **12z UTC** | pendiente (runner) |
| 19 | **Clima pronóstico operacional — Open-Meteo Forecast** | api.open-meteo.com/v1/forecast | API JSON | No | JSON | Horaria, 16 días | past_days ≤92 | 4 corridas/día | Pipeline nocturno (corre 02:00 D+1 con corrida 12z/18z de D) | pendiente (runner) |
| 20 | **Hidrología DGA** | snia.mop.gob.cl/dgasat (HIDROlínea, ~650 estaciones) | Scraping (sin API documentada) | No | Web | Horaria | Décadas (límites por consulta) | Horaria | ✅ intradiaria | fase 2 (no MVP) |
| 21 | **Calendario** | librería Python `holidays` v0.98 + tabla manual elecciones/irrenunciables + tz IANA para DST | Offline | No | — | Diaria | Ilimitada | Con releases de la lib | ✅ trivial (conocido con años de anticipación) | **verificada localmente** ✅ |
| 22 | **Noticias/eventos** | EAF (rezago ~3 semanas), medios, Reporte Novedades CDC | — | — | — | — | — | — | **DESCARTADA del MVP** (señal redundante o tardía; EAF sirve ex-post para etiquetar días anómalos). Ver anexo | descartada |

## La variable objetivo: hallazgo central

**No existe serie oficial publicada del costo total de operación diario.** Lo que existe:

1. **Costo de operación programado diario** — función objetivo del modelo de despacho (PLEXOS/PCP) dentro del ZIP del Programa de Operación. Diario, público, histórico ≥2021. Es la definición que el CEN audita en su Reporte Anual Art. 72-15 contra el costo real.
2. **Costo real de operación** — solo agregados mensuales (Informe Mensual SEN, MM USD) y anuales (Reporte Art. 72-15; 2024: 1.670 MM USD, 2023: 2.745 MM USD).
3. **Construcción del costo real diario** (recomendada): Σ (generación real horaria por central × costo variable declarado de esa central), validada contra los agregados mensuales/anuales. Insumos: fuente #6 + archivo COSTOSVARIABLES del PO (#1).

Decisión y justificación completa en `wiki/decisiones.md` D-004. Estrategia de implementación en dos etapas: el backfill captura #1 y #6 + costos variables; mientras el parser del ZIP del PO no esté validado contra muestras reales, la tabla maestra usa como objetivo provisional la valorización Σₕ(demanda_h × CMg_h barra de referencia), reemplazable por columna sin tocar el resto del pipeline.

## Riesgos principales detectados

1. **Hora de publicación del PO de D+1 sin confirmar** (fuente #1) — si se publica después de las 20:00, el CMg programado de D+1 no es feature válida y se reemplaza por el PO del día D + pronósticos centralizados (#7). Plan de verificación empírica en `anexos/coordinador.md` §7.
2. **Quiebre de serie del CMg real el 2024-07-15** ("CMg real nuevo") — requiere armonización en el ETL y flag de régimen.
3. **API SIP requiere `user_key`** (registro gratuito) — secret `COORDINADOR_USER_KEY` pendiente de que el usuario lo registre; mientras tanto los extractores usan los endpoints de descarga web públicos.
4. **Carbón API2/JKM sin fuente spot gratuita** — proxy de futuros con huecos; documentado en anexo combustibles.
5. **Previous Runs API solo desde 2024** — el backfill de pronósticos climáticos pre-2024 usa clima observado con corrección documentada (techo de desempeño optimista; se reporta por separado en la evaluación).
6. **Feriados decretados con poca anticipación y librería `holidays` sin elecciones** — mitigado con tabla manual versionada.

## Anexos por familia (detalle completo)

| Anexo | Contenido |
|-------|-----------|
| [`anexos/coordinador.md`](./anexos/coordinador.md) | CEN: definiciones del costo de operación, PO, API SIP, CMg, demanda/generación, indisponibilidades, transferencias, ecosistema de terceros (8+ repos que consumen la API hoy) |
| [`anexos/cne.md`](./anexos/cne.md) | CNE Energía Abierta: API Junar legacy + capa desarrolladores, MEPCO, PNCP, capacidad instalada |
| [`anexos/combustibles.md`](./anexos/combustibles.md) | EIA/FRED/yfinance/stooq, JKM/API2, BCCh, rezagos por serie |
| [`anexos/hidrologia.md`](./anexos/hidrologia.md) | Embalses CEN, DGA HIDROlínea, energía afluente, CR2/CAMELS-CL, ranking por valor predictivo |
| [`anexos/clima.md`](./anexos/clima.md) | Open-Meteo (5 APIs), análisis anti-fuga de corridas de modelos, 11 puntos geográficos justificados |
| [`anexos/calendario.md`](./anexos/calendario.md) | Validación ejecutada de `holidays`, gaps (elecciones, irrenunciables), features propuestas |
| [`anexos/noticias.md`](./anexos/noticias.md) | Veredicto de descarte con evidencia (EAF ~3 semanas de rezago, redundancia con fuentes estructuradas) |
