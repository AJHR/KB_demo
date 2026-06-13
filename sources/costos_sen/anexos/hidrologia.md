# Fuentes públicas de hidrología chilena para predicción del costo de operación del SEN

> Fase 1 — Investigación documental vía WebSearch (18 búsquedas, 2026-06-12).
> Red saliente del sandbox bloqueada: ninguna URL fue verificada por fetch directo.
> Estado de verificación de TODAS las fuentes: **pendiente — red sandbox bloqueada**.
> Regla anti-fuga: para predecir el costo del día D solo sirve lo publicado **antes de las 20:00 hora Chile del día D**.

---

## 1. Catálogo de fuentes

### 1.1 Coordinador Eléctrico Nacional (CEN)

| Campo | Cotas de Embalses Reales | Cotas de Embalses Programadas | Energía Afluente / Condición Hidrológica | API Pública SIP (sipubv2) | Sistema de Pronóstico de Caudales (SPC) | Pronóstico de Deshielo CEN | Informe Mensual SEN |
|---|---|---|---|---|---|---|---|
| **URL exacta** | https://www.coordinador.cl/operacion/graficos/operacion-real/cotas-de-embalses-reales/ | https://www.coordinador.cl/operacion/graficos/operacion-programada/cotas-de-embalses-programadas/ (desviación: https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-las-cotas-de-embalses-programadas/) | https://www.coordinador.cl/operacion/graficos/operacion-real/informacion-condicion-hidrologica/ | https://portal.api.coordinador.cl/ — doc: https://portal.api.coordinador.cl/documentacion?service=sipubv2 — PDF: https://www.coordinador.cl/wp-content/uploads/2019/01/Uso-Api-SIP-Sistema-Informacion-Publica-v1.1.pdf | https://spc.coordinador.cl/ — informe metodológico: https://www.coordinador.cl/wp-content/uploads/2021/08/Informe-Sistema-Pronostico-de-Caudales.pdf | https://www.coordinador.cl/mercados/documentos/pronostico-centralizado-de-generacion-y-demanda-2/pronostico-de-deshielo/ (caudales: .../pronostico-de-caudales/) | Patrón: https://www.coordinador.cl/wp-content/uploads/AAAA/MM/CEN_Informe_Mensual_SEN_MesAA.pdf (ej. Feb26) |
| **Método de acceso** | Web con botón "Exportar" → CSV (scrapeable; backend probablemente mismo SIP) | Web + export CSV | Web + export CSV | API REST. Endpoints confirmados por búsqueda: `/api/v2/recursos/cotas_embalses/` (campos: embalse, fecha, hora, cota, afluente_diario m3/s; filtros limit/offset/fecha), `/api/v2/recursos/cotas_embalses_maximas_minimas/`, `/api/v2/recursos/cotas_afluentes_embalses_programado/` (+ `/slices/`) | Portal web con visualizador de pronósticos de afluentes (17 puntos de control: Aconcagua, Colorado, Olivares, Maipo, Cachapoal, Tinguiririca, Pilmaiquén, Duqueco, etc.) | Descarga de documentos/planillas desde página web | PDF descarga directa |
| **Autenticación** | No (público) | No | No | Registro gratuito en portal del desarrollador → API key/usuario (por confirmar el flujo exacto) | No aparente (por confirmar) | No | No |
| **Formato** | CSV | CSV | CSV | JSON | Web/posibles CSV | XLSX/PDF (por confirmar) | PDF |
| **Granularidad** | Diaria (cota final diaria por embalse); incluye precipitaciones y vertimientos según la página | Horaria/diaria programada | Diaria/semanal agregada SEN (energía afluente + probabilidad de excedencia) | Horaria (cota) y diaria (afluente) según schema del endpoint | Pronóstico horario/diario a días-semanas vista | Estacional (sep–mar), por cuenca | Mensual (incluye energía embalsada GWh y generación hidro embalse) |
| **Profundidad histórica** | Varios años vía export (por verificar; el sitio menciona "histórico de embalses": precipitación, cota final diaria, vertimientos) | Por verificar | Por verificar | Por verificar (probablemente desde ~2019, año de la doc v1.1) | Operativo desde 2019 (lanzamiento portal) | Anual desde hace años | PDFs mensuales ≥2023 visibles; serie larga probable |
| **Frecuencia / hora publicación** | Diaria, día vencido (D-1); hora exacta por verificar — típicamente mañana del día siguiente → **compatible con corte 20:00 para predecir D+1** | Diaria (programa del día siguiente publicado la tarde anterior — por verificar hora) | Semanal/diaria por verificar | Continua (API); actualización ligada a procesos del CEN | Actualización diaria (por verificar) | 1–2 veces por temporada (sep, con revisiones) | Mensual, ~mediados del mes siguiente |
| **Verificación** | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

Cobertura esperada de embalses CEN: Lago Laja (El Toro), Rapel, Colbún/Machicura, Ralco/Pangue, Chapo (Canutillar), Invernada, Melado — son los embalses de regulación que el CEN modela en PCP/PLP; lista exacta por endpoint **por verificar**.

Adicional CEN: **Programas de Operación Histórico** (https://www.coordinador.cl/operacion/documentos/programas-de-operacion/) — el programa diario incluye política de operación, cotas y costos marginales programados; útil como "pronóstico implícito" del propio operador. Modelo PCP: https://www.coordinador.cl/operacion/documentos/modelacion-del-sen/modelos-para-la-planificacion-y-programacion-de-la-operacion/informacion-relacionada-con-el-modelo-pcp/

### 1.2 DGA (Dirección General de Aguas, MOP)

| Campo | HIDROlínea / Sistema Hidrométrico en Línea | Estadística Hidrológica en Línea (SNIA) | Boletín mensual hidrométrico | Pronóstico de caudales de deshielo |
|---|---|---|---|---|
| **URL exacta** | https://dga.mop.gob.cl/sistema-hidrometrico-en-linea/ → app: https://snia.mop.gob.cl/dgasat/pages/dgasat_param/dgasat_param.jsp?param=1 | https://snia.mop.gob.cl/portal-web/ y https://www.mop.gob.cl/serviciosmop/estadistica-hidrologica-en-linea/ | https://dga.mop.gob.cl/servicios-de-informacion/boletines/ (ej.: Boletín N°571 nov-2025: https://dga.mop.gob.cl/uploads/sites/13/2025/01/Boletin-Hidrometrico-DGA-Noviembre-2025-ver-2.pdf) | https://dga.mop.gob.cl/uploads/sites/13/2024/09/Pronostico_Caudales_Deshielo_2024_2025.pdf (anuncio 25/26: https://doh.mop.gob.cl/pronostico-de-caudales-de-deshielo-primavera-2025-verano-2026-...) |
| **Método de acceso** | Web app (JSP, scrapeable). ~650–1.330 estaciones satelital/GPRS: caudal, nivel, precipitación, nieve, **niveles y volúmenes de embalses y lagos**. No se encontró API REST/OGC documentada pública | Web app de reportes oficiales. Límites: máx. 10 estaciones por consulta; 40 años (anual), 10 años (mensual), 4 años (diario) | PDF mensual | PDF anual |
| **Autenticación** | No (hay login para perfiles avanzados: dgasat_login.htm) | No | No | No |
| **Formato** | HTML/tablas (export por confirmar) | HTML/XLS (por confirmar) | PDF | PDF |
| **Granularidad** | Horaria (mayoría de estaciones se actualiza cada hora) | Diaria/mensual/anual | Mensual (estado de embalses en volumen, pluviometría, fluviometría) | Estacional: volúmenes de deshielo y caudales medios mensuales sep–mar, 19 cuencas |
| **Profundidad histórica** | Tiempo real + reciente | Décadas (estadística oficial validada) | Serie larga de boletines | Desde al menos 2012 en línea |
| **Frecuencia / hora publicación** | Cada ~1 hora → **única fuente intradiaria del día D utilizable antes de las 20:00** | Datos validados con rezago (semanas/meses) | Mensual, con rezago ~1 mes | 1 vez/año (sep) + actualizaciones |
| **Verificación** | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

### 1.3 Otras fuentes

| Campo | DMC — Boletín Tendencias Climáticas / pronóstico S2S | CNE Energía Abierta — Energía almacenada en embalses | CR2 — Caudales históricos / CAMELS-CL |
|---|---|---|---|
| **URL exacta** | https://climatologia.meteochile.gob.cl/application/publicaciones/boletinTendenciasClimaticas (PDF ej.: .../boletinTendenciasClimaticas-202510.pdf) | http://energiaabierta.cl/visualizaciones/energy-reservoir/ — API: http://datos.energiaabierta.cl/developers/ | https://www.cr2.cl/datos-de-caudales/ ; https://www.cr2.cl/camels-cl/ ; https://github.com/calvarezgarreton/camels-cl ; https://dataclima.cr2.cl/ |
| **Método de acceso** | PDF mensual; DMC además ofrece servicios climáticos (suscripción: servicios_climatologicos@meteochile.gob.cl); existencia de API REST de meteochile **por confirmar** | Visualizador + **API RESTful JSON** del portal de datos abiertos CNE (datos provienen del CEN) | Descarga ZIP/CSV (caudales diarios y mensuales DGA 1930–2016; CAMELS-CL: 516 estaciones con caudal diario + forzantes met.) |
| **Autenticación** | No | Por confirmar (API CNE suele ser abierta) | No |
| **Formato** | PDF | JSON / web | CSV/TXT |
| **Granularidad** | Pronóstico probabilístico mensual y trimestral (precipitación, temperaturas) | Energía almacenada (GWh) por embalse, histórica y actual; granularidad diaria/semanal por confirmar | Diaria y mensual |
| **Profundidad histórica** | Boletines desde ~2014 | Serie histórica multi-año | 1930–2016 (CR2); CAMELS-CL ~1913–2018 |
| **Frecuencia / hora publicación** | Última semana de cada mes | Según actualización CNE (rezago por confirmar) | Estática (corpus de entrenamiento, no operacional) |
| **Verificación** | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

**CDOM**: no se encontró una fuente pública activa con ese nombre (las búsquedas devuelven solo material descriptivo de la cuenca del Maule). Probablemente se refiere a organismos de cuenca (juntas de vigilancia) sin publicación estructurada. Descartar para el MVP; los datos del Maule (Colbún, Invernada, Melado, laguna del Maule) están cubiertos por CEN y DGA.

---

## 2. Ranking por valor predictivo para el costo del SEN

| # | Fuente | Justificación física |
|---|--------|----------------------|
| 1 | **CEN — cotas/afluentes de embalses (API SIP `cotas_embalses`)** | La cota define la energía embalsada y, vía el valor del agua (programación hidrotérmica), el costo marginal: embalses bajos → el agua "vale" caro → despacho térmico (diésel/GNL/carbón) marca el costo. Es exactamente la variable de estado que usa el propio CEN para programar. Diaria, estructurada, JSON. |
| 2 | **CEN — energía afluente y probabilidad de excedencia del SEN** | Resume la condición hidrológica agregada (año húmedo/seco) en la métrica que el modelo PLP/PCP usa; correlaciona directamente con el costo marginal esperado de semanas siguientes. |
| 3 | **CNE Energía Abierta — energía almacenada (GWh) por embalse** | Misma física que (1) pero ya convertida a GWh (cota×volumen×rendimiento): feature lista para el modelo, vía API JSON. Redundante con (1); útil como respaldo y para histórico. |
| 4 | **DGA — HIDROlínea (caudales afluentes horarios)** | Los afluentes son la derivada del stock: anticipan el cambio de energía embalsada días/semanas antes de que se refleje en cotas. Única fuente intradiaria del día D publicada antes de las 20:00. |
| 5 | **CEN — pronóstico de deshielo + SPC** | El deshielo (sep–mar) determina la oferta hidro del semestre; el pronóstico del propio operador entra en su programación, por lo que mueve el costo programado aun antes de materializarse el caudal. |
| 6 | **DGA — pronóstico de caudales de deshielo** | Señal estacional independiente (19 cuencas, basada en nieve acumulada al 31-ago); horizonte largo, frecuencia anual: útil como regressor estacional, no diario. |
| 7 | **DMC — pronóstico estacional S2S** | Precipitación trimestral probable (ENSO) → anticipa hidrología con 1–3 meses de adelanto, pero con alta incertidumbre: valor marginal sobre (5)-(6). |
| 8 | **DGA boletín mensual / CEN informe mensual (PDF)** | Validación y contexto; rezago ~1 mes los hace poco útiles como feature operativa. |
| 9 | **CR2 / CAMELS-CL** | Sin valor operativo (corte 2016/2018), pero el mejor corpus para entrenar/validar relaciones caudal-cota-costo con décadas de historia. |

## 3. Estrategia MVP recomendada

1. **Serie mínima primero**: cota diaria + afluente diario por embalse desde la **API SIP del CEN** (`/api/v2/recursos/cotas_embalses/`), priorizando Lago Laja, Colbún, Ralco, Rapel, Invernada, Melado, Chapo. Es JSON estructurado, del operador que fija el costo, y con la cota se reconstruye energía embalsada por embalse y agregada.
2. **Complemento agregado**: energía almacenada (GWh) desde Energía Abierta (API CNE) como cross-check y para profundidad histórica de la serie agregada SEN.
3. **Derivada de corto plazo**: scraper horario de 5–10 estaciones fluviométricas DGA HIDROlínea aguas arriba de Laja, Maule y Biobío (cumple corte 20:00 del día D).
4. **Features estacionales**: ingestar 2 veces/año el pronóstico de deshielo (DGA + CEN) y mensualmente el boletín S2S de la DMC como variables de régimen (seco/normal/húmedo).
5. **Entrenamiento**: usar CR2/CAMELS-CL + exports CSV históricos del CEN para construir ≥5 años de historia; validar contra el informe mensual del CEN.
6. **Verificación pendiente** (cuando haya red): confirmar flujo de registro/API key del portal CEN, lista exacta de embalses del endpoint, profundidad histórica de sipubv2, hora exacta de publicación de cotas D-1, y si la API de Energía Abierta sigue activa (dominio http, posible migración).
