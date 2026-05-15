---
title: PMGD y generacion distribuida — marco regulatorio actualizado 2026
sources:
  - sources/regulation-cne-reglamentos-mercado/2026.02.19_NTCO-PMGD-2026.pdf
  - sources/regulation-cne-reglamentos-mercado/Reglamento_Sistemas_Medianos_DS_229_xdoc_12x.pdf
  - sources/regulation-cne-reglamentos-mercado/DOC23_-_reglamento_electrico.pdf
  - sources/regulation-minenergia-marco-regulatorio/2._iir_decreto_que_modifica_reglamento_de_transferencias_de_potencia_entre_empresas.pdf
  - sources/regulation-minenergia-marco-regulatorio/5._iir_estabilizacion_tarifaria.pdf
last_synthesized: 2026-05-15
---

# PMGD y generacion distribuida — marco regulatorio actualizado 2026

> Para proyectos de hasta 9 MW conectados en media tension. La norma vigente es la **NTCO-PMGD de febrero 2026** publicada por la CNE.

## 1. Que es un PMGD

**Pequeno Medio de Generacion Distribuida**: central con potencia conectada al sistema de distribucion (no transmision) menor o igual a 9 MW. Su regimen tiene reglas especificas porque opera con una contraparte distinta (la distribuidora local), tiene plazos y procedimientos mas livianos, y accede a un precio estabilizado que la diferencia del mercado mayorista pleno.

La norma rectora actual es la **Norma Tecnica de Conexion y Operacion de PMGD en Instalaciones de Media Tension**, version febrero 2026 (`sources/regulation-cne-reglamentos-mercado/2026.02.19_NTCO-PMGD-2026.pdf`, 138 paginas).

## 2. Estructura de la NTCO-PMGD 2026

Capitulos y temas clave (del indice oficial):

| Capitulo | Tema |
|----------|------|
| 1 | Terminologia y exigencias generales (objetivos, alcance, otras tecnologias, plazos, formularios) |
| 1 (cont) | **Bloques horarios de inyeccion para PMGD con componente de almacenamiento** (Art. 1-11) |
| 2 | Informacion publica de redes de distribucion (estandares constructivos, sistemas de generacion) |
| 3 | **Procedimiento de Conexion** (SCR, cronograma, admisibilidad, proceso expeditivo, escenarios de demanda, flujos, cortocircuito, coordinacion de protecciones, transmision zonal) |
| 3-5 | Limitacion de inyecciones cuando se conecta a servicios auxiliares |
| 4 | **Factor de Referenciacion (FR)** — clave para remuneracion: responsabilidad del calculo, metodologia, distribucion de demanda |
| 5/6 | Auditorias y monitoreo |
| 7 | Exigencias tecnicas para conexion al sistema de distribucion |

Articulos especificos relevantes para un nuevo proyecto:
- **Art. 1-7** Procedimientos de Conexion y Entrada en Operacion
- **Art. 1-10** Valorizacion Actividades para la Conexion
- **Art. 1-11** Bloques horarios para PMGD con almacenamiento (BESS)
- **Art. 3-3** Solicitud de Conexion a la Red (SCR)
- **Art. 3-6** Declaracion de Admisibilidad
- **Art. 3-9** Calificacion del Proceso Expeditivo (via rapida)
- **Art. 3-29** PMGD con Componente de Almacenamiento
- **Art. 3-34** Analisis de Flujos de Potencia en Transmision Zonal
- **Art. 3-37** Informe de Criterios de Conexion + Informe de Costos
- **Art. 3-52/3-53** Pruebas de Puesta en Servicio (PES)
- **Art. 4-6** Calculo del Factor de Referenciacion

## 3. Que cambia con BESS (lo nuevo de 2026)

El gran cambio de esta version es el reconocimiento de **PMGD con componente de almacenamiento**: la norma incluye reglas especificas para baterias que permiten **inyectar segun bloques horarios**, en vez de solo seguir el recurso primario. Esto cambia la rentabilidad: un PMGD solar+BESS puede vender en horas de alta CMg (no solo medio dia).

Articulos clave: 1-11 (bloques horarios), 3-29 (modelamiento), y el Capitulo 4 completo (Factor de Referenciacion ajustado para almacenamiento).

## 4. Sistemas Medianos: el otro regimen especial

Sistemas aislados o quasi-aislados (Aysen, Magallanes, etc.) tienen su propio reglamento: **DS 229/2014** (`Reglamento_Sistemas_Medianos_DS_229_xdoc_12x.pdf`). Si el proyecto esta en zona de Sistema Mediano (no SEN), la NTCO-PMGD no aplica directamente y rige el regimen del DS 229. Los decretos de fijacion de precios para sistemas medianos estan en `sources/regulation-cne-normas-tecnicas/` (decretos de los sistemas Hornopiren, Cochamo, Aysen-Palena-G.Carrera, Pta.Arenas-Pto.Natales-Porvenir-Pto.Williams).

## 5. Estabilizacion tarifaria

El regimen de **precios estabilizados** (que es el que reciben PMGD por defecto si no negocian PPA) ha tenido modificaciones recientes. El informe de impacto regulatorio del decreto de estabilizacion esta en `sources/regulation-minenergia-marco-regulatorio/5._iir_estabilizacion_tarifaria.pdf`.

## 6. Transferencias de potencia (afecta a PMGD)

La modificacion al reglamento de transferencias de potencia entre empresas (`2._iir_decreto_que_modifica_reglamento_de_transferencias_de_potencia_entre_empresas.pdf`) ajusta como se reconoce y paga la potencia firme de **todos** los generadores, PMGD incluidos. Para un solar PMGD sin BESS la potencia firme es estructuralmente baja; con BESS sube.

## 7. Lagunas conocidas

- No quedo capturado el **DS 244** (reglamento de medios de generacion no convencionales y pequenos medios de generacion, anterior a la NTCO-PMGD 2026 pero que sigue siendo referencia historica). Esta en `cne.cl/normativas/electrica/sector-electrico/` con filtros que no agarraron — reintentar.
- Faltan las **plantillas y formularios oficiales** de la SCR (Solicitud de Conexion a la Red) — viven en el portal del Coordinador.
- Falta el **Pliego Tecnico Normalizado** (PTN) del CEN aplicable a PMGD.

## 8. Para profundizar

- Mercado mayorista (donde PMGD se conecta para inyectar) → `wiki/mercado-mayorista-chile.md`
- Servicios complementarios y transferencias → `wiki/servicios-complementarios-y-transferencias.md`
- Conexion fisica y transmision (transmision zonal aguas arriba del punto PMGD) → `wiki/conexion-y-transmision.md`
