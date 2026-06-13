---
title: Features del modelo de costo de operación D+1
sources:
  - tools/etl/construir_tabla_maestra.py
  - sources/costos_sen/catalogo_fuentes.md
  - data/processed/metadatos_features.json
last_synthesized: 2026-06-12
---

# Features de la tabla maestra

Convención global (decisión D-006): cada fila está indexada por la **fecha
objetivo T**; toda feature de la fila se computa solo con información
disponible públicamente **antes de las 20:00 hora Chile del día T-1**. Los lags
los aplica `tools/etl/construir_tabla_maestra.py` (única implementación) y cada
columna queda declarada en `data/processed/metadatos_features.json`;
`models/evaluacion.py::verificar_antifuga` rechaza automáticamente cualquier
feature no declarada o declarada no conforme. La fuente y hora de publicación
de cada insumo están en `sources/costos_sen/catalogo_fuentes.md`.

## Objetivo

| Columna | Definición | Nota |
|---------|-----------|------|
| `costo_op_usd` | Placeholder transitorio: Σₕ demanda_h(T) × CMg_h(T) promedio de 5 barras de referencia 220 kV, USD | ⚠️ valorización de retiros, NO costo de operación (revisión adversarial C1); se reemplaza por costo PLEXOS del PO + costo real reconstruido post-backfill. Es label: jamás entra como feature sin lag ≥ 2 |

## Features por familia

| Familia | Columnas | Fuente | Lag aplicado | ¿Por qué cumple la regla 20:00? |
|---------|----------|--------|-------------|--------------------------------|
| Calendario | `dia_semana`, `mes`, `es_finde`, `es_feriado`, `es_irrenunciable`, `es_vispera_feriado`, `es_sandwich`, `semana_18sept`, `vacaciones_verano`, `vacaciones_invierno`, `es_eleccion`, `es_vispera_eleccion`, `es_dst` | `holidays` + tabla manual de elecciones + tz IANA | 0 | Determinista; conocido con años de anticipación |
| Autoregresivas del objetivo | `costo_lag{2,3,7,14,21,28}`, `costo_ma7`, `costo_ma28` | derivadas del objetivo | ≥ 2 | El día T-1 no cierra hasta las 24:00; el último día completo conocido a las 20:00 de T-1 es T-2 → lag mínimo 2 |
| Demanda | `demanda_total_mwh`, `demanda_max_mwh` | CEN demanda real | 2 | Ídem: dato de T-2, publicado la mañana de T-1 |
| Generación por tecnología | `gen_*`, `share_*` (hidro, solar, eólica, térmicas, etc.) | CEN generación real | 2 | Ídem |
| Hidrología | `cota_*` (5 embalses) | CEN cotas embalses | 2 | Cota publicada diariamente; lag 2 conservador |
| CMg reciente | `cmg_medio`, `cmg_max` | CEN CMg real/preliminar | 3 | El CMg real se publica con rezago de días; lag 3 conservador (el CMg online, casi tiempo real, queda como mejora) |
| Combustibles (futuros) | `fx_brent_usd_bbl`, `fx_henry_hub_usd_mmbtu`, `fx_diesel_ho_usd_gal`, `fx_carbon_api2_usd_t`, `fx_usd_clp` | stooq/yfinance/mindicador | 1 | Settlement NYMEX 14:28-14:30 ET = 15:30-17:30 Chile < 20:00; dólar observado se publica en la mañana |
| Combustibles (spot EIA, opcional) | `fx_*_spot_*` | EIA | 7 | Las series spot EIA se publican con rezago de hasta una semana |
| Clima pronóstico para T | `pron_{temp_media,radiacion_media,viento100m_medio,precipitacion_total,temp_max,viento100m_max}_{punto}` (11 puntos) | Open-Meteo Previous Runs (`previous_day2`) | 0 (pronóstico emitido en T-2) | `previous_day2` garantiza emisión ≥ 24 h antes del inicio de T, siempre anterior a las 20:00 de T-1; `previous_day1` fue descartada porque filtra corridas post-corte para horas tardías de T (hallazgo del anexo clima) |
| Clima observado | `precip_hidro_30d`, `precip_hidro_90d`, `temp_hidro` | Open-Meteo Archive (ERA5) | 5 | Consolidación ERA5 tarda 2-5 días |

## Features capturadas pero BLOQUEADAS (no conformes)

| Columna | Razón del bloqueo | Cómo se desbloquea |
|---------|-------------------|--------------------|
| `costo_lag1` ("costo de hoy") | El día T-1 no ha cerrado a las 20:00 de T-1 | Nunca; existe solo para el baseline teórico de persistencia (vía `saltar_antifuga`, prohibido fuera de baselines) |
| `cmg_programado_d1` (CMg programado del PO para T) | Hora de publicación del PO **sin confirmar** (riesgo nº1 del catálogo); las re-publicaciones PID durante el propio día T agravan el riesgo | Verificación empírica desde el runner: si la primera versión del PO de T se publica consistentemente antes de las 20:00 de T-1, se cambia `cumple_regla_2000` a `true` con la evidencia documentada aquí |

## Verificación

- Chequeo automático: `verificar_antifuga` corre dentro de `evaluar_walk_forward`
  para todo modelo (los baselines de persistencia/estacional declaran su excepción
  explícitamente).
- Auditoría manual: revisar este archivo contra la columna "Hora publicación"
  del catálogo de fuentes; cualquier discrepancia es un bug de severidad máxima.
