# Captura de datos climáticos vía Open-Meteo — Modelo de costo de operación del SEN

> **Fase 1 — Investigación de fuentes de datos.**
> Fecha: 2026-06-12. Red saliente del sandbox bloqueada: ningún endpoint fue ejecutado en vivo.
> Verificación basada en búsquedas web sobre la documentación oficial de Open-Meteo (open-meteo.com/en/docs) + conocimiento del dominio.
> **Estado de verificación de TODOS los endpoints: pendiente — red sandbox bloqueada.** Validar con `curl` real antes de congelar el pipeline.

---

## 1. Tabla de endpoints

| # | API | URL de ejemplo (parámetros reales) | Variables clave | Granularidad | Profundidad histórica | Límite gratuito | Verificación |
|---|-----|-----------------------------------|-----------------|--------------|----------------------|-----------------|--------------|
| 1 | **Histórica (reanálisis)** | `https://archive-api.open-meteo.com/v1/archive?latitude=-22.4&longitude=-68.9&start_date=2015-01-01&end_date=2026-06-05&hourly=temperature_2m,shortwave_radiation,wind_speed_10m,wind_speed_100m,precipitation&daily=shortwave_radiation_sum,temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=America%2FSantiago` | `shortwave_radiation(_sum)`, `wind_speed_10m/100m`, `temperature_2m`, `precipitation(_sum)`, `direct_normal_irradiance`, `et0_fao_evapotranspiration`, `snowfall` | Horaria + agregados diarios | Desde **1940** (reanálisis ERA5, 0.25° ≈ 25 km; ERA5-Land 0.1° para variables de superficie, sin viento 100 m). Rezago de publicación ~2–5 días (ERA5T) | <10.000 llamadas/día, 5.000/h, 600/min (uso no comercial). Peticiones largas cuentan como múltiples llamadas (~2 semanas + >10 variables ≈ 1.5 llamadas; 4 semanas ≈ 3.0) | **pendiente — red sandbox bloqueada** |
| 2 | **Pronóstico** | `https://api.open-meteo.com/v1/forecast?latitude=-33.45&longitude=-70.66&hourly=temperature_2m,shortwave_radiation,wind_speed_100m,precipitation&daily=shortwave_radiation_sum,precipitation_sum,temperature_2m_max&forecast_days=16&past_days=7&timezone=America%2FSantiago&models=best_match` | Mismas variables que histórica + nubosidad, presión, humedad; viento a 10/80/100/120/180 m según modelo | Horaria (y 15-min en algunos modelos); horizonte **7 días default, hasta 16** (`forecast_days=16`); `past_days` hasta 92 | Solo presente + `past_days` (≤92 días hacia atrás) | Igual que arriba (mismo contador global) | **pendiente — red sandbox bloqueada** |
| 3 | **Historical Forecast (archivo de pronósticos)** | `https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=-35.7&longitude=-71.0&start_date=2022-01-01&end_date=2026-06-10&hourly=temperature_2m,shortwave_radiation,wind_speed_100m,precipitation&timezone=America%2FSantiago&models=ecmwf_ifs025` | Mismas variables y formato que la Forecast API | Horaria | Desde **~2022** (lo más antiguo: julio 2022 según issue #694 del repo; varía por modelo). **OJO: archiva la serie "seamless" (siempre la corrida más reciente), es decir lead time corto (~0–6 h)** | Igual que arriba | **pendiente — red sandbox bloqueada** |
| 4 | **Previous Runs (lead times fijos)** | `https://previous-runs-api.open-meteo.com/v1/forecast?latitude=-37.7&longitude=-72.6&start_date=2024-01-01&end_date=2026-06-10&hourly=temperature_2m_previous_day1,temperature_2m_previous_day2,wind_speed_100m_previous_day1,wind_speed_100m_previous_day2,shortwave_radiation_previous_day1,shortwave_radiation_previous_day2,precipitation_previous_day1&timezone=America%2FSantiago&models=gfs_seamless` | Cualquier variable horaria con sufijo `_previous_dayN`, N=1..7 (`previous_day1` = valor pronosticado **24 h antes** del tiempo válido; `previous_day2` = 48 h, etc.) | Horaria | Mayoría de modelos archivados desde **enero 2024**; GFS `temperature_2m` desde **marzo 2021** | Igual que arriba | **pendiente — red sandbox bloqueada** |
| 5 | **Single Runs (corrida específica)** — complementaria | docs: `open-meteo.com/en/docs/single-runs-api`; parámetro `&run=2026-06-11T12:00` (datetime UTC de inicialización, ISO 8601). Host exacto por confirmar cuando haya red | Variables horarias de la corrida exacta indicada | Horaria, por corrida | Corridas archivadas desde **sep-2025** (mayoría de modelos); ECMWF IFS HRES 9 km desde **mar-2024** | Igual que arriba | **pendiente — red sandbox bloqueada** |

Notas transversales:

- **Formato**: JSON por defecto (`&format=json`); también FlatBuffers y CSV/XLSX. Respuesta JSON: `latitude/longitude` de la celda, `hourly.time[]` + un array por variable, `hourly_units`, `daily.*` análogo.
- **`timezone=America/Santiago`**: devuelve timestamps en hora local de Chile con DST aplicado (UTC-3 verano ~sep–abr, UTC-4 invierno) y alinea los agregados `daily` al día civil chileno (clave para que `shortwave_radiation_sum` y `precipitation_sum` correspondan al día de operación del SEN). Recomendación de ingeniería: almacenar crudo en UTC (`timezone=UTC`) y convertir a hora Chile en la capa de features, para evitar huecos/duplicados en los cambios de hora; usar `timezone=America/Santiago` solo donde importe el agregado diario civil.
- **Nombres de variables**: la convención vigente usa guion bajo (`wind_speed_100m`); los alias legacy (`windspeed_100m`) siguen aceptados. Usar la forma nueva.
- **Multi-punto en una llamada**: `latitude=-22.4,-25.4,-33.45&longitude=-68.9,-70.5,-70.66` (listas separadas por coma) reduce el número de requests.
- **Presupuesto de llamadas**: backfill histórico de ~10 años horarios × 11 puntos ≈ algunos cientos de "llamadas equivalentes" (hacerlo en 1–2 días, por chunks anuales). Operación diaria: ~11–22 llamadas/día. Muy por debajo del límite gratuito; el uso debe ser no comercial (si el modelo es comercial, plan API desde ~29 EUR/mes).

---

## 2. Puntos representativos para Chile (SEN)

| Zona | Lat | Lon | Tecnología que representa | Justificación (capacidad instalada cercana) |
|------|-----|-----|---------------------------|---------------------------------------------|
| María Elena / Calama (Atacama interior) | -22.4 | -68.9 | Solar FV + CSP | Corredor con mayor densidad FV del país (comuna de María Elena: Cerro Dominador CSP 110 MW + FV; clusters FV en torno a Calama/Crucero, varios GW en la región de Antofagasta). Radiación entre las más altas del mundo |
| Diego de Almagro (Atacama sur) | -26.4 | -70.0 | Solar FV | Segundo cluster FV histórico del SEN (Diego de Almagro, Salvador, Javiera y plantas vecinas en la región de Atacama); captura el gradiente norte-sur de nubosidad costera |
| Taltal (costa Antofagasta) | -25.4 | -70.5 | Eólica norte | Parque Eólico Taltal (~99 MW) y desarrollo eólico costero del norte; régimen de viento distinto al del sur (brisa costera/topografía) |
| Renaico / Angol (La Araucanía) | -37.7 | -72.6 | Eólica sur (cluster principal) | Mayor concentración eólica del SEN: Malleco (~273 MW, uno de los mayores del país), Renaico (~88 MW), San Gabriel, Cuel y vecinos en Biobío–Araucanía |
| Ancud / Chiloé (Los Lagos) | -41.9 | -73.8 | Eólica austral | Parques San Pedro/Chiloé (~100 MW) y Aurora (Llanquihue); régimen de frentes del Pacífico sur, poco correlacionado con Renaico → diversificación del recurso |
| Cuenca del Maule | -35.7 | -71.0 | Hidro embalse/pasada | Complejos Colbún–Machicura (~570 MW), Pehuenche (~570 MW), Cipreses/Isla; precipitación + temperatura (deshielo) gobiernan cota y energía embalsada |
| Cuenca Biobío / Laja | -37.3 | -71.5 | Hidro embalse (mayor del SEN) | El Toro (450 MW), Ralco (690 MW), Pangue (467 MW), Antuco (320 MW), Angostura; el lago Laja es el embalse interanual clave del SEN |
| Rapel (O'Higgins) | -34.0 | -71.0 | Hidro embalse centro | Central Rapel (~377 MW) y cuenca del Cachapoal; representa la hidrología de la zona central más seca |
| Santiago | -33.45 | -70.66 | Demanda | Región Metropolitana ≈ 40% del consumo del SEN; `temperature_2m` driver principal de demanda (climatización) |
| Concepción | -36.8 | -73.05 | Demanda sur + industrial | Segundo polo de consumo (industria forestal, papelera, siderúrgica); temperatura de calefacción en invierno |
| Antofagasta | -23.65 | -70.4 | Demanda minera norte | Gran minería del cobre = carga industrial plana pero sensible a eventos climáticos; proxy del consumo del norte grande |

**Estrategia de agregación — recomendación:**

1. **Features separadas por punto (recomendado para el modelo principal)**: 11 puntos × 4–6 variables ≈ 50–70 features, perfectamente manejable para gradient boosting / redes. Deja que el modelo aprenda los pesos; preserva señales no lineales (p.ej. viento en Taltal vs Renaico descorrelacionados).
2. **Agregados ponderados por capacidad (features derivadas + baseline)**: construir además `solar_ponderado`, `eolico_norte/sur_ponderado`, `precip_hidro_ponderada`, `temp_demanda_ponderada` usando capacidad instalada por zona (fuente: capacidad instalada del Coordinador Eléctrico Nacional / CNE, actualizar pesos trimestralmente). Útiles para modelos lineales de referencia, explicabilidad y como regularización implícita.
3. No promediar a nivel nacional: el SEN tiene >2.000 km de extensión y los regímenes (desierto vs frentes australes) se cancelarían.

---

## 3. Anti-fuga de datos: pronósticos históricos y la regla de las 20:00 Chile

### El problema

El modelo de costo de operación se decide el día D (cierre 20:00 hora Chile) para el día D+1. Si se entrena con el **clima observado** de D+1 (reanálisis ERA5), el modelo aprende con información que no existía al momento de decidir → fuga de datos y sobreestimación del desempeño. Debe entrenarse con **el pronóstico que estaba disponible a las 20:00 de D**.

### Qué corrida está disponible antes de las 20:00 Chile

Equivalencia horaria: 20:00 Chile = **23:00 UTC** (verano, UTC-3, ~sep–abr) o **00:00 UTC del día siguiente** (invierno, UTC-4).

| Corrida (init UTC) | Disponible en Open-Meteo (aprox.) | Hora Chile invierno (UTC-4) | Hora Chile verano (UTC-3) | ¿Antes de las 20:00? |
|--------------------|-----------------------------------|------------------------------|---------------------------|----------------------|
| GFS 12z | NOAA completa el horizonte de 16 días ~17:15 UTC; Open-Meteo la integra ~10 min después → **~17:30 UTC** | 13:30 | 14:30 | **Sí, con holgura → corrida de referencia** |
| GFS 18z | ~23:30 UTC | 19:30 | 20:30 | Riesgosa: margen de 30 min en invierno, **NO disponible en verano** |
| ECMWF IFS 12z | dissemination + integración ≈ 18:00–19:00 UTC (IFS 9 km open-data sin delay adicional desde oct-2025; IFS 0.25° con +2 h; AIFS 0.25° ~5 h 45 post-init) | ~14:00–15:00 | ~15:00–16:00 | **Sí** |
| ECMWF IFS 18z | ~00:00–01:00 UTC (D+1) | 20:00–21:00 | 21:00–22:00 | **No** |

**Conclusión: la corrida 12z UTC del día D (GFS y ECMWF) es la última garantizada antes del cierre de las 20:00 Chile, todo el año.** La 18z solo sirve como sensibilidad y nunca debe entrar al pipeline de producción/entrenamiento.

### Qué API usar para entrenar sin fuga

1. **Previous Runs API** (`previous-runs-api.open-meteo.com/v1/forecast`, sufijos `_previous_day1.._day7`) — la herramienta principal. `previous_day1` = valor pronosticado 24 h antes del tiempo válido; `previous_day2` = 48 h antes.
   - **Sutileza crítica**: `previous_day1` NO es uniformemente seguro frente al corte de las 20:00. Para las horas tardías de D+1 (p.ej. 23:00 Chile ≈ 02–03 UTC de D+2), "24 h antes" cae en la noche del día D **después de las 20:00** → fuga parcial.
   - **Regla segura**: usar `previous_day2` para todas las horas de D+1 (toda la información proviene de corridas del día D-1, siempre anteriores al cierre). Alternativa más fina: mezclar `previous_day1` para las horas tempranas de D+1 (donde el run de origen es ≤12z de D) y `previous_day2` para las tardías, replicando exactamente la información de la corrida 12z.
   - Profundidad: mayoría de modelos desde **ene-2024** (GFS temperatura desde mar-2021) → ~2.5 años de muestra de entrenamiento "limpia".
2. **Single Runs API** (`&run=YYYY-MM-DDT12:00`) — reconstrucción exacta del pronóstico disponible a las 20:00 (corrida 12z de D). Ideal conceptualmente, pero archivo solo desde **sep-2025** (ECMWF IFS HRES desde mar-2024) → poca profundidad; usar para validación fina del último año y para producción.
3. **Historical Forecast API** (`historical-forecast-api.open-meteo.com`) — **advertencia**: archiva la serie "seamless" donde cada hora proviene de la corrida más reciente (lead ~0–6 h). NO representa el pronóstico day-ahead; usarla como entrenamiento "pronóstico" sobreestima la calidad de la información disponible en D. Usos legítimos: extender features hacia 2022 con una corrección de sesgo lead-time (estimada comparando seamless vs `previous_day2` en el período común), análisis exploratorio, y como techo superior de desempeño.
4. **Archive API (ERA5)** — solo como *target-side* (clima realizado para construir labels indirectos, verificación de pronósticos, climatologías y features de largo plazo tipo "lluvia acumulada 90 días" que al día D ya son pasado conocido → sin fuga).

### Esquema operativo propuesto

- **Entrenamiento**: features de D+1 desde Previous Runs (`previous_day2`, o mezcla day1/day2 calibrada al run 12z) + features de pasado conocido desde Archive (acumulados hidrológicos). Período: 2024-01 en adelante (extensible a 2022 con Historical Forecast corregido, marcado con flag de calidad).
- **Producción**: descarga diaria ~18:30–19:00 Chile de la Forecast API con `models=gfs_seamless` (y `ecmwf_ifs` como segundo modelo), registrando timestamp de descarga; la corrida subyacente será la 12z. Congelar el snapshot antes de las 20:00.
- **Validación anti-fuga**: backtest comparando el modelo entrenado con `previous_day2` vs entrenado con ERA5 realizado; la brecha de desempeño cuantifica la fuga que se evitó.

---

## Fuentes consultadas (vía WebSearch; fetch directo bloqueado)

- https://open-meteo.com/en/docs/historical-weather-api
- https://open-meteo.com/en/docs (Forecast API)
- https://open-meteo.com/en/docs/historical-forecast-api
- https://open-meteo.com/en/docs/previous-runs-api
- https://open-meteo.com/en/docs/single-runs-api
- https://open-meteo.com/en/docs/gfs-api (horarios de disponibilidad GFS)
- https://open-meteo.com/en/docs/ecmwf-api y https://openmeteo.substack.com/p/ecmwf-transitions-to-open-data (delays ECMWF)
- https://open-meteo.com/en/pricing y https://open-meteo.com/en/terms (límites gratuitos)
- https://openmeteo.substack.com/p/weather-forecasts-from-previous-model-runs
- https://openmeteo.substack.com/p/introducing-the-historical-forecast
- https://github.com/open-meteo/open-meteo/issues/694 (profundidad Historical Forecast)
- https://github.com/open-meteo/open-meteo/issues/1393 (profundidad Previous Runs)
