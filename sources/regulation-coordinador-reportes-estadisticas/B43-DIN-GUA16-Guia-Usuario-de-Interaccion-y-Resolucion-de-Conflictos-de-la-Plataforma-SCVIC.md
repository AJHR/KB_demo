---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA16-Guia-Usuario-de-Interaccion-y-Resolucion-de-Conflictos-de-la-Plataforma-SCVIC.pdf
pdf_sha256: ad58a1a8538424e55a0b88d5e3c39ee50457cbf652a35399d1cfd5d974349bd0
pdf_pages: 11
extracted_pages: 11
extracted_chars: 16034
extracted_at: 2026-05-19T13:23:05Z
extractor: pypdf
---

# B43 DIN GUA16 Guia Usuario de Interaccion y Resolucion de Conflictos de la Plataforma SCVIC

<!-- page 1 -->

Hito 4:
Guía de Interacción y resolución de
conflictos de la Plataforma SCVIC


Gerencia de Mercados
Departamento de Análisis Económico

<!-- page 2 -->

1


Índice
1 Introducción .......................................................................................................................... 2
2 Acceso a Plataforma. ............................................................................................................. 3
2.1 Previo a acceder a la plataforma. .................................................................................. 3
2.2 Nuevo Usuario. .............................................................................................................. 3
2.3 Inicio de Sesión. ............................................................................................................. 3
3 Costos Combustible. .............................................................................................................. 4
3.1 Actualización de Costos combustibles y declaración de nuevos Combustibles e
insumos. .................................................................................................................................... 4
3.1.1 Archivo XML .......................................................................................................... 4
3.1.2 Declaración del Costo Combustible en el SCVIC. .................................................. 4
4 Disponibilidad e Inventario de combustibles. ....................................................................... 5
4.1 Declaración GNL y modificaciones por serie. ................................................................ 5
4.2 Programa Anual de Entregas. ........................................................................................ 6
5 Costos Variables no combustibles. ........................................................................................ 7
5.1 Declaraciones de costos variables no combustibles. .................................................... 7
6 Gestión GNL. .......................................................................................................................... 7
6.1 Ingreso de acuerdos de Suministro y Mercados Secundarios. ..................................... 7
6.2 Observaciones Estudio GNL. ......................................................................................... 8
7 Informe de Combustible art.2-10 .......................................................................................... 9
8 Archivos para realizar declaraciones. .................................................................................. 10

<!-- page 3 -->

2

1 Introducción

La plataforma de Costos Variables e Información de Combustibles (SCVIC 1), es una
aplicación tecnológica a  cargo del Departamento de Análisis Económico (DAE) , que
forma parte de la Subgerencia de la Programación . A través de sus distintos módulos
permite consolidar , clasificar y estandarizar  información ingresada por l as empresas
coordinadas de forma diaria, s emanal, mensual y anual, teniendo como propósito dar
cumplimiento a los establecido en los requerimientos  de la “Norma Técnica para la
Programación y Coordinación de la Operación de unidades que utilices Gas Natural
Licuado regasificado” ( NT GNL)  y la reci ente “Norma Técnica de la coordinación y
operación del sistema eléctrico nacional – Capítulo sobre declaración de Costos
Variables” ( NT CyO). Otro aspecto fundamental de contar con esta plataforma
tecnológica es dar cumplimiento a lo indicado en el artícul o 50 del Decreto 125,
Reglamento de la Coordinación y Operación del Sistema Eléctrico Nacional , donde el
Coordinador será responsable de resguardar la completitud, trazabilidad y veracidad de
la información utilizada en la programación de la operación.

Las actualizaciones frecuentes de las normativas relacionadas con la declaración de
costos de combustibles generan cambios en la plataforma SCVIC, lo que podría llevar a
que los usuarios no estén familiarizados con ciertas funcionalidades, resultando en
ocasiones en un uso incorrecto o incompleto de la misma . Este documento  busca
minimizar los inconvenientes habituales y mejorar la experiencia de usuario  con
indicaciones prácticas pero efectivas.

Sin perjuicio de lo anterior, al registrars e alguna duda con el funcionamiento m ódulo,
formato o unidad de medida, no dude en tomar contacto a la casilla de correo electrónico
analisiseconomico@coordinador.cl.


1 SCVIC - Coordinador Eléctrico Nacional

<!-- page 4 -->

3

2 Acceso a Plataforma.
2.1 Previo a acceder a la plataforma.
Para acceder a la plataforma SCVIC, es indispensable que el usuario esté registrado en el
Registro Único de Coordinados (REUC 2). Se destaca la importancia de tener en cuenta
las siguientes indicaciones:
• Los Encargados, tanto Titular como Suplente, son responsables ante el
Coordinador de realizar o validar las solicitudes para la creación de usuarios en
REUC. Esto se debe llevar a cabo mediante el envío de la petición a través de
soporte.reuc@coordinador.cl.
• Todos los encargados cuentan con acceso a REUC y tienen el perfil necesario para
añadir como usuario a aquellos que consideren conveniente.
• Es necesario estar registrado en REUC para obtener el Acceso Único, ya que
REUC funciona como validador tanto para empresas como para los usuarios
asociados a ellas.
2.2 Nuevo Usuario.
Para solicitar un Nuevo Usuario, favor de contactar a través del correo
analisiseconomico@coordinador.cl. En el asunto del correo, especificar “Nuevo Usuario
SCVIC” y en el cuerpo del mensaje proporcionar los siguientes datos:
• Nombre Completo Usuario.
• RUT Usuario:
• Empresa:
• Centrales:
• Correo Electrónico:
• Teléfono o celular de Contacto:
Nota: Solo podrán solicitar un usuario de la plataforma SCVIC los Coordinados sujeto a
las declaraciones de costos, según lo indicado en el art. 2-1 de la NT CyO.
2.3 Inicio de Sesión.

Figura N°1: Ventana de ingreso SCVIC.

Finalmente, el usuario declarante podrá acceder al SCVIC utilizando las mismas
credenciales (Usuario y Contraseña) de la plataforma REUC.

2 REUC - Coordinador Eléctrico Nacional

<!-- page 5 -->

4

3 Costos Combustible.
3.1 Actualización de Costos combustibles y declaración de nuevos
Combustibles e insumos.
3.1.1 Archivo XML
En la Figura N°2, se presenta el menú de la Macro (ver punto 8) que facilitará la creación
de un archivo de tipo  XML, el cual es compatible con la plataforma para cada tipo de
combustible.

Figura N°2: Menú Macro: “Declaración de costos de combustible e insumos”.


Antes de declarar, es esencial tener en cuenta las siguientes indicaciones:
• Rellenar sección “Empresa generadora”.
• Rellenar sección “Fecha Inicio Vigencia” solo del combustible que se declarará.
• Rellenar sección “Directorio de trabajo”.
• Con respecto a la hoja Excel dedicada a cada combustible, es fundamental rellenar
toda la información de la columna “Dato/Información”.
3.1.2 Declaración del Costo Combustible en el SCVIC.
Para poder cargar el archivo XML en la sección mostrada en la Figura N°3, hay que tener
en consideración lo siguiente:
• No olvidar cargar  el archivo en la sección “Archivo XML declaración de costo
combustible” y la memoria de cálculo en la sección del “Informe Justificativo”.
• Todo documento que justifique el cálculo y sea de carácter reservado, se debe
cargar en la sección “Antecedentes adicionales”
• Si la declaración de costos corresponde a un “Combustible sólido Fósiles
(embarques recibidos”, se desplegará un campo tipo lista (nombre de embarque
y código de carga) para que seleccione del listado el embarque a reemplazar.
• La declaración de “Combustible GNL Regas (Según NT de GNL)” , se debe
realizar según las indicaciones del punto 4.1.

<!-- page 6 -->

5


Figura N°3: Menú Macro: “Declaración de costos de combustible e insumos”.

4 Disponibilidad e Inventario de combustibles.
4.1 Declaración GNL y modificaciones por serie.
En esta sección se realiza la declaración de costos combustibles y disponibilidad
volumétrica del GNL, en una ventana de información de 8 semanas.
Seleccionando el tipo de Terminal, automáticamente aparece lo opción de declaración de
GNL para las distintas series, como se muestra en la Figura N°4.


Figura N°4: Ejemplo Declaración GNL.

Considerar los siguientes puntos antes de rellenar los campos de la declaración y cargar
los archivos relacionados:
• No olvidar cargar el archivo en la sección “Archivo XML declaración de costo
combustible” y la memoria de cálculo en la sección del “Informe Justificativo”.
• Todo documento que justifique el cálculo y sea de carácter reservado, se debe
cargar en la sección “Antecedentes adicionales”.
• Se pueden realizar declaraciones simultaneas de mas de una serie, sin embargo,
los archivos a cargar en “Informe Justificativo” y “Antecedentes adicionales”,
deben contener la información de todas las series que se están declarando.
• La “Declaración Semanal”, asociada al artículo 3-3 Declaración GNL de la NT
GNL, se debe realizar semanalmente todos los martes antes de las 11:59 am. De
lo contrario, el sistema no dejará ingresar la información.

<!-- page 7 -->

6

• De requerir utilizar la “Modificación Declaración Semanal”, dado un cambio en
la ventana de información vigente, se deberá acoger a unos de los Numerales que
se desplegaran al elegir esta opción.
• Dado que se puede hacer uso de las funciones “Copiar” y “Pegar” Se recomienda
utilizar la hoja “Ventana de Información” mostrada en la Figura N°5 de la Macro:
“Declaración de costos combustibles e insumos ”, como base para rellenar los
campos requeridos en el formulario que se desplegará en el SCVIC.

Figura N°5: Formulario Ventana de información GNL.

4.2 Programa Anual de Entregas.
La declaración tanto de Carbón como de GNL comparte los campos a completar de:
• Nombre de embarque/nombre buque.
• Fecha de arribo.
• País de origen.
• Cantidad estimada.
• Tipo de Carga.
• Terminal.
En el caso del GNL, se solicita más puntos a rellenar, como lo muestra la Figura N°6.

Figura N°6: Ejemplo de Declaración Programa Anual de Entregas GNL.

<!-- page 8 -->

7

Es necesario considerar las siguientes indicaciones para hacer un correcto uso del
espacio de declaración:

• Para el campo de “Distribución anual de volumen”, se debe cargar un archivo
de tipo Excel que contenga el volumen dedicado a generación el cual debe estar
repartido por semana GNL y separado por series.
• Para poder completar los campos de “Acuerdo de Suministro” y “Acuerdo de
Mercado Secundario”, previamente es necesario cargar la información indicada
en el punto 6.1.
• La lista que se desplegará en los campos “Acuerdo de Suministro” y “Acuerdo
de Mercado Secundario”, tienen relación al nombre ingresado en el campo
“Informe Ejecutivo Sección 1” de la Figura N°8.


5 Costos Variables no combustibles.
5.1 Declaraciones de costos variables no combustibles.
Existen tres componentes del Costo Variable No Combustible:
• CVNCa: Costo Variable No Combustible de Abatimiento.
• CVONC: Costo Variable de Operación No Combustible.
• CVM: Costo Variable de Mantenimiento.
Si la central requiere una actualización de alguno de los tres  costos, la plataforma
permitirá declarar simultáneamente por cada unidad de esta el costo relacionado a
“Operación o Despacho en orden económico” y “Operación o Despacho fuera de orden
económico”, definido el art . 2-28 de la NT CyO. Es importante recordar adjuntar los
archivos relacionados a la declaración, de lo contrario el sistema no permitirá finalizar el
proceso.

Figura N°7: Ejemplo de declaración de costo variable no combustible.

6 Gestión GNL.
6.1 Ingreso de acuerdos de Suministro y Mercados Secundarios.
Si el o los acuerdos de compra están relacionado al ADP del año en curso se deberá
ingresar la información de la siguiente manera:

<!-- page 9 -->

8

• Empresa declarante: Coordinado.
• Año: Año del ADP.
• Mes: Enero.
• Publicación: Acuerdos de suministro GNL.
• Empresa Suministradora: Empresa con la que se firmó el Acuerdo.
• Empresa Suministradora Relacionada: Si/No.
• Empresa Compradora: Razón social del coordinado.
En el caso de que el volumen del Acuerdo de suministro GNL ingresado no sea dedicado
completamente a generación, se deberá realizar una declaración eligiendo los siguientes
campos:
• Empresa declarante: Coordinado.
• Año: Año del ADP.
• Mes: Enero.
• Publicación: Acuerdos de Mercados secundarios.
• Volumen: Volumen para el Mercado Secundario en metros cúbicos.
Si se desea realizar una declaración por un acuerdo de volumen spot, se deberán rellenar
los mismos campos que una publicación de  Acuerdos de suministro GNL  y la única
diferencia será el mes, ya que este corresponderá al mes de la compra.

Figura N°8: Ejemplo de Ingreso de Acuerdos.

6.2 Observaciones Estudio GNL.
Toda Coordinado GNL podrá realizar sus observaciones al Informe Técnico preliminar
del Estudio GNL, en un plazo de 15 días desde que el coordinar lo carga en la plataforma,
de acuerdo con el punto 3 de del art. 5-7 Hitos del Estudio GNL de la NT GNL.

<!-- page 10 -->

9


Figura N°9: Ejemplo de Observación Estudio GNL.

Únicamente será necesario seleccionar el Informe al que se quiere añadir la observación
y especificar en el campo “Alcance” a qué sección hace referencia. No hay un límite
establecido para la cantidad de observaciones por coordinado GNL.
7  Informe de Combustible art. 2-10.
De acuerdo con lo indicado en el ar t. 2-9 de la NT CyO, aquel coordinado mantenga un
contrato asociado con una vigencia mayor o igual a un año deberá realizar la declaración
del Informe de combustible  indicado en el ar t. 2-10 de la NT CyO. Para realizar la
declaración deberá utilizar los formatos entregados en la carta DE DE03071-23 y que
también están disponibles en la plataforma SCVIC. A continuación, algunas indicaciones
que pueden ayudar a declarar de forma más expedita:
• Empresa declarante: Coordinado.
• Fecha Inicio vigencia: Tiene relación con el contrato de combustible o servicio.
• Fecha Fin vigencia: Tiene relación con el contrato de combustible o servicio.
• Tipo de combustible:
o Biomasa.
o Gas Natural Por Ducto.
o GNL Regas.
o Combustibles líquidos (Diésel o Fuel Oil).
o Carbón.
o Hidrogeno.
o Otros Combustibles.
• Casos:
o Caso 1: Contratos de Suministro de Combustible.
o Caso 2: Contratos asociados a servicios.
• Informe de combustible ( Documento Confidencial): Información que será
recibida y manejada con discreción.
• Informe de combustibles  (Documento público): Quedará disponible en los
reportes públicos, después de su aprobación.
Los Formatos ingresados deben cumplir con los establecidos por el coordinador, de lo
contrario se rechazará la declaración.

<!-- page 11 -->

10


Figura N°10: Ejemplo de Declaración Informe de Combustible

Nota: Recordar que aquellas empresas generadoras GNL que no cumplan con el art. 1-4
de la NT GNL, deberán entregar el Informe de Combustible siempre que sus contratos
correspondan a lo indicado en el art 2-9 de la NT CyO:
a) Contratos de suministro asociados a la adquisición del combustible o
insumos, cuyo periodo de duración sea igual o mayor a un año; o,
b) Contratos asociados a servicios que guarden relación con la adquisición del
combustible o insumo cuya duración sea igual o mayor a un año.
8 Archivos para realizar declaraciones.
Las Macros, Formatos y Formularios para completar y realizar las distintas declaraciones,
se indican en la Figura N°11. Cabe mencionar que contantemente estos archivos van
sufriendo modificaciones en sus formatos, por lo que es de vital importancia revisar
periódicamente esta sección.


Figura N°11: Documentos para realizar declaraciones

Nota: Para poder acceder a la sección “Archivos para realizar declaraciones”  del
SCVIC3, es necesario haber iniciado sesión, dada que estos documentos no están
disponibles en la sección publica de la plataforma.

3 SCVIC - Coordinador Eléctrico Nacional
