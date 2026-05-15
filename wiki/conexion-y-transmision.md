---
title: Conexion al SEN y regimen de transmision para generadores
sources:
  - sources/regulation-cne-reglamentos-mercado/DS_144_2009_-_Reglamento_Administrativo_de_Substransmisixn.pdf
  - sources/regulation-cne-reglamentos-mercado/DS_48_2009_Reglamento_Procedimiento_Realizacion_Estudio_Transmision_Troncal.pdf
  - sources/regulation-cne-reglamentos-mercado/DOC23_-_reglamento_electrico.pdf
  - sources/regulation-coordinador-desarrollo-transmision/2026-04-13-JORNADA-TECNICA-TRANSMISION.pdf
  - sources/regulation-coordinador-desarrollo-transmision/2026-04-16-CONTROL-DINAMICO-DE-TENSION.pdf
  - sources/regulation-coordinador-desarrollo-transmision/2026-04-13-DESAFIOS-DE-LA-INTEGRACION-MASIVA-DE-BESS-AL-SEN.pdf
  - sources/regulation-coordinador-desarrollo-transmision/2026-04-23-INFORME-MONITOREO-2025-.pdf
  - sources/regulation-cne-obras-nuevas-urgentes/Adenda-Informe-Tecnico-Costo-de-Falla.pdf
last_synthesized: 2026-05-15
---

# Conexion al SEN y regimen de transmision para generadores

> Que tiene que pasar para que una central nueva se conecte, como se financian y planifican las obras de transmision, y cuales son los desafios actuales (BESS, control de tension).

## 1. Segmentos del sistema de transmision

La LGSE distingue tres segmentos, cada uno con reglamento propio:

- **Sistema Nacional (ex Troncal)**: las grandes lineas que cruzan el pais y son de uso comun. Su valorizacion sigue el procedimiento del **DS 48/2009** (ver `DS_48_2009_Reglamento_Procedimiento_Realizacion_Estudio_Transmision_Troncal.pdf`: "APRUEBA REGLAMENTO QUE FIJA EL PROCEDIMIENTO PARA LA REALIZACION DE LOS ESTUDIOS PARA LA DETERMINACION DEL VALOR ANUAL DEL SISTEMA DE TRANSMISION TRONCAL", publicado el 4 de agosto de 2009).
- **Sistema Zonal (ex Subtransmision)**: redes de tension intermedia que conectan zonas. Su valor anual se calcula segun **DS 144/2009** (`DS_144_2009_-_Reglamento_Administrativo_de_Substransmisixn.pdf`: el Articulo 108 de la Ley establece que "el valor anual de los sistemas de subtransmision sera calculado por la Comision cada cuatro anos").
- **Sistema de Distribucion**: la red final hasta el cliente. Regulado bajo el mismo reglamento general electrico (`DOC23_-_reglamento_electrico.pdf` — DS 327/1998 fija el reglamento de la LGSE).

## 2. Como conectar una central nueva (esquema)

Pasos basicos para un nuevo proyecto:

1. **Solicitud de conexion** al Coordinador (CEN) identificando punto de conexion, capacidad, tecnologia, fecha proyectada.
2. **Estudios de conexion** (impacto en cortocircuito, regulacion de tension, flujos, estabilidad). Estos los hace el generador y los revisa el CEN.
3. **Coordinacion con el dueno de la red** donde te conectas (transmision o distribucion, segun voltaje).
4. **Cumplimiento de la NTSyCS** (norma tecnica de seguridad y calidad de servicio) — ver `sources/regulation-cne-normas-tecnicas/` para anexos y resoluciones.
5. **Pruebas de puesta en servicio** segun protocolos del CEN.
6. **Inscripcion como coordinado** y habilitacion de sistemas de medida (ver `wiki/mercado-mayorista-chile.md` seccion 6).

Las **obras de transmision nuevas y urgentes** (las que decreta el ejecutivo cuando hay necesidad sistemica) se publican como decretos anuales — ver `sources/regulation-cne-obras-nuevas-urgentes/` (48 PDFs de decretos 2024-2026, e.g. `Decreto-6T-2024.pdf`, `Decreto-14T.pdf`).

## 3. Como se planifica la expansion

El CEN elabora un **Plan de Expansion Anual** que la CNE revisa y aprueba. Las obras resultantes se licitan publicamente. Procesos relevantes capturados en `sources/regulation-coordinador-desarrollo-transmision/`:

- **Jornada Tecnica de Transmision** (`2026-04-13-JORNADA-TECNICA-TRANSMISION.pdf`) — discusion abierta sobre criterios de planificacion.
- **Control Dinamico de Tension** (`2026-04-16-CONTROL-DINAMICO-DE-TENSION.pdf`) — desafio creciente con alta penetracion solar/eolica.
- **Informe de Monitoreo 2025** (`2026-04-23-INFORME-MONITOREO-2025-.pdf`) — desempeno del plan anterior.

## 4. Tema critico actual: BESS y grid forming

La integracion masiva de almacenamiento (BESS) reabre el debate de como remunerar **inercia sintetica, control de tension y partida en negro** desde inversores. Ver:

- `2026-04-13-DESAFIOS-DE-LA-INTEGRACION-MASIVA-DE-BESS-AL-SEN.pdf` — diagnostico de la integracion masiva BESS.
- En el KB tambien estan apuntadas la **Guia Grid Forming** del CEN (en `sources/regulation-coordinador-normativa-tecnica/` cuando se complete esa carpeta — ahora vacia, ver REPORTE_INGESTA).

## 5. Costo de falla: insumo clave para todo lo anterior

El **costo de falla** (lo que vale interrumpir 1 MWh de suministro al cliente) es el parametro que justifica casi cualquier decision de expansion. Su calculo y actualizaciones recientes estan en `sources/regulation-cne-obras-nuevas-urgentes/`:

- `Adenda-Informe-Tecnico-Costo-de-Falla.pdf`
- `Adenda-N_2-Informe-Tecnico-Costo-de-Falla.pdf` (y version `_final.pdf`)
- `Res.Exta_.N314-Aprueba-Adenda-2-IT-Costo-Falla.pdf`

Para un generador en la zona afectada, un costo de falla mas alto = mas obras de transmision aprobadas = mejor acceso al SEN.

## 6. Lagunas conocidas

- El **Pliego Tecnico Normalizado (PTN)** del CEN — el documento mas operativo para conectarse, donde estan las especificaciones detalladas por equipo — no quedo capturado. Vive en `coordinador.cl/normativa-tecnica/` (URL que el scraper no llego en esta corrida; ver issue en `regulation_only.py`).
- Los **Procedimientos DO** (Direccion de Operacion) del CEN tampoco bajaron — son los protocolos del dia a dia operativo.
- Falta el **Plan de Expansion vigente** del Coordinador (PDF anual con las obras a licitar).

## 7. Para profundizar

- Marco general del mercado → `wiki/mercado-mayorista-chile.md`
- Como te pagan SSCC → `wiki/servicios-complementarios-y-transferencias.md`
- Si tu proyecto es PMGD (<= 9 MW) → `wiki/marco-pmgd-y-distribuida.md`
