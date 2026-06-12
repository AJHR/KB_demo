# Fuente de calendario para el modelo de costo de operación del SEN

**Fase 1 — Investigación de fuentes de datos · 2026-06-12**
**Estado: VERIFICADA LOCALMENTE** (única fuente 100% offline del proyecto: librería Python `holidays`, validada con código ejecutado en el sandbox).

---

## 1. Validación local de la librería `holidays` (PyPI)

- **Versión instalada:** `holidays==0.98` (`pip install holidays` funcionó sin problemas; sin dependencias pesadas: solo `python-dateutil`).
- **Cobertura validada:** 2019-2027 → **148 feriados nacionales** generados sin error. Idioma por defecto `es` (soporta `en_US`, `uk`).

### 1.1 Output real — feriados nacionales 2026

```
$ python /tmp/validate_holidays.py
=== holidays version: 0.98 ===
Total feriados nacionales 2019-2027: 148

--- Feriados Chile 2026 (nacional) ---
2026-01-01 (Thu): Año Nuevo
2026-04-03 (Fri): Viernes Santo
2026-04-04 (Sat): Sábado Santo
2026-05-01 (Fri): Día Nacional del Trabajo
2026-05-21 (Thu): Día de las Glorias Navales
2026-06-21 (Sun): Día Nacional de los Pueblos Indígenas
2026-06-29 (Mon): San Pedro y San Pablo
2026-07-16 (Thu): Virgen del Carmen
2026-08-15 (Sat): Asunción de la Virgen
2026-09-18 (Fri): Día de la Independencia
2026-09-19 (Sat): Día de las Glorias del Ejército
2026-10-12 (Mon): Día del Encuentro de dos Mundos
2026-10-31 (Sat): Día Nacional de las Iglesias Evangélicas y Protestantes
2026-11-01 (Sun): Día de Todos los Santos
2026-12-08 (Tue): La Inmaculada Concepción
2026-12-25 (Fri): Navidad
```

Coincide 1:1 con el calendario oficial 2026 publicado (16 feriados nacionales, fuentes web abajo).

### 1.2 Feriados fijos clave — chequeo programático 2019-2027

Se verificó por código que **todos los años 2019-2027** contienen: 1-ene, 1-may, 21-may, 16-jul, 18-sep, 19-sep, 25-dic.

```
--- Check feriados fijos 2019-2027 ---
Todos los fijos presentes 2019-2027: True
```

### 1.3 Feriados móviles — reglas legales correctamente implementadas

**Viernes Santo / Sábado Santo** (Pascua, cómputo astronómico): presente todos los años, fechas correctas (2024-03-29, 2025-04-18, 2026-04-03, 2027-03-26).

**Ley 19.668 (traslado al lunes)** — aplica a San Pedro y San Pablo (29-jun) y Encuentro de Dos Mundos (12-oct): si caen martes/miércoles/jueves se trasladan al lunes anterior; si caen sáb/dom/lun no se mueven. Output real:

```
--- San Pedro y San Pablo ---
2021: 2021-06-28 (Mon)  [29-jun cae Tue]   <- trasladado
2022: 2022-06-27 (Mon)  [29-jun cae Wed]   <- trasladado
2023: 2023-06-26 (Mon)  [29-jun cae Thu]   <- trasladado
2024: 2024-06-29 (Sat)  [no se mueve]
2025: 2025-06-29 (Sun)  [no se mueve]
2027: 2027-06-28 (Mon)  [29-jun cae Tue]   <- trasladado
(idéntico patrón para 12-oct: 2021->11-oct, 2022->10-oct, 2023->09-oct, 2027->11-oct)
```

**Ley 21.357 — Día Nacional de los Pueblos Indígenas** (solsticio de invierno, varía 20/21-jun): implementado correctamente (2024 y 2025: 20-jun; 2021-2023 y 2026-2027: 21-jun).

**Ley 20.983 — 2 de enero feriado cuando 1-ene cae domingo**: verificado (2017 y 2023 → `True`, "Feriado nacional"; 2028, donde 1-ene cae sábado → `False`, correcto).

**21 de mayo (Combate Naval de Iquique / Glorias Navales)**: fijo, NO trasladable; presente todos los años (sec. 1.2).

### 1.4 Feriados regionales — soportados vía `subdiv`

16 subdivisiones ISO 3166-2:CL: `('AI','AN','AP','AR','AT','BI','CO','LI','LL','LR','MA','ML','NB','RM','TA','VS')`. Output real (diferencia vs nacional, 2026):

```
--- Regional AP 2026 ---
2026-06-07: Asalto y Toma del Morro de Arica          (Ley 20.663)
--- Regional NB 2026 ---
2026-08-20: Nacimiento del Prócer de la Independencia (Chillán y Chillán Viejo)  (Ley 20.768)
```

⚠️ Matiz: la librería asigna el 20-ago a toda la subdivisión `NB` (Ñuble), pero legalmente aplica solo a las comunas de Chillán y Chillán Viejo. Para un modelo zonal del SEN el impacto es de segundo orden.

### 1.5 Limitaciones encontradas (gaps que el modelo debe cubrir aparte)

1. **NO distingue feriados irrenunciables.** Categorías soportadas: solo `('bank', 'public')` (`bank` = 31-dic feriado bancario). El flag irrenunciable debe mantenerse como tabla propia (es estable: Ley 19.973 → 1-ene, 1-may, 18-sep, 19-sep, 25-dic, más días de elección con voto obligatorio).
2. **NO incluye feriados electorales ni censos.** Búsqueda programática por regex (`elecci|plebis|censo`) sobre 2019-2027: **0 resultados**. Faltan, p. ej.: plebiscito 25-oct-2020, elecciones 15/16-may-2021, 21-nov-2021, 19-dic-2021, plebiscito 4-sep-2022, 7-may-2023, 17-dic-2023, municipales 26/27-oct-2024, presidencial 16-nov-2025 y balotaje 14-dic-2025. **Crítico para el histórico de entrenamiento** → tabla manual (sección 4).
3. Las entradas son solo `date -> str` (sin metadatos de tipo de feriado).
4. Feriados nuevos decretados requieren `pip install -U holidays` (lag de release) → mantener tabla de overrides.

---

## 2. Tabla de fuentes

| Fuente | Tipo | Acceso / costo | Cobertura | Estado de validación |
|---|---|---|---|---|
| **`holidays` (PyPI) v0.98** | Librería Python, offline | Gratuita, MIT | Feriados nacionales + 16 regiones, 1915→futuro (regla) | **VERIFICADA LOCALMENTE** (código ejecutado, output arriba) |
| [feriadosapp.com/api](https://www.feriadosapp.com/api) | API REST JSON | **Gratuita, sin restricciones declaradas** (sin SLA formal) | Feriados legales de Chile del año en curso; incluye flag irrenunciable según su documentación | NO validada (red saliente bloqueada en sandbox); usar como **verificación cruzada** desde entorno con red. Listada en [listado de APIs públicas chilenas](https://github.com/juanbrujo/listado-apis-publicas-en-chile) |
| [feriados.cl](https://www.feriados.cl/) | Sitio web (calendario) | Gratuito; sin API documentada → scraping | Feriados por año, nota irrenunciables | NO validada; verificación visual/cruzada |
| [Ley Chile (BCN)](https://www.bcn.cl/leychile/Navegar?idNorma=1211955) | Texto legal oficial | Gratuito | Leyes y decretos (19.668, 19.973, 20.983, 21.357, D.224/2022, D.93/2025) | Fuente autoritativa de respaldo |
| Servel + prensa ([calendario electoral hasta 2029](https://www.biobiochile.cl/noticias/servicios/toma-nota/2025/11/17/cuando-son-las-proximas-elecciones-revisa-el-calendario-electoral-hasta-2029.shtml)) | Calendario electoral | Gratuito, no programático | Elecciones futuras con fecha legal fija | Verificada vía WebSearch |
| [Mineduc / Ayuda Mineduc](https://www.ayudamineduc.cl/ficha/calendarios-escolares-2026) | Calendario escolar anual por región | Gratuito, no programático (resoluciones anuales) | Vacaciones escolares por región | Verificada vía WebSearch (2026) |

**Decisión propuesta:** `holidays` (pinneada por versión) como fuente primaria offline + tabla manual `calendario_overrides.csv` en el repo (elecciones, feriados decretados, eventos especiales) + verificación cruzada anual contra feriadosapp.com.

---

## 3. Cambio de hora — regla vigente (verificada vía WebSearch)

- **Regla (Decreto 224/2022, vigente hasta abril 2026):** horario de invierno (UTC-4) comienza a las **24:00 del primer sábado de abril** (atraso 60 min); horario de verano (UTC-3) comienza a las **24:00 del primer sábado de septiembre** (adelanto 60 min). En 2026: cambio el sábado 4-abr; retorno a verano el sábado 5-sep ([Emol](https://www.emol.com/noticias/Nacional/2026/04/04/1196259/cambio-de-hora-abril-invierno.html), [Reporte Minero](https://www.reporteminero.cl/noticia/noticias/2026/03/cambio-de-hora-chile-fecha-2026-horario-invierno)).
- **Excepciones:** Magallanes (UTC-3 permanente desde 2017) y **Aysén (UTC-3 permanente desde marzo 2025, Decreto 93/2025**, consulta ciudadana 94% a favor) ([CNN Chile](https://www.cnnchile.com/pais/region-de-aysen-mantendra-horario-de-verano-todo-el-ano_20250320/), [BCN](https://www.bcn.cl/leychile/Navegar?idNorma=1211955)).
- ⚠️ El decreto vigente cubre **solo hasta abril 2026**; a mayo 2026 aún se discutía si se mantendrá el esquema o se fijará un horario permanente ([El Mostrador](https://www.elmostrador.cl/datos-utiles/2026/05/18/se-acaba-el-cambio-de-hora-la-razon-por-la-que-podrias-quedarte-en-el-horario-de-invierno-este-ano/)). **Recomendación: no hard-codear la regla; derivar el flag DST de la tz IANA `America/Santiago` con `tzdata` actualizada** (y `America/Punta_Arenas` / `America/Coyhaique` para zonas australes).

---

## 4. Cambios legales recientes y elecciones (WebSearch 2025-2026)

- **2026: sin feriados nacionales nuevos.** Calendario oficial 2026 = 16 feriados nacionales + 2 regionales/comunales (7-jun AP, 20-ago Chillán), 5 irrenunciables (1-ene, 1-may, 18/19-sep, 25-dic) ([24horas](https://www.24horas.cl/te-sirve/feriados-en-chile/calendario-2026-oficial-chile-feriados), [feriados.cl](https://www.feriados.cl/), [Buk](https://www.buk.cl/blog/feriados-2026-chile-cuales-son-irrenunciables)).
- **Irrenunciables sin cambios legales**: siguen regidos por Ley 19.973 art. 2 ([Dirección del Trabajo](https://www.dt.gob.cl/portal/1628/w3-article-95017.html)). Existe una propuesta CPC de reordenar feriados, **en discusión sin fecha de aprobación** a marzo 2026 ([Buk](https://www.buk.cl/blog/feriados-irrenunciables-chile)) → monitorear.
- **Calendario electoral** (días feriados legales con voto obligatorio, ausentes en `holidays`): tras el balotaje del 14-dic-2025, "pausa electoral" de ~30 meses. Próximos hitos: primarias 9-jul-2028 (voluntario), **municipales/regionales 29-oct-2028**, 2.ª vuelta gobernadores 26-nov-2028, primarias 1-jul-2029, **presidencial/parlamentaria 18-nov-2029**, balotaje 16-dic-2029 ([El Mostrador](https://www.elmostrador.cl/datos-utiles/2025/12/21/cuando-son-las-proximas-elecciones-en-chile-asi-queda-el-calendario-electoral-a-partir-del-2026/), [T13](https://www.13.cl/programas/servicios-13/actualidad/cuando-son-las-proximas-elecciones-en-chile-revisa-el-calendario)).

### Tabla manual de eventos electorales (histórico para entrenamiento, a mantener en el repo)

| Fecha | Evento | Voto | Nota |
|---|---|---|---|
| 2020-10-25 | Plebiscito nacional | Voluntario | Domingo |
| 2021-05-15/16 | Convencionales + municipales | Voluntario | Dos días (sáb-dom) |
| 2021-06-13 | 2.ª vuelta gobernadores | Voluntario | |
| 2021-07-18 | Primarias presidenciales | Voluntario | |
| 2021-11-21 | Presidencial/parlamentaria | Voluntario | |
| 2021-12-19 | Balotaje presidencial | Voluntario | |
| 2022-09-04 | Plebiscito de salida | **Obligatorio** | |
| 2023-05-07 | Consejeros constitucionales | **Obligatorio** | |
| 2023-12-17 | Plebiscito constitucional | **Obligatorio** | |
| 2024-10-26/27 | Municipales/regionales | **Obligatorio** | Dos días |
| 2024-11-24 | 2.ª vuelta gobernadores | **Obligatorio** | |
| 2025-06-29 | Primarias presidenciales | Voluntario | Coincide con feriado San Pedro y San Pablo |
| 2025-11-16 | Presidencial/parlamentaria | **Obligatorio** | |
| 2025-12-14 | Balotaje presidencial | **Obligatorio** | |
| 2028-10-29 | Municipales/regionales | **Obligatorio** | Futuro (Servel) |
| 2029-11-18 | Presidencial/parlamentaria | **Obligatorio** | Futuro (Servel) |

**Censos:** el Censo 2017 (19-abr-2017) fue feriado irrenunciable de un día; el Censo 2024 se realizó durante meses sin feriado. Próximo censo de un día: sin fecha. → fila en la misma tabla manual.
**Eventos masivos** (Teletón ~fin de noviembre/inicio de diciembre, partidos de la selección, conciertos grandes): sin fuente programática → tabla manual `eventos_especiales.csv` con fecha, tipo, alcance (nacional/RM) y hora aproximada.

---

## 5. Features de calendario propuestas para el modelo

Granularidad base: día (expandible a horaria). Todas derivables offline de `holidays` + tablas manuales + tzdata.

| # | Feature | Tipo | Definición precisa |
|---|---|---|---|
| 1 | `dow` | categórica 0-6 | Día de la semana (lunes=0, domingo=6). |
| 2 | `month` | categórica 1-12 | Mes calendario. Capturar estacionalidad junto con features climáticas. |
| 3 | `is_weekend` | binaria | `dow >= 5`. |
| 4 | `is_holiday` | binaria | Fecha ∈ `holidays.Chile(years=y)` ∪ tabla manual (elecciones, decretados). Para modelo zonal: variante `is_holiday_regional(subdiv)` con `subdiv='AP'`/`'NB'`. |
| 5 | `is_irrenunciable` | binaria | Fecha ∈ {1-ene, 1-may, 18-sep, 19-sep, 25-dic} ∪ {elecciones con voto obligatorio}. Comercio cerrado por ley → caída adicional de demanda diurna. NO viene de la librería: tabla propia. |
| 6 | `is_sandwich` | binaria | Día hábil (lun-vie, no feriado) cuyo día anterior **y** posterior son ambos no laborables (feriado o fin de semana). Ej.: viernes tras feriado en jueves (22-may-2026, 17-jul-2026... no aplica si el feriado se trasladó por Ley 19.668). Proxy de ausentismo/puente. |
| 7 | `is_holiday_eve` | binaria | Día siguiente es feriado (`is_holiday(d+1)`). Variante `is_irrenunciable_eve`: comercio extiende horario la víspera → mayor demanda vespertina. |
| 8 | `is_fiestas_patrias_week` | binaria | Ventana fija [15-sep, 20-sep] más cualquier feriado puente decretado ese año (override manual). Semana con caída sostenida de demanda industrial. |
| 9 | `school_summer_break` | binaria | Desde ~última semana de diciembre (fin año escolar) hasta inicio de clases de marzo según calendario Mineduc del año; aproximación robusta: 1-ene → último día de febrero. |
| 10 | `school_winter_break` | binaria **por región** | Ventana del calendario Mineduc anual. ⚠️ No siempre es "dos semanas de julio": en 2026 zona central (Atacama-Los Ríos, incl. RM) fue 22-jun a 3-jul; Antofagasta/Los Lagos 6-jul a 17-jul; AP/Tarapacá 13-jul a 24-jul; Aysén/Magallanes 3 semanas (29-jun a 17-jul) ([CNN Chile](https://www.cnnchile.com/servicios/vacaciones-invierno-escolares-2026/), [Mineduc](https://www.mineduc.cl/ministerio-de-educacion-oficializa-el-calendario-escolar-2026/)). Actualizar cada año. |
| 11 | `is_dst` | binaria | Hora oficial en UTC-3 (verano) vs UTC-4 (invierno) para Chile continental. Derivar de tz IANA `America/Santiago`, no de regla fija. Magallanes y Aysén: siempre UTC-3 (sin feature). |
| 12 | `days_since_dst_change` | entera (0-14, cap) | Días desde la última transición; captura el ajuste transitorio del perfil de iluminación/demanda vespertina. |
| 13 | `is_election_day` / `is_election_eve` | binarias | Desde tabla manual (sección 4); distinguir voto obligatorio (feriado legal, perfil tipo domingo) de voluntario. |
| 14 | `special_event` | categórica | Desde `eventos_especiales.csv`: censo de un día, Teletón, eventos masivos. Default `none`. |

---

## 6. Riesgos

1. **Feriados decretados con poca anticipación** (riesgo principal): Chile ha creado feriados puntuales por ley con semanas o días de aviso (ej. lunes 17-sep-2018, feriados puente de Fiestas Patrias; feriados electorales definidos por calendario legal pero el balotaje se confirma ~4 semanas antes). La librería `holidays` los incorpora con lag de release. **Mitigación:** tabla `calendario_overrides.csv` versionada en el repo con prioridad sobre la librería + chequeo mensual contra feriadosapp.com/prensa.
2. **Regla de cambio de hora sin garantía post-abril-2026:** el Decreto 224 expiró; existe discusión pública de fijar un horario permanente. Mitigación: usar `tzdata`/IANA actualizada, nunca la regla "primer sábado" hard-codeada.
3. **Cambios legales en irrenunciables:** propuesta CPC en trámite (sin ley a la fecha). Bajo riesgo en horizonte 2026-2027, monitorear.
4. **feriadosapp.com sin SLA:** API comunitaria gratuita; no usarla como dependencia de runtime, solo verificación cruzada.
5. **Granularidad regional imperfecta:** `NB` en la librería marca toda la región Ñuble cuando la ley cubre 2 comunas; calendario escolar es regional y cambia cada año.
6. **Histórico electoral ausente en la librería:** si se entrena con `holidays` "a secas", los días 25-oct-2020, 4-sep-2022, 16-nov-2025, etc. quedan etiquetados como días normales siendo feriados legales con perfil de demanda atípico → sesgo. La tabla manual de la sección 4 es **obligatoria** antes de entrenar.

---

*Generado y validado el 2026-06-12. Scripts de validación: `/tmp/validate_holidays.py`, `/tmp/validate2.py` (ejecutados con `holidays==0.98`, Python 3.11).*
