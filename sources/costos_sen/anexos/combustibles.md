# Fase 1 — Fuentes gratuitas de precios internacionales de combustibles

> Investigación vía WebSearch (2026-06-12). La red saliente del sandbox está bloqueada (curl/WebFetch → 403),
> por lo que **ningún endpoint pudo verificarse en vivo**. Estado de verificación de TODAS las series:
> `pendiente — red sandbox bloqueada`. Verificar en CI/GitHub Actions con red abierta.

Contexto: las térmicas chilenas queman GNL importado (indexado típicamente a Henry Hub/Brent, con JKM/TTF como
referencia de cargamentos spot), carbón importado (referencias API2 Rotterdam / Newcastle) y diésel.
Se necesita: 5+ años de datos diarios, formato programático (JSON/CSV) y rezago de publicación conocido
(regla anti-fuga: corte 20:00 hora Chile).

---

## 1. Gas natural / GNL

| Campo | Henry Hub spot (EIA) | Henry Hub spot (FRED) | Henry Hub futuros (Yahoo) | TTF futuros — proxy de JKM (Yahoo) | JKM spot (Platts) |
|---|---|---|---|---|---|
| Commodity | Gas natural spot EE.UU. | Gas natural spot EE.UU. | Gas natural, futuro front-month NYMEX | Gas Europa (EUR/MWh), proxy de precio GNL spot Asia | GNL spot Asia (USD/MMBtu) |
| Fuente | EIA Open Data API v2 | FRED (St. Louis Fed) | yfinance, ticker `NG=F` | yfinance, ticker `TTF=F` | S&P Global Platts — **DE PAGO** |
| Endpoint / método | `https://api.eia.gov/v2/natural-gas/pri/fut/data/?api_key=KEY&frequency=daily&data[0]=value&facets[series][]=RNGWHHD&start=2019-01-01&sort[0][column]=period&sort[0][direction]=desc` (ruta exacta por confirmar en el browser: https://www.eia.gov/opendata/browser/natural-gas/pri) | `https://api.stlouisfed.org/fred/series/observations?series_id=DHHNGSP&api_key=KEY&file_type=json` | `yf.download("NG=F", period="max", interval="1d")` | `yf.download("TTF=F", period="max", interval="1d")` | Sin API gratuita. Alternativas pagas: oilpriceapi.com, commodities-api.com (símbolo `JKMC1`), Trading Economics |
| API key | Sí — gratuita en https://www.eia.gov/opendata/register.php (email, llega al instante) | Sí — gratuita con cuenta FRED (https://fredaccount.stlouisfed.org/apikeys) | No | No | N/A (suscripción comercial) |
| Formato | JSON (también XML); máx. 5.000 filas/request | JSON (`file_type=json`) o XML | DataFrame/CSV (OHLCV) | DataFrame/CSV (OHLCV) | — |
| Granularidad | Diaria (días hábiles) | Diaria (días hábiles) | Diaria | Diaria | Diaria |
| Profundidad histórica | Desde 1997-01-07 | Desde 1997 (espejo de EIA) | ~Desde 2000 (sobra para 5 años) | Listado en Yahoo hace pocos años; verificar que cubra 5 años | — |
| Rezago de publicación | El sitio "Today in Energy Daily Prices" se actualiza cada día hábil 7:30–8:30 am ET con el día anterior, pero la serie API/dnav se refresca en ciclo semanal (miércoles). **Asumir rezago efectivo 1–8 días; conservador T+7** | Observado: series diarias EIA en FRED llegan con ~3–5 días corridos de rezago (ver Brent abajo) | Settlement del día disponible el mismo día (~17:00 ET ≈ 18:00–19:00 Chile) → utilizable antes de las 20:00 Chile, pero es futuro, no spot | Igual que NG=F (cierre ICE/NYMEX del día) | Publicación diaria solo para suscriptores |
| Rate limits | No publicado; throttling dinámico (sobra para 1 pull diario) | 120 requests/min | No documentado; errático (`YFRateLimitError`) | Ídem | — |
| Verificación | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

**Sobre JKM**: no existe fuente gratuita programática del índice Platts JKM. Los futuros JKM de NYMEX/CME existen
(TradingView `NYMEX:JKM1!`, CME web con delay) pero **no tienen ticker funcional en Yahoo Finance** ni API gratuita.
Proxies recomendados: (a) `TTF=F` — desde 2021 JKM y TTF arbitran vía flete y se mueven juntos; (b) Henry Hub + Brent,
que es como realmente se indexan los contratos de suministro GNL de Quintero/Mejillones. Documentar el proxy elegido
en el modelo.

---

## 2. Carbón (API2 Rotterdam / Newcastle)

| Campo | API2 futuros (Yahoo) | Newcastle | Histórico manual (respaldo) | Índices oficiales |
|---|---|---|---|---|
| Commodity | Carbón API2 CIF ARA (USD/t), futuro front-month | Carbón Newcastle FOB (USD/t) | Carbón API2 / Newcastle | API2 (Argus/McCloskey), NEWC (globalCOAL) |
| Fuente | yfinance, ticker `MTF=F` ("Coal (API2) CIF ARA ARGUS-McCloskey", NYMEX) — verificado que existe en Yahoo | **Sin ticker Yahoo confiable.** ICE `NCF` visible en TradingView/Barchart/Investing con delay, sin API gratuita | Investing.com (descarga CSV manual), Barchart (límite diario gratuito) | **DE PAGO** (Argus, globalCOAL, ICE market data, oilpriceapi.com) |
| Endpoint / método | `yf.download("MTF=F", period="max", interval="1d")` | — (scraping no recomendado) | Descarga manual una vez para el histórico; no automatizable | Suscripción |
| API key | No | — | No | N/A |
| Formato | DataFrame/CSV (OHLCV) | — | CSV | — |
| Granularidad | Diaria, **con huecos** (baja liquidez: días sin transar) | Diaria | Diaria | Diaria/semanal |
| Profundidad histórica | Por confirmar; típicamente ~10 años en Yahoo para este contrato | — | 10+ años en Investing.com | Décadas |
| Rezago | Settlement mismo día (~12:00–17:00 ET) | — | Manual | T+0 para suscriptores |
| Rate limits | No documentado (yfinance) | — | — | — |
| Verificación | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

**Conclusión carbón**: no existe API gratuita oficial de API2/Newcastle. `MTF=F` vía yfinance es el único proxy
gratuito y programático; rellenar huecos con forward-fill y sembrar el histórico con un CSV manual de Investing.com.
Respaldo adicional sin key: stooq.com (CSV directo por URL, sin API key; verificar si lista el contrato de carbón).

---

## 3. Petróleo / diésel

| Campo | Brent spot (EIA) | Brent (FRED) | WTI (EIA / FRED) | Diésel USGC ULSD (EIA) | Diésel proxy futuros (Yahoo) |
|---|---|---|---|---|---|
| Serie | `RBRTE` | `DCOILBRENTEU` | `RWTC` / `DCOILWTICO` | `EER_EPD2DXL0_PF4_RGC_DPG` (USD/gal) | `BZ=F` (Brent fut.), `HO=F` (NY Harbor ULSD fut., USD/gal) |
| Endpoint / método | `https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key=KEY&frequency=daily&data[0]=value&facets[series][]=RBRTE` (ruta confirmada por el browser oficial de EIA) | `https://api.stlouisfed.org/fred/series/observations?series_id=DCOILBRENTEU&api_key=KEY&file_type=json` | Mismos endpoints (cambiar serie) | Mismo endpoint EIA `petroleum/pri/spt`, facet `series=EER_EPD2DXL0_PF4_RGC_DPG` | `yf.download(["BZ=F","HO=F"], period="max")` |
| API key | Sí (EIA, gratuita) | Sí (FRED, gratuita) | Ídem | Sí (EIA) | No |
| Formato | JSON, máx. 5.000 filas/request | JSON | JSON | JSON | DataFrame/CSV |
| Granularidad | Diaria (días hábiles) | Diaria | Diaria | Diaria | Diaria |
| Profundidad | Desde 1987-05-20 | Desde 1987-05-20 | Desde 1986 | Desde ~junio 2006 (inicio espec ULSD) | HO=F ~2000; BZ=F ~2007 |
| Rezago | Serie API se refresca en ciclo semanal (miércoles, ~10:30 am ET); rezago efectivo 1–8 días. **Conservador: T+7** | **Evidencia concreta**: al 2026-06-12 la última observación era 2026-06-08 → ~4 días corridos. Conservador: T+5 | Igual que Brent | Igual (mismo release de spot prices EIA) | Mismo día tras settlement (~14:30–17:00 ET) → disponible antes de 20:00 Chile |
| Rate limits | No publicado | 120 req/min | Ídem | Ídem | No documentado |
| Verificación | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

---

## 4. Tipo de cambio USD/CLP

| Campo | Banco Central de Chile (API BDE) | mindicador.cl | CMF (api.cmfchile.cl) |
|---|---|---|---|
| Serie | Dólar observado, código `F073.TCO.PRE.Z.D` (diario) | Indicador `dolar` (dólar observado, scrapeado del BCCh) | Dólar observado |
| Endpoint / método | `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=USER&pass=PASS&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=YYYY-MM-DD&lastdate=YYYY-MM-DD` (REST, JSON). Librería oficial-ish Python: `bcchapi` (PyPI) | `https://mindicador.cl/api` (valores del día) · `https://mindicador.cl/api/dolar` (serie reciente) · `https://mindicador.cl/api/dolar/{dd-mm-yyyy}` (fecha) · `https://mindicador.cl/api/dolar/{yyyy}` (año completo) | `https://api.cmfchile.cl/api-sbifv3/recursos_api/dolar?apikey=KEY&formato=json` |
| Registro / key | Sí — **credenciales usuario/contraseña** (no API key): registro gratuito vía formulario del BCCh / contacto_ws@bcentral.cl. Docs: https://si3.bcentral.cl/estadisticas/Principal1/Web_Services/doc_es.htm | **No requiere key** — gratuita, open source, sin fines de lucro | Sí — API key gratuita con registro |
| Formato | JSON | JSON | JSON/XML |
| Granularidad | Diaria | Diaria | Diaria |
| Profundidad | Décadas (toda la BDE del BCCh) | Histórico por año (varios años hacia atrás) | Años |
| Rezago | Dólar observado: promedio de transacciones del día hábil anterior, publicado el día hábil siguiente en la mañana → **T+1 hábil** (apto para corte 20:00 Chile usando el valor publicado en el día) | Igual que BCCh (es su espejo); riesgo: servicio comunitario sin SLA | T+1 hábil |
| Rate limits | No publicados; uso razonable | No documentados | No documentados |
| Verificación | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada | pendiente — red sandbox bloqueada |

---

## 5. Evaluación de yfinance como fuente unificada de futuros

Tickers relevantes verificados por búsqueda: `NG=F` (Henry Hub), `BZ=F` (Brent), `HO=F` (NY Harbor ULSD ≈ diésel),
`MTF=F` (carbón API2), `TTF=F` (gas Europa, proxy JKM).

**Ventajas**
- Una sola librería/formato para 5 commodities; sin API key ni registro.
- Datos del MISMO día (settlement ~17:00 ET ≈ 18:00–19:00 Chile): único candidato que entrega precio de hoy antes del corte de las 20:00 Chile. EIA/FRED llegan con días de rezago.
- Profundidad: NG=F y HO=F ~2000, BZ=F ~2007 (5+ años cubiertos); MTF=F más corto y con huecos.

**Desventajas**
- API **no oficial** (scraping de Yahoo): endpoints cambian sin aviso, `YFRateLimitError` frecuente desde 2024-2025, posible violación de ToS para uso comercial → no apto como única fuente de producción.
- Son **futuros front-month, no spot**: roll del contrato genera saltos artificiales al vencimiento; difiere del spot que usa el CDEC/Coordinador para costos variables.
- MTF=F tiene días sin transacciones (baja liquidez) → requiere forward-fill.
- Sin SLA ni rate limits documentados.

**Veredicto**: usar yfinance como capa de *nowcast* (precio de hoy) y como única vía gratuita para carbón/TTF;
usar EIA/FRED como fuente de verdad para series spot históricas y entrenamiento.

---

## Recomendación de stack mínimo (MVP)

| Commodity | Primario MVP | Respaldo | Nota anti-fuga (corte 20:00 Chile) |
|---|---|---|---|
| Gas natural (Henry Hub) | **EIA API** `RNGWHHD` | FRED `DHHNGSP`; nowcast `NG=F` | En features usar lag ≥ T-7 para EIA / T-5 para FRED; `NG=F` sí está disponible el mismo día |
| GNL Asia (JKM) | **Proxy `TTF=F`** (yfinance) + Henry Hub/Brent como indexadores contractuales | Trading Economics / commodities-api (pago, post-MVP) | Mismo día (settlement antes de 20:00 Chile) |
| Carbón (API2) | **`MTF=F`** (yfinance) — única opción gratuita programática | CSV manual Investing.com (histórico); stooq.com | Mismo día; forward-fill en días sin trade |
| Brent | **EIA API** `RBRTE` | FRED `DCOILBRENTEU`; nowcast `BZ=F` | Lag ≥ T-7 (EIA) / T-5 (FRED) |
| WTI | EIA API `RWTC` | FRED `DCOILWTICO` | Ídem |
| Diésel | **EIA API** `EER_EPD2DXL0_PF4_RGC_DPG` (USGC ULSD) | Nowcast `HO=F` | Lag ≥ T-7 (EIA); `HO=F` mismo día |
| USD/CLP | **mindicador.cl** (sin key, cero fricción) | BCCh API BDE `F073.TCO.PRE.Z.D` (oficial; migrar en producción) | T+1 hábil; el valor del día está publicado antes de 20:00 |

### Secretos a registrar en GitHub Actions (pedir al usuario)

| Secret | Cómo obtenerlo | Obligatorio para el MVP |
|---|---|---|
| `EIA_API_KEY` | Gratis e inmediato: https://www.eia.gov/opendata/register.php | **Sí** (HH, Brent, WTI, diésel) |
| `FRED_API_KEY` | Gratis con cuenta FRED: https://fredaccount.stlouisfed.org/apikeys | Recomendado (respaldo) |
| `BCCH_USER` / `BCCH_PASS` | Registro gratuito API BDE del BCCh (formulario; docs en si3.bcentral.cl) | No (solo si se migra desde mindicador) |
| — yfinance / mindicador / stooq | No requieren key | — |

### Pendientes de verificación cuando haya red
1. Ruta v2 exacta de `RNGWHHD` (¿`natural-gas/pri/fut`?) — confirmar en https://www.eia.gov/opendata/browser/.
2. Profundidad real de `MTF=F` y `TTF=F` con `period="max"`.
3. Rezago efectivo de EIA API por serie (comparar `period` máximo vs fecha de consulta durante una semana).
4. Si stooq.com lista carbón API2 y TTF (descarga CSV por URL sin key).
