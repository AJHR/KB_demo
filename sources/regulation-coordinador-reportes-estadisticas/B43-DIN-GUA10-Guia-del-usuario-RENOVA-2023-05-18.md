---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/B43-DIN-GUA10-Guia-del-usuario-RENOVA-2023-05-18.pdf
pdf_sha256: 5a7ef34313944f4ae696869205be8b195fc7793a252d7ed798d9fce72481c6d9
pdf_pages: 55
extracted_pages: 55
extracted_chars: 79137
extracted_at: 2026-05-19T13:23:03Z
extractor: pypdf
---

# B43 DIN GUA10 Guia del usuario RENOVA 2023 05 18

<!-- page 1 -->

MANUAL DE USUARIO
Registro Completo de Energías
Renovables a Nivel Nacional


2021

<!-- page 2 -->

1


CONTEXTO

RENOVA es la plataforma de registro completo del mercado voluntario de atributos de
energía renovable en el Sistema Eléctrico Nacional,  desarrollada por el Coordinador
Eléctrico Nacional -Corporación autónoma de derecho público, sin fines de lucro, con
patrimonio propio y de duración indefinida, en adelante el “Coordinador”, entidad que es
reconocida por el Ministerio de Energía  y cuya base tecnológica se centra en
Blockchain1. Dicho registro garantiza la  transparencia, trazabilidad y robu stez del
mercado de atributos de energía renovable, evitando la doble contabilidad, doble venta
o proclamación de atributos renovables y con ello  habilitar que  empresas
Suministradoras y Clientes Finales puedan verificar el cumplimiento de sus
compromisos contractuales asociados.
La plataforma funciona en base a los Balances de Inyecciones y Retiros mensuales de
energía, Balance Anual ERNC, de información ex portada desde plataformas del
Coordinador, (Infotécnica para Instalaciones y REUC -Registro Único de Coordinados-
para Organizaciones) como también requiere que las Organizaciones Usuarias registren
y validen Contratos (transacciones automáticas)  entre la parte  Vendedora y
Compradora. Es así como  la plataforma con los diversos parámetros que gestiona
dispondrá de Reportes con distintas granularidades, Factores de Emisión y Certificados
de cumplimiento.
De acuerdo con lo anterior y con el objetivo de facilitar la navegación de los Usuarios en
la plataforma, es que el Coordinador entrega el presente Manual de Uso, que pretende
explicar y detallar las funcionalidades, pasos y principales características del aplicativo.
Este Manual de Uso  se divide  en tres partes, un primer capítulo con las bases  de
funcionamiento de RENOVA, un segundo capítulo con las indicaciones acerca del
ingreso a la plataforma, mientras que el tercero y cuarto poseen las características de
navegación para los módulos de Generador y Cliente, respectivamente, iniciando con la
vista de resumen hasta las consideraciones para crear un contrato.  Por último, se
encuentra un quinto y sexto capitulo los cuales poseen las preguntas frecuentes
respecto a la plataforma como también un anexo de metodología de asignación de
atributos según sus características.

1 Blockchain o Cadena de Bloques es un registro único distribuido e inalterable, que facilita el proceso de
registrar transacciones y rastrear activos dentro de una red empresarial.  Adicionalmente, debido a que
los usuarios comparten una única fuente fidedigna de información, puede ver todos los detalles de una
transacción de principio a fin, lo que le permite generar mayor confianza y eficienci a.

<!-- page 3 -->

2


En caso de consultas o presentar problemas para acceder a la plataforma,
recomendamos tomar contacto a través de la siguiente casilla de correo electrónico:
renova@coordinador.cl, indicando al menos una breve descripción de la solicitud,  su
Nombre, teléfono de contacto, Razón Social y Rut de su Organización.

INFORMACIÓN IMPORTANTE
Las figuras definidas en el presente Manual ha sido extraídas de cuentas ficticias de un
ambiente QA de RENOVA, es decir una pagina de pruebas con un desarrollo espejo a
RENOVA en producción, por ende toda información proporcionada en dichas figuras es
de carácter simulado con data totalmente ficticia.

<!-- page 4 -->

3


Contenido

1.- Bienvenido a RENOVA ................................................................................................ 7
1.1 Alcance ....................................................................................................................... 7
1.2 Participación en RENOVA ...................................................................................... 8
1.3 Funcionamiento de RENOVA ................................................................................ 8
1.3.2 Tipo de transacciones. ..................................................................................... 10
2. PRIMEROS PASOS ........................................................................................................ 11
2.2 Conceptos Básicos ................................................................................................... 11
2.2 Acceso a la plataforma ............................................................................................ 13
3. NAVEGACIÓN COMO USUARIO GENERADOR ...................................................... 15
3.1 Vista Resumen .......................................................................................................... 15
3.1 Vista Reportes Anual ............................................................................................... 16
3.2 Vista Reporte Mensual ............................................................................................ 19
3.3 Vista Usuario ............................................................................................................. 21
3.4 Vista Organizaciones ............................................................................................... 23
3.5 Vista Contratos ....................................................................................................... 25
3.5.1 Crear contrato ................................................................................................. 28
3.5.1 Lista de contratos .......................................................................................... 32
4 NAVEGACIÓN COMO USUARIO CLIENTE ............................................................... 34
4.1 Vista Resumen .......................................................................................................... 34
4.2 Vista Reportes ........................................................................................................... 35
4.2.1 Reportes Anuales ............................................................................................. 35
4.2.1 Reportes Mensuales ........................................................................................ 36
4.3 Vista Usuario ............................................................................................................. 37
4.4 Vista Organizaciones ............................................................................................... 38
4.5 Vista Contratos ......................................................................................................... 40
4.5.1 Crear contrato ................................................................................................. 43
4.5.2 Lista de contratos .......................................................................................... 47
5. PREGUNTAS FRECUENTES ........................................................................................ 50

<!-- page 5 -->

4


INDICE DE FIGURAS

Figura 1.1: Tipo de organizaciones que pueden acceder a RENOVA.  ............................................ 7
Figura 1.2: Canal de comunicación para participar en RENOVA ..................................................... 8
Figura 1.3: Funcionamiento de RENOVA ............................................................................................. 9
Figura 1.4: Diagrama de periodo de transferencia. ............................................................................. 9
Figura 1.5: Tipo de transacciones en RENOVA. ............................................................................... 10
Figura 2.1: Pestaña de Inicio de sesión .............................................................................................. 13
Figura 2.2: Vista de Reportes Públicos general. ............................................................................... 14
Figura 2.3: Vista de Reportes Públicos general, Reportes Públicos  . ........................................ 14
Figura 3.1: Vista de Resumen general de una organización generadora.  .................................... 15
Figura 3.2: Vista de instalaciones asociadas a la organización.  ..................................................... 16
Figura 3.3: Vista de Reportes organización generador. ................................................................... 16
Figura 3.4: Vista de Reportes organización generador. ...................... ¡Error! Marcador no definido.
Figura 3.5: Vista de reportes anuales para organización generador  .............................................. 17
Figura 3.6: Parámetros de Reporte de balance anual para organización generador.  ................. 17
Figura 3.7: Grafico disponible en parámetro AER Creados, (Atributos renovables).  ................... 18
Figura 3.8: Vista de listado de Reportes de Balances Mensual ...................................................... 20
Figura 3.9: Vista de parámetros de Reportes de Balances Mensual  ............................................. 20
Figura 3.10: Vista de gráficos de parámetros de Reportes de Balances Mensual  ....................... 20
Figura 3.11: Vista de gráficos de parámetros de Reportes de Balances Mensual  ....................... 21
Figura 3.12: Vista de creación de usuarios en pestaña Usuario.  ................................................... 22
 Figura 3.13: Vista de listado de usuarios en pestaña Usuario. ...................................................... 22
Figura 3.14: Vista de detalles de usuarios en pestaña Usuario. ..................................................... 23
 Figura 3.15: Vista de listado de instalaciones en pestaña Organizaciones.  ................................ 23
 Figura 3.16: Vista de detalles de instalaciones en pestaña Organizaciones.  .............................. 24
Figura 3.17: Vista de detalles de instalaciones en pestaña Organizaciones.  .............................. 24
 Figura 3.18: Vista de Contratos, Crear contratos. ............................................................................ 28
Figura 3.19: Vista de Contratos, Crear contratos. ............................................................................. 30
Figura 3.20: Vista de Contratos, Crear contratos, primera parte. ...... ¡Error! Marcador no definido.
Figura 3.21: Vista de Contratos, Crear contratos, segunda vista. .................................................. 30
Figura 3.22: Vista de Contratos, Crear contratos, seleccionando Cantidad máxima. .................. 31
Figura 3.23: Vista de Contratos, Crear contratos, seleccionando Instalación.  ............................. 31
 Figura 3.24: Vista de Contratos, Crear contratos, seleccionando Instalación.  ............................ 31
 Figura 3.25: Vista de Contratos, Crear contratos, seleccionando Instalación.  ............................ 32
Figura 3.26: Vista de Contratos, Crear contratos, seleccionando Instalación.  ............................. 32
Figura 4.1:Vista Resumen de un usuario de organización suministrada.  ...................................... 34
Figura 4.2: Vista Resumen de un usuario de organización suministrada, selección pestaña
Reportes. ................................................................................................................................................... 35
  Figura 4.3: Vista Reportes de Balance Anual. ................................................................................. 35
Figura 4.4:Vista Reportes de Balance Mensual ................................................................................. 36
 Figura 4.5:Vista Reportes de Balance Mensual e indicación de gráficos.  ....... ¡Error! Marcador no
definido.
Figura 4.6:Vista Reportes de Balance Mensual, Parámetros de Cantidad de AERC (atributos
de energía convencional) y ARNC (atributo de energía renovable no convencional) generados.
 .................................................................................................................................................................... 36
Figura 4.7:Vista Usuario, creación de un usuario. ............................................................................. 37
 Figura 4.8:Vista Listado de usuarios de la organización. ................................................................ 38
Figura 4.9:Vista Descripción de usuario de la organización. ........................................................... 38
Figura 4.10:Vista del listado de instalaciones de consumo asociadas a la organización.  .......... 39
Figura 4.11:Vista del detalle de instalaciones de consumo asociadas a la organización. .......... 39

<!-- page 6 -->

5


Figura 4.12:Vista del detalle de instalaciones de consumo asociadas a la organización (cont.)
 .................................................................................................................................................................... 39
 Figura 4.13:Vista Crear contrato. ........................................................................................................ 43
 Figura 4.14: Primera vista para crear contrato  ................................................................................. 44
Figura 4.15: Primera vista para crear contrato ................................................................................... 45
Figura 4.16: Creación de contrato seleccionando como limite de transferencia la cantidad
máxima a transferir. ................................................................................................................................. 45
Figura 4.17: Creación de contrato seleccionando como límite de transferencia porcentaje de
selección. .................................................................................................................................................. 46
Figura 4.18: Creación de contrato seleccionando como límite de transferencia ambas
condiciones de borde. ............................................................................................................................. 46
Figura 4.19: Creación de contrato seleccionando como límite de transferencia ambas
condiciones de borde. ............................................................................................................................. 47
Figura 4.20: Vista Listado de contrato. ................................................................................................ 47
Figura 4.21: Vista descripción de contrato. ........................................................................................ 48
Figura 4.22: Vista descripción de contrato. (cont.) ............................................................................ 48

<!-- page 7 -->

6


INDICE DE TABLAS

Tabla 1.1: Definiciones plataforma RENOVA ..................................................................................... 11
Tabla  2.1 Definición de indicadores de reportes de balances ......................................................... 18
Tabla 2.2: Indicador definido en reportes de balances mensual ..................................................... 19
Tabla 2.3: Definición de parámetros solicitados en la creación de contratos.  ............................... 25
Tabla 2.4: Definición de parámetros solicitados en la creación de contratos. (cont.)  .................. 26
Tabla 2.5: ................................................................................................................................................. 33
Tabla 3.1: Definición de parámetros solicitados en la creación de contratos  ................................ 40
Tabla 3.2: Definición de parámetros solicitados en la creación de contratos  ................................ 41
Tabla 3.3: Criterios asociados a la periodicidad de contratos .......................................................... 42
Tabla 3.4: Criterios asociados a la periodicidad de contratos. (cont.) ¡Error! Marcador no definido.
Tabla 3.5: Descripción de parámetros entregados en detalle de contratos  ................................... 49

<!-- page 8 -->

7


1.- Bienvenido a RENOVA

1.1 Alcance

RENOVA es un sistema de trazabilidad de energías renovables el cual permite el
registro a nivel nacional de generación y consumo de energías renovables, es así como
pueden participar Generadores, quienes inyectan energía renovable al Sistema
Eléctrico Nacional como también aquellos clientes que tengan consumo de energías
renovables y tengan un compromiso contractual con una organización generadora.


Figura 1.1: Tipo de organizaciones que pueden acceder a RENOVA.
Por ende, todas aquellas organizaciones Consumidoras de energías renovables que
posean un contrato por energía renovables con una Generadora podrán acceder al
Registro Nacional de Energías Renovables.
Cabe destacar que, RENOVA como una plataforma de trazabilidad local a nivel nacional
y emisor oficial de información de transferencias de atributos renovables del Sistema
Eléctrico Nacional, facilitará la información a Certificadoras que mediante un acceso en
el cual podrán obtener información del registro de transferencia de aquellas
organizaciones que autoricen a dicha Certificadora para acreditar sus atributos
renovables*2.


2 *Es importante considerar que a noviembre 2021, se encuentra en desarrollo tecnológico el acceso a Certificadoras a
RENOVA, prontamente se darán noticias respecto a su avance.

<!-- page 9 -->

8


1.2 Participación en RENOVA

Si su organización cumple con los requisitos anteriores, es importante seguir los
siguientes pasos:


Figura 1.2: Canal de comunicación para participar en RENOVA
El canal informativo de RENOVA es renova@coordinador.cl, canal por el cual se
facilitará toda la información asociada a RENOVA.

1.3 Funcionamiento de RENOVA

RENOVA al ser una plataforma desarrollada por el Coordinador Eléctrico Nacional, esta
es suministrada de información gestionada por la Institución que en su calidad de
organismo técnico e independiente coordinador de las operaciones del Sistema
Eléctrico Nacional, sostiene plataformas como es Infotécnica y REUC (Registro Único
de Coordinados), las cuales proveen de información a RENOVA. Plataforma Infotécnica
tiene como función contener toda la información técnica asociada al sistema eléctrico
local de cent rales de generación, subestaciones, líneas de transmisión, equipos de
compensación y las empresas coordinadas que se encuentren en el mercado eléctrico
de forma pública. Mientras que REUC, es el aplicativo que contiene la información de
registro de coordinados del Sistema Eléctrico Nacional. Por último, el desarrollo de un
sistema de trazabilidad de energías renovables requiere de información de la energía
generada y consumida a nivel nacional, es por lo anterior que RENOVA se conecta con
el Balance de Inye cciones y Retiros, en adelante BIR,  proporcionando toda la
información necesaria de forma confiable y segura para registrar el consumo de
energías renovables.
Es importante destacar que RENOVA también considerará como fuente de información
el Balance ERNC gestionado por el Coordinador Eléctrico Nacional, del cual de igual
manera se obtendrá la información de Traspasos y Obligación que será registrada en
RENOVA para efectos mayor centralización de información.

<!-- page 10 -->

9


Figura 1.3: Funcionamiento de RENOVA

1.3.1 Periodos de transferencia para transferir atributos.

El periodo de transferencia denominado en RENOVA es aquel periodo en el cual se
puede transferir atributos según el mes actual. En la figura siguiente se ejemplifica para
un periodo de 2 años (2020 y 2021) es así como se establece que en el rango de tiempo
entre enero y diciembre se encontrará disponible el actual año para transferir, pero
también existirá un periodo de ajuste en el cual las organizaciones podrán transferir
atributos en el año anterior, establecido entre enero a mayo. Cabe destacar que se
podrán transferir atributos generados de un año anterior, es decir se podrán declara r
atributos de arrastre3.

Figura 1.4: Diagrama de periodo de transferencia.


3 Se debe mencionar que a noviembre 2021, se tiene cargada la información  de Base de Datos del año
2020, por ende se pueden registrar al momento en la presente marcha blanca los atributos retirados
durante ese periodo.

<!-- page 11 -->

10


1.3.2 Tipo de transacciones.

En RENOVA las organizaciones pueden transferir atributos de energía renovable según
el tipo de transacción, es decir pueden vender o comprar independientemente de su tipo
de organización (Generador o Cliente). Es así como las organizaciones pueden adquirir
o transferir atributos según sus requerimientos.

Figura 1.5: Tipo de transacciones en RENOVA.

<!-- page 12 -->

11


2. PRIMEROS PASOS
2.2 Conceptos Básicos
En seguida se presentan los conceptos de mayor importancia para navegar en la plataforma,
favor de revisar el presente glosario.

Tabla 2.1: Definiciones plataforma RENOVA

Concepto Significado
Atributo de
Consumo o AC
Corresponde a 1 megavatio -hora de energía que se retira del Sistema
Eléctrico Nacional y posee todas las características no energéticas de su
punto de consumo como ubicación, tipo de consumo (Libre, Libre en
Distribución o Regulado), código de medidor, entre otros.
Atributo de
Energía o AE
Corresponde a 1 megavatio -hora de energía renovable o no renovable que
se inyecta al Sistema Eléctrico Nacional y posee todas las características no
energéticas de su instalación de generación, como ubicación, antigüedad,
combustible (si aplica), entre otros.
AER Atributo de energía renovable, considera la suma de los atributos de energía
renovable convencional (AERC) y no convencional (AERNC).
AERC Atributo de energía renovable convencional.
AERNC Atributo de energía renovable no convencional.
AENR Atributo de energía no renovable
Certificaciones Producto de energía no tangibles que representan 1 megavatio -hora de
electricidad generada por un recurso renovable, sea éste convencional o no.
Coordinador o
Coordinador
Eléctrico
Nacional
Coordinador Independiente del Sistema Eléctrico Nacional, es una
corporación autónoma de derecho público, sin fines de lucro, con patrimonio
propio y de duración indefinida, cuya Organización, composición, funciones y
atribuciones se rigen según lo establecido en la Ley N° 20.936 y su
Reglamento. El Coordinador representa la autoridad para operar o supervisar
la administración e implementación de los Procedimientos Operativos de
RENOVA.
Cuenta Corresponde a la “Billetera” de cada Organización. En ella se depositan los
atributos de la plataforma de acuerdo con los Procedimientos Operativos de
RENOVA.
Energía Producto eléctrico físico que es transmitido a través de electrones por el
Sistema Eléctrico Nacional.
Energía
Renovable o
ER
Producto eléctrico físico que es transmitido por el Sistema Eléctrico Nacional
y fue generado a partir de fuentes naturales inagotables.

<!-- page 13 -->

12


Tabla 2.1: Definiciones plataforma RENOVA (cont.)


Concepto Significado
Energía
Renovable No
Convencional o
ERNC
Energía eléctrica generada por medios de generación cuya fuente de energía
primaria provenga de una fuente natural. En Chile, la Ley establece, para la
energía hidráulica, un límite de generación de 20 MW.
MWh Megavatio-hora
Procedimientos
Operativo de
Renova
Procedimientos del Sistema de Seguimiento de la Energía Renovable del
Sistema Eléctrico Nacional y del RENOVA.
Renova Sistema de software de propiedad del Coordinador, para el Sistema de
Trazabilidad de Energías Renovables del Sistema Eléctrico Nacional, donde
se crean, traspasan y validan los atributos y certificados de energía
renovable.
Tokens Unidad de valor que el Coordinador establece para facilitar la transacción de
los atributos de energía entre las empresas eléctricas.
Atributos de
consumo
propio
Corresponde a 1 megavatio -hora de energía que se retira del Sistema
Eléctrico Nacional , conforme a los requerimientos energéticos de la
Organización Generadora para poder operar la Unidad Generadora.
Atributos de
consumo
Corresponde a 1 megavatio -hora de energía que se retira del Sistema
Eléctrico Nacional, conforme al suministro energético de Clientes Finales.
Atributos de
perdidas
Representa 1 megavatio-hora de energía perdido en la transmisión de la
energía, desde el punto de inyección al punto de retiro.

<!-- page 14 -->

13


2.2 Acceso a la plataforma
Una vez en la página web https://renova.coordinador.cl/summary haga clic en el botón “Iniciar
Sesión” ubicado en la parte superior derecha de la pantalla, el cual lo dirigirá a una vista de inicio
de sesión donde debe ingresar su s “Credenciales de acceso” entregadas a través de la casilla
de correo de Renova.

Figura 2.1: Pestaña de Inicio de sesión


Seguido a ingresar el correo y la clave otorgada hacer clic en Acceder. Al costado derecho puede
seleccionar el idioma en el cual estime conveniente trabajar en la plataforma  (ES: español, EN:
inglés).

<!-- page 15 -->

14


2.3  Reportes Públicos
En la página principal de RENOVA se reportan cifras públicas de las Organizaciones y
montos de atributos registrados y la cantidad de atributos transados mediante Contratos en
el periodo seleccionado (Filtro de Año), con la siguiente vista:
Figura 2.2: Vista de Reportes Públicos general.


En la presente vista, se publicarán los siguientes reportes.
Figura 2.3: Vista de Reportes Públicos general, Reportes Públicos  .

<!-- page 16 -->

15


3. NAVEGACIÓN COMO USUARIO GENERADOR

3.1 Vista Resumen

Al ingresar a la plataforma a través de las Credenciales de una Organización tipo Generador, lo
primero que se observa es la pantalla de “Resumen”, en donde se muestra el total de atributos
de energías renovables convencionales (AERC) y no convencionales (AERNC) disponibles en la
cuenta de la Organización:

Figura 3.1: Vista de Resumen general de una organización generadora.


 El scroll de la pantalla, se encontrará una primera fila con la Razón Social de la Organización y
los AERC y AERNC disponibles y que han sido transferidos desde otras Organizaciones.
Luego, en las filas inferiores, se despliega el detalle de las Unidades de Generación en que se
asoció inyección a la Organización Generadora (de acuerdo al Balance de Inyecciones y Retiros).
Es posible observar  la tecnología de dicha unidad de generación y los atributos de energía
renovables convenciones (AERC  en adelante) y no convencionales (AERNC  en adelante )
disponibles de dichas instalaciones.

<!-- page 17 -->

16


Figura 3.2: Vista de instalaciones asociadas a la organización.

La segunda pestaña disponible en la parte superior izquierda de la pantalla muestra los reportes
dinámicos de un año activo y estáticos para aquellos años cerrados , de los balances con una
granularidad mensual y anual.

3.1 Vista Reportes Anual

Figura 3.3: Vista de Reportes organización generador.


En la opción de Reporte de Balance Anual puede encontrar la información segregada por mes,
desde el 2020 en adelante. Al seleccionar la opción “Ir” del listado de cada año, el usuario podrá
ingresar observaciones a la información del reporte, si correspondiera.

<!-- page 18 -->

17


Figura 3.4: Vista de reportes anuales para organización generador

Adicionalmente, si seleccionamos la opción “Ver”, podremos ingresar a explorar el detalle de los
indicadores almacenados para el Reporte Balance Anual:
 Figura 3.5: Parámetros de Reporte de balance anual para organización generador.

<!-- page 19 -->

18


El reporte almacena indicadores de AER 4 Creados, Recibidos, Transferidos y Cantidad total de
AER disponibles, los que se definen a continuación:
Tabla  3.1 Definición de indicadores de reportes de balances
Indicador Definición
AER Creados Son todos los atributos de energías renovables  horarios inyectados por
la Organización Generadora al SEN.
AER Recibidos Atributos de energías renovables que han sido obtenidos  de otras
Organizaciones a través de Contratos (transacciones) por la
Organización Generadora.
AER Trasferidos Atributos de energías renovables que han sido transferidos desde la
Organización Generadora a otras Organizaciones a través de Contratos
(transacciones).
Cantidad Total de
AERC y AERNC
Disponible
Corresponde al balance de atributos de energías renovables disponibles
para una transferencia de atributos. Cuya fórmula responde a:
AER disponibles = AER Creados + AER Recibidos – AER Transferidos

Por último, cada indicador tiene una vista de  su comportamiento  gráfico, un ejemplar es el
siguiente de AER Creados.
Figura 3.6: Grafico disponible en parámetro AER Creados, (Atributos renovables).


4 Los Atributos de Energía Renovable, según el reporte consultado, puede corresponder a AERC, AERNC
o la suma de ambos.

<!-- page 20 -->

19


Para el Reporte Balance Anual, se dispone de un gráfico para observar el comportamiento anual
de cada indicador.
La funcionalidad de ingresar observaciones solo está disponible para cada año definido en el
Listado de Reporte Balance Anual.

3.1 Vista Reporte Mensual

De la misma forma como se tiene los reportes anuales de atributos, también están disponibles
los reportes  de forma mensual,  estos s e encuentran organizados por año y mes respectivo.
Además, cabe notar que se presentan  los mismos indicadores, sin embargo, se agregan los
indicadores definidos en la Tabla 3.2
Tabla 3.2: Indicador definido en reportes de balances mensual
Indicador  Definición
AER Creados a la fecha Atributos de energías renovable generados en las instalaciones
de la organización.
AER Recibidos a la fecha Atributos de energías renovable que han sido transferidos a su
organización desde otra organización.
AER Transferidos a la fecha Atributos de energías renovable que han sido transferidos
desde organización a otra organización.
AER acumulados en la
cuenta de activos a la fecha
Atributos de energía renovable disponible en la Organización
de forma mensual en formato acumulado, es decir, se indica la
suma de los atributos desde enero al mes de consulta, del
pertinente año.
De forma general, este indicador corresponde al resultado de la
siguiente fórmula:
AER disponibles = AER Creados + AER Recibidos – AER
Transferidos

<!-- page 21 -->

20


 Figura 3.7: Vista de listado de Reportes de Balances Mensual

Figura 3.8: Vista de parámetros de Reportes de Balances Mensual


Figura 3.9: Vista de gráficos de parámetros de Reportes de Balances Mensual

<!-- page 22 -->

21


La vista anterior, es aquella que se visualiza al ingresar a los gráficos asociado a los reportes
mensuales de cada indicador disponible (AER Creados, AER Recibidos y AER Transferidos).

3.2 Vista Usuario

 Figura 3.10: Vista de gráficos de parámetros de Reportes de Balances Mensual


La plataforma tiene un a pestaña  de “Usuario”. La que contiene 2 subpestañas: “Listado de
usuarios” y “Crear usuarios” . Esta última, so lo la pueden visualizar los usuarios con Rol de
“Administrador”, los que en ella  pueden crear un usuario para su misma Organización. N o
obstante, los usuarios creados tendrán Rol de “Solo vista” y con el estado “Inactivo”. Por lo que
a continuación, deberán contactar con el Coordinador para solicitar:
- Activar las cuentas de usuarios
- Credenciales de acceso de usuarios
- Cambio de rol5 (opcional)
En el correo por enviar debe indicar al menos la siguiente información de cada usuario:
- Rut registrado
- Correo electrónico registrado
- Número de teléfono registrado
Estos ítems, deben registrarse en RENOVA con el siguiente formato:
- Rut registrado: X.XXX.XXX -X, XX.XXX.XXX -X, en caso de terminar en la letra K,
considerar letra mayúscula.
- Correo electrónico registrado: xxxxxxx…x@institución.org, la que debe poseer al menos
7 caracteres y considerar letra minúscula.
- Número de teléfono registrado: +56 9xxxxxxxx, la que comienza con símbolo de suma,
código estándar telefónico de Chile, específicamente de teléfonos móviles,
correspondiente al teléfono móvil de contacto directo del usuario registrado.

5 Los usuarios poseen 2 posibles Rol: Solo Vista y Administrador. Adicionalmente, cada usuario puede
poseer 3 tipos de estado: Activo, Inactivo y Eliminado.

<!-- page 23 -->

22


Figura 3.11: Vista de creación de usuarios en pestaña Usuario.


Y finalmente, debe indicar al menos la siguiente información de la Organización:
- Razón Social Organización
- Rut Organización
Los usuarios, independiente de su Rol, podrán visualizar solo los usuarios asociados a la misma
Organización respectiva. Estos se encuentran disponibles en la pestaña “Listado de usuarios”,
los cuales podrán filtrarse por Rut de usuario, estado o fecha de creación.
 Figura 3.12: Vista de listado de usuarios en pestaña Usuario.


Es importante destacar que una vez creado el usuario la plataforma lo redirigirá a la lista de
usuario automáticamente.

<!-- page 24 -->

23


 Figura 3.13: Vista de detalles de usuarios en pestaña Usuario.


Por último, cabe notar que se está desarrollando una funcionalidad la cual permita modificar su
número de teléfono y correo, estaremos enviando las actualizaciones de dichas funcionalidades
en el momento correspondiente.

3.3 Vista Organizaciones
 Figura 3.14: Vista de listado de instalaciones en pestaña Organizaciones.


En Organizaciones podrá ver la lista de las instalaciones asociadas a su Organización, es decir,
instalaciones de generación o consumo asociadas a su Organización de acuerdo con la carga
del Balance Mensual de Inyecciones y Retiros.
En esta pantalla  se dispone del  ID Instalación, Nombre, Tipo, Organización, tecnología de
obtención de energía y estado en la plataforma. Además, tiene la opción de filtrar según nombre,
tipo, Organización y/o tecnología.

<!-- page 25 -->

24


Finalmente, al ingresar al detalle de la instalación, se aprecian los siguientes datos:
 Figura 3.15: Vista de detalles de instalaciones en pestaña Organizaciones.

Figura 3.16: Vista de detalles de instalaciones en pestaña Organizaciones.

<!-- page 26 -->

25


3.4 Vista Contratos
En el presente apartado se definirá todos los conceptos involucrados en la Vista de Contratos,
para mayor comprensión del usuario en  el proceso de creación de Contratos en RENOVA
(transacciones en Renova).
Como l a Organización que “Declara” un Contrato, corresponde a una Organización tipo
Generador, debe indicar los siguientes datos:
Tabla 3.3: Definición de parámetros solicitados en la creación de contratos.
Concepto Descripción
Rut Contraparte (*) Declarar el RUT de la Organización Contraparte del Contrato, en
formato que contenga punto y guion.
Tipo de transacción
(*): Compra o Venta.
El “Tipo de transacción” permite al declarante indicar si el Contrato es
de tipo “Compra” o “Venta” en referencia a su Organización. En el caso
de que se registre una “ Compra”, el Declarante establece en el
Contrato que será su Organización quien recibirá los atributos de
energía, caso contrario de “Venta”, la Organización a quien representa
el Declarante transferirá los atributos de energía a la  Organización
Contraparte.

Periodicidad de la
transacción (*):
La “Periodicidad de la transacción” permitirá establecer la frecuencia
con la que el Contrato deberá ejecutar el traspaso de atributos de
energía renovable considerando la información de la declaración del
contrato (conceptos como fecha inicio, término, cantidad máxima,
entre otros) .  Podrá seleccionar tipo:  Una vez, Horaria, Diaria,
Mensual, Trimestral o Anual.
Tipo de AER a
traspasar (*):
AERC (Atributos de Energía R enovable Convencional), es dec ir,
atributos de energías renovables convencionales, entendiéndose
según Ley N°20.257, como la energía proveniente de centrales
hidroeléctricas con una potencia máxima mayor a 20[MW] . Mientras
que los  AERNC son aquellos que se definen como Atributos de
generados por medios de generación de Energías Renovables No
Convencional (ERNC), que según Ley N° 20.257, se determina como
ERNC según el Artículo 255°, todo Medio de Generación de Energías
Renovables son a partir de biomasa, hidráulica cuya potencia máxima
es inferior a 20 [MW], geotérmica, energía solar desde radiación solar,
eólica, energía de los mares, otro medio de generación determinado
por la Comisión a partir de energías renovables que permita
diversificar las fuentes de energías.

<!-- page 27 -->

26


Tabla 3.4: Definición de parámetros solicitados en la creación de contratos. (cont.)
Concepto Descripción
Fecha de inicio del
contrato.

Definir la fecha de inicio como también la hora de caducidad
establecida en el contrato.
Cabe señalar que la fecha es obligatoria de declarar mientras que la
hora es opcional.
Fecha de término del
contrato.

Definir la fecha de finalización como también la hora de caducidad
establecida en el contrato.
Cabe señalar que la fecha es obligatoria de declarar mientras que la
hora es opcional.
Clase de contrato Prioridad de Contrato por sobre otros definidos con otras
Organizaciones. Las opciones de Clase son A, B o C , donde la
prioridad A es la más alta.
Este concepto, debe ser ingresado solo por la parte Vendedora del
Contrato declarado. Si un usuario declara el contrato como C ompra,
este concepto será ingresado por la parte Vendedora cuando deba
aceptar el Contrato.

Respecto a la periodicidad es importante considerar los siguientes puntos:
 Tabla 2.5: Criterios asociados a la periodicidad de contratos
Periodicidad ¿Atributos disponibles?6
Sí7 Parcialmente8 No9
Única vez
Se ejecuta contrato
inmediatamente
después de su
aprobación.
- -
Horaria
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir en cada hora
del periodo
establecido.
Realizará las
transferencias para
los meses cargados.
Dejará el Contrato en
estado Activo, hasta
la carga del próximo
mes de ejecución.
Quedará el Contrato en
estado Activo, hasta la
carga del próximo mes
de ejecución.


6 Los atributos de energía “inyectados a la red”, se depositan en las billeteras de cada empresa en el
mismo momento, con la carga mensual del Balance de Inyecciones y Retiros, del respectivo mes y año.
7 Meses involucrados entre la fecha de inicio y término del contrato, se encuentran totalmente cargados
en Renova.
8 Meses involucrados entre la fecha de inicio y término del contrato, se encuentran parcialmente
cargados en Renova.
9 Meses involucrados entre la fecha de inicio y término del contrato, aún no se encuentran cargados en
Renova.

<!-- page 28 -->

27


Periodicidad ¿Atributos disponibles?6
Sí7 Parcialmente8 No9
Diaria
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir en cada día,
entre el periodo
establecido.
Mensual
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir al mes, entre
el periodo establecido.
Trimestral
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir al término de
cada trimestre10, entre
el periodo establecido.
Anual
Realiza una única
transferencia,
transfiriendo la
cantidad de atributos
establecida,
disponiendo de la
información de todos
los meses del año.
-
 -

Se debe considerar que, en la actual versión de RENOVA (Noviembre 2021), solo está disponible
la periodicidad “ Única vez”.  Se avisar á a todos los usuarios  la disponibilidad la siguiente
actualización de RENOVA y sus respectivas funcionalidades.


10 Las periodicidades Trimestrales, se ejecutan con la carga del Balance de Inyecciones y Retiros del
último mes del trimestre (1T: Marzo, 2T: Junio, 3T: Septiembre y 4T: Diciembre), buscando la cantidad
de atributos a transferir, en el total de atributos del trimestre (1T: Enero-Marzo, 2T: Abril-Junio, 3T:
Julio-Septiembre y 4T: Octubre-Diciembre).

<!-- page 29 -->

28


3.4.1 Crear contrato
Para crear Contrato debe dirigirse a la pestaña “Contratos” y seleccionar la opción “Crear
Contrato”.
 Figura 3.17: Vista de Contratos, Crear contratos.


Para crear Contrato se requiere conocer:

Para definir los criterios anteriores, se debe articular con la Contraparte el interés por ser parte
de RENOVA y de sus beneficios y así, definir entre ambos, las anteriores reglas de contrato.
No existe una única forma de declarar un Contrato en RENOVA, las posibilidades se adecuarán
a las necesidades del  acuerdo entre el  Generador y su Cliente, como también, a las
funcionalidades disponibles en el formulario de Crear Contrato.
Considerando que el declarante es una Organización de tipo Generador, el usuario deberá
completar los siguientes conceptos dependiendo del tipo de transacción escogida:
I
•RUT Contraparte (formato de
RUT: con punto y guión)
II
•Tipo de transacción (compra o
venta)
III •Clase de contrato
IV •Fecha de inicio y término
V
•Tipo de atributos (AERC y/o
AERNC)

<!-- page 30 -->

29


Compra
•Monto máximo de AER
comprometida en [MWh]
acorde a la periodicidad de la
transacción.
•Nombre de la instalación de
generación asociada al
contrato.
•Porcentaje de la producción
de la planta asociada al
contrato.
Venta
•Prioridad del contrato (A, B o
C).
•Monto máximo de AER
comprometida en MWh
acorde a la periodicidad de la
transacción.
•Nombre instalación de
generación asociada al
contrato.
•Porcentaje de la producción
de la planta asociada al
contrato.

<!-- page 31 -->

30


Figura 3.18: Vista de Contratos, Crear contratos.


Una vez completados todos los requerimientos se activará el botón “Siguiente”. Al ir a la opción,
RENOVA lo redirigirá a la segunda pestaña del formulario de “Crear Contrato”, donde es de suma
importancia definir si la condición de borde del Contrato la estimará por cantidad máxima de
atributos según la periodicidad seleccionada, por una instalación de generación específica  del
Contrato o ambas opciones seleccionadas, se mostrarán las tres alternativas para cerrar el
contrato. se sugiere cantidad máxima.
Figura 3.19: Vista de Contratos, Crear contratos, segunda vista.

<!-- page 32 -->

31


A) Cantidad Máxima de atributos a transferir según periodicidad establecida.
 Figura 3.20: Vista de Contratos, Crear contratos, seleccionando Cantidad máxima.

B) Instalación de generación asociada al contrato

 Figura 3.21: Vista de Contratos, Crear contratos, seleccionando Instalación.


C) Cantidad máxima de atributos e instalación asociada a contrato.
 Figura 3.22: Vista de Contratos, Crear contratos, seleccionando Instalación.

Una vez creado el contrato, podrá revisar su estado en la lista de contratos.

<!-- page 33 -->

32


3.4.2 Lista de contratos

Por último, existe la opción de revisar los Contratos creados solo por y para la Organización, en
la segunda opción de la pestaña de Contratos, es decir “Listado de contratos”, donde:
 Figura 3.23: Vista de Contratos, Crear contratos, seleccionando Instalación.

Se podrá filtrar la información  de los Contratos por el RUT o Razón Social  de la Organización
Contraparte y el estado de dicho Contrato. Adicionalmente, esta lista muestra la siguiente forma:

  Figura 3.24: Vista de Contratos, Crear contratos, seleccionando Instalación.


Los estados de cada Contrato, indican la siguiente información:

El Detalle de cada Contrato, muestra un listado de conceptos asociados a la transacción
correspondiente.
• Espera la aprobación de la Organización Contraparte.Declarado
• Ha sido aprobado por la Organización Contraparte aunque el Contrato aún se
escuentra transfieriendo atributos. También puede corresponder a la espera de
carga de nueva información.Activo
• El contrato ya transfirió la totalidad de atributos asociados al Contrato, LOS
ATRIBUTOS ASOCIADOS A LA TRANSACCIÓN COMERCIALIZADOS POR EL
GENERADOR QUE REALIZÓ LA TRANSACCIÓN.Caducado
• El Contrato ha sido rechazado por la Organización Contraparte.Inactivo

<!-- page 34 -->

33


Tabla 3.5: Descripción de parámetros entregados en Detalle de Contratos
Concepto Descripción
ID del Contrato  Número identificador único del Contrato en la Base de Datos
de RENOVA.
Estado Declarado, Activo, Caducado o Inactivo.
RUT Organización Emisora  Rut asociado a Organización que Declara el Contrato.
RUT Organización
Contraparte
Rut asociado a Organización Contraparte del Contrato.
Nombre Contraparte  Razón Social de la Organización Contraparte del Contrato.
Tipo de transacción  Corresponde si la declaración corresponde a tipo “Compra”
o “Venta”.
Clase de Contrato  Prioridad del Contrato en relación con los otros Contratos de
la Organización. Si mi Contrato es A, se suministrarán los
atributos al presente contrato.
Tipo de AER transados  Declara la clase de AER cedido: Convencional o No
Convencional.
Fecha de declaración del
Contrato
Corresponde a la fecha de creación del Contrato.
Hora de declaración del
Contrato
Corresponde a la hora de creación del Contrato.
Fecha de inicio del Contrato  Corresponde a la fecha de inicio seleccionada en la primera
parte del formulario de “Crear Contrato”.
Fecha de término del Contrato  Corresponde a la fecha de término seleccionada en la
primera parte del formulario de “Crear Contrato”.
Fecha de confirmación del
acuerdo
Declara la fecha de aceptación del acuerdo por la
Contraparte.
Periodicidad de la transacción  Única Vez, Horaria, Diaria, Mensual, Trimestral o Anual.
Cantidad mínima  de AER
establecida
Cantidad mínima de atributos asignados a condicionar en la
creación del Contrato.
Nombre de instalación
asociada al Contrato
Nombre de la instalación que genera atributos destinados a
la Contraparte del Contrato.
Porcentaje de generación de
la instalación
Porcentaje a transferir de la organización contraparte desde
la instalación asignada.
Cantidad de la generación de
la instalación
Cantidad de atributos producidos de la instalación que se
destinan a la Contraparte.
Cantidad de AER transados  Declaración de atributos  renovables cedidos entre
Generador y Cliente.

<!-- page 35 -->

34


Concepto Descripción
Cantidad de AERC transados  Total de atributos transferidos desde la cuenta de la
organización de tipo AERC según condiciones de contrato.
Cantidad de AERNC
transados
Total de atributos transferidos desde la cuenta de la
organización de tipo AERNC según condiciones de contrato.
Cuenta AE activos de origen  Declaración de atributos del generador creados
almacenados en la presente cuenta.
Cuenta AE activo s de destino Declaración de atributos del generador creados
almacenados en la presente cuenta que serán destinado a
la Contraparte.

4. NAVEGACIÓN COMO USUARIO CLIENTE

4.1 Vista Resumen
Al ingresar a la plataforma se observará un Resumen de términos de atributos de energía, se
presenta una breve descripción de la vista:
Figura 4.1:Vista Resumen de un usuario de organización suministrada.


Si observa en la parte superior izquierda, existe la opción de revisar los reportes que se puedan
generar de información, de los balances con una granularidad mensual y anual.

<!-- page 36 -->

35


4.2 Vista Reportes

 Figura 4.2: Vista Resumen de un usuario de organización suministrada, selección pestaña
Reportes.


En la opción de Reporte de Balance Anual puede encontrar graficas de los atributos energias
renovables (AER en adelante); AER recibidos, AER transferidos y la cantidad total  de atributos
de energia renovables convencionales  (AERC en adelante) , atributos de energía renovable no
convencionales  (AERNC en adelante) disponibles desde el 2020 en adelante, con la opción de
visualizar graficas correspondientes y crear observaciones al hacer clic en la opción “Ir” del
listado de cada año si es así el requerimiento.
4.2.1 Reportes Anuales

  Figura 4.3: Vista Reportes de Balance Anual.

<!-- page 37 -->

36


4.2.1 Reportes Mensuales

De la misma forma como se tiene los reportes anuales de atributos, también están disponibles
los reportes de forma mensual, que si se observa se encuentran organizados por año y mes
respectivo. Además, cabe notar que se presentan los mismos indicadores, sin embargo, se
agregan los indicadores definidos en la siguiente tabla.

 Figura 4.4:Vista Reportes de Balance Mensual


 Figura 4.5:Vista Reportes de Balance Mensual, Grafico de AC consumidos.


La vista anterior, es aquella que se visualiza al hacer clic en el grafico asociado a los reportes
mensuales de cada indicador.

<!-- page 38 -->

37


4.3 Vista Usuario
  Figura 4.6:Vista Usuario, creación de un usuario.

La plataforma tiene un a pestaña  de “Usuario”. La que contiene 2 subpestañas: “Listado de
usuarios” y “Crear usuarios”. Esta última, so lo la pueden visualizar los usuarios con Rol de
“Administrador”, los que en ella  pueden crear un usuario para su mism a Organización. No
obstante, los usuarios creados tendrán Rol de “Solo vista” y con el estado “Inactivo”. Por lo que
a continuación, deberán contactar con el Coordinador para solicitar:
- Activar las cuentas de usuarios
- Credenciales de acceso de usuarios
- Cambio de rol11 (opcional)
En el correo por enviar debe indicar al menos la siguiente información de cada usuario:
- Rut registrado
- Correo electrónico registrado
- Número de teléfono registrado
Estos ítems, deben registrarse en RENOVA con el siguiente formato:
- Rut registrado: X.XXX.XXX -X, XX.XXX.XXX -X, en caso de terminar en la letra K,
considerar letra mayúscula.
- Correo electrónico registrado: xxxxxxx…x@institución.org, la que debe poseer al menos
7 caracteres y considerar letra minúscula.
- Número de teléfono registrado: +569xxxxxxxx, la que comienza con símbolo de suma,
código estándar telefónico de Chile, específicamente de teléfonos móviles,
correspondiente al teléfono móvil de contacto directo del usuario registrado.

11 Los usuarios poseen 2 posibles Rol: Solo Vista y Administrador. Adicionalmente, cada usuario puede
poseer 3 tipos de estado: Activo, Inactivo y Eliminado.

<!-- page 39 -->

38


Como cliente podrá ver los usuarios creado s para su Organización, los cuales podrá filtrar por
RUT, estado o fecha de creación, tal como se muestra en la figura:
Figura 4.7:Vista Listado de usuarios de la organización.


Figura 4.8:Vista Descripción de usuario de la organización.


4.4 Vista Organizaciones

En Organizaciones podrá ver la lista de las instalaciones asociadas a su Organización,
instalaciones que proveen de atributos renovables y se pueden ver su ID, Nombre, Tipo,
Organización, tecnología de obtención de energía y estado en la plataforma. Además, tiene la
opción de filtrar según nombre, tipo, Organización o tecnología.

<!-- page 40 -->

39


 Figura 4.9:Vista del listado de instalaciones de consumo asociadas a la organización .

Figura 4.10:Vista del detalle de instalaciones de consumo asociadas a la organización.


Figura 4.11:Vista del detalle de instalaciones de consumo asociadas a la organización (cont.)

<!-- page 41 -->

40


4.5 Vista Contratos
En el presente apartado se definirá todos los conceptos involucrados en la vista para mayor
comprensión para el proceso de creación de contrato.
La Organización “Declara” del Contrato debe indicar los siguientes datos:
Tabla 4.1: Definición de parámetros solicitados en la creación de contratos
Concepto Descripción
Rut Contraparte (*) Declarar el RUT de la Organización Contraparte del contrato, en
formato el cual contenga punto y guion el RUT declarado.
Tipo de transacción
(*): Compra o Venta.
El “Tipo de transacción” permite al declarante establecer si el Contrato
es de “compra” o “venta” para su Organización. En el caso de que se
registre una “compra”, el Declarante establece en el Contrato que será
su Organización quien recibirá los atributos de energía, caso contrario
de “venta”, la Organización a quien representa el Declarante
transferirá los atributos de energía a la Contraparte.

Periodicidad de la
transacción (*):
La “Periodicidad de la transacción” permitirá establecer la frecuencia
con la que el Contrato deberá ejecutar el traspaso de atributos de
energía renovable considerando la información de la declaración del
contrato.  Puede ser Una vez, horaria, diaria, mensual, trimestral o
anual.
Tipo de AER a
traspasar (*):
AERC (Atributos de Energía Renovable Convencional), es decir,
atributos de energías renovables convencionales, entendiéndose
según Ley N°20.257, como la energía proveniente de centrales
hidroeléctricas con una potencia máxima mayor a 20[MW]. Mientras
que los AERNC son aquellos que se definen como Atributos de
generados por medios de generación de Energías Renovables No
Convencional (ERNC), que según Ley N° 20.257, se determina como
ERNC según el Artículo 255°, todo Medio de Generación de Energías
Renovables son a partir de biomasa, hidráulica cuya potencia máxima
es inferior a 20 [MW], geotérmica, energía solar desde radiación solar,
eólica, energía de los mares, otro medio de generación determinado
por la Comisión a partir de energías renovables que permit a
diversificar las fuentes de energías.

<!-- page 42 -->

41


Tabla 4.2: Definición de parámetros solicitados en la creación de contratos
Concepto Descripción
Fecha de inicio del
contrato.

Definir la fecha de inicio como también la hora de caducidad
establecida en el contrato.
Cabe señalar que la fecha es obligatoria de declarar mientras que la
hora es opcional.
Fecha término del
contrato.

Definir la fecha de finalización como también la hora de caducidad
establecida en el contrato.
Cabe señalar que la fecha es obligatoria de declarar mientras que la
hora es opcional.
Clase de contrato Prioridad de Contrato por sobre otros definidos con otras
Organizaciones, lo anterior es solo para Contrato declarado como
venta y si se declara compra, cuando se acepta el Contrato se define
su prioridad.

Respecto a la periodicidad es importante considerar los siguientes puntos

<!-- page 43 -->

42


Tabla 4.3: Criterios asociados a la periodicidad de contratos
Periodicidad ¿Atributos disponibles?12
Sí13 Parcialmente14 No15
Única vez
Se ejecuta contrato
inmediatamente
después de su
aprobación.
- -
Horaria
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir en cada hora
del periodo
establecido.
Realizará las
transferencias para
los meses cargados.
Dejará el Contrato en
estado Activo, hasta
la carga del próximo
mes de ejecución.
Quedará el Contrato en
estado Activo, hasta la
carga del próximo mes
de ejecución.


Diaria
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir en cada día,
entre el periodo
establecido.
Mensual
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir al mes, entre
el periodo establecido.
Trimestral
Realiza todas las
transferencias
necesarias entre la
fecha de inicio y final,
que cumpla con la
cantidad de atributos a
transferir al término de
cada trimestre 16, entre
el periodo establecido.

12 Los atributos de energía “inyectados a la red”, se depositan en las billeteras de cada empresa en el
mismo momento, con la carga mensual del Balance de Inyecciones y Retiros, del respectivo mes y año.
13 Meses involucrados entre la fecha de inicio y término del contrato, se encuentran totalmente
cargados en Renova.
14 Meses involucrados entre la fecha de inicio y término del contrato, se encuentran parcialmente
cargados en Renova.
15 Meses involucrados entre la fecha de inicio y término del contrato, aún no se encuentran cargados en
Renova.

16 Las periodicidades Trimestrales, se ejecutan con la carga del Balance de Inyecciones y Retiros del
último mes del trimestre (1T: Marzo, 2T: Junio, 3T: Septiembre y 4T: Diciembre), buscando la cantidad
de atributos a transferir, en el total de atributos del trimestre (1T: Enero-Marzo, 2T: Abril-Junio, 3T:
Julio-Septiembre y 4T: Octubre-Diciembre).

<!-- page 44 -->

43


Periodicidad ¿Atributos disponibles?12
Sí13 Parcialmente14 No15
Anual
Realiza una única
transferencia,
transfiriendo la
cantidad de atributos
establecida,
disponiendo de la
información de todos
los meses del año.
-
 -


Sin embargo, es importante declara que la primera versión de RENOVA solo tiene disponible la
periodicidad “única vez” (Noviembre 2021).

4.5.1 Crear contrato
Para crear Contrato debe dirigirse a la pestaña Contratos y seleccionar la opción crear contratos.
 Figura 4.12:Vista Crear contrato.

<!-- page 45 -->

44


Para crear Contrato se requiere conocer:

Para definir los criterios anteriores, se debe articular con la Contraparte su interés por ser parte
de RENOVA con el objetivo de definir las anteriores reglas de contrato.
Es muy importante completar los requerimientos en el orden establecido, considerando que el
declarante es Cliente, respecto al tipo de transacción es importante saber:

 Figura 4.13: Primera vista para crear contrato


I • RUT Contraparte (Formato de
Rut, punto y guiòn)
II
• Tipo de transacción
(compra o venta)
III • Fecha de inicio y fin
IV • Periodicidad
Compra
•Monto máximo de AER
comprometida en [MWh]
acorde a la periodicidad de la
transacción.
•Nombre de la instalación de
generación asociada al
contrato.
•Porcentaje de la producción
de la planta asociada al
contrato.
Venta
•Monto máximo de AER
comprometida en MWh
acorde a la periodicidad de la
transacción.
•Nombre instalación de
generación asociada al
contrato.
•Porcentaje de la producción
de la planta asociada al
contrato.

<!-- page 46 -->

45


Una vez completados todos los requerimientos se activará Siguiente y seleccionar la etapa
haciendo clic en “siguiente”. Al ir a la opción, verá la siguiente interfase, es de suma importancia
definir si la condición de borde del Contrato la estimará por cantidad máxima de atributos según
periodicidad o por instalación asociada al Contrato o ambas opciones seleccionadas, se
mostrarán las tres alternativas para cerrar el contrato. se sugiere cantidad máxima.
 Figura 4.14: Primera vista para crear contrato


A) Cantidad Máxima de atributos a transferir según periodicidad establecida.
 Figura 4.15: Creación de contrato seleccionando como limite de transferencia la cantidad
máxima a transferir.

<!-- page 47 -->

46


B) Instalación de generación asociada al contrato

 Figura 4.16: Creación de contrato seleccionando como límite de transferencia porcentaje de
selección.


C) Cantidad máxima de atributos e instalación asociada a contrato.
 Figura 4.17: Creación de contrato seleccionando como límite de transferencia ambas
condiciones de borde.


Una vez creado el contrato, podrá revisar su estado en la lista de contratos.

<!-- page 48 -->

47


4.5.2 Lista de contratos

Por último, existe la opción de revisar los Contratos establecidos haciendo clic en Contratos >>
Lista de contratos, es así como se registran
 Figura 4.18: Creación de contrato seleccionando como límite de transferencia ambas
condiciones de borde.


Existe un filtro a su disposición para obtener información directa de los Contratos definidos con
el RUT Contraparte, el estado de dicho contrato, la lista tiene la siguiente forma:

  Figura 4.19: Vista Listado de contrato.


La descripción de los estados de Contrato se puede observar en la siguiente figura la cual se
condiciona según el estado de los atributos transado.

• Espera la aprobación de la Organización Contraparte.Declarado
• Ha sido aprobado por la Organización Contraparte aunque el Contrato aún se
escuentra transfieriendo atributos. También puede corresponder a la espera de
carga de nueva información. Activo
• El contrato ya transfirió la totalidad de atributos asociados al Contrato, LOS
ATRIBUTOS ASOCIADOS A LA TRANSACCIÓN COMERCIALIZADOS POR EL
GENERADOR QUE REALIZÓ LA TRANSACCIÓN.Caducado
• El Contrato ha sido rechazado por la Organización Contraparte.Inactivo

<!-- page 49 -->

48


El detalle de cada Contrato se visualiza de la siguiente manera forma, seguida a la vista se
presenta una tabla con todas las descripciones de los conceptos asociados en el detalle.
Figura 4.20: Vista descripción de contrato.

Figura 4.21: Vista descripción de contrato. (cont.)

<!-- page 50 -->

49


Tabla 4.4: Descripción de parámetros entregados en detalle de contratos
Parámetro  Descripción
Cantidad máxima de Atributos
de Energía a transferir según
periodicidad establecida

Se observa la cantidad de atributos asignados como
máximos a transar en la creación de contrato.
Cantidad mínima  Cantidad mínima de atributos asignados a condicionar en la
creación del Contrato.
Porcentaje de la generación
de la instalación asociada al
contrato:
Porcentaje de atributos de la instalación a transferir a la
contraparte..
Instalación de Generación
asociada al contrato
Nombre de la instalación que genera atributos destinados a
la Contraparte del contrato.
Cantidad de la generación de
la instalación asociada al
contrato.
Cantidad de atributos producidos de la instalación que se
destinan a la Contraparte.
Clase del contrato  Prioridad del Contrato en relación con los otros Contratos de
la Organización. Si mi Contrato es A, se suministrarán los
atributos al presente contrato.
Cantidad de AER transados:  Declaración de atributos renovables cedidos entre
generador y cliente.
Tipo de AER transados: Declara la clase de AER cedido, Convencional o no
convencional
Cuenta AE activos de origen:  Declaración de atributos del generador creados
almacenados en la presente cuenta.
Cuenta AE activo s de destino: Declaración de atributos del generador creados
almacenados en la presente cuenta que serán destinado a
la Contraparte.
Fecha declaración del
acuerdo:
Declara la fecha de creación de contrato
Fecha de confirmación del
acuerdo:
Declara la fecha de aceptación del acuerdo por la
Contraparte.

<!-- page 51 -->

50


5. PREGUNTAS FRECUENTES

1.- ¿Puedo hacer una prueba de trasferencias de atributos en la plataforma?
Se permitirán pruebas, pero una vez cuando ya todas las funcionalidades de RENOVA estén
implementadas. Por ende, al momento no se permiten pruebas en la plataforma.
2.- ¿Se pueden registrar atributos ya registrados en IREC?
RENOVA posee un carácter de emisor oficial de información de atributos renovables, es por lo
anterior, que toda información debe ser declarada en primera instancia en RENOVA y
posteriormente en alguna certificadora si la organización consumidora lo estima pertinente.
3.- ¿Quién es el responsable de cargar el contrato o registrar las transferencias?
Ambas partes pueden declarar la transferencia de atributos o el contrato en RENOVA, de esa
forma ambas partes poseen grados de responsabilidad en la declaración como la aceptación del
contrato. Sin embargo, deben acordar entre las partes quién será el declarante de contrato en la
plataforma.
4.-  ¿Qué debo acordar con mi contraparte?
Con su contraparte se debe acordar lo siguientes puntos, la periodicidad, el inicio y fin de mi
contrato, las reglas del contrato tales como el máximo a transferir o el porcentaje de instalación
asociado a la transferencia de atributos.
5.- ¿Se puede registrar mi consumo nocturno?
RENOVA registra los atributos renovables que son transferidos a las organizaciones según su
origen, fecha y hora de producción, siendo indistinto el horario en el cual es consumido. Una vez
que se tenga implementada la periodicidad horaria, se podrá tener el control horario del registro
de atributos transferido a esa organización.
6.- ¿RENOVA puede ser una plataforma para ser parte de Huella Chile?
RENOVA es una plataforma la cual permite acreditar el total de créditos de ERNC [MWh] y el
factor de emisión residual [ 𝑡𝐶𝑂2/𝑀𝑊ℎ] en parámetro de “Emisiones Indirectas por energía
importada.
Lo anterior, es posible dado el convenio actual entre el Coordinador Eléctrico Nacional, en
adelante CEN, y Huella Chile del Ministerio Medio Ambiente (MMA).
7.- ¿Hay exigencia normativa que me obligue a participar en RENOVA?
De momento no hay exigencia normativa que obligue a alguna organización a ser parte de
RENOVA. Es importante considerar que RENOVA tiene por objetivo ser el Registro completo
con alcance nacional de energías renovables, por ende, es significativo contar co n la
participación de todas las organizaciones.

<!-- page 52 -->

51


8.- ¿Cuántas horas de mi organización debo invertir en esta iniciativa?
La organización invierte recurso horario en la declaración de contratos en RENOVA, el cual se
estime de 5 a 10 minutos como rango para declarar cada contrato o registro de transferencia de
atributos.
9.- ¿Aquí se registran mis obligaciones por ley ERNC?
Cómo parte del desarrollo tecnológico de RENOVA se considera justamente el acceso a
Reportes en RENOVA donde se indique las Obligaciones por Ley ERNC en la plataforma.
10.- ¿Mis datos son públicos?
RENOVA es suministrada de información obtenida desde Infotécnica, base de datos publica de
instalaciones de generación y consumo del Sistema Eléctrico Nacional, como también de REUC,
Registro Único de Coordinados, plataforma la cual contiene la base de datos de identificación de
cada organización coordinada, plataforma REUC sólo tiene acceso organizaciones coordinadas
a su usuario y el Coordinador.  Respecto a las transferencias de atributos, RENOVA proporciona
carácter de confidencialidad a todas las trasf erencias que se realicen en la plataforma de una a
otra organización, mientras que el total de atributos transferidos en la plataforma y el total de
organizaciones participantes de la plataforma, tienen carácter público, el cual se puede encontrar
en “Reportes públicos” de la página principal.
11.- ¿Habrá una plataforma para declara discrepancias de los datos presentados en
RENOVA?
Una plataforma, en especifica para dicha función no, sin embargo, cualquier eventualidad de
diferencias observadas favor de informar a renova@coordinador.cl .
12.- ¿Cuál es la granularidad de la información en  RENOVA?
La información actualmente posee una granularidad mensual, no obstante, se están trabajando
en actualizaciones que permitan gestionar la información con una granularidad de 15 minutos.
13.- ¿Puedo transferir atributos entre generadores?
En RENOVA se pueden gestionar declaración de transferencias entre generadores -cliente,
generador – generador, cliente-cliente.
14.- ¿Qué debo declarar exactamente en RENOVA?
Dado que el objetivo de la plataforma es dar trazabilidad a los atributos renovables generados y
consumidos a nivel nacional, para cumplir con el anterior objetivo es necesario declarar las
siguientes características.
RUT Contraparte Debe declarar el rut de la organización a quien transferirá los atributos
(vender o comprar).
Tipo de transacción  Debe definir si va a Vender atributos, es decir transferir desde sus
atributos disponibles a otra organización, o Compra atributos, es decir,
adquirir atributos desde su contraparte.
Periodicidad del
contrato.
Debe definir la frecuencia con la cual se estarán transfiriendo atributos,
cabe comentar que en esta fase piloto se encuentra disponible la
periodicidad de “Única Vez”, de esa forma todo atributo declarado será
transferido al momento de aceptar los término s del contrato por la
contraparte.

<!-- page 53 -->

52


Inicio y fin de
contrato
Se debe establecer la fecha de inicio y termino del ciclo de transferencia
de los atributos declarados.
Condiciones de
trasferencias
Se debe determinar si se transfieren atributos de origen convencional,
es decir desde centrales hidroeléctricas o renovables no convencional,
atributos de origen solar, eólico, hidroeléctrica de pasada.
Condiciones de
borde de la
transferencia
Definir si el tope máximo de atributos será limitado por un porcentaje
asociado a una instalación de generación por atributos máximos a
transferir.

Puede encontrar mayor información en la sesión “Crear Contrato” del capitulo 3 o 4 si su
organización el Generador o Cliente.

15.- ¿RENOVA tiene alcance nacional o internacional?
RENOVA actualmente posee un alcance nacional, al generar trazabilidad de todo atributo
renovable inyectado y retirado del Sistema Eléctrico Nacional.
16.- ¿RENOVA está compitiendo con Certificadoras?
Renova al tener un carácter de registro completo de atributos renovables, es un emisor oficial de
información, por lo anterior es que las certificadoras si la organización suministrada lo estima
pertinente debe obtener la información desde RENOVA, certificando atributos ya acreditados por
RENOVA. Por ende, hay una complementariedad de ambos proyectos.
17.- Actualmente que atributos consumidos o generados puedo declarar en RENOVA?
Al momento considerando la fase piloto de RENOVA, se tiene cargado el año 2020, por ende, se
pueden registrar las transferencias de atributos de dicho año, en un corto plazo ya se encontrará
disponible el año 2021.
18.-¿Tiene costos asociados el uso de RENOVA?
De momento el uso de RENOVA y el registro de transferencia no posee costos.
19.- ¿Qué es el Coordinador Eléctrico Nacional?
Es una corporación autónoma de derecho público, SFL, cuya composición, obligación, funciones
y atribuciones están bajo el marco de la ley 20936. El Coordinador opera como un organismo
técnico e independiente, encargado de la coordinación de la operación en  conjunto de las
instalaciones del sistema eléctrico nacional que operen interconectadas entre sí.
20.- ¿Cómo se evita la doble contabilidad de atributos renovables?
RENOVA es el registro de atributos renovables completo a nivel nacional. Por ende, el registro
de todas las organizaciones dentro de la iniciativa y utilizando tecnología blockchain, la cual
permite dar confiabilidad al sistema de trazabilidad dada sus atr ibuciones de inmutabilidad de
datos encriptados, son las dos aristas fundamentales que sostiene RENOVA para evitar la doble
contabilidad.
21.- ¿Cada generador solo verá los contratos asociados a su organización?
Así es, cada generador solo verá en la vista de su organización los contratos asociados a su
organización.

<!-- page 54 -->

53


22.- ¿Qué sucede con aquellos contratos entre Vendedor y Comprador que terminan de
manera anticipada?
Si los atributos ya están transferidos, se deben devolver, generando un contrato de venta desde
la organización deudora a la contraparte.
23.- ¿La información que será ingresada en la plataforma será compartida con alguna
otra entidad?
No, no obstante el Coordinador está sujeto a que si la autoridad pertinente lo requiere debe de
transparentar toda la información necesaria.
24.- ¿Entre clientes pueden ver los contratos suscritos en plataforma Renova?
No.
25.- ¿Quién y cómo se establece la prioridad de los contratos?
El generador establece la prioridad de contrato, esta se asigna según letra A, B, C, siendo la letra
A, alta prioridad, media y baja para B y C respectivamente. Si no quiere hacer uso de la prioridad
del contrato, debe asignar a todos a la par la misma letra y de esa forma se desestima su efecto
en el contrato.
26.-  ¿RENOVA es útil para participar en el mercado de Bonos de Carbono internacional?
Renova posee un carácter de alcance nacional, dado que es un sistema de trazabilidad del
Sistema Eléctrico Nacional, por ende, todo sistema internacional queda fuera del alcance de
RENOVA.
27.- ¿Cuál es la vigencia de los certificados emitidos por RENOVA?
La vigencia esta dada por el inicio y fin de contrato definido en el registro de transferencia de
atributos.
28. El contrato en RENOVA debe ser igual a mi acuerdo contractual con mi contraparte?
No, es importante destacar que el contrato de RENOVA es un mecanismo para registrar la
transferencia de atributos el cual puede ser muy distinto de los contratos físicos. El contrato de
RENOVA esta definido por reglas y condiciones que pueden ser diferente al contrato físico. Por
ejemplo, hoy en día hay contratos físicos de 15 años, pero en RENOVA posiblemente se tengan
que declarar varios contratos para esos 15 años según las condiciones que se estimen
conveniente.

<!-- page 55 -->

54


6. MÉTODO DE CÁLCULO DE ATRIBUTOS EN RENOVA


Concepto Significado
Atributo de
Consumo o
AC
Corresponde a 1 megavatio-hora de energía que se retira del Sistema Eléctrico
Nacional y posee todas las características no energéticas de su punto de
consumo como ubicación, tipo de consumo (Libre, Libre en Distribución o
Regulado), código de medidor, entre otros.
La metodología consiste en el cumplimiento de las siguientes condiciones:
- Si es Generador y Medida Horaria [kWh]<0
- Si es Cliente o consumidor y la Medida Horaria [kWh]<0
AER Atributo de energía renovable , considera la suma de los atributos de energía
renovable convencional (AERC) y no convencional (AERNC).
La metodología consiste en el cumplimiento de las siguientes condiciones:
- Si es Generador , Medida Horaria [kWh] ≥0, tecnología de instalación
asociada Convencional renovable.

AENR Atributo de energía no renovable
La metodología consiste en el cumplimiento de las siguientes condiciones:
- Si es Generador y Medida Horaria [kWh] ≥0, tecnología de instalación
asociada Convencional renovable.
