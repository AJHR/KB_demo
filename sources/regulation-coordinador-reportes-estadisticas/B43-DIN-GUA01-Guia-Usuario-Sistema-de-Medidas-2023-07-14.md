---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA01-Guia-Usuario-Sistema-de-Medidas-2023-07-14.pdf
pdf_sha256: f530754a0cc499d91d206f603888bc1112dd6990cd3afeed8a207cd2f0ba4d05
pdf_pages: 9
extracted_pages: 9
extracted_chars: 14892
extracted_at: 2026-05-19T13:23:00Z
extractor: pypdf
---

# B43 DIN GUA01 Guia Usuario Sistema de Medidas 2023 07 14

<!-- page 1 -->

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 1 / 9

INDICE DE CONTENIDOS
1. Introducción .............................................................................................................................................. 2
2. Ingreso de Usuario e inicio ....................................................................................................................... 2
3. Módulos y funcionalidades ....................................................................................................................... 3
3.1. Documentación: .................................................................................................................................... 3
3.1.1. Normativa: .................................................................................................................................... 3
3.1.2. Presentaciones ............................................................................................................................. 3
3.1.3. Instructivos y manuales ................................................................................................................ 3
3.1.4. Descargas ..................................................................................................................................... 3
3.2. Aplicaciones: ......................................................................................................................................... 4
3.2.1. Registro desde plataforma de medidas ........................................................................................ 4
3.2.1.1. Bitácora ..................................................................................................................................... 5
3.2.2. Recolector de medidas (requiere autenticación) .......................................................................... 6
3.3. Reportes: .............................................................................................................................................. 7
3.3.1. Medidores habilitados en plataforma de medidas ........................................................................ 7
3.3.2. Medidas históricas ........................................................................................................................ 7
3.3.3. Factor de disponibilidad ................................................................................................................ 8
3.3.4. Medidas transferencias económicas ............................................................................................ 8
3.3.5. Balance físico de energía Art. 3-30 norma técnica de coordinación y operación. ....................... 9
3.4. Preguntas ............................................................................................................................................. 9
3.5. Contacto ............................................................................................................................................... 9


CONTROL DE CAMBIOS

VERSIÓN FECHA COMENTARIO DE LA MODIFICACION RESPONSABLE
01 14-07-2023 Versión inicial Juan Soto Riveros


DOCUMENTOS DECLARADOS

CODIGO NOMBRE DOCUMENTO


ELABORACIÓN Y APROBACIÓN

ELABORADO POR REVISADO POR APROBADO POR
Juan Soto Tomás Valenzuela
Nombre Apellido Nombre Apellido Nombre Apellido

<!-- page 2 -->

2

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 2 / 9


GUÍA DEL USUARIO
Sistema de Medidas: Página web de Sistemas de medidas.


1. Introducción

El sistema de medidas web considera las aplicaciones asociadas a la Plataforma de Medición de Energía del
Coordinador Eléctrico Nacional, definida en la Normativa vigente.

En la página web se pone a disposición de todas las empresas Coordinadas y público general, aplicaciones y
módulos que permiten descargar medidas de energía de los puntos que participan en el proceso de transferencias
económicas del Coordinador Eléctrico Nacional.

2. Ingreso de Usuario e inicio

Esta es la pantalla de inicio de la página web Sistema de Medidas desde donde se puede acceder a las distintas
secciones del sistema.

La URL de la página web Sistema de Medidas es la siguiente: https://medidas.coordinador.cl/

El sistema considera las siguientes secciones/módulos:

• Documentación
• Aplicaciones
• Reportes
• Preguntas
• Contacto

<!-- page 3 -->

3

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 3 / 9


3. Módulos y funcionalidades

3.1. Documentación:

En esta sección se pone a disposición para empresas Coordinadas y público general, la información relacionada
con el sistema de medidas web, presentaciones realizadas por el Coordinador, normativa asociada a medición,
instructivos y manuales.

3.1.1. Normativa:

En esta sección de la página se podrá tener acceso a las normas aplicable al sector eléctrico, tanto en lo relativo
a su funcionamiento como a los diversos agentes del mercado. Se pueden descargar en formato .pdf tod a la
normativa, anexos, documentos técnicos, actas y guías relacionados al marco regulatorio del Sistema de Medidas
para Transferencias Económicas.

3.1.2. Presentaciones

En este apartado podrá se pueden visualizar y descargar en formato.pdf todas las presentaciones oficiales
realizadas por el Departamento de Medición de Energía del del Coordinador Eléctrico Nacional.

3.1.3. Instructivos y manuales

Se encuentran los enlaces a los manuales y/o instructivos del sistema de medidas, estos podrán ser descargados
en formato PDF.

• Manual Recolector Medidas
• Manual Sistema de Medidas

3.1.4. Descargas

En esta sección, se pueden descargar en formato comprimido (zip o rar) instaladores y complementos asociados
a las aplicaciones disponibles para el acceso a las medidas de las empresas coordinadas, en particular permite
la descarga del software necesario para instalar el aplicativo Recolector de Medidas:

• Instalador Base de Datos SQL SERVER
• Instalador Recolector de Medidas
• Scripts Recolector de Medidas

<!-- page 4 -->

4

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 4 / 9


3.2. Aplicaciones:

3.2.1. Registro desde plataforma de medidas

En esta aplicación se podrá descargar un archivo Excel o CSV con los datos correspondientes a los criterios de
búsqueda seleccionados:

• Coordinado: Muestra todos los coordinados en orden alfabético. Al seleccionar un coordinado se
actualizan los siguientes campos: subestación, nivel de tensión y punto de medida.
• Subestación: Por defecto muestra todas las subestaciones en orden alfabético. Si se selecciona un
coordinado, se muestra las subestaciones asociadas a él. Al seleccionar una o varias subestaciones, se
actualizan los siguientes campos: nivel de tensión y punto de medida.
• Nivel de Tensión: Por defecto muestra todos los niveles de tensión. Si se selecciona un coordinado y/o
subestación, se muestra los niveles de tensión asociada a ellos. Es un campo de selección múltiples. Al
seleccionar uno o varios niveles de tensión, se actualiza el campo punto de medida, y se guarda en la
sesión el valor seleccionado.
• Punto de medida: Muestra todos los puntos de medidas
• Periodo: Muestra los últimos 5 periodos (incluido mes en curso) en formato Mes- Año.
• Frecuencia Registro: Es un campo de selección simple, las opciones son 1 Hora o 15 minutos.
• Tipo de Archivo: Es un campo de selección simple, las opciones son Excel XLSV o CSV.
• Botón descargar: Permite realizar la descarga del archivo Excel o Csv  con los criterios de filtro
establecidos en los filtros.
• Botón Limpiar: Permite eliminar todos los filtros establecidos, en cada uno de los campos se mostrará los
valores por defecto.

<!-- page 5 -->

5

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 5 / 9


Ejemplo archivos Excel 15 minutos y CSV horario:


3.2.1.1. Bitácora

Dentro del aplicativo “Registro de Medidas (PRMTE)”, existen las bitácoras de intervenciones, en donde se podrá
descargar un archivo con el registro de las modificaciones y carga de datos provenientes del módulo Recolector
de Medidas, con el objetivo de dar trazabilidad a la información utilizada por el Coo rdinador en el Plataforma de
Medidas:

<!-- page 6 -->

6

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 6 / 9


En el archivo, se puede identificar la fecha de intervención que corresponde a cuando se realizó la carga de las
medidas. Por otra parte, se identifica la fecha de inicio y fin de los registros que fueron cargados.

3.2.2. Recolector de medidas (requiere autenticación)

Recolector de medidas es un módulo que utiliza la aplicación de terreno “Prime Mobile”, que nace de la necesidad
de solucionar aquellos inconvenientes en la interrogación remota de los medidores desde la plataforma del
Coordinador (PRMTE), asegurando la recolección tanto del perfil de carga, registros y eventos de los equipos de
medida, en cualquier situación en la que las comunicaciones remotas presenten fallas y/o no se disponga de otro
tipo de enlace para la conexión con la PRMTE.

El uso del aplicativo y su instalación se detalla en la sección Instructivos y manuales: Manual Recolector Medidas
y para su uso, se requieren credenciales de acceso que deben ser solicitadas sistemas.medidas@coordinador.cl

En la esquina superior derecha se encuentra el enlace “I ngreso Coordinados” el cual levantará un formulario de
autenticación que le permitirá el acceso a las aplicaciones que requieren Usuario y contraseña:

Esta aplicación permite a los usuarios subir archivos en formato PRMTE al sistema de medidas del coordinador.

<!-- page 7 -->

7

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 7 / 9


En esta pantalla se deberá completar:

• Coordinado: Se presenta el nombre de la empresa Coordinada, asociado al usuario con el cual se ingresó
la autenticación del Sitio web.
• ID Medidor: Muestra lista con todos los medidores asociados al c oordinado. debiendo ser seleccionado
uno de ellos. Por default se presenta el primer ID Medidor asociado al coordinado, ordenado por orden
alfabético del ID.
• Fecha de Inicio: Campo informativo se muestra la fecha - hora del último dato leído para ese medidor.
• Fecha de Fin: Se debe indicar la fecha - hora de fin de la información que se está cargando.
• Email: Campo informativo se detallan los correos a los cuales se informará del ingreso de la información
(encargado titular y suplente de la empresa Coordinada)
• Mensaje: Se permite ingresar algún mensaje pertinente al archivo que se desea cargar.

• Cargar Archivo PRMTE: Al presionar el botón de carga se podrá seleccionar el archivo que desea subir.
El nombre del archivo debe ser idéntico al ID del medidor seleccionado y debe tener una extensión. bmm.
El tamaño máximo del archivo es de 5MB.

• Enviar Archivo: Para concretar la carga del archivo se deberá dar click en el botón ENVIAR.
• Se enviará un email a encargado titular y suplente con la información del formulario  y copia del
archivo.
• Se mostrará un mensaje de carga exitosa.

• Limpiar: Si presiona el botón Limpiar se eliminará la información que haya seleccionado.

3.3. Reportes:

3.3.1. Medidores habilitados en plataforma de medidas

Se encuentra un enlace el cual le permitirá hacer la descarga del archivo Socket_habilitado.xlsx, con información
de todos los medidores habilitados. El reporte se actualiza diariamente.

3.3.2. Medidas históricas

En esta sección se podrán descargar los reportes históricos de medidas. La información está organizada por Año
→Mes →Frecuencia de integración (15Min- 1Hora) → Formato (Excel, Csv).

La información para descargar está disponible en archivos .ZIP que contienen planillas Excel (o Csv para el caso
de 15 minutos), con la información de las medidas correspondientes a la selección realizada.  El criterio de
agrupación de la información en cada archivo ZIP Excel es la letra inicial del nombre del punto de medida
correspondiente.

El nombre del archivo se conforma de la siguiente forma: “Subestacion_x_yyyy_zzzz.zip”, donde:

• x Letra Inicial de Puntos de Medidas Contenidos en Archivo, ordenados por Subestación.
• xyyy Frecuencia de integración de las medidas (15Min o 1Hora).
• xzzz Formato (Csv o Excel).

Por restricciones técnicas cada planilla Excel contiene un máximo de 100 puntos de medida, por lo que en cada
archivo ZIP puede haber más de un archivo Excel según cuantos puntos de medida clasifiquen con la agrupación
indicada.

<!-- page 8 -->

8

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 8 / 9


En el caso del ejemplo (Subestacion_A_15MIN_xlsx.zip) el archivo contiene 3 archivos Excel, a saber:


3.3.3. Factor de disponibilidad

De acuerdo con lo señalado en el Anexo Técnico Sistemas de Medidas para Transferencias Económicas  el
Coordinador las empresas coordinadas deberán garantizar una disponibilidad de información mayor o igual  a
97%, medida en una ventana móvil de 12 meses, incluyendo en el cálculo la disponibilidad  de los EM, mediante
el reporte adjunto se publica el cumplimiento de cada empresa Coordinada:


3.3.4. Medidas transferencias económicas

Este reporte corresponde a las medidas que son informadas mensualmente para su utilización en el proceso de
cálculo del balance de energía y transferencias económicas.

<!-- page 9 -->

9

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
SISTEMA DE MEDIDAS
Código:
Elaborado: 14-07-2023
Página: 9 / 9


3.3.5. Balance físico de energía Art. 3-30 norma técnica de coordinación y operación.

Este reporte corresponde al balance físico de energía simplificado, el cual incluye las inyecciones y retiros a las
cuales tiene acceso el  Coordinador mediante la  plataforma PRMTE, en las barras del sistema de 110 kV o
superiores, de manera de dar cuenta de las pérdidas por cada tramo del Sistema de Transmisión.

3.4. Preguntas

En esta sección se desplegarán las preguntas y respuestas generales con el objetivo de que puedan ser
visualizadas por cualquier visitante del sitio y que buscan aclarar dudas sobre la usabilidad del sitio web.

3.5. Contacto

Finalmente, en el apartado de Contacto, se pueden poner en contacto con el Departamento de Medición de
Energía del Coordinador, en caso de consultas y/o requerimientos particulares de  los interesados:
