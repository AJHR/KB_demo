---
title: Valorizacion y remuneracion de las inversiones en transmision (como se valida la inversion de una instalacion nueva)
sources:
  - sources/regulation-cne-sector-electrico/LGSE_actualizada_xdoc_1x_VERSIxN_NO_OFICIAL.md
  - sources/regulation-cne-reglamentos-mercado/DS_48_2009_Reglamento_Procedimiento_Realizacion_Estudio_Transmision_Troncal.md
  - sources/regulation-cne-sector-electrico/DS_144_2009_-_Reglamento_Administrativo_de_Substransmisixn.md
last_synthesized: 2026-07-01
---

# Valorizacion y remuneracion de las inversiones en transmision

> **La pregunta**: cuando entra al sistema una instalacion de transmision nueva —por ejemplo una **subestacion**— su inversion no se paga "a lo que costo" sin mas: pasa por un proceso reglado de **valorizacion** que fija cuanto se reconoce y se remunera. Esta pagina explica **que se valida, quien lo valida y que rol tiene el Coordinador**, cruzando la LGSE con sus reglamentos de transmision troncal (DS 48/2009) y de subtransmision (DS 144/2009).
>
> **Nota de regimen (leer primero)**: las fuentes de este KB describen el regimen de la **Ley 19.940** (troncal / subtransmision / adicional, con "CDEC" y "Direccion de Peajes"). La **Ley 20.936 (2016)** renombro los segmentos a **nacional / zonal / dedicado / polos de desarrollo**, disolvio el CDEC en el **Coordinador Electrico Nacional (CEN)** y traspaso a este las funciones de la antigua Direccion de Peajes. Donde las fuentes dicen "CDEC / Direccion de Peajes", hoy leer **Coordinador**; donde dicen "troncal", hoy leer **sistema nacional**. La mecanica de fondo (V.I. -> licitacion/estudio -> decreto -> liquidacion) se mantiene.

## 1. Que se valida: V.I., A.V.I. y COMA

Toda instalacion de transmision —el DS 48 define el sistema como el "conjunto de lineas y **subestaciones** electricas" (`sources/regulation-cne-reglamentos-mercado/DS_48_2009_Reglamento_Procedimiento_Realizacion_Estudio_Transmision_Troncal.md`, Art. 4)— se remunera sobre tres componentes definidos en el Art. 5 del mismo reglamento:

| Sigla | Significado | Que es |
|-------|-------------|--------|
| **V.I.** | Valor de Inversion | El costo de capital reconocido a la instalacion. Es lo que "se valida" cuando entra una obra nueva. |
| **A.V.I.** | Anualidad del Valor de Inversion | El V.I. anualizado segun su **vida util** y la tasa de descuento regulada. |
| **COMA** | Costos de Operacion, Mantencion y Administracion | "Suma de los costos de operacion, mantencion y administracion incurridos por un sistema de transmision adaptado en un ano cualquiera de operacion" (Art. 5, num. 4). |

La remuneracion anual de un tramo de transmision es, en esencia, **A.V.I. + COMA**. "Validar la inversion" de tu subestacion equivale a **fijar su V.I.** (y con el, el A.V.I. + COMA que se paga cada ano).

## 2. Quien hace que (resumen)

| Actor | Rol en la valorizacion |
|-------|------------------------|
| **CNE (la "Comision")** | **Valoriza**: elabora las bases y el informe tecnico del estudio de transmision, y determina A.V.I./COMA por tramo y los V.I./COMA referenciales de obras nuevas. |
| **Ministerio de Energia** | **Formaliza**: dicta el **decreto de valorizacion** y el decreto de expansion que hacen vinculantes los valores. |
| **Mercado (licitacion publica)** | **Valida a precio de mercado**: para obras nuevas, el valor reconocido es el que **resulta de la licitacion**, no el referencial del estudio. |
| **Coordinador (ex CDEC / Direccion de Peajes)** | **Ejecuta y liquida**: convoca y resuelve la licitacion de obras nuevas, aplica el V.I. referencial desde la puesta en servicio y el definitivo tras el decreto, y realiza las **reliquidaciones**. Ademas **planifica** la expansion y **revisa** los estudios de conexion. |
| **Panel de Expertos** | **Dirime**: resuelve discrepancias sobre bases, informe tecnico y valorizaciones. |

En una frase: **la CNE valoriza (via estudio + decreto), la licitacion publica valida el monto a precio de mercado, y el Coordinador planifica, corre la licitacion y liquida los pagos.**

## 3. Camino A — Instalacion NUEVA (linea o subestacion nueva): licitacion

Cuando el decreto de expansion identifica como parte del sistema a **lineas y subestaciones nuevas**, estas se adjudican por **licitacion publica** (LGSE `sources/regulation-cne-sector-electrico/LGSE_actualizada_xdoc_1x_VERSIxN_NO_OFICIAL.md`, Art. 95):

1. Los proyectos "seran adjudicados, mediante el proceso de licitacion (...), en cuanto a su ejecucion y al derecho a su explotacion, a una empresa de transmision" (Art. 95).
2. **La licitacion se resuelve segun el valor anual de la transmision por tramo que oferten las empresas**, y "solo se consideraran de manera referencial el V.I. y COMA definidos en el (...) decreto" (Art. 95). Es decir: **el valor del estudio es solo un piso referencial; el valor que se valida y se paga es el ofertado ganador.**
3. Ese valor anual resultante "constituira la remuneracion de las nuevas lineas troncales y se aplicara durante **cinco periodos tarifarios**", tras los cuales la instalacion y su valorizacion se revisan en el estudio (Art. 95).
4. **Quien corre la licitacion**: "Correspondera a la Direccion de Peajes del CDEC respectivo (...) efectuar una **licitacion publica internacional** de los proyectos" (Art. 96) — hoy esa funcion es del **Coordinador**. Las **bases de licitacion las elabora la CNE** y especifican condiciones, informacion tecnica/comercial, plazos, garantias y las caracteristicas tecnicas de las lineas o subestaciones (Art. 96).
5. La Direccion de Peajes (Coordinador) resuelve la adjudicacion en un plazo no superior a 60 dias desde recibidas las propuestas (Art. 97).

> **Para tu ejemplo (subestacion nueva)**: el "cuanto vale" que se reconoce **no lo fija el Coordinador ni la CNE a dedo**: sale de la **oferta ganadora de la licitacion** que el propio Coordinador administra, sobre bases de la CNE. Ese valor queda fijo (indexado) por cinco periodos tarifarios.

## 4. Camino B — AMPLIACION de una instalacion existente: V.I. referencial -> definitivo

Si la obra es una **ampliacion de instalaciones existentes** (no una obra nueva independiente), el mecanismo es de construccion obligatoria del propietario con **doble valorizacion** (LGSE, Art. 22 transitorio, ilustrativo del procedimiento general):

1. Es "de construccion obligatoria para las empresas propietarias de dichas instalaciones".
2. El decreto fija el **V.I. con caracter referencial**.
3. Para el V.I. que "debera reflejarse definitivamente en el pago del servicio de transmision, las empresas propietarias (...) deberan **licitar la construccion de las obras a empresas calificadas, a traves de procesos de licitacion publicos, abiertos y transparentes, auditables por la Superintendencia**".
4. El **V.I. definitivo** lo establece el Ministerio "previo informe de la Comision Nacional de Energia (...) mediante un decreto, lo que dara origen ademas a las **reliquidaciones** que correspondan, las que seran realizadas por la Direccion de Peajes" (hoy el Coordinador).
5. Entretanto, "el centro de despacho economico de carga (...) considerara el **V.I. referencial a partir de su puesta en servicio** y el **V.I. definitivo** una vez que (...) lo establezca mediante un decreto".

> **Idea clave**: aqui tambien la validacion real del monto pasa por una **licitacion de construccion** (auditable por la SEC) y por un **decreto**; el Coordinador aplica primero el valor referencial y luego reliquida contra el definitivo.

## 5. El estudio de valorizacion (donde se recalcula la base existente)

Cada cuatro anos, la base instalada se **revaloriza** en un estudio dirigido por la CNE. Dos reglamentos, uno por segmento:

### 5.1 Sistema nacional (ex troncal) — DS 48/2009

El DS 48 "fija el procedimiento para la realizacion de los estudios para la determinacion del **valor anual del sistema de transmision troncal**". Hitos del proceso (`sources/regulation-cne-reglamentos-mercado/DS_48_2009_...md`):

- **Bases** (Art. 34): la CNE publica bases preliminares que incluyen "los A.V.I. y COMA que sustentan los valores por tramo vigentes" y la "fecha de entrada en operacion, A.V.I. y COMA de las instalaciones de transmision en construccion".
- **Estudio** (Art. 39): el consultor entrega el A.V.I. y COMA de las instalaciones existentes, los valores referenciales de las ampliaciones y las recomendaciones de nuevas obras con sus valores referenciales.
- **Audiencia publica** y observaciones (Arts. 40-44).
- **Informe tecnico** (Art. 49): la CNE fija "el valor anual de transmision por tramo, A.V.I. del tramo, y el COMA (...) con sus formulas de indexacion para cada uno de los siguientes **cuatro anos**", identifica las ampliaciones con su A.V.I./COMA referenciales y, "si correspondiere, la identificacion de proyectos de **nuevas lineas y subestaciones** troncales con sus respectivos **V.I. y COMA referenciales**".
- **Discrepancias** ante el **Panel de Expertos** (Arts. 37, 50).
- **Decreto de valorizacion** (Cap. 9): el Ministerio formaliza los valores.

### 5.2 Sistema zonal (ex subtransmision) — DS 144/2009

Segun el DS 144 (`sources/regulation-cne-sector-electrico/DS_144_2009_-_Reglamento_Administrativo_de_Substransmisixn.md`), el Art. 108 de la Ley "establece que el **valor anual de los sistemas de subtransmision sera calculado por la Comision cada cuatro anos**". El estudio considera, entre otros, "la **vida util** por cada tipo de instalacion" (Art. 8, letra e) y sigue una estructura analoga de bases -> estudio -> informe tecnico -> Panel, dirigido por la CNE.

## 6. Rol del Coordinador, en detalle

El Coordinador (CEN), como sucesor del CDEC y su Direccion de Peajes, interviene en la inversion de instalaciones nuevas en cuatro planos —ninguno de ellos es "fijar el valor a dedo":

1. **Planifica**: elabora el **Plan de Expansion Anual** de transmision, que la CNE revisa y aprueba; las obras aprobadas se licitan (ver `wiki/conexion-y-transmision.md`, seccion 3).
2. **Revisa la conexion**: valida tecnicamente los estudios de conexion de la instalacion nueva (cortocircuito, tension, flujos, estabilidad) y las pruebas de puesta en servicio (ver `wiki/conexion-y-transmision.md`, seccion 2).
3. **Corre la licitacion**: convoca y resuelve la licitacion publica (internacional) de las obras nuevas, sobre bases elaboradas por la CNE (LGSE Arts. 96-97).
4. **Aplica y liquida**: reconoce el V.I. referencial desde la puesta en servicio, el V.I. definitivo tras el decreto, y ejecuta las **reliquidaciones** (LGSE Art. 22 transitorio).

## 7. Lagunas conocidas

- **Regimen legal desactualizado en las fuentes**: el articulado citado es del regimen troncal (Ley 19.940 / DS 48 2009 / DS 144 2009). Falta capturar el texto vigente post **Ley 20.936** con los segmentos nacional/zonal/dedicado y las atribuciones actuales del Coordinador. Verificar terminologia antes de citar hacia afuera.
- **Documentos operativos ausentes** (ver `wiki/conexion-y-transmision.md`, seccion 6): no estan en el KB el **Plan de Expansion vigente**, los **Procedimientos DO** ni el **Pliego Tecnico Normalizado (PTN)** del Coordinador. Lo que hay es el marco **legal y reglamentario**, no el procedimiento operativo paso a paso ni los formularios/plataformas actuales.
- **Tasa de descuento y vida util**: los parametros numericos (tasa regulada, vidas utiles por tipo de instalacion) viven en decretos/normas especificas no sintetizados aqui.

## 8. Para profundizar

- Como conectar una central nueva y segmentos de transmision -> `wiki/conexion-y-transmision.md`
- Vision general del mercado (quien decide que) -> `wiki/mercado-mayorista-chile.md`
- Como se pagan los servicios de sistema y transferencias -> `wiki/servicios-complementarios-y-transferencias.md`
