---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-04-Diccionario-de-Datos-Web-SIP.pdf
pdf_sha256: 49b5938552ca611844a272877e710d84c792b474dbf953d023a0a787ac0f6b06
pdf_pages: 15
extracted_pages: 15
extracted_chars: 27875
extracted_at: 2026-05-19T13:23:00Z
extractor: pypdf
---

# B43 DIN 04 Diccionario de Datos Web SIP

<!-- page 1 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 1 / 15


Documento impreso no controlado


ÍNDICE DE CONTENIDOS

1. OBJETIVO Y ALCANCE DE APLICACIÓN
2. DOCUMENTOS DE REFERENCIA
3. DEFINICIONES
4. RESPONSABILIDADES Y RIESGOS
5. DESARROLLO
6. ANEXOS

CONTROL DE CAMBIOS

VERSIÓN FECHA COMENTARIO DE LA MODIFICACION RESPONSABLE
01 02-11-2022 Versión inicial Coordinador


DOCUMENTOS DECLARADOS

CODIGO NOMBRE DOCUMENTO


ELABORACIÓN Y APROBACIÓN

ELABORADO POR REVISADO POR APROBADO POR

Coordinador Coordinador Coordinador

<!-- page 2 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 2 / 15


Documento impreso no controlado

1. OBJETIVO Y ALCANCE DE APLICACIÓN

El objetivo de este documento es definir un Diccionario de Datos (o repositorio de metadatos) para la descarga
de datos del Sistema de Información Pública (SIP), con tal de proveer un lenguaje común entre el Coordinador
y los usuarios del portal web. Además de facilitar la interpretación y análisis de estos.

Este Diccionario describe los siguientes atributos y características: definición del dato, fuente de origen, URL de
la descargar del dato, formato de descarga, filtros, formatos y estructura de datos

Adicional a este Diccionario de Datos , el Documento Interno “ H31-DIN-01 API Pública del SIP ” describe el
funcionamiento de la API Pública, cuyo propósito es exponer los datos almacenados en el SIP a usuarios externos
que soliciten estos antecedentes1.


2. DOCUMENTOS DE REFERENCIA

No hay documentos de referencia.


3. DEFINICIONES

Este documento introduce las definiciones que se detallan a continuación:

3.1 Diccionario de datos: Conjunto de definiciones de los objetos o elementos de datos en un sistema de
información. Tiene como objetivo proveer un lenguaje común entre el autor de los datos y los usuarios. A
menudo, un diccionario de datos es un repositorio de metadatos centralizado.
3.2 LGSE: Ley General de Servicios Eléctricos.
3.3 SEN: Sistema Eléctrico Nacional.
3.4 SIP: Sistema de Información Pública (Art 72-8, LGSE).


4. RESPONSABILIDADES Y RIESGOS

De acuerdo con el Art 72-8 de la LGSE, será de responsabilidad del Coordinador verificar la completitud, calidad,
exactitud y oportunidad de la información publicada en los respectivos sistemas de información . La actualización
del presente documento recae en el responsable interno del proceso respectivo.


5. DESARROLLO

El Diccionario de Datos  que se presenta a continuación, está estructurado según la cadena de valor del
Coordinador (Planificación y Desarrollo, Operación y Mercado ) y con el mismo orden que se encuentran
publicados en el sitio web en la sección “Gráficos y Datos”. El objetivo es definir la estructura de los datos que se
pueden obtener del cuadro “Descargar Datos” (ver Figura 1).


Figura 1: Ejemplo de cuadro de descarga de datos disponible en el sitio web (formato de descarga diario).


1 https://www.coordinador.cl/desarrollo/documentos/sistema -de-informacion-publica/api-publica-del-sip/

<!-- page 3 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 3 / 15


Documento impreso no controlado
5.1 Planificación y Desarrollo

5.1.1 Oferta Proyectada

• Definición dato: Plan de obras de generación, para los distintos escenarios evaluados en el Informe de
Expansión de la Transmisión.
• Fuente de origen: Propuesta del Plan de Expansión de la Transmisión del año respectivo.
• URL: https://www.coordinador.cl/desarrollo/graficos/planificacion-de-la-transmision/oferta-proyectada/

Actualmente no cuenta con un sistema de descarga de datos.

5.1.2 Demanda Proyectada

• Definición dato: Proyección de demanda a 20 años utilizada en el Informe de Expansión de la Transmisión.
• Fuente de origen: Propuesta del Plan de Expansión de la Transmisión del año respectivo.
• URL: https://www.coordinador.cl/desarrollo/graficos/planificacion-de-la-transmision/demanda-proyectada-
por-regiones

Actualmente no cuenta con un sistema de descarga de datos.

5.1.3 Costo Marginal Proyectado

• Definición dato: Proyección de costo marginal a 20 años para los distintos escenarios evaluados en el
Informe de Expansión de la Transmisión.
• Fuente de origen: Propuesta del Plan de Expansión de la Transmisión del año respectivo.
• URL: https://www.coordinador.cl/desarrollo/graficos/planificacion-de-la-transmision/costo-marginal-
proyectado/

Actualmente no cuenta con un sistema de descarga de datos.

<!-- page 4 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 4 / 15


Documento impreso no controlado
5.2 Operación

5.2.1  Operación Programada

5.2.1.1 Demanda Programada

• Definición dato: La demanda programada es una de las variables críticas para determinar adecuadamente
el nivel de producción de las centrales generadoras en el proceso de la Programación de Operación de Corto
Plazo.
• Fuente de origen: Datos procesados desde Pronóstico centralizado de demanda.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-programada/demanda-programada
• Formato de descarga: TSV
• Filtros: mensual (mes de inicio y mes de termino)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Demanda Número Demanda programada del sistema (MWh/h)


5.2.1.2 Generación Programada

• Definición dato: La generación programada del SEN, corresponde al resultado del proceso de optimización
de la operación y determina el estado y los puntos de operación de todas las unidades generadoras del
sistema.
• Fuente de origen: Proceso de Programación de Operación de Corto Plazo.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-programada/costo-marginal-programado

Actualmente no cuenta con un sistema de descarga de datos.


5.2.1.3 Cotas de Embalse Programadas

• Definición dato: Trayectorias de las cotas programadas de los embalses que abastecen centrales
generadoras conectadas al SEN. Las cotas de los embalses permiten determinar al Coordinador la energía
embalsada y con ello optimizar la operación económica del sistema en el corto y mediano plazo.
• Fuente de origen: Proceso de Programación de Operación de Corto Plazo.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-programada/cotas-de-embalses-
programadas

Actualmente no cuenta con un sistema de descarga de datos.

<!-- page 5 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 5 / 15


Documento impreso no controlado
5.2.1.4 Costo Marginal Programado

• Definición dato: El costo marginal de energía programado es resultado del proceso de programación de la
operación que se realiza diariamente. A partir de la optimización de los recursos, estado de las instalaciones
y proyección de variables relevantes, como la demanda, se realiza el proceso de optimización de la operación
del sistema eléctrico nacional para el día siguiente, en donde uno de los resultados de dicho proceso es el
costo marginal de energía horario para un conjunto de barras del SEN.
•
• Fuente de origen: Proceso de Programación de Operación de Corto Plazo.
• URL: https://www.coordinador.cl/desarrollo/graficos/planificacion-de-la-transmision/costo-marginal-
proyectado/
• Formato de descarga: TSV
• Filtros: mensual (mes y año)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Id Barra
infotécnica Texto Id barra en infotécnica
Nombre Barra Texto Nombre barra en infotécnica
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)


5.2.2  Operación Real

5.2.2.1 Demanda Real

• Definición dato: Demanda bruta de energía eléctrica del SEN.
• Fuente de origen: Plataforma Operación Real / Balance de Transferencias de Energía.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/demanda-real/
• Formato de descarga: TSV
• Filtros: diaria (día y mes)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura  para cada
gráfico asociado al dato Demanda Real.

i. Demanda Sistémica Real (Plataforma Operación Real)

Ítem Formato Comentarios
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Demanda Número Demanda de energía (MWh/h)

ii. Detalle diario de Retiro de Energía – Barras (Balance de Transferencias de Energía)

Ítem Formato Comentarios
Barra
mnemotecnico Texto Mnemotecnico de la barra
Barra nombre Texto Nombre de la barra
Fecha Fecha Fecha (YYYY-MM-DD)
Retiro ajustado Número Retiro de energía (KWh)
Retiro ajustado
valorizado Número Retiro valorizado de energía ($)

<!-- page 6 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 6 / 15


Documento impreso no controlado
iii. Retiros físicos y valorizados por barra horario (Balance de Transferencias de Energía)

Ítem Formato Comentarios
Barra
mnemotecnico Texto Mnemotecnico de la barra
Barra nombre Texto Nombre de la barra
Suministrador
mnemotecnico Fecha Mnemotecnico de la empresa suministradora
Suministrador
nombre Texto Nombre de la empresa suministradora
Propietario
mnemotecnico Texto Mnemotecnico de la empresa propietaria
Propietario
nombre Texto Nombre de la empresa propietaria
Cliente
mnemotecnico Texto Mnemotecnico de la empresa cliente
Cliente nombre Texto Nombre de la empresa cliente
Retiro ajustado Número Retiro de energía (KWh)
Retiro ajustado
valorizado Número Retiro valorizado de energía ($)
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)

iv. Demanda neta (Plataforma OpReal)

Ítem Formato Comentarios
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Generación total Número Generación total de energía por hora (MWh)
Generación
ERNC Número Generación ERNC (multiplicada por factor ERNC) (MWh)
Generación neta Número Diferencia entre la Generación total y Generación ERNC (MWh)


5.2.2.2 Generación Real

• Definición dato: Generación de energía eléctrica en el SEN.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/generacion-real/
• Formato de descarga: TSV y XLSX
• Filtros: Unidad, central y mensual (mes y año)
• Datos: El cuadro de descargas  de Generación Real pone a disposición un set de datos  agrupados “por
Unidad” y “por Central”, y por formato TSV y XLSX.

<!-- page 7 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 7 / 15


Documento impreso no controlado
i. Unidad y TSV

Ítem Formato Comentarios
Fecha opreal Fecha Fecha (YYYY-MM-DD)
Hora opreal Número Hora (hh)
nemotecnico Texto Nemotécnico de la central
nombre Texto Nombre de la central
Central nombre Texto Nombre de la central
Central
infotecnica id Número ID de la central
Coordinado Texto Nombre empresa coordinada de la central
Central tipo Texto Tipo de tecnología de la central
Central tipo
nemotecnico Texto Tipo de tecnología de la central
subtipo Texto Tipo de tecnología de la central
Subtipo
nemotecnico Texto Tipo de combustible de la central (si aplica)
Grupo reporte
nombre Texto Grupo reporte de la central generadora
Generación real
mwh Número Generación de energía eléctrica (MWh)
Generación real
ernc mwh Número Generación ERNC (multiplicada por factor ERNC) (MWh)

ii. Unidad y XLSX

Ítem Formato Comentarios
Central Texto Nombre de la central generadora
Llave Texto Llave opreal de la central generadora
Coordinado Fecha Nombre empresa coordinada de la central
Grupo reporte Texto Grupo reporte de la central generadora
Tipo Texto Tipo de tecnología de la central
Subtipo Texto Tipo de combustible de la central (si aplica)
Fecha Fecha Fecha (YYYY-MM-DD)
Hora  Número Hora (hh)

iii. Central y TSV

Ítem Formato Comentarios
Fecha opreal Fecha Fecha (YYYY-MM-DD)
Hora opreal Número Hora (hh)
Central
Infotecnica id Número ID de la central
Central nombre Texto Nombre de la central
Central tipo Texto Tipo de tecnología de la central
Central tipo
nemotecnico Texto Tipo de tecnología de la central
Generación real
mwh Número Generación de energía eléctrica (MWh)
Generación real
ernc mwh Número Generación ERNC (multiplicada por factor ERNC) (MWh)

<!-- page 8 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 8 / 15


Documento impreso no controlado
5.2.2.3 Generación Real En Línea (SCADA)

• Definición dato: Generación real promedio del SEN, datos provenientes del SCADA.
• Fuente de origen: SCADA
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/generacion-real-horaria-scada

Actualmente no cuenta con un sistema de descarga de datos.


5.2.2.4 Cotas y Niveles de Embalses Reales

• Definición dato: Trayectorias de las cotas reales de los embalses que abastecen centrales generadoras
conectadas al SEN.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/cotas-y-niveles-de-embalses-reales/
• Formato de descarga: TSV
• Filtros: diario (fecha inicio y fecha final)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

i. Cotas de Embalses Reales

Ítem Formato Comentarios
Nombre embalse Texto Nombre del embalse
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Cota Número Cota del embalse (m.s.n.m)

ii. Afluentes

Ítem Formato Comentarios
Nombre embalse Texto Nombre del embalse
Fecha Fecha Fecha (YYYY-MM-DD)
Afluente Número Afluente m3/seg

iii. Precipitaciones

Ítem Formato Comentarios
Reservorio Texto Nombre del embalse
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Cota Número Cota del embalse (m.s.n.m)


5.2.2.5 Potencia Transitada por el Sistema de Transmisión

• Definición dato: Flujos netos de potencia horarios transitados por el sistema de transmisión, considerando
tanto líneas como transformadores del SEN.
• Fuente de origen: Datos procesados desde la plataforma de medidas (PRMTE).
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/potencia-transitada-por-el-sistema-de-
transmision/
• Formato de descarga: TSV
• Filtros: diaria (fecha de inicio y fecha de término)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

<!-- page 9 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 9 / 15


Documento impreso no controlado

Ítem Formato Comentarios
tramo_nombre Texto Nombre del tramo
fecha Fecha Fecha (YYYY-MM-DD)
intervalos Número Hora indexada (hh)
potencia_sum Número Potencia transitada (MW)


5.2.2.6 Ofertas no Adjudicadas de SSCC (Servicios Complementarios)

• Definición dato: Ofertas no Adjudicadas de SSCC  de los servicio de Control  Primario de Bajada y  Control
Secundario y Terciario de Frecuencia de Bajada y Subida.
• Fuente de origen: Datos procesados desde Plataforma de Subastas de Servicios Complementarios.
• URL: https://www.coordinador.cl/desarrollo/graficos/planificacion-de-la-transmision/costo-marginal-
proyectado/
• Formato de descarga: XLSX
• Filtros: mensual
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Servicio Texto Tipo de servicio de control
Fecha Fecha Fecha (YYYY-MM-DD)
Periodo Número Hora indexada (hh)
Promedio Precio Número Precio promedio de ofertas no adjudicadas (USD/MWh)
Desviación
Estándar Precio Número Desviación estándar de ofertas no adjudicadas (USD/MWh)


5.2.2.7 Información de Energía Afluente y Probabilidad de Excedencia del SEN

• Definición dato: Energía afluente disponible en el SEN y la probabilidad de excedencia.
• Fuente de origen: Elaboración propia del Coordinador.
• URL: https://www.coordinador.cl/operacion/graficos/operacion-real/informacion-condicion-hidrologica/
• Formato de descarga: XLSX
• Filtros: mensual
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Mes Texto Mes año hidrológico anterior
Semana Número Número de semana del mes
Energía Afluente  Número Energía Afluente (GWh) por Condición hidrológica (SECA, MEDIA y
HÚMEDA).
Probabilidad de
Excedencia Porcentaje Probabilidad de excedencia del SEN

<!-- page 10 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 10 / 15


Documento impreso no controlado
5.2.3  Desviación de la Operación Programada

5.2.3.1 Desviación de la Generación Programada

• Definición dato: Comparación horaria entre la generación real y la programada.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-
la-generacion-programada

Actualmente no cuenta con un sistema de descarga de datos.


5.2.3.2 Desviación de los Costos Marginales Programados

• Definición dato: Comparación horaria entre el costo marginal real y el programado para todas las barras a
las que se determina el Costo Marginal desde el Proceso la Programación Diaria de la Operación.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-
los-costos-marginales-programados/
• Formato de descarga: TSV
• Filtros: mensual (mes de inicio y mes de termino)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Id Barra
infotécnica Texto Id barra en infotécnica
Nombre Barra Texto Nombre barra en infotécnica
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Costo Marginal
programado Número Costo Marginal programado (USD/MWh)
Costo Marginal
programado Número Costo Marginal programado (USD/MWh)
Desviación Número Desviación de costos marginal real vs costo marginal programado
(USD/MWh)
Porcentaje Número Porcentaje de desviación de costos marginal real vs costo marginal
programado (%)


5.2.3.3 Desviación de la Demanda Programada

• Definición dato: Comparación horaria entre el nivel de demanda real y el programado del SEN.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-
la-demanda-programada/
• Formato de descarga: TSV
• Filtros: mensual (mes de inicio y mes de termino)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

<!-- page 11 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 11 / 15


Documento impreso no controlado
Ítem Formato Comentarios
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Demanda real Número Demanda real del sistema (MWh/h)
Demanda
programada Número Demanda programada del sistema (MWh/h)
Desviación Número Desviación de demanda real vs demanda programada (MWh/h)
Porcentaje Número Porcentaje de desviación de demanda real vs demanda programado (%)


5.2.3.4 Desviación de las Cotas de Embalses Programadas

• Definición dato: Comparación horaria entre el nivel de demanda real y el programado del SEN.
• Fuente de origen: Plataforma Operación Real.
• URL: https://www.coordinador.cl/operacion/graficos/desviacion-de-la-operacion-programada/desviacion-de-
las-cotas-de-embalses-programadas

Actualmente no cuenta con un sistema de descarga de datos.

<!-- page 12 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 12 / 15


Documento impreso no controlado
5.3 Mercado

5.3.1 Transferencias Económicas

5.3.1.1. Energía

• Definición dato: Las Transferencias de Energía son resultado de la valorización de inyecciones y retiros
efectuados en el sistema eléctrico nacional por las empresas generadoras del sector. Dichas empresas,
además de las inyecciones que son un resultado de la operación de las centrales generadoras de su
propiedad, también realizan los retiros de energía desde el SEN, en el rol de suministradores de clientes
libres como regulados.
• Fuente de origen: Proceso de Cálculo del Balance de Energía.
• URL: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/energia
• Formato de descarga: TSV
• Filtros: mensual (mes y año)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Propietario
mnemotécnico Texto Mnemotécnico de propietario en infotécnica
Propietario
nombre Texto Nombre de propietario
Balance energía Fecha Balance físico de energía (GWh)
Balance
valorizado Número Valorización de Transferencias (MM$ clp)
mes Fecha Fecha (YYYY-MM-DD)


5.3.1.2. Potencia

• Definición dato: Las Transferencias de Potencia son resultado de la valorización del balance físico de
potencia el cual se construye a partir de las inyecciones de potencia de suficiencia de cada generador y los
respectivos retiros de potencia para el suministro de contratos con clientes libres o regulados .
• Fuente de origen: Proceso de Cálculo del Balance de Potencia.
• URL: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/potencia/
• Formato de descarga: TSV
• Filtros: mensual (mes y año)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Propietario
mnemotécnico Texto Mnemotécnico de propietario en infotécnica
Propietario
nombre Texto Nombre de propietario
Balance potencia Fecha Balance de potencia (KW)
Balance
valorizado Número Valorización de Transferencias (MM$ clp)
mes Fecha Fecha (YYYY-MM-DD)

<!-- page 13 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 13 / 15


Documento impreso no controlado
5.3.1.3. Transmisión

• Definición dato: Empresas transmisoras que participan en la determinación de los pagos de Peajes del
SEN.
• Fuente de origen: Proceso de Liquidación de Peajes.
• URL: https://www.coordinador.cl/mercados/graficos/transferencias-economicas/transmision/
• Formato de descarga: TSV
• Filtros: mensual (mes y año)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Tramo valorizado
id Texto ID del tramo valorizado
Tramo valorizado
nombre Texto Nombre del tramo valorizado
Tramo id Número ID del tramo
Tramo nombre Texto Nombre del tramo
Propietario
mnemotecnico Texto Mnemotécnico del propietario en infotécnica
Empresa
explotadora
mnemotecnico
Texto Mnemotécnico de empresa explotadora en infotécnica
Ingreso tarifario
potencia Número Valor ingreso tarifario energía (MM$ clp)
Ingreso tarifario
energía Número Valor ingreso tarifario potencia (MM$ clp)
avi Número Valor AVI (MM$ clp)
peaje Número Valor Peaje (MM$ clp)
coma Número Valor COMA (MM$ clp)
vatt Número Valor VATT (MM$ clp)
segmento Texto  Segmento de pertenencia del tramo (nacional, zonal)
subsistema Texto Subsistema al que pertenece el tramo (sistema A, B, C, D, E y F)
Código
coordinador Número Código interno.
Fecha referencia
valorización Fecha Fecha de indexación (YYYY-MM-DD)
mes Fecha Fecha (YYYY-MM-DD)

<!-- page 14 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 14 / 15


Documento impreso no controlado
5.3.2. Costos Marginales

5.3.2.1. Costo Marginal Online

• Definición dato: El Costo Marginal Online  es un valor calculado a partir de las instrucciones de operación
emitidas por el Centro de Despacho y Control hacia los diversos Centros de Control del SEN. Este es un
resultado preliminar.
• Fuente de origen: Registro de Instrucciones de la Operación.
• URL: https://www.coordinador.cl/mercados/graficos/costos-marginales/costo-marginal-online
• Formato de descarga: TSV
• Filtros: diaria (fecha inicio y fecha de término)
• Datos: El cuadro de descargas pone a disposición un set de datos con la siguiente estructura.

Ítem Formato Comentarios
Fecha Fecha Fecha (YYYY-MM-DD) y Hora (hh:mm:ss)
Barra Texto Nombre barra
CMg Número Costo Marginal Online (USD/MWh)


5.3.2.2. Costo Marginal Real

• Definición dato: El Costo Marginal de energía corresponde al costo en que se incurre para suministrar una
unidad adicional de producto para un nivel dado de producción.
• Fuente de origen: Proceso de Cálculo de los Costos Marginales Reales.
• URL: https://www.coordinador.cl/mercados/graficos/costos-marginales/costo-marginal-real/
• Formato de descarga: TSV y XLSX
• Filtros: Barra, mes y año
• Datos: El cuadro de descargas de Costo Marginal Real pone a disposición un set de datos agrupados “por
Año y Barra” y “por Mes y Año”, y por formato TSV y XLSX para este último.

iv. Año y Barra TSV

Ítem Formato Comentarios
Barra
mnemotecnico Texto Mnemotécnico barra en infotécnica
Barra referencia
mnemotecnico Texto Mnemotécnico barra referencia en infotécnica
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)
Costo en dolares Número Costo marginal en dólares (USD/MWh)
Costo en pesos Número Costo marginal en pesos ($/kWh)
nombre Texto Nombre barra en infotécncia

<!-- page 15 -->

DICCIONARIO DE DATOS
PARA LA DESCARGA DE DATOS PORTAL WEB
SISTEMA DE INFORMACIÓN PÚBLICA (SIP)
Código: B43-DIN-01
Elaborado: 02-11-2022
Página: 15 / 15


Documento impreso no controlado
v. Mes y Año TSV

Ítem Formato Comentarios
Barra
mnemotecnico Texto Mnemotécnico barra en infotécnica
Barra referencia
mnemotecnico Texto Mnemotécnico barra referencia en infotécnica
fecha Fecha Fecha (YYYY-MM-DD)
hora Número Hora (hh)
Costo en dólares Número Costo marginal en dólares (USD/MWh)
Costo en pesos Número Costo marginal en pesos ($/kWh)
nombre Texto Nombre barra en infotécncia

vi. Mes y Año XSLX

Ítem Formato Comentarios
Valor Texto USD o $ (clp)
Barra -
Mnemotecnico Texto Mnemotécnico barra en infotécnica
Barra - Nombre Texto Nombre barra en infotécnica
Fecha Fecha Fecha (YYYY-MM-DD)
Hora Número Hora (hh)


5.3.3. Costos Combustibles

5.3.3.1. Stock de Combustibles

• Definición dato: Disponibilidad declarada por las empresas coordinadas para las centrales del SEN.
• Fuente de origen: Plataforma Sistema de Costos Variables e Información de Combustibles.
• URL: https://www.coordinador.cl/mercados/graficos/combustibles/stock-de-combustibles

Actualmente no cuenta con un sistema de descarga de datos.


5.3.3.2. Costos de Combustibles

• Definición dato: Costos declarados por las empresas coordinadas,  utilizados para el cálculo del Costo
Variable de cada unidad generadora.
• Fuente de origen: Plataforma Sistema de Costos Variables e Información de Combustibles.
• URL: https://www.coordinador.cl/mercados/graficos/combustibles/costos-de-combustibles-combustibles

Actualmente no cuenta con un sistema de descarga de datos.
