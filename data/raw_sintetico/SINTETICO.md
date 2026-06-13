# ADVERTENCIA: DATOS 100% SINTETICOS

**TODO el contenido de `data/raw_sintetico/` es GENERADO por
`tools/etl/generar_sintetico.py` (numpy seed=42). NO son datos reales del
CEN, de Open-Meteo ni de ningun mercado.**

## Para que existe

El backfill real corre en GitHub Actions (la red del sandbox esta bloqueada) y
puede tardar en poblar `data/raw/`. Este dataset replica los ESQUEMAS exactos
del pipeline (los mismos que consumen `construir_tabla_maestra.py` y los
extractores `extractor_cen_*` / `extractor_clima*` / `extractor_combustibles`)
para que baselines y autoresearch sean demostrables de punta a punta.

**Se descarta automaticamente cuando llegan los datos reales**: la tabla
maestra construida desde aca queda marcada con `origen_datos="sintetico"`
(columna y `metadatos_features.json`), y basta reconstruir con
`--dir-raw data/raw --origen real`.

## Que NO se puede concluir de estos datos

Los resultados de baselines/modelos sobre este dataset **NO son metricas del
problema real**: la dificultad, los regimenes y el ruido son inventados. Solo
validan la MAQUINARIA (esquemas, lags anti-fuga, joins, splits, evaluacion).

## Logica generativa (resumen)

- **Mundo comun**: un indice `deficit_hidrico` (0=humedo, 1=seco; seco
  2019-2021, humedo 2023-2025) gobierna coherentemente precipitacion de
  cuencas, generacion hidro, cotas/afluentes de embalses y nivel de CMg.
- **`cen_demanda`**: nivel medio ~8.800 MWh/h, crecimiento 2,5%/año,
  estacionalidad con maximo en invierno, perfil intradiario de doble pico
  (mediodia y 20-22h), -8% fin de semana, -12% feriados (feriados REALES de
  `data/raw/calendario`; 2019 con lista sintetica), sensibilidad a la
  temperatura sintetica de Santiago, ruido AR(1).
- **`cen_cmg_real`**: orden de merito sintetico
  `35 + 0.9*(brent/10) + 25*deficit_hidrico + 30*max(0, dnn-0.75)^2`,
  hundimiento solar de mediodia creciente (duck curve, 5 USD en 2019 a 35 USD
  en 2026; CMg ~0-5 en primaveras de alta radiacion), ~8 spikes de escasez por
  año (x2-x4, 4-12 h), piso 0, ruido lognormal. 5 barras correlacionadas
  (factor comun 0.92): CRUCERO mas barata de dia (solar), CHARRUA mas barata
  en años humedos. `regimen` cambia 'antiguo'->'nuevo' el 2024-07-15.
- **`cen_generacion`**: cuadra con `demanda*(1.06±0.02)` por hora. Solar con
  share creciente 8%->25%; eolica con persistencia; hidro anticorrelada con el
  deficit; termicas cierran el balance carbon->gnl->diesel (diesel casi solo
  en spikes); carbon decreciente (descarbonizacion); bess chico desde 2023.
- **`cen_embalses`**: cota = base + ciclo anual (deshielo oct-ene) + tendencia
  interanual ligada al deficit + ruido suave; afluente correlacionado con la
  precipitacion sintetica de cuenca + deshielo.
- **`combustibles`**: caminos log-OU con anclas historicas estilizadas (spike
  2022 en brent/henry hub/carbon), solo dias habiles, carbon API2 con ~15% de
  dias faltantes (iliquidez), `origen='sintetico'` en cada fila.
- **`clima_observado` / `clima_pronostico`**: 11 puntos de
  `extractor_clima.PUNTOS`; radiacion alta y estable en `solar_*`, lluvia
  may-ago en `hidro_*`/Concepcion escalada por el año hidrologico; el
  pronostico es el observado + error gaussiano (~8% radiacion, ~1.2 C temp,
  ~15% viento, falsos positivos/negativos de lluvia) y existe solo desde
  2021-01-01 (simula archivo limitado de la API real).
- **`calendario/`**: copia del calendario REAL de `data/raw/calendario`
  (2020-2026) extendida con un 2019 sintetico de mismo schema.

Rango: 2019-01-01 a 2026-06-10. Regenerar: `cd tools/etl && python3 generar_sintetico.py`.
