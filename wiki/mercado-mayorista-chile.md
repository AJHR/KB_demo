---
title: Mercado mayorista electrico chileno — vision para generadores
sources:
  - sources/regulation-cne-reglamentos-mercado/DOC23_-_reglamento_electrico.pdf
  - sources/regulation-cne-reglamentos-mercado/Reglamento_LGSE_actualizado_xdoc_2x_VERSIxN_NO_OFICIAL.pdf
  - sources/regulation-cne-reglamentos-mercado/NT-de-Coordinacion-y-Operacion-del-SEN.pdf
  - sources/regulation-cne-reglamentos-mercado/Norma-Tecnica-de-Coordinacion-y-Operacion-Capitulo-sobre-la-Declaracion-de-Costos-Variables-2.pdf
  - sources/regulation-cne-reglamentos-mercado/SISTEMAS-DE-MEDIDAS-PARA-TRANSFERENCIAS-ECON_MICAS.pdf
  - sources/regulation-cne-reglamentos-mercado/DOC25_-_Reglamento_Panel_de_Expertos.pdf
  - sources/regulation-cne-obras-nuevas-urgentes/D2T-Fija-Precios-Estabilizados.pdf
last_synthesized: 2026-05-15
---

# Mercado mayorista electrico chileno — vision para generadores

> Sintesis para entender, desde la posicion de un generador (hidro/eolico/solar/termico), como esta organizado el mercado mayorista chileno, quien decide que, y como se cobra cada flujo. Trazabilidad de cada hecho via `sources:` arriba y citas inline.

## 1. Estructura institucional

Tres entes definen el juego:

- **CNE (Comision Nacional de Energia)**: regula. Fija normas tecnicas, precios de nudo, decretos tarifarios. Es quien emite la **Norma Tecnica de Coordinacion y Operacion** (NT) que rige al sistema (ver `sources/regulation-cne-reglamentos-mercado/NT-de-Coordinacion-y-Operacion-del-SEN.pdf`).
- **CEN (Coordinador Electrico Nacional)**: opera. Ex CDEC. Despacha en tiempo real, calcula costos marginales, contabiliza transferencias entre empresas, audita declaraciones de costos.
- **Panel de Expertos**: resuelve disputas regulatorias y tecnicas entre actores. Su funcionamiento y atribuciones estan en el `DOC25_-_Reglamento_Panel_de_Expertos.pdf`.

El marco legal raiz es el **DFL 4/2006** (texto refundido de la Ley General de Servicios Electricos, LGSE), reglamentado por el **DS 327/1998** del Ministerio de Mineria (ver `DOC23_-_reglamento_electrico.pdf`: "FIJA REGLAMENTO DE LA LEY GENERAL DE SERVICIOS ELECTRICOS. DECRETO SUPREMO N° 327. MINISTERIO DE MINERIA. Publicado en el Diario Oficial del 10 de septiembre de 1998"). El Articulo 1 del DS 327 ya define a quien aplica: empresas de generacion, transporte, distribucion, los antiguos CDEC y los usuarios.

## 2. Como se despacha tu central

El despacho es **por orden de merito de costos variables auditados**, no por oferta de precio. Esto es central:

- Cada generador termico **declara su costo variable** (combustible + no-combustible + partida/detencion) siguiendo el procedimiento del **Capitulo sobre Declaracion de Costos Variables** de la NT (ver `Norma-Tecnica-de-Coordinacion-y-Operacion-Capitulo-sobre-la-Declaracion-de-Costos-Variables-2.pdf`, indice). La NT distingue: declaracion de combustible (TITULO 2-2), declaracion de costo variable no combustible (TITULO 2-3), determinacion de costos variables (TITULO 2-4), costos de partida y detencion (TITULO 2-5).
- El CEN **verifica y audita** esas declaraciones (TITULO 2-6 y 2-7 del mismo capitulo). Auditoria fuera de banda implica sanciones / ajustes retroactivos.
- Hidro, eolico y solar entran con **costo variable cercano a cero** (uso del agua/recurso variable), por lo que estructuralmente despachan primero salvo restriccion de transmision o reserva.

El **Costo Marginal (CMg)** del sistema en cada hora y cada barra es el costo variable de la ultima central despachada para satisfacer la demanda en esa barra (ver Capitulo 2 de `NT-de-Coordinacion-y-Operacion-del-SEN.pdf`: TITULO 2-1 a 2-6 cubren determinacion, exclusiones por condiciones operativas, costos marginales en falla, en barras, publicacion).

## 3. Como te pagan: dos flujos paralelos

Para cualquier generador conectado al SEN, los ingresos vienen de dos mercados que conviven:

### a) Mercado de contratos (PPA)
Acuerdos bilaterales con clientes libres o ganados en licitaciones publicas para clientes regulados (suministro a distribuidoras). El precio del contrato es pactado y le da estabilidad.

### b) Mercado spot / transferencias economicas
Lo que efectivamente generas vs. lo que te comprometiste a entregar se liquida en el mercado spot **a costo marginal**. El CEN calcula las transferencias mensuales (Capitulo 3 de la NT: "DE LAS TRANSFERENCIAS ECONOMICAS Y LA COORDINACION DE MERCADO"). El indice de la NT es claro:

- TITULO 3-1 Aspectos generales
- TITULO 3-2 Coordinacion de mercado
- TITULO 3-4 Transferencias economicas de la coordinacion del mercado
- TITULO 3-5 Transferencias economicas del mercado de corto plazo
- TITULO 3-6 Otras transferencias economicas
- TITULO 3-7 Facturacion y cadena de pagos
- TITULO 3-8 Garantias

Para que esto funcione, **cada generador debe tener sistemas de medida con requisitos minimos**. El Anexo Tecnico de `SISTEMAS-DE-MEDIDAS-PARA-TRANSFERENCIAS-ECON_MICAS.pdf` regula esto: "establece los requerimientos minimos que deben cumplir los Sistemas de Medidas para Transferencias Economicas y las responsabilidades asociadas, a efectos de asegurar la confiabilidad de la informacion utilizada en los procesos de transferencias economicas" (Articulo 1). Define equipo de medida, equipo remarcador, comunicaciones VPN, obligaciones del Coordinado, plazos, auditorias.

## 4. Pago por potencia (potencia firme)

Ademas de energia, los generadores reciben pago por **potencia firme** (capacidad disponible en horas de demanda maxima). La modificacion reciente esta en `sources/regulation-minenergia-marco-regulatorio/2._iir_decreto_que_modifica_reglamento_de_transferencias_de_potencia_entre_empresas.pdf`.

## 5. Precios de nudo y el cliente regulado

La CNE fija semestralmente los **Precios de Nudo de Corto Plazo (PNCP)** que pagan los clientes regulados via distribuidoras. Cuando esos precios divergen mucho de los de licitaciones, entran mecanismos de **estabilizacion** — ver `sources/regulation-cne-obras-nuevas-urgentes/D2T-Fija-Precios-Estabilizados.pdf` y las **Adendas Informe Tecnico Costo de Falla** en la misma carpeta.

## 6. Que tiene que cumplir un generador (resumen rapido)

| Obligacion | Fuente |
|------------|--------|
| Declarar costos variables auditables | NTCO Cap. Declaracion Costos Variables (`Norma-Tecnica-de-Coordinacion-y-Operacion-Capitulo-sobre-la-Declaracion-de-Costos-Variables-2.pdf`) |
| Equipo de medida certificado + VPN al CEN | Anexo Sistemas de Medidas (`SISTEMAS-DE-MEDIDAS-PARA-TRANSFERENCIAS-ECON_MICAS.pdf`) |
| Cumplir NT de Coordinacion y Operacion | `NT-de-Coordinacion-y-Operacion-del-SEN.pdf` |
| Reportar fallas y eventos | `INFORMES-DE-FALLA-DE-COORDINADOS-dic19.pdf` |
| Cumplir norma de seguridad y calidad (NTSyCS) | Ver `wiki/conexion-y-transmision.md` y `sources/regulation-cne-normas-tecnicas/` |

## 7. Adonde mirar despues

- **Como conectar una nueva central** → ver `wiki/conexion-y-transmision.md`
- **Servicios complementarios (control de frecuencia, reservas, partida en negro)** → ver `wiki/servicios-complementarios-y-transferencias.md`
- **Si tu central es chica (<= 9 MW)**: regimen PMGD → ver `wiki/marco-pmgd-y-distribuida.md`

## Lagunas conocidas en este KB

- Falta capturar las **Resoluciones Exentas** de la CNE que aprueban anexos especificos a la NT (estaban detras de paginas no scrapeadas; la carpeta `regulation-cne-precios-nudo/` quedo vacia).
- Faltan los **Procedimientos DO** del CEN (operativa diaria del despacho); el sub-portal del Coordinador con esos procedimientos no entrego PDFs en esta corrida.
