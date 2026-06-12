# Auditoría adversarial anti-fuga — Pipeline de costo de operación D+1 (fase 3)

**Auditor:** agente adversarial de data leakage / metodología
**Fecha:** 2026-06-12
**Alcance:** `models/evaluacion.py`, `models/baselines.py`, `tools/etl/construir_tabla_maestra.py`,
`autoresearch/harness.py`, `autoresearch/model.py`, `data/processed/metadatos_features.json`,
`data/processed/tabla_maestra.parquet` (origen: **sintético**, seed=42, 2718 filas, 2019-01-01..2026-06-10).
**Mandato:** intentar DEMOSTRAR fuga de datos y walk-forward mal implementado. Verificaciones empíricas ejecutadas en Python sobre la tabla real.

---

## Resumen ejecutivo

El núcleo metodológico es **sólido**: el walk-forward es expansivo, sin shuffle, con corte temporal estricto, re-instancia el modelo por fold y reproduce los cuatro números del wiki **al decimal**. Todos los lags declarados están correctamente alineados **por calendario** (verifiqué 100 fechas aleatorias por feature, alineación perfecta). No encontré ninguna fuga de datos *activa* en el pipeline tal como está configurado.

Los hallazgos reales son **dos agujeros de gobernanza** (no fugas presentes, pero explotables por un agente experimentador) y **un conjunto de fragilidades de robustez** que no afectan los números sintéticos actuales pero pueden morder con datos reales. El hallazgo más serio es que el mecanismo anti-fuga verifica **nombres, no procedencia**: `model.py` (único archivo que el agente edita) puede mutar `df` por referencia y sobrescribir una columna conforme con el label del día T, pasando todos los chequeos.

---

## Tabla de hallazgos

| # | Componente | Hallazgo | Severidad | Evidencia | Parche propuesto |
|---|------------|----------|-----------|-----------|------------------|
| H1 | `harness.py` + `model.py` | **`verificar_antifuga` valida nombres, no procedencia.** `seleccionar_features(conformes, df)` recibe el `df` por referencia y puede **sobrescribir** una columna ya declarada conforme (p.ej. `df["costo_lag2"] = df["costo_op_usd"]*1.0001`). El nombre sigue en metadatos como conforme → `verificar_antifuga` pasa → fuga total del label. El harness solo re-verifica nombres preexistentes. | **CRÍTICA** | Reproduje el ataque: tras sobrescribir `costo_lag2` con el label del día T dentro de `seleccionar_features`, `verificar_antifuga([...])` no lanzó error y la "persistencia_lag2 conforme" bajó de **MAPE 8.87% → 0.0100%**. `nuevas=[]` (la columna no se detecta como nueva porque ya existía). | (a) Pasar a `seleccionar_features` una **copia** (`df.copy()`) o un df sin la columna objetivo; (b) en el harness, recalcular un hash/snapshot de las columnas conformes ANTES y DESPUÉS de `seleccionar_features` y abortar si alguna cambió; (c) prohibir `costo_op_usd` y derivados sin lag dentro del df entregado al experimento. Mínimo viable: `df_exp = df.drop(columns=[col_objetivo]); ... ; assert columnas conformes intactas vía hash`. |
| H2 | `harness.py` | **Features NUEVAS (nombre nuevo) saltan `verificar_antifuga`.** El harness solo verifica `[c for c in feats if c in conformes]`; las nuevas solo se imprimen como AVISO. La intención (derivarlas solo de conformes) **no se valida**. | **ALTA** | `evaluar_walk_forward` SÍ tiene 2ª línea de defensa y RECHAZA nombres sin metadatos (probado: `mi_feature` derivada de `y.shift(-1)` → `ValueError: FUGA DE DATOS POTENCIAL`). El agujero queda solo si el agente declara la nueva en el JSON (puede: `model.py` tiene permiso de escritura del repo) o usa H1. La segunda línea mitiga el caso ingenuo, pero el AVISO no es un control. | En el harness, tras `seleccionar_features`, **fallar (no avisar)** si hay features nuevas no declaradas conformes: `if nuevas: raise ValueError(...)`. Forzar que toda feature nueva se declare vía el flujo de `declarar()` en `construir_tabla_maestra.py`, no a mano en el JSON. |
| H3 | `evaluacion.py` | **`saltar_antifuga=True` acepta CUALQUIER columna sin restricción de lag.** El docstring dice "SOLO baselines de persistencia/estacional", pero no hay enforcement. | **MEDIA** | Probado: `evaluar_walk_forward(df, ["mi_feature"=y.shift(-1)], ..., saltar_antifuga=True)` corre sin chistar (MAPE 7.10%). Hoy solo lo usa `persistencia_lag1` (legítimo, lag≥1). Riesgo latente: cualquier caller futuro lo abusa. | Restringir el bypass: cuando `saltar_antifuga=True`, exigir que `columnas_features ⊆ {columnas que son la serie objetivo con lag≥1}` (whitelist explícita de nombres `costo_lag\d+` con lag≥1), o exponer un parámetro `motivo` + log obligatorio. |
| H4 | `evaluacion.py::_metricas` | **MAPE y MAE/RMSE se calculan sobre poblaciones distintas.** MAPE filtra `real != 0` (`err[con_base]/real[con_base]`), MAE/RMSE/sesgo usan todos. Además el MAPE no protege contra `real` pequeño-pero-no-cero (denominador explota) ni documenta el filtrado. El sesgo de MAPE con `real` negativos usa `|err/real|` con signo en el denominador implícito vía división — correcto en magnitud pero no excluye negativos. | **MEDIA** | `_metricas(real=[0,100,-50,200], pred=[50,110,-40,180])` → MAPE=13.33% (excluye el cero), MAE=22.5 (lo incluye). Con `real=[1, 1e7]` el MAPE=50% lo domina el valor ~0. En la tabla sintética **no muerde** (objetivo min=5.8M USD, 0 ceros, 0 negativos), pero el proxy real Σdemanda·CMg colapsa a ~0 en horas de vertimiento solar (advertido en `catalogo_fuentes.md` C1) → con datos reales el MAPE será inestable. | (a) Loggear `n` excluido del MAPE y reportarlo en `ResultadoEvaluacion`; (b) usar un piso/epsilon o sMAPE/WAPE como métrica secundaria robusta; (c) si el objetivo puede ser ≤0, abortar o documentar. No cambiar la métrica canónica sin decisión en `wiki/decisiones.md`, pero **declarar la limitación**. |
| H5 | `evaluacion.py` | **El último corte puede generar un fold con `n_test` pequeño** (cola < 28 días). No es fuga, pero diluye/infla el MAPE global al mezclar folds de tamaño desigual (MAPE global pondera por observación, no por fold — correcto, pero los folds parciales reciben menos peso del esperado). | **BAJA** | El bucle corre `while corte <= fechas.iloc[-1]`; el último fold cubre `[corte, corte+28)` truncado por los datos. 85 folds, N=2353. No afecta la validez, solo la interpretación por-fold. | Documentar; opcionalmente descartar el último fold parcial o reportar su tamaño. Sin acción urgente. |
| H6 | `construir_tabla_maestra.py` | **Shift POSICIONAL pre-merge en demanda/generación/embalses/CMg.** Los `shift(LAG_CEN)` se aplican sobre dataframes agregados por fecha ANTES del merge, no por calendario. Si faltan días en esos raw, `shift(2)` por posición trae T-3 (o más viejo), no T-2. | **BAJA** (dirección del error: **CONSERVADORA**, no fuga) | Demostré formalmente: con groupby ascendente y fechas únicas, una fecha faltante hace que `shift(2)` traiga un dato **más antiguo** (T-3), nunca más nuevo → degrada a staleness, **nunca adelanta el futuro**. Verifiqué empíricamente que en la tabla sintética NO hay huecos en demanda/generación/embalses/CMg (0 faltantes) y los 100 puntos aleatorios alinean perfecto por calendario. Combustibles SÍ tiene 776 huecos (días no hábiles) pero usa `asfreq("D").ffill()` ANTES del shift → alineación por calendario correcta (100/100). | Robustecer para datos reales: reindexar cada agregado diario a un calendario completo (`asfreq("D")`) ANTES de `shift(LAG)`, como ya se hace en combustibles y clima_observado. Hoy demanda/gen/embalses/cmg NO lo hacen — funciona porque el sintético no tiene huecos, pero el CEN real sí tendrá. Esto es el parche más importante para producción. |
| H7 | `metadatos_features.json` | **`costo_lag3` declara `lag_dias: 2`** (debería ser 3). Declaración "mentirosa" menor: la nota copiada dice lag≥2. | **BAJA** | El JSON declara `costo_lag3 → lag_dias: 2`. El código (`construir_tabla_maestra.py` L131) agrupa lag 3 en el bloque `declarar(..., 2, ...)`. La feature en sí es conforme (lag real 3 ≥ 2), pero el metadato miente sobre el lag exacto. Verifiqué `costo_lag3[T]==costo_op_usd[T-3]` (100/100). | En `declarar`, emitir el lag real por columna en vez de un lag fijo de bloque, o al menos documentar que `lag_dias` del bloque es un mínimo. |
| H8 | `construir_tabla_maestra.py` | **`cmg_programado_d1` se declara en metadatos pero NUNCA se computa como columna del parquet.** Declaración fantasma. | **BAJA** (sin impacto: está marcada no-conforme) | La tabla tiene 126 columnas; `cmg_programado_d1` está en el JSON pero NO en el parquet (verificado: `declaradas NO en tabla: ['cmg_programado_d1']`). Como `cumple_regla_2000=false`, nunca entraría a features igual. Es ruido, no riesgo. | Declarar solo columnas existentes, o generar la columna (NaN) para coherencia. Cosmético. |

---

## Verificaciones empíricas (output)

### (a) Smell test de dirección de shift — correlación con objetivo futuro vs pasado
Para cada feature numérica calculé `corr(x[T], y[T])`, el máximo `|corr(x[T], y[T+1..3])|` (futuro) y `|corr(x[T], y[T-1..7])|` (pasado).

```
features cuya correlacion con el objetivo FUTURO supera (>0.02) a la del presente/pasado:
  NINGUNA — direccion de shifts consistente
corr(costo_lag2[T], y[T-2]) = 1.0   # identidad perfecta, alineacion correcta
```
**Veredicto:** no hay ninguna feature que "vea el futuro". Todas correlacionan máximo con el pasado/presente. Smell test limpio.

### (b) Alineación por CALENDARIO de los lags del costo (100 fechas aleatorias)
```
costo_lag1: 100/100   costo_lag2: 100/100   costo_lag3: 100/100
costo_lag7: 100/100   costo_lag14: 100/100  costo_lag21: 100/100  costo_lag28: 100/100
costo_ma7:  100/100 == mean(costo[T-8..T-2])   -> usa solo <= T-2: SI
costo_ma28: 100/100 == mean(costo[T-29..T-2])
```
Y contra los raw sintéticos:
```
demanda_total_mwh[T] == raw_sum[T-2]: 100/100
gen_solar[T]         == raw[T-2]:     100/100
cota_colbun[T]       == raw[T-2]:     100/100
cmg_medio[T]         == raw_mean[T-3]:100/100
fx_brent[T]          == ffill(raw)[T-1]:100/100
pron_temp_santiago[T]== raw_previous_day2[T] (lag 0): 100/100
```
**El `costo_ma7 = shift(2).rolling(7)` SÍ usa solo datos ≤ T-2** (confirmado: equivale a `mean(costo[T-8..T-2])`). El pivot de pronóstico lag 0 es legítimo: el raw solo contiene `lead='previous_day2'` (emitido ~48h antes), nunca clima observado de T.

### (c) Huecos de fechas (fase 2b)
```
tabla_maestra: 0 fechas faltantes, 0 duplicadas, 0 NaN en objetivo, 0 ceros, 0 negativos (min=5.81M USD)
raw cen_demanda/cen_generacion/cen_embalses/cen_cmg_real: 0 huecos
raw combustibles: 776 huecos (días no hábiles, ESPERADO — manejado con asfreq+ffill)
```
Demostración de la dirección del error con hueco posicional:
```
fila 2025-01-05 (falta 2025-01-04) con shift(2) recibe v de 2025-01-02 = T-3 (mas viejo) => CONSERVADOR, no fuga
```

### (d) Reproducción manual de un fold + números del wiki
```
persistencia_lag2: MAPE=8.87 (wiki: 8.87)  folds=85  N=2353
estacional:        MAPE=6.59 (wiki: 6.59)  folds=85  N=2353
lightgbm_baseline: MAPE=6.85 (wiki: 6.85)  sesgo=+265,772  n_feats=122

fold 3 a mano:    MAPE=6.576341  MAE=732963.61  n_test=28  corte=2020-03-25
fold 3 protocolo: MAPE=6.576341  MAE=732963.61  n_test=28  corte=2020-03-25
identicos: True

fold 0: corte=2020-01-01; max(fecha train)=2019-12-31, min(fecha test)=2020-01-01  -> sin solape
```
**El primer fold NO ve datos de test** (train termina 2019-12-31, test empieza 2020-01-01). El re-instanciado por fold es real (`constructor_modelo()` se llama dentro del bucle, L159). No hay shuffle (`sort_values` + assert de monotonía). Los cuatro números del wiki reproducen al decimal.

---

## Veredicto final

**¿Los números de `wiki/resultados_baselines.md` son defendibles? SÍ, con dos asteriscos.**

1. **Metodológicamente, los números son correctos y reproducibles.** El walk-forward está bien implementado (expansivo, sin shuffle, sin solape train/test, re-instancia por fold), los lags están correctamente alineados por calendario, no hay fuga de datos activa, y los cuatro MAPE reproducen exactamente. El smell test de correlaciones es limpio. No pude demostrar fuga en el pipeline tal como corre hoy.

2. **Asterisco 1 — son datos SINTÉTICOS.** El propio wiki lo advierte en negrita. No son métricas del problema real; validan la maquinaria. La maquinaria está bien validada.

3. **Asterisco 2 — el objetivo proxy (Σdemanda·CMg) no es defendible ante el CEN** (advertido en `catalogo_fuentes.md` C1: rentas inframarginales, colapso en vertimiento solar, sesgo no estacionario). Esto es una limitación del *label*, no del pipeline, pero acota qué significan los números.

**Lo que un revisor externo debe exigir antes de pasar a datos reales:**
- **H1 (CRÍTICA):** cerrar el agujero de mutación de `df` en `seleccionar_features` — hoy un experimentador puede fabricar MAPE arbitrariamente bajo sobrescribiendo una columna conforme con el label, y todos los chequeos pasan. Es la diferencia entre "anti-fuga real" y "anti-fuga teatral".
- **H6 (BAJA hoy, importante en prod):** reindexar a calendario completo antes de los `shift()` posicionales en demanda/generación/embalses/CMg. El error es conservador (nunca adelanta el futuro), pero con los huecos reales del CEN introducirá staleness silenciosa.
- **H4:** declarar la limitación del MAPE con objetivo que puede colapsar a ~0 bajo el proxy real.

Los hallazgos H1-H3 son de **gobernanza/superficie de ataque** (un agente malicioso o descuidado), no fugas presentes. El pipeline que generó los números del wiki es honesto; la *defensa* contra fugas futuras tiene agujeros parcheables.

---

## Estado de los parches (post-auditoría, misma sesión 2026-06-12)

| Hallazgo | Parche aplicado | Verificación |
|----------|-----------------|--------------|
| H1 (CRÍTICA) | `harness.py::_features_del_modelo`: el modelo recibe copia SIN columna objetivo; columnas conformes verificadas intactas tras la selección | Exploit reproducido y bloqueado (ValueError); label confirmado inaccesible |
| H2 (ALTA) | Features nuevas: test de invarianza a truncamiento (60 días) + registro en overlay de metadatos para el gate canónico | `shift(-1)` y normalización con stats globales bloqueados; derivada causal legítima aceptada |
| H3 (MEDIA) | `evaluacion.py`: `saltar_antifuga` solo admite lags puros del objetivo (lista cerrada) | ValueError con cualquier otra columna |
| H4 (MEDIA) | Documentado en `_metricas` + warning cuando MAPE excluye días con objetivo 0 | docstring + log |
| H6 (BAJA) | `construir_tabla_maestra.py::_a_calendario`: reindex a calendario continuo antes de cada shift (demanda, generación, embalses, CMg) | Tabla reconstruida; baselines reproducen exacto (sintéticos sin huecos) |
| H7 (BAJA) | Cada `costo_lagK` declara su lag real | metadatos regenerados |
| H8 (BAJA) | `cmg_programado_d1` anotada como "columna aún no materializada (pre-registro)" | metadatos regenerados |

Re-corrida end-to-end post-parches: `exp001_objetivo_l1` reproduce MAPE 4.551 exacto.
