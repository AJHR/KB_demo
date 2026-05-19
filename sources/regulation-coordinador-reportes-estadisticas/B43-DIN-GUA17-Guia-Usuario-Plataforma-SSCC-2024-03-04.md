---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA17-Guia-Usuario-Plataforma-SSCC-2024-03-04.pdf
pdf_sha256: e38098e5a3c6f5bb9d7e3c8c2d1bf590ae28de2b401ce960f21044470643129f
pdf_pages: 22
extracted_pages: 22
extracted_chars: 18036
extracted_at: 2026-05-19T13:23:05Z
extractor: pypdf
---

# B43 DIN GUA17 Guia Usuario Plataforma SSCC 2024 03 04

<!-- page 1 -->

Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


Manual de Usuario
Usuarios Coordinados

Plataforma de
Subastas para Servicios
Complementarios


Versión: 1.0
Fecha del documento: 26 de Diciembre 2019

<!-- page 2 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
2 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Sumario
1 Introducción y objetivos ................................ ................................ .. 5
 Propósito del documento ............................................................................. 5
Conceptos generales ................................ ................................ ............... 6
2 Plataforma de Subastas para Servicios Complementarios -Usuario
Coordinado: ................................ ................................ .................. 7
 Inicio de aplicación ..................................................................................... 7
2.1.1 Acceso a la aplicación como Usuario Coordinado ............................................ 7
 Flujo de envío de ofertas ............................................................................. 9
2.2.1 Envío de ofertas por formulario .................................................................... 9
2.2.1.1 Creación de borrador: ............................................................ 11
2.2.1.2 Recuperación de borrador/configuración: .................................. 13
2.2.1.3 Formalización/envío de Oferta: ............................................... 16
2.2.2 Envío de ofertas mediante fichero: .............................................................. 17
2.2.3 Consulta de ofertas aceptadas .................................................................... 19
2.2.4 Consulta de Ofertas Adjudicadas: ................................................................ 21

<!-- page 3 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
3 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Resumen Ejecutivo
El presente documento constituye el manual de usuario  de la Plataforma Tecnológica de
Subastas de Servicios Complementarios  con las funcionalidades destinadas a los
coordinados del sistema eléctrico interconectado chileno Coordinador Eléctrico Nacional.

Glosario
Unidad Generadora Conjunto de componentes que transforman las distintas fuentes
de energía primaria (eólica, hidráulica, solar, biomas a,
geotérmica y térmica) en electricidad.
Componente Son componentes de una Unidad Generadora las turbinas a gas,
turbinas a vapor, turbinas hidráulicas, aerogeneradores, motores
y conjunto de paneles fotovoltaicos.
Arreglo Posibles combinaciones funcionales de componentes de la unidad
generadora, las cuales permiten a la unidad generadora producir
energía eléctrica.
Configuración
Operativa
Corresponde a un Arreglo y que tiene un costo variable de
operación asociado a un tipo o subtipo de energía primaria.
Coordinado o
Empresa
Coordinada
Todo propietario, arr endatario, usufructuario o quien opere, a
cualquier título, centrales generadoras, sistemas de transporte,
instalaciones para la prestación de servicios complementarios,
sistemas de almacenamiento de energía, instalaciones de
distribución e instalaciones d e clientes libres y que se
interconecten al sistema, en adelante “los Coordinados”, estará
obligado a sujetarse a la coordinación del sistema que efectúe el
Coordinador de acuerdo a la normativa vigente.
Son también coordinados los medios de generación que  se
conecten directamente a instalaciones de distribución, a que se
refiere el inciso sexto del artículo 149° de la Ley General de
Servicios Eléctricos y que no cumplan con las condiciones y
características indicadas en el artículo 149° bis, también
llamados “pequeños medios de generación distribuida.
Coordinador
Eléctrico Nacional
o Coordinador –
CEN
Coordinador Independiente del Sistema Eléctrico Nacional,
definido en el artículo 212 -1 de la Ley General de Servicios
Eléctricos, modificada por la Ley N° 20.936.
Ley N°20.936 Ley que establece un nuevo Sistema de Transmisión Eléctrica y
crea un Organismo Coordinador Independiente del Sistema
Eléctrico Nacional, publicada el 20 de julio de 2016.

<!-- page 4 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
4 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Días Siempre que no se indique lo contrario, significa lo mismo que
días hábiles, esto es, de lunes a viernes, en una secuencia
cronológica de 24 horas, contados desde la medianoche, sin
contar días sábados, domingos o festivos en Santiago de Chile.
Día N Día de operación para el cual es válida una subasta.
Servicios
Complementarios –
SSCC -
Prestaciones que permiten efectuar la coordinación de la
operación del Sistema Eléctrico Nacional. El Coordinador, a
través de los Servicios Complementarios, deberá preser var la
seguridad del servicio en el sistema eléctrico y garantizar la
operación más económica y de calidad para el conjunto de las
instalaciones del referido sistema.
Plataforma Sistema informático de servicios computacionales con las
funcionalidades de r ecepción y validación de ofertas para
subastas de Servicios Complementarios
CSF Control Secundario de Frecuencia
CTF Control Terciario de Frecuencia

<!-- page 5 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
5 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
1 Introducción y objetivos
 Propósito del documento
El presente documento contiene el manual de usuario de los Coordinados de la Plataforma
de Subastas de Servicios Complementarios para el Coordinador Eléctrico Nacional de
Chile.
El alcance del manual se centrará en la funcionalidad inicial definida para la  plataforma:
envío de borradores y ofertas mediante formularios web y/o meditante el uso de  ficheros
asi como consultas sobre sus operaciones.

<!-- page 6 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
6 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Conceptos generales

El alcance del manual de  la plataforma, se agrupa en los siguientes bloques funcionales:
1. Inicio de la aplicación: se indica como ingresar en la aplicación.
2. Envío de Ofertas: se indica como hacer borradores mediante formulario y fichero,
enviar ofertas y resto de funcionalidades adyancentes.
3. Consultas de ofertas aceptadas: se indica tanto la consulta para visualizar las
ofertas aceptadas.

<!-- page 7 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
7 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
2 Plataforma de Subastas para Servicios Complementarios -
Usuario Coordinado:

 Inicio de aplicación

2.1.1 Acceso a la aplicación como Usuario Coordinado

El link de acceso a la pla taforma, el cual estará contenido dentro del situo web del
Coordinador, así como el usuario y password para cada coordinado, se comunicará junto
con el lanzamiento de la plataforma.

Al acceder a la aplicación de la Plataforma se muestra una pantalla inicial con:
- Pestaña Coordinador
- Pestaña Coordinado
- Campos de credenciales: usuario y contraseña
- Check para recordar las credenciales
- Botón Ingresar


En el caso de acceder a la pestaña de Coordinado e introducir las credenciales correctas,
el sistema abre la pantalla de inici o con el menú superior para acceder a las diferentes
pantallas  que conforman la aplicación:

<!-- page 8 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
8 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Cabe mencionar que al ingresar por primera vez el sistema de autentific ación obliga al coordinado a
realizar un cambio de password.
Por otra parte, al ingresar por primera vez a la plataforma, se despliegara un pop -up (con un texto
aceptando las Bases Administrativas de cada coordinado sobre la plataforma, esta aceptación de
condiciones se realizará solamente la primera vez que se ingresa a la página).


En dicha pantalla inicial se muestra el menú superior en función de las operaciones
asociadas al perfil del usuario logado; así como los iconos de la parte superior derecha:

El icono  permite visualizar el usuario logado.
El icono permite abrir el listado de notificaciones que tenga el usuario. Al pulsar se
abre la siguiente pantalla con el listado de mensajes:

<!-- page 9 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
9 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
El icono  permite visualizar los datos de contacto de la aplicación PTSSC.
El icono  permite salir de la aplicación, cerrando la sesión del usuario logado.

 Flujo de envío de ofertas
Las ofertas para las cuales el Coordinado puede acceder mediante el siguiente menú
desplegable:


En los siguientes puntos se detalla la operativa para cada uno de los SSCC.
2.2.1 Envío de ofertas por formulario

El acceso al envío de ofertas mediante formulario se encuentra en el menú  Funciones
Generales > Envio de Ofertas > Control Secundario Subida > Formulario:


Los controles accesibles por el usuario en la interfaz de usuario son los siguientes:

<!-- page 10 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
10 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


Menú desplegable Coordinado: En este menú el usuario puede seleccionar el Coordinado
para el cual se va a remitir una oferta. En este desplegable apareceran la totalidad de los
Coordinados para los que el usuario tenga permisos.


Selección fecha de programación (fecha validez subasta): El usuario en este control debe
seleccionar la sesión para la cual desea formular una oferta y/o enviar un borrador:


Las fechas seleccionables en este menú corresponden a las sesiones (abiertas o cerradas)
para las cuales se han formulado ofertas en el pas ado o bien sesiones abiertas para las
cuales se desea formular ofertas.

El interfaz muestra al usuario los borradores y ofertas ya enviadas a la Plataforma:
A B C

<!-- page 11 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
11 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


En caso de existir sesiones abiertas para la fecha seleccionada esta se mostrará en la
interfaz de usuario en la parte superior derecha  junto a la fecha y hora de cierre de la
misma.

2.2.1.1 Creación de borrador:
El Coordinado puede generar un nuevo borrador de oferta mediante el control Añadir
Borrador:

Al activar el control en la parte de edición de la pantalla se generará un nuevo registro
correspondiente a la configuración y fechas establecidas en los controles B y C:

<!-- page 12 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
12 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


Se habilitarán tres cuadros de texto donde los precios de los tres bloques horarios pueden
establecerse. Una vez editados los valores dentro de los cuadros de texto, el borrador se
almacenará mediante el control Guardar Borrador:


Los borradores de oferta pueden editarse mediante el uso del control D  pudiendo aplicar
los cambios o descartarlos mediante el uso de los controles E y F:
B C
D

<!-- page 13 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
13 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional

Los borradores con precios más altos que los precios máximos son notificadas al usuario.
Sin embargo, dichos borradores son almacenados con las correspondientes validaciones:


NOTA: Los borradores enviados sólo estarán disponibles en la aplicación mientras las
sesiones estén abiertas, eliminándose de la plantalla una vez la sesión esté cerrada.
2.2.1.2 Recuperación de borrador/configuración:

El usuario puede recuperar configuraciones y/o ofertas pasadas para formular ofertas de
manera más ágil:

E F

<!-- page 14 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
14 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional

Mediante la selección de los mismos  estos se cargarán como borradores para la fecha
indicada en la página principal:

<!-- page 15 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
15 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional

<!-- page 16 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
16 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


2.2.1.3 Formalización/envío de Oferta:
Para el envío de ofertas el usuario debe seleccionar uno o varios borradores previamente
cargados en la aplicación y utilizar el control Enviar Oferta.

Una vez enviada la oferta esta se visualizará en la parte inferior del interfaz de usuario.

Validación contra precios máximos:
En caso de que los borradores contengan precios superiores a los precios máximos
establecidos en la Plataforma, la oferta esta será rechazada y el usuario será debidamente
informado mediante la aparición de mensajes en la parte derecha del interfaz:

En caso de no existir una sesión abierta para la fecha seleccionada el control de envío
de oferta permanecerá deshabilitado.

<!-- page 17 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
17 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional

2.2.2 Envío de ofertas mediante fichero:

La plataforma permite al usuario subir borradores de ofertas mediante ficheros
formateados (.CSV):

El nombre del fichero debe seguir el siguiente formato  (ejemplo)
“CSF_LW_0003_20191225_2.CSV” siendo:
CSF_LW_3_20191225_2.CSV: Descripción del servicio ofertado siendo:
CSF_ LW Control Secundario de Bajada
CSF_ UP Control Secundario de Bajada
CTF_LW Control Terciaria de Bajada
CTF_UP Control Terciaria de Subida

CSF_LW_0003_20191225_2.CSV: El primer numero del nombre del fichero correspode
con el código del coordinado el cual es único para cada cada coordinado, cabe mencionar
que el código de cada coordinado estará disponible en la plataforma . Nota: Se debe
respetar la cantidad de ceros contenidos en el código , esto aplica para el nombre de l
fichero como para los datos contenidos dentro del fichero . Cabe señalar que para
mantener los ceros del código la celda debe estar formato Texto.
CSF_LW_3_20191225_2.CSV: La sig uiente serie numérica idéntica la fecha de
programación en formato YYYYMMDD.
CSF_LW_3_20191225_2.CSV:El último dígito corresponde con la versión del borrador de
oferta para cada sesión.
Al subir un fichero con el formato correcto se muestra afimativo en la parte superior de
la interfaz. Cabe señalar que las ofertas cargadas por fichero serán cargadas inicialmente
como borradores en la Plataforma, a efectos de que el usuario pueda revisar y conocer
resultados de las validaciones realizadas por la Plataforma, previo a la formalización/envío
de las ofertas.

<!-- page 18 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
18 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


En caso contrario se mostrará el error correspondiente.


Formato del fichero CSV es el siguiente:

El formato del fichero CSV es el siguiente:

<!-- page 19 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
19 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
Coordinado,          configuración,                AÑO, MES, DIA, PERIOD, BAND, VALUE, MARGEN
0003,                ATACAMA-1TG1A_TG1A+0.5TV1_GNL_D,  2019,12,25,       1,    1,    15
0003,                ATACAMA-1TG1A_TG1A+0.5TV1_GNL_D,  2019,12,25,       9,    1,    16
0003,                ATACAMA-1TG1A_TG1A+0.5TV1_GNL_D,  2019,12,25,      19,    1,    39

La cabecera del fichero se compone de los siguientes campos:
Coordinado: Código Numérico del Coordinado correspondiente
Configuración: Configuración operativa del Coordinado
Año: Año del día de programación
Mes: Mes del día de programación
Día: Dia de Programación a la que el borrador de la oferta hace referencia
Period: Periodo de la oferta, donde:
• 1: bloque de horas comprendido entre 00:00 y las 07:59hrs.
• 9: bloque de horas comprendido entre 08:00 y las 18:59hrs.
• 19: bloque de horas comprendido entre 19:00 y las 23:59hrs.
BAND: Valor para futuras funcionalidades (valor 1 por defecto)
VALUE: Precio ofertado para cada banda. Nota: La plataforma soporta solo dos decimales.
MARGEN: Valor para futuras funcionalidades (vacío por defecto)
Una vez enviado el borrador de la oferta, esta puede consultarse siguiendo los pasos del
apartado 2.2.1.3 Formalización/envío de Oferta:.

2.2.3 Consulta de ofertas aceptadas

El usuario puede consultar las ofertas aceptadas por la Plataforma:

<!-- page 20 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
20 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


Los controles de búsqueda habilitados a los usuarios son:


La consulta muestra todas las ofertas aceptadas para todas las horas de los periodos
ofertados (valores horarios).
En la parte derecha el control acciones que se muestra al final de cada periodo horario
permite al usuario consultar los valores históricos de las ofertas , es decir las versiones,
así como los precios máximo correspondientes a cada bloque:

<!-- page 21 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
21 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional


El usuario puede exportar los resultados a ficheros Excel y PDF:


2.2.4 Consulta de Ofertas Adjudicadas:

De manera similar al punto anterior las ofertas adjundicadas pueden consultarse mediante
la consulta correspondiente:

<!-- page 22 -->

Manual de Usuario Plataforma SSCC
© Copyright 2011, Atos Worldgrid
22 de 22
Iniciales
Atos Worldgrid
Iniciales
Coordinador Electrico
Nacional
