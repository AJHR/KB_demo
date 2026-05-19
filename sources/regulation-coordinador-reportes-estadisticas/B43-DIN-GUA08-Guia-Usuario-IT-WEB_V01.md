---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA08-Guia-Usuario-IT-WEB_V01.pdf
pdf_sha256: f4add4b689b1560c061e737ac9fdf587cde9a6c5c832be9f2125609ca74219bb
pdf_pages: 18
extracted_pages: 18
extracted_chars: 11685
extracted_at: 2026-05-19T13:23:01Z
extractor: pypdf
---

# B43 DIN GUA08 Guia Usuario IT WEB V01

<!-- page 1 -->

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 1 / 18


ÍNDICE DE CONTENIDOS

CONTEXTO
COMO SE OBTIENE LA INFORMACIÓN
CONEXIÓN CON OTRAS PLATAFORMAS
¿CUÁL ES SU OBJETIVO PRINCIPAL?
¿QUIÉNES INTERACTÚAN EN ESTE SISTEMA?
TIPOS DE USUARIOS
INCIDENCIAS EN EL USO DE LA PLATAFORMA


CONTROL DE CAMBIOS

VERSIÓN FECHA COMENTARIO DE LA MODIFICACION RESPONSABLE
01 20-09-2023 Versión inicial DAIT


DOCUMENTOS DECLARADOS

CODIGO NOMBRE DOCUMENTO


ELABORACIÓN Y APROBACIÓN

ELABORADO POR REVISADO POR APROBADO POR
INDRA Juan Quezada Victor Alvarez
Nombre Apellido Nombre Apellido Nombre Apellido

<!-- page 2 -->

2

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 2 / 18


GUÍA DEL USUARIO
Infotécnica Web

CONTEXTO

De acuerdo con lo indicado en el Articulo 72-8 de la Ley General de Servicios Eléctricos, “el Coordinador Eléctrico
Nacional, deberá implementar sistemas de información pública que contengan las principales características
técnicas y económicas de las instalaciones sujetas a coordinación”. En particular las plataformas de Infotécnica,
contiene lo requerido en el literal a):

Características técnicas detalladas de todas las instalaciones de generación, transmisión y clientes libres
sujetas a coordinación, tales como, eléctricas, constructivas y geográficas; y de instalaciones de
distribución, según corresponda.

Cabe destacar que el detalle de la información que contiene la plataforma se encuentra indicado en el Anexo
Técnico “Anexo Técnico: Información Técnica De Instalaciones y Equipamiento” , en adelante Anexo
Técnico, el cual se encuentra público en la página de la Comisión Nacional de Energía.

Es en este Anexo Técnico, se especifica lo siguiente:

Artículo 4, literal c), dentro de las funciones del Coordinador se encuentra “Recopilar, organizar y administrar la
incorporación y actualización de la Información Técnica entregada por los Coordinados en la BDIT .”
Artículo 6, primer y segundo inciso, que “El Coordinador administrará en su sitio Web un sistema computacional
habilitado para la entrega de información, modificación, actualización y registro histórico de Información Técnica
de las instalaciones sujetas a coordinación. La BDIT registrará además a l responsable y la fecha de entrega de
cada Información Técnica por parte de cada Coordinado. Este sistema será de uso obligatorio para todos los
Coordinados, quienes deberán disponer de los medios necesarios para poder operar con el sistema definido por
el Coordinador en el marco del presente Anexo”.

La plataforma Infotecnica Web, entre otras funciones, permite dar cumplimiento a lo indicado anteriormente, junto
permitir visualizar públicamente el registro de toda la información técnica de las instalaciones que se encuentran
registradas en la plataforma Infotécnica Instalaciones y que se encuentran en operación.

Esta web permite visualizar dicha información (Fichas Técnicas y sus Anexos), visualizar gráficos con el grado
de completitud y calidad de los registros, visualizar las instalaciones a través de un mapa, etc.

<!-- page 3 -->

3

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 3 / 18


COMO SE OBTIENE LA INFORMACIÓN

El ingreso de la información de las instalaciones de las empresas, en operación o en proyectos es ingresada a
través de la aplicación Infotécnica Instalaciones (https://ingresoweb.coordinador.cl/).

Para aquello, los usuarios ingresan con sus credenciales entregadas por el respectivo aplicativo.


Luego seleccionan el tipo de instalación que desean actualizar la información.


A continuación, seleccionan la instalación.

<!-- page 4 -->

4

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 4 / 18


Por cada instalación o equipo existe el ingreso de una ficha técnica.


Luego esta información es obtenida, guardada en la BD, procesada y desplegada en Infotécnica Web
(https://infotecnica.coordinador.cl/).

<!-- page 5 -->

5

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 5 / 18

<!-- page 6 -->

6

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 6 / 18


También la información con la que cuenta Infotécnica Web es utilizada por otros sistemas del  coordinador,
como el ID de las instalaciones por que es rescato por Opreal, el nombre de las instalaciones obtenido por
Neomante, etc.

<!-- page 7 -->

7

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 7 / 18


CONEXIÓN CON OTRAS PLATAFORMAS

El siguiente esquema, muestra la conexión de la plataforma Infotecnica Web con otros aplicativos del
Coordinador, y quienes consumen su información.

<!-- page 8 -->

8

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 8 / 18


¿CUÁL ES SU OBJETIVO PRINCIPAL?

Registrar la información técnica de cada uno de las instalaciones o equipos, poder certificar dicha información por
medio de los Anexos que son los datos de placa o hoja de vida de las instalaciones disponibilizada por el
coordinado; con estos anexos el co ordinador corrobora la información que se encuentra en la ficha técnica,
además, complementa esta revisión con la revisión del Diagrama unilineal, sistema Scada, diagrama unilineal
general e informes de protecciones; Sí, todo esto concuerda se valida, de l o contrario se pregunta al coordinado
y en caso de no haber certeza se realiza una auditoría y se va a terreno a buscar la instalación.

El objetivo principal por lo que esta BD fue creada, es para resguardar dicha información, ya que una ley le exige
al coordinador disponibilzar esta información a todo público sin costo alguno por normativa.

¿QUIÉNES INTERACTÚAN EN ESTE SISTEMA?

Los usuarios Coordinadores: Administran conceptos generales de la página como preguntas frecuentes,
contactos, información legal, validan la información de los nuevos proyectos, consistencia de los datos,
completitud y calidad, revisión de la información desplegada en los reportes y gráficos de las instalaciones.

Los usuarios coordinados: Accede a visualizar, descargar la información técnica e informar sí los datos no están
correctos.

Público en general: Accede a visualizar la información para fines personales como académicos.

Actividades que realizan los Coordinadores

Los coordinadores coordinan todas las instalaciones desde Arica a Chiloé y parte de los sistemas medianos, en
donde hay toda una red de instalaciones eléctricas que están interconectadas; todas las centrales inyectan
energía a lo largo del país a través de  líneas de transmisión, estas líneas llegan a las subestaciones y luego se
transmite energía hacía las comunas o las ciudades; esta energía se inyecta independiente de donde este.

La información de las instalaciones o equipos que componen lo indicado, ya sea transformador, barra,
transformador de potencial, etc, se encuentra en cada equipo en una placa.


Esta información es entregada por los coordinados y es registrada en las fichas técnicas, validada con los
diagramas unilineales, scada y anexos. Toda esta información es revisada en infotécnica web por el coordinador
en cuanto a consistencia, cumplimiento  y calidad de manera que dicha información este visible al público en
general.

Algunas de las vistas de Infotécnica Web.

<!-- page 9 -->

9

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 9 / 18


Vista principal:


En esta vista se puede visualizar a través del mapa las instalaciones existentes por regiones.


Se puede acceder a la información de las instalaciones, propietarios, sus anexos y fichas técnicas .

<!-- page 10 -->

10

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 10 / 18


Se puede visualizar los campos completos y datos certificados de la ficha técnica.

Vista Proyecto:


Se puede visualizar la completitud y Calidad de todos los proyectos y visualizar gráficos con la
completitud y calidad de los proyectos en general.

<!-- page 11 -->

11

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 11 / 18


Se puede visualizar detalle de un proyecto, descargar PDF con esta información y visualizar gráficos.

<!-- page 12 -->

12

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 12 / 18

<!-- page 13 -->

13

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 13 / 18


Vista Grado de Cumplimiento:


Se visualiza la información general de la información técnica de las empresas, descargar Excel y visualizar
gráficos con los datos por informar, los datos informados y completitud y calidad de los datos.

<!-- page 14 -->

14

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 14 / 18


Se puede visualizar el detalla de la información técnica de una empresa en particular, Excel de sus instalaciones
y gráficos.

<!-- page 15 -->

15

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 15 / 18


Vista Material de ayuda: Es de ayuda general y administradas por el coordinador.


Vista preguntas frecuentes: Es de ayuda general y administradas por el coordinador.


Vista contacto: Es de ayuda general y administradas por el coordinador.

<!-- page 16 -->

16

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 16 / 18


Vista Activos de Transmisión: link a otra aplicación del coordinador.


Vista Ingreso Información Técnica Instalaciones: link a otra aplicación del coordinador.

<!-- page 17 -->

17

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 17 / 18


TIPOS DE USUARIOS

Todos los usuarios, ya sea coordinados y público en general, pueden ingresar a la web y visualizar y descargar
toda la información de las instalaciones.

<!-- page 18 -->

18

DOCUMENTO INTERNO
GUÍA DEL USUARIO PARA LA PLATAFORMA
INFOTÉCNICA WEB
Código: B34-DIN-XX
Elaborado: 20-09-2023
Página: 18 / 18


INCIDENCIAS EN EL USO DE LA PLATAFORMA

En caso de que los usuarios experimenten dificultades en el uso de la plataforma, estas deben ser enviadas a la
casilla soporte.infotecnica@coordinador.cl, para la cual deben incluir al menos la siguiente información.

• Datos de contacto
• Imagen con mensaje de error
• Descripción del problema, incluyendo un paso a paso de las acciones realizadas al momento de
presentarse la incidencia.

Cabe destacar que, una vez recibida la incidencia, el ingeniero gestor del Departamento, ingresa la incidencia en
la mesa de ayuda y responde al usuario indicando el N° de ticket con el que se registró la incidencia para futuras
consultas.

En caso de que la incidencia afecte a otros procesos, esta será informada desde la casilla
soporte.infotecnica@coordinador.cl a los Departamentos que pueden verse afectados indicando el N° de ticket
de la mesa de ayuda.
