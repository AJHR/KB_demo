---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA15-Guia-Usuario-Plataforma-SIREP-2024-01-09.pdf
pdf_sha256: 6d75aaffd04c0261f1594743b87e9932049eaf10e20084efe9f28bd4f2a4afef
pdf_pages: 10
extracted_pages: 10
extracted_chars: 4237
extracted_at: 2026-05-19T13:23:05Z
extractor: pypdf
---

# B43 DIN GUA15 Guia Usuario Plataforma SIREP 2024 01 09

<!-- page 1 -->

Manual de Usuario Coordinado para Plataforma SIREP
Enero 2023
Departamento de Modelación y Aplicaciones EMS
Subgerencia de Aseguramiento de la Operación
Gerencia de Operación


Rev Fecha Comentario Realizó Revisó / Aprobó
1 09-01-2023 Manual de usuario Jorge Vargas Jorge Vargas

<!-- page 2 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 1


El presente documento contiene el Manual de Usuario de la Plataforma SIREP, con los pasos necesarios para el
acceso, uso y desarrollo de APIs por parte de usuarios Coordinados.
Cabe recordar que la plataforma SIREP (Sistema de Registro de Protecciones), corresponde a la plataforma web
mediante la cual los Coordinados debe rán ingresar manualmente los registros oscilográficos de los equipos de
protección de su propiedad, en un plazo inferior a las 12 horas de ocurrida una contingencia.  Lo anterior, según
lo requerido en el Artículo 28 del Anexo Técnico de Sistemas de Monitoreo.

1. LINK A SIREP
El ingreso a la plataforma web de SIREP se realiza a través del siguiente link:

https://sirep.coordinador.cl/

2. INGRESO A SIREP
Ingresar credenciales de acceso:

En caso de requerir credenciales de acceso, podrá solicitarlas directamente a  los correos
soporte.sirep@coordinador.cl y dmap@coordinador.cl .
Se debe tener en consideración que, los relés o sistemas de protecciones deben estar previamente ingresados
a la Plataforma INFOTECNICA del Coordinador, pues la base de registros de SIREP se sincroniza con la base de
datos de INFOTECNICA. En caso de no hac erlo, no aparecerá en SIREP los equipos de protecciones de
propiedad de un Coordinado que no hayan sido ingresados a INFOTECNICA y, por lo tanto, no podrá subir los
correspondientes registros de falla.

<!-- page 3 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 2

3. PÁGINA PRINCIPAL DE SIREP
Al acceder se encontrará la página principal de SIREP, donde podrá adjuntar los archivos con registros de
protecciones en formato COMTRADE y, además, podrá encontrar los registros cargados con anterioridad:


4. SUBIR UN REGISTRO DE PROTECCIONES
Para subir un nuevo registro deberá seguir los siguientes pasos:
a) Crear Evento:

<!-- page 4 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 3


b) Llenar campo correspondiente a la Fecha y Hora Local en que ocurrió la falla. Procurar que la hora
UTC sea la correcta para la época del año en que ocurrió la falla que se está ingresando:


c) Autocompletar el Nombre de la Subestación donde se encuentra el sistema de protección o relé que
se está ingresando:

<!-- page 5 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 4

d) Autocompletar el Paño correspondiente a la ubicación del sistema de protección:


e) Seleccionar el relé o sistema de protección específico que generó el registro oscilográfico a cargar:

<!-- page 6 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 5

f) Agregar comentarios opcionales y presionar “Subir Archivos”


g) Selecciona los archivos en formato COMTRADE que deseas subir:

<!-- page 7 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 6

h) Con esto, quedarán cargados los registros oscilográficos en SIREP y finaliza presionando “Guardar”:


5. BUSCAR UN REGISTRO DE PROTECCIONES HISTÓRICO
Para buscar un registro histórico, desde la página principal, podrá hacerlo filtrando por Subestación y/o Paño y/o
Protección y/o Fecha del registro:

<!-- page 8 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 7
6. EDITAR UN REGISTRO DE PROTECCIONES
Para editar o eliminar un registro histórico, deberá acceder a las selecciones opcionales ubicados a la derecha de
cada registro:


7. DESCARGAR REGISTROS COMTRADE HISTÓRICOS
Para descargar un archivo COMTRADE histórico, deberá acceder a los links de la columna Archivos, ubicadas a la
izquierda de cada registro:

<!-- page 9 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 8

8. IMPLEMENTACIÓN DE API PARA CARGA AUTOMÁTICA DE REGISTROS
Para implementar una API, que permita automatizar la creación de registros y la carga de archivos COMTRADE a
SIREP, podrá encontrar las especificaciones necesarias en el link superior derecho:

<!-- page 10 -->

Manual de Usuario Coordinado para Plataforma SIREP – Enero 2023 9
