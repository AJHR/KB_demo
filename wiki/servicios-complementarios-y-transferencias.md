---
title: Servicios complementarios y transferencias economicas en el SEN
sources:
  - sources/regulation-cne-reglamentos-mercado/NT-de-Coordinacion-y-Operacion-del-SEN.pdf
  - sources/regulation-cne-reglamentos-mercado/SISTEMAS-DE-MEDIDAS-PARA-TRANSFERENCIAS-ECON_MICAS.pdf
  - sources/regulation-cne-reglamentos-mercado/INFORMES-DE-FALLA-DE-COORDINADOS-dic19.pdf
  - sources/regulation-cne-reglamentos-mercado/DESEMPE_O-DEL-CONTROL-DE-FRECUENCIA-dic19.pdf
  - sources/regulation-cne-reglamentos-mercado/Norma-Tecnica-de-Coordinacion-y-Operacion-Capitulo-sobre-la-Declaracion-de-Costos-Variables-2.pdf
  - sources/regulation-minenergia-marco-regulatorio/2._iir_decreto_que_modifica_reglamento_de_transferencias_de_potencia_entre_empresas.pdf
  - sources/regulation-minenergia-marco-regulatorio/8._iir_ds_125.pdf
last_synthesized: 2026-05-18
---

# Servicios complementarios y transferencias economicas en el SEN

> Como se remunera a un generador por mantener al sistema operando confiablemente (no solo por inyectar energia), y como se liquidan los flujos mensuales entre coordinados.

## 1. Que son los servicios complementarios (SSCC)

Recursos tecnicos que el sistema necesita ademas de la energia: control de frecuencia primario y secundario, reservas en giro, control de tension, capacidad de partida en negro, deslastre de carga, inercia. El marco general esta en el **DS 125** del Ministerio de Energia (reglamento de coordinacion y operacion del SEN; ver `sources/regulation-minenergia-marco-regulatorio/8._iir_ds_125.pdf`, que es el informe de impacto regulatorio del decreto que modifica/aprueba ese reglamento).

El CEN, segun la NT, debe **identificar la necesidad de SSCC, asignarlos y remunerarlos** via los procesos descritos en los TITULOS 3-4 a 3-6 (`NT-de-Coordinacion-y-Operacion-del-SEN.pdf`):

- TITULO 3-4 Transferencias economicas de la coordinacion del mercado
- TITULO 3-5 Transferencias economicas del mercado de corto plazo
- TITULO 3-6 Otras transferencias economicas

## 2. Transferencias economicas: flujo mensual

El proceso es **mensual** y lo ejecuta el CEN. Los flujos se calculan a partir de:

1. **Mediciones** de energia generada/consumida por cada coordinado, recolectadas via los sistemas regulados en `SISTEMAS-DE-MEDIDAS-PARA-TRANSFERENCIAS-ECON_MICAS.pdf`. El Anexo establece "los requerimientos minimos que deben cumplir los Sistemas de Medidas para Transferencias Economicas... a efectos de asegurar la confiabilidad de la informacion utilizada en los procesos de transferencias economicas" (Art. 1).
2. **Costos marginales horarios por barra** (calculados por el CEN segun Capitulo 2 de la NT).
3. **Costos variables auditados** declarados via NTCO Cap. Declaracion de Costos Variables (`Norma-Tecnica-de-Coordinacion-y-Operacion-Capitulo-sobre-la-Declaracion-de-Costos-Variables-2.pdf`).
4. **Eventos** del mes (fallas, redespachos, exclusiones de costo marginal por condiciones operativas — TITULO 2-3 y 2-4 de la NT).

Resultado: un balance por coordinado que se traduce en **facturas entre empresas** (TITULO 3-7 Facturacion y Cadena de Pagos) respaldadas por **garantias** (TITULO 3-8).

## 3. Pago por potencia firme

La **potencia** se remunera aparte de la energia. Cada central tiene una potencia firme reconocida segun su disponibilidad estadistica en horas de demanda maxima. La modificacion vigente al regimen de transferencias de potencia esta en `2._iir_decreto_que_modifica_reglamento_de_transferencias_de_potencia_entre_empresas.pdf` (informe de impacto regulatorio del decreto del Minenergia).

Para hidro, eolico y solar el calculo es no trivial — depende de la **definicion de potencia firme** vigente (hay debate regulatorio constante sobre como reconocer aporte de renovables variables con / sin BESS).

## 3.bis Como se mide el desempeno del Control de Frecuencia

Anexo Tecnico CNE: **Desempeno del Control de Frecuencia** (dic 2019, 6 pp.). Define el **Factor de Eficiencia del Control de Frecuencia (FECF)** que el CEN debe calcular **hora a hora** y publicar en su sitio web **antes del dia 10 de cada mes** (`sources/regulation-cne-reglamentos-mercado/DESEMPE_O-DEL-CONTROL-DE-FRECUENCIA-dic19.pdf`, Art. 1-4).

> "El objetivo del presente Anexo Tecnico es definir la metodologia para calcular el Factor de Eficiencia del Control de Frecuencia (FECF) que permite evaluar el desempeno del Control de Frecuencia del SI." — Art. 1

Componentes del calculo (Art. 5-6):

- **CPF**: Control Primario de Frecuencia (respuesta automatica de gobernadores de turbinas).
- **CRF**: Control Rapido de Frecuencia (respuesta de BESS y otros inversores).
- **FECF** = 1 si la desviacion filtrada de frecuencia coincide con la nominal; 0 si se agota la reserva CPF+CRF.

Las medidas de frecuencia vienen del **Sistema de Informacion en Tiempo Real (SITR)** del CEN, con muestreo cada 10 segundos. Si tu central provee CPF/CRF, este factor monitorea si **efectivamente cumples** lo declarado — y se usa para auditoria y eventual sancion.

## 4. Informes de falla

Los coordinados **deben reportar** todo evento que afecte la operacion (fallas, indisponibilidades forzadas, eventos en transmision). La especificacion del formato esta en `INFORMES-DE-FALLA-DE-COORDINADOS-dic19.pdf`. Estos informes alimentan:

- Calculo de **costo de falla** del sistema (proxy de cuanto vale interrumpir suministro).
- **Auditoria de causas** y eventual sancion al coordinado responsable.
- Ajuste retroactivo de transferencias si el evento implico costo marginal "artificial".

## 5. Datos clave del proceso (chequeo rapido)

| Elemento | Periodicidad | Quien lo emite | Quien lo recibe |
|----------|--------------|----------------|------------------|
| CMg horario por barra | horario, publicado al cierre | CEN | publico via portal |
| Declaracion de costos variables | mensual (con anticipacion) | Coordinados (generadores termicos) | CEN auditoria |
| Balance de transferencias economicas | mensual | CEN | Coordinados (facturacion) |
| Informe de falla | por evento | Coordinados involucrados | CEN |
| Calculo de potencia firme | anual | CEN | Coordinados |

## 6. Lagunas conocidas

- En este KB no quedo capturado el **anexo de servicios complementarios** especifico (el sub-portal del CEN con anexos tecnicos por sscc no entrego PDFs en esta corrida).
- Falta tambien la **resolucion CNE que aprueba los precios de los SSCC** del periodo vigente.
- El **DS 113** especifico de servicios complementarios no aparecio en la ingesta; lo que tenemos es el `8._iir_ds_125.pdf` que cubre el reglamento general de coordinacion. Reintentar con scraping enfocado.

## 7. Para profundizar

- Vision general del mercado → `wiki/mercado-mayorista-chile.md`
- Conexion al sistema → `wiki/conexion-y-transmision.md`
- PMGD con almacenamiento → `wiki/marco-pmgd-y-distribuida.md`
