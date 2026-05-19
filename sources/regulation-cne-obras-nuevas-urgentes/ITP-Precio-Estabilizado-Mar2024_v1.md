---
pdf_source: sources/regulation-cne-obras-nuevas-urgentes/ITP-Precio-Estabilizado-Mar2024_v1.pdf
pdf_sha256: d2c10fbe81cb4ae7d15ad7877523eecd866efadce025da61e20eaf3bf6c09cfc
pdf_pages: 19
extracted_pages: 19
extracted_chars: 34264
extracted_at: 2026-05-19T13:21:32Z
extractor: pypdf
---

# ITP Precio Estabilizado Mar2024 v1

<!-- page 1 -->

DETERMINACIÓN DE PRECIOS
ESTABILIZADOS


INFORME TÉCNICO PRELIMINAR
MARZO 2024

<!-- page 2 -->

2

ÍNDICE
INTRODUCCIÓN ................................................................................................................................... 3
1 ANTECEDENTES ........................................................................................................................... 5
1.1 DEMANDA, COSTOS MARGINALES ESPERADOS Y FACTOR DE REGULACIÓN DE TENSIÓN. 5
1.2 MODELACIÓN TEMPORAL DE LAS VARIABLES .................................................................... 5
1.3 TIPO DE CAMBIO ................................................................................................................. 5
1.4 TASA DE ACTUALIZACIÓN .................................................................................................... 5
2 METODOLOGÍA ............................................................................................................................ 6
2.1 DETERMINACIÓN DE LOS PRECIOS BÁSICOS DE ENERGÍA POR INTERVALO TEMPORAL .... 6
2.2 DETERMINACIÓN DEL AJUSTE A LA BANDA DE MERCADO AL PRECIO BÁSICO DE ENERGÍA
POR INTERVALO TEMPORAL Y DETERMINACIÓN DE LOS PRECIOS ESTABILIZADOS ..................... 10
3 RESULTADOS ............................................................................................................................. 13
3.1 PRECIOS BÁSICOS DE ENERGÍA POR INTERVALO TEMPORAL Y PRECIO BÁSICO PROMEDIO
DE ENERGÍA ................................................................................................................................... 13
3.2 DETERMINACIÓN BANDA DE PRECIOS DE MERCADO Y COMPARACIÓN PRECIO MEDIO
TEÓRICO CON PRECIO MEDIO DE MERCADO ................................................................................ 15
3.2.1 Determinación Precio Medio Básico ......................................................................... 15
3.2.2 Determinación de Banda de Precios ......................................................................... 15
3.2.3 Comparación Precio Medio Teórico – Precio Medio de Mercado ............................ 16
3.3 PRECIOS ESTABILIZADOS ................................................................................................... 17
3.4 FORMULA DE INDEXACIÓN DE LOS PRECIOS ESTABILIZADOS .......................................... 18

<!-- page 3 -->

3

INTRODUCCIÓN
De conformidad a lo dispuesto en el artículo 9º del Decreto Supremo Nº 88 del Ministerio de Energía,
de 2019, que aprueba reglamento para medios de generación de pequeña escala1 (en adelante, “DS
88/2020”), los propietarios u operadores de los Medios de generación de pequeña escala
sincronizados a un sistema eléctrico, tendrán derecho a vender la energía que evacuen al sistema a
costo marginal instantáneo, pudiendo acceder al mecanismo de estabilización de precios, y a vender
sus excedentes de potencia al precio de nudo de la potencia, debiendo participar en las
transferencias de energía y potencia a que se refiere el artículo 149º del D.F.L. Nº 4/20.018, de 2006,
del Ministerio de Economía, Fomento y Reconstrucci ón, que fija el texto refundido, coordinado y
sistematizado del D.F.L. Nº 1, de Minería, de 1982, Ley General de Servicios Eléctricos, en materia
de energía eléctrica (en adelante, la “Ley”), de acuerdo a las disposiciones contenidas en el citado
reglamento y en la normativa vigente.
En virtud de lo dispuesto en el artículo 17º del DS 88/2020, los precios estabilizados a que se refiere
el párrafo primero serán fijados por el Ministerio de Energía, mediante decreto expedido bajo la
fórmula "por orden del Presidente de la República", previo informe técnico de la Comisión Nacional
de Energía (en adelante, “Comisión”) y regirán a partir de su publicación en el  Diario Oficial. Estos
precios serán calculados por la Comisión sobre la base de los antecedentes y la simulación de la
operación esperada del Sistema Eléctrico Nacional (en adelante, “SEN”) realizada con ocasión de la
fijación de Precios de Nudo de Corto Plazo de febrero y agosto de cada año respectivamente.
Para efectos de realizar dicho cálculo, un mes después de la comunicación del informe técnico
definitivo del cálculo de los Precios de Nudo de Corto Plazo, la Comisión, deberá comunicar el
informe técnico preliminar con el cálculo de los precios estabiliza dos al Ministerio de Energía y al
Coordinador, y éste último lo pondrá a disposición de los Coordinados, debiendo además ser
publicado en el sitio web de la Comisión. Los Coordinados tendrán un plazo de diez días hábiles para
observar dicho informe.
El informe técnico de precios estabilizados deberá contener, al menos lo siguiente:
a) La asignación de bloques de la simulación de Precio de Nudo de Corto Plazo realizada en febrero
o agosto de cada año, según corresponda, a los distintos intervalos temporales definidos para el
cálculo;
b) Los precios estabilizados de energía por intervalo temporal para las barras donde se determine el
Precio de Nudo de Corto Plazo de febrero o agosto de cada año, según corresponda;

1 Publicado en el Diario Oficial con fecha 8 de octubre de 2020.

<!-- page 4 -->

4

c) El ajuste a la banda de mercado definida para los precios estabilizados; y,
d) Las fórmulas de indexación aplicables al precio estabilizado.
Según el procedimiento establecido en el artículo 17º del DS 88/2020 ya citado, la Comisión deberá
analizar las observaciones recibidas al informe técnico preliminar de precios estabilizados, las cuales
podrán ser acogidas, total o parcialmente, o rechazadas fundadamente, y deberá publicar en su sitio
web un informe técnico definitivo con los resultados del proceso de determinación de los precios
estabilizados, a más tardar , dentro de  los tres meses siguientes a la comunicación del informe
técnico definitivo del cálculo de los Precios de Nudo de Corto Plazo, el que deberá ser comunicado
al Ministerio de Energía para efectos de la dictación del correspondiente decreto.
Atendido que, con fecha 29 de febrero de 2024, se comunicó la Resolución Exenta Nº 73 de la
Comisión, de la misma fecha, que aprueba el Informe Técnico Definitivo, de enero de 2024, para la
Fijación de Precios de Nudo de Corto Plazo del Sistema Eléctrico Nacional (en adelante, “ITD PNCP”),
a través del presente informe se da cumplimiento a lo dispuesto en el inciso tercero del artículo 17°
del DS 88/2020 que contiene el cálculo preliminar de los precios estabilizados.

<!-- page 5 -->

5

1 ANTECEDENTES
En este capítulo, se presentan los principales antecedentes utilizados en la determinación de los
precios estabilizados en el SEN , que, conforme a lo establecido en el artículo 17° del DS 88/2020,
corresponderán a aquellos utilizados en la determinación de Precios de Nudo de Corto Plazo
contenida en el ITD PNCP, según lo ya señalado en la introducción de este informe.
1.1 DEMANDA, COSTOS MARGINALES ESPERADOS Y FACTOR DE REGULACIÓN DE
TENSIÓN
En virtud de lo establecido en el inciso segundo del artículo 17° del DS 88/2020, los antecedentes de
demanda y de la simulación de la operación esperada del SEN provienen de los  resultados
contenidos en el ITD PNCP, por lo que el detalle de la demanda y de los costos marginales esperados,
tanto en términos geográficos asociados a barras del SEN, como en su temporalidad, asociada a la
relación año, mes y bloque, corresponden íntegramente a aquellos contenidos en el ITD PNCP y sus
bases de cálculo.
Asimismo, se considera el factor de regulación de tensión determinado en el ITD PNCP.
1.2 MODELACIÓN TEMPORAL DE LAS VARIABLES
En consistencia con la modelación temporal de las variables utilizada en el ITD PNCP, se considera
una temporalidad para cada mes de 24 bloques. Así, cada mes contiene 12 bloques que representan
un día hábil promedio y 12 bloques que representan un día no hábil promedio.
1.3 TIPO DE CAMBIO
Se utiliza el mismo tipo de cambio utilizado en el ITD PNCP, que corresponde a 886,61 $/USD.
1.4 TASA DE ACTUALIZACIÓN

La tasa de actualización considerada para los cálculos es de 10% real anual, según lo establecido en
la letra d), del artículo 165° de la Ley.

<!-- page 6 -->

6

2 METODOLOGÍA
Para dar cumplimiento a lo establecido en el Capítulo 3 del Título I del DS 88/2020, la Comisión ha
aplicado la metodología para determinar los precios estabilizados de acuerdo al procedimiento
indicado en los párrafos 2° y 3° del citado capítulo, según se indica a continuación:
a) Determinación de los Precios Básicos de Energía por intervalo temporal.
b) Determinación del ajuste a la banda de mercado al Precio Básico de Energía por intervalo
temporal y determinación de los precios estabilizados.
c) Determinación de la fórmula de indexación de los precios estabilizados.
La metodología empleada para dar cumplimiento con  las etapas indicadas anteriormente se
describe a continuación.
2.1 DETERMINACIÓN DE LOS PRECIOS BÁSICOS DE ENERGÍA POR INTERVALO
TEMPORAL
Los Precios Básicos de Energía son determinados por intervalo temporal, para cada una de las barras
del SEN en las cuales se determinaron los Precios de Nudo de Corto Plazo contenido en el ITD PNCP,
de forma tal que éstos representen la operación del sistema en intervalos temporales dentro del
día. En virtud de lo establecido en el artículo 18° del DS 88/2020, en la Tabla 1 son presentados los
intervalos temporales utilizados para el cálculo de precios estabilizados.
Tabla 1: Intervalos temporales para el cálculo de precios estabilizados
Número
intervalo
Hora de
inicio
Hora de
término
1 0:00 3:59
2 4:00 7:59
3 8:00 11:59
4 12:00 15:59
5 16:00 19:59
6 20:00 23:59
Complementariamente, a partir de los antecedentes y la simulación de la operación esperada del
sistema eléctrico utilizada con ocasión del ITD PNCP, de acuerdo a lo establecido en el subcapítulo
1.1 del presente informe, se obtienen los costos marginales esperados y la demanda de energía del
sistema, en cada una de las subestaciones del sistema eléctrico en las que se definieron los Precios
de Nudo de Corto Plazo.
Por otra parte, d e acuerdo con lo indicado en el artículo 19° del DS 88/2020, se determinan los
Precios Básicos de Energía por intervalo temporal de acuerdo a la siguiente expresión:

<!-- page 7 -->

7

𝑃𝑟𝑒𝑐𝑖𝑜 𝐵á𝑠𝑖𝑐𝑜 𝐸𝑛𝑒𝑟𝑔í𝑎 𝑝𝑜𝑟 𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙𝑜 𝑡𝑒𝑚𝑝𝑜𝑟𝑎𝑙𝑛,𝑡=
∑𝐶𝑀𝑔𝑖,𝑛,𝑡∙𝐸𝑖,𝑛,𝑡
(1+𝑟)𝑖−1
𝑁
𝑖
∑ 𝐸𝑖,𝑛,𝑡
(1+𝑟)𝑖−1
𝑁
𝑖

Donde:
𝑖  : Mes 𝑖-ésimo del horizonte de evaluación.
𝑛  : Nodo o barra del sistema de transmisión nacional.
𝑡  : Intervalo temporal 𝑡  dentro del día, de acuerdo con la Tabla 1.
𝑁  : Número de meses del periodo de cálculo respectivo.
𝐶𝑀𝑔𝑖,𝑛,𝑡 : Costo marginal promedio , en el mes 𝑖, en el nodo o barra  𝑛, para el intervalo
temporal 𝑡.
𝐸𝑖,𝑛,𝑡  : Energía del mes 𝑖, en el nodo o barra 𝑛,  para el intervalo temporal 𝑡.
𝑟 : Tasa de actualización definida en el artículo 165° literal d) de la Ley.
Cada antecedente y resultado de la operación esperada presenta una granularidad temporal igual a
los bloques de la simulación indicada en el subcapítulo 1.2. Es decir, cada mes es representado por
dos tipos de días promedio, uno hábil y otro no hábil, en los cuales cada día es modelado mediante
doce bloques. Para efectos de determinar el costo marginal promedio  y la energía por intervalo
temporal, se aplica el procedimiento listado a continuación.
a) A partir de los costos marginales esperados por bloque, se determina el valor del costo
marginal esperado horario, de acuerdo con la siguiente expresión:

𝐶𝑀𝑔 ℎ𝑜𝑟𝑎𝑟𝑖𝑜𝑖,𝑛,𝑡𝑑,ℎ=𝐶𝑀𝑔 𝑏𝑙𝑜𝑞𝑢𝑒𝑖,𝑛,𝑡𝑑,𝑏
Con:
𝑖   : Mes 𝑖-ésimo del horizonte de evaluación.
𝑛   : Nodo o barra del sistema de transmisión nacional.
𝑡𝑑   : Tipo de día (hábil o no hábil).
𝑏   : Número de bloque según tipo de día.
ℎ   : Hora perteneciente al bloque “b”.

<!-- page 8 -->

8

𝐶𝑀𝑔 𝑏𝑙𝑜𝑞𝑢𝑒𝑖,𝑛,𝑡𝑑,𝑏 : Costo marginal esperado del bloque “𝑏”, en el horizonte temporal “𝑖”, para
el nodo “𝑛”, en el tipo de día “𝑡𝑑”.
b) A partir de la energía de cada bloque , se determina la energía horaria de cada día
representativo, de acuerdo con la siguiente expresión.

𝐸𝑛𝑒𝑟𝑔í𝑎 ℎ𝑜𝑟𝑎𝑟𝑖𝑎𝑖,𝑛,𝑡𝑑,ℎ=𝐸𝑛𝑒𝑟𝑔í𝑎 𝑏𝑙𝑜𝑞𝑢𝑒𝑖,𝑛,𝑡𝑑,𝑏
ℎ𝑜𝑟𝑎𝑠 𝑎𝑠𝑖𝑔𝑛𝑎𝑑𝑎𝑠𝑖,𝑡𝑑,𝑏

Con:
𝑖   : Mes 𝑖-ésimo del horizonte de evaluación.
𝑛   : Nodo o barra del sistema de transmisión nacional.
𝑡𝑑   : Tipo de día (hábil o no hábil).
𝑏   : Número de bloque según tipo de día.
ℎ   : Hora perteneciente al bloque “b”.
𝐸𝑛𝑒𝑟𝑔í𝑎 𝑏𝑙𝑜𝑞𝑢𝑒𝑖,𝑛,𝑡𝑑,𝑏 : Energía esperada del bloque “𝑏”, en el horizonte temporal “𝑖”, para el nodo
“𝑛”, en el tipo de día “𝑡𝑑”.
c) Debido a que el mes es representado por dos  tipos de días, lo anterior resulta en que se
cuenta con 48 valores de energía horaria y costos marginales esperados horarios, para cada
nodo y mes.  Luego, se asignan los costos marginales esperados horarios y la energía horaria
a cada intervalo de tiempo de acuer do con lo definido en la Tabla 1, y cuyo detalle se
encuentra en la Tabla 2. La asignación señalada anteriormente implica que, debido a que
son seis intervalos por día, se asign an, para cada mes e intervalo,  doce valores de energía
horaria (𝐸𝑛𝑒𝑟𝑔í𝑎 ℎ𝑜𝑟𝑎𝑟𝑖𝑎𝑖,𝑛,𝑡𝑑,ℎ,𝑡) y de costos marginales esperados
(𝐶𝑀𝑔 ℎ𝑜𝑟𝑎𝑟𝑖𝑜𝑖,𝑛,𝑡𝑑,ℎ,𝑡).

<!-- page 9 -->

9

Tabla 2: Asignación de bloques a intervalos temporales
Intervalo
temporal
para cálculo
de precios
estabilizados
Hora del día
Asignación día hábil Asignación día no hábil
Mes Mes
1 2 3 4 5 6 7 8 9 10 11 12 1 2 3 4 5 6 7 8 9 10 11 12
1 1 1 1 1 1 1 1 1 1 1 1 1 1 13 13 13 13 13 13 13 13 13 13 13 13
1 2 1 1 1 1 1 1 1 1 1 1 1 1 13 13 13 13 13 13 13 13 13 13 13 13
1 3 2 2 2 2 2 2 2 2 2 2 2 2 14 14 14 14 14 14 14 14 14 14 14 14
1 4 2 2 2 2 2 2 2 2 2 2 2 2 14 14 14 14 14 14 14 14 14 14 14 14
2 5 3 3 3 3 3 3 3 3 3 3 3 3 15 15 15 15 15 15 15 15 15 15 15 15
2 6 3 3 3 3 3 3 3 3 3 3 3 3 15 15 15 15 15 15 15 15 15 15 15 15
2 7 4 4 4 4 4 4 4 4 4 4 4 4 16 16 16 16 16 16 16 16 16 16 16 16
2 8 4 4 4 4 4 4 4 4 4 4 4 4 16 16 16 16 16 16 16 16 16 16 16 16
3 9 5 5 5 5 5 5 5 5 5 5 5 5 17 17 17 17 17 17 17 17 17 17 17 17
3 10 5 5 5 5 5 5 5 5 5 5 5 5 17 17 17 17 17 17 17 17 17 17 17 17
3 11 6 6 6 6 6 6 6 6 6 6 6 6 18 18 18 18 18 18 18 18 18 18 18 18
3 12 6 6 6 6 6 6 6 6 6 6 6 6 18 18 18 18 18 18 18 18 18 18 18 18
4 13 7 7 7 7 7 7 7 7 7 7 7 7 19 19 19 19 19 19 19 19 19 19 19 19
4 14 7 7 7 7 7 7 7 7 7 7 7 7 19 19 19 19 19 19 19 19 19 19 19 19
4 15 8 8 8 8 8 8 8 8 8 8 8 8 20 20 20 20 20 20 20 20 20 20 20 20
4 16 8 8 8 8 8 8 8 8 8 8 8 8 20 20 20 20 20 20 20 20 20 20 20 20
5 17 9 9 9 9 9 9 9 9 9 9 9 9 21 21 21 21 21 21 21 21 21 21 21 21
5 18 9 9 9 9 9 9 9 9 9 9 9 9 21 21 21 21 21 21 21 21 21 21 21 21
5 19 10 10 10 10 10 10 10 10 10 10 10 10 22 22 22 22 22 22 22 22 22 22 22 22
5 20 10 10 10 10 10 10 10 10 10 10 10 10 22 22 22 22 22 22 22 22 22 22 22 22
6 21 11 11 11 11 11 11 11 11 11 11 11 11 23 23 23 23 23 23 23 23 23 23 23 23
6 22 11 11 11 11 11 11 11 11 11 11 11 11 23 23 23 23 23 23 23 23 23 23 23 23
6 23 12 12 12 12 12 12 12 12 12 12 12 12 24 24 24 24 24 24 24 24 24 24 24 24
6 24 12 12 12 12 12 12 12 12 12 12 12 12 24 24 24 24 24 24 24 24 24 24 24 24


d) Posteriormente, el costo marginal esperado por intervalo es determinado a partir de la
siguiente expresión:

𝐶𝑀𝑔𝑖,𝑛,𝑡=
∑ ∑ 𝐶𝑀𝑔 ℎ𝑜𝑟𝑎𝑟𝑖𝑜𝑖,𝑛,𝑡𝑑,ℎ,𝑡⋅ 𝐸𝑛𝑒𝑟𝑔𝑖𝑎 ℎ𝑜𝑟𝑎𝑟𝑖𝑎𝑖,𝑛,𝑡𝑑,ℎ,𝑡 4𝑡
ℎ=3⋅(𝑡−1)+𝑡  𝑡𝑑
∑ ∑ 𝐸𝑛𝑒𝑟𝑔𝑖𝑎 ℎ𝑜𝑟𝑎𝑟𝑖𝑎𝑖,𝑛,𝑡𝑑,ℎ,𝑡 4𝑡
ℎ=3⋅(𝑡−1)+𝑡  𝑡𝑑

<!-- page 10 -->

10

e) Por otra parte, la energía esperada del intervalo es determinada a partir de la siguiente
expresión:
𝐸𝑖,𝑛,𝑡=  ∑ ∑ 𝐸𝑛𝑒𝑟𝑔𝑖𝑎 ℎ𝑜𝑟𝑎𝑟𝑖𝑎𝑖,𝑛,𝑡𝑑,ℎ,𝑡
4𝑡
ℎ=3⋅(𝑡−1)+𝑡

𝑡𝑑

Una vez determinados los Precios Básicos de Energía por intervalo temporal, se amplifican en un
valor igual al factor de regulación de tensión señalado en el subcapítulo 1.1.
Finalmente, el período de cálculo considerado en la fórmula anterior es el mismo que fue utilizado
para efectos de la determinación de los precios de nudo en el ITD PNCP, esto es, 48 meses iniciados
desde octubre del año 2023.
2.2 DETERMINACIÓN DEL AJUSTE A LA BANDA DE MERCADO AL PRECIO BÁSICO
DE ENERGÍA POR INTERVALO TEMPORAL Y DETERMINACIÓN DE LOS PRECIOS
ESTABILIZADOS
Una vez determinados los Precios Básicos de Energía por intervalo temporal, de acuerdo a lo
indicado en el subcapítulo 2.1, se realiza un ajuste de estos precios considerando una Banda de
Precios de Mercado.
Para tal efecto , de acuerdo a lo indicado en el inciso tercero del artículo 20° del DS 88/2020, se
determina un precio básico promedio de energía para la barra de referencia2, el cual se calcula como
el promedio ponderado por la demanda de energía correspondiente a cada intervalo temporal de
los Precios Básicos de Energía, por intervalo temporal en la barra de referencia indicada
anteriormente. Lo anterior, es determinado a través de la siguiente expresión:
𝑃𝐵𝐸𝑃=
∑ 𝑃𝐵𝐸𝑡⋅𝐸𝑡
𝑇
𝑡=1
∑ 𝐸𝑡𝑇
𝑡=1

Donde:
𝑡  : Intervalo temporal 𝑡 dentro del día.
𝑃𝐵𝐸𝑃  : Precio básico promedio de energía para la barra de referencia.
𝑃𝐵𝐸𝑡  : Precio básico promedio de energía, para la barra de referencia, en el intervalo t.
𝐸𝑡  : Demanda de energía, para la barra de referencia, en el intervalo t.

2
 Se utiliza la misma que en el ITD PNCP.

<!-- page 11 -->

11

𝑇  : Total de intervalos temporales definidos.
BREF  : Barra de referencia utilizada en el ITD PNCP.
Para realizar el ajuste, se considera el Precio Medio de Mercado, en adelante “ 𝑃𝑀𝑀”, el que
corresponde al mismo valor utilizado en el ITD PNCP.
Luego, en virtud de lo estipulado en el artículo 22° del DS 88/2020,  se determina para la barra de
referencia definida, un Precio Medio Básico, conforme a la siguiente expresión:
𝑃𝑀𝐵[ $
𝑘𝑊ℎ]=𝑃𝐵𝐸𝑝[ $
𝑘𝑊ℎ]+ 𝑃𝐵𝑃[
$
𝑘𝑊
𝑚𝑒𝑠]∙ 12 [𝑚𝑒𝑠]
8760 [ℎ]∙𝑓𝑐
Donde:
𝑃𝑀𝐵 : Precio Medio Básico para la barra de referencia.
𝑃𝐵𝐸𝑝 : Precio básico promedio de energía para la barra de referencia.
𝑃𝐵𝑃 : Precio básico de la potencia, referido a la barra de referencia.
𝑓𝑐  : Factor de carga del sistema eléctrico, determinado por la Comisión en base a antecedentes
históricos, de forma de representar adecuadamente el comportamiento de la demanda.
Posteriormente, de acuerdo a lo indicado en el inciso primero del artículo 23 ° del DS 88/2020, se
determina la diferencia porcentual entre el 𝑃𝑀𝐵 y 𝑃𝑀𝑀, de acuerdo con la siguiente expresión:
𝐷𝐼𝐹%𝑃𝑀𝐵−𝑃𝑀𝑀=|𝑃𝑀𝐵−𝑃𝑀𝑀
𝑃𝑀𝑀 |∙100%
Si la diferencia determinada por la expresión del presente artículo es inferior a 30%, se definirá como
banda de precios de mercado un valor igual al 5% en torno al 𝑃𝑀𝑀. Si la diferencia es igual o superior
a 30% e inferior a 80%, se definirá como banda de precios de mercado un valor igual a las dos quintas
partes de la diferencia porcentual determinada por la expresión del presente artículo, menos 2%, en
torno al 𝑃𝑀𝑀. Si la diferencia es igual o superior a 80%, se definirá como banda de precios de
mercado un valor igual a 30% en torno al 𝑃𝑀𝑀. Esta banda de precios de mercado, en adelante
“𝐵𝑃𝑀”, será definida de acuerdo a la siguiente expresión:

<!-- page 12 -->

12

𝐵𝑃𝑀=
{


 5%;𝑠𝑖 |𝑃𝑀𝐵−𝑃𝑀𝑀
𝑃𝑀𝑀 |%<30%
2
5|𝑃𝑀𝐵−𝑃𝑀𝑀
𝑃𝑀𝑀 |%−2%;𝑠𝑖 30%≤|𝑃𝑀𝐵−𝑃𝑀𝑀
𝑃𝑀𝑀 |%≤80%
30%;𝑠𝑖 80%≤|𝑃𝑀𝐵−𝑃𝑀𝑀
𝑃𝑀𝑀 |


A continuación, se determina el Precio Medio Teórico, en adelante “ PMT”, el que de acuerdo a lo
estipulado en el numeral 2) del artículo 167° de la Ley, es igual al cuociente entre: (i) la facturación
teórica que resulta de valorar los suministros a clientes libres y distribuidoras a los precios de nudo
de energía y potencia determinados en el presente informe, incorporando los cargos destinados a
remunerar el sistema de transmisión nacional conforme a lo señalado en el artículo 115° de la Ley ,
en sus respectivos puntos de suministro y nivel de tensión, y las disposiciones transitorias de la Ley
N° 20.936 ; y, (ii) la energía asociada a dichos suministros . Ambas componentes del cuociente
anterior, ocurridas en el periodo de cuatro meses que culmina en el tercer mes anterior al
establecido para la comunicación del informe técnico a que se refiere el artículo 169° de la Ley.
De acuerdo a lo señalado en el literal (i) del párrafo precedente y , considerando que se deben
incorporar los respectivos puntos de suministro y nivel de tensión  para determinar el PMT ,
corresponde que se adicionen los cargos destinados a remunerar la transmisión zonal.
Posteriormente, se debe evaluar si el Precio Medio Teórico, se encuentra contenido en la banda de
precios de mercado, ante lo cual se pueden dar las siguientes dos situaciones:
1. Si el Precio Medio Teórico se encuentra contenido en la banda de precios de mercado, los
precios estabilizados por intervalo temporal serán los determinados de acuerdo a lo
indicado en el subcapítulo 2.1.

2. Si el Precio Medio Teórico no se encuentra contenido en la banda de precios de mercado,
se deberá adicionar o sustraer un valor constante al precio básico promedio de energía, de
modo que el Precio Medio Teórico ajustado alcance el límite más próximo, superior o
inferior, de la banda de precios de mercado. En este caso, los precios estabilizados por
intervalo temporal se calcularán como los Precios Básicos de Energía por intervalo temporal,
determinados de acuerdo a lo indicado en el subcapítulo 2.1, adicionando o sustrayendo el
valor constante ya indicado, con la restricción de que como resultado de la operatoria el
precio estabilizado, para cada uno de sus intervalos, no puede ser inferior a cero.

<!-- page 13 -->

13

3 RESULTADOS
En el presente capítulo se realiza la determinación de los Precios Básicos de Energía por intervalo
temporal, la banda de precios de mercado y los precios de energía por intervalo temporal.
3.1 PRECIOS BÁSICOS DE ENERGÍA POR INTERVALO TEMPORAL Y PRECIO BÁSICO
PROMEDIO DE ENERGÍA
Sobre la base de los antecedentes definidos en el capítulo 1 y la metodología establecida en el
capítulo 2, se han determinado para cada intervalo y subestación, los Precios Básicos de Energía por
intervalo temporal, y los precios básicos promedio de energía, los cuales se presentan en la Tabla 3.
Tabla 3: Precios Básicos de Energía por intervalo temporal y precio básico promedio de energía
NUDO TENSIÓN
PRECIO BÁSICO DE ENERGÍA POR INTERVALO
TEMPORAL [$/kWh] PRECIO
BÁSICO
PROMEDIO
DE ENERGÍA
[$/kWh]
1 2 3 4 5 6
PARINACOTA 220 63,050 52,348 2,674 0,000 28,887 85,523 37,595
POZO ALMONTE 220 60,750 50,749 3,055 0,000 28,007 82,493 38,233
CONDORES 220 61,476 51,106 2,816 0,000 28,198 83,492 36,246
TARAPACA 220 59,865 49,741 2,799 0,000 27,016 82,088 36,691
LAGUNAS 220 59,398 49,371 2,783 0,000 26,808 81,423 36,405
NUEVA VICTORIA 220 59,137 49,160 2,762 0,000 26,697 81,049 36,243
CRUCERO 220 56,445 46,652 3,298 0,000 26,281 77,216 35,630
ENCUENTRO 220 57,326 48,124 3,279 0,000 26,650 77,785 36,162
CHUQUICAMATA 220 58,079 48,638 3,382 0,000 26,869 79,101 36,656
CALAMA 220 57,759 48,237 3,009 0,000 28,171 78,875 37,294
EL TESORO 220 58,493 49,005 3,257 0,000 27,218 79,376 36,605
ESPERANZA SING 220 58,485 48,998 3,257 0,000 27,215 79,365 36,600
ATACAMA 220 56,408 46,643 2,910 0,000 27,621 78,107 35,246
EL COBRE 220 57,664 48,975 3,125 0,000 26,681 77,921 34,438
LABERINTO 220 58,296 48,293 3,116 0,000 26,434 78,774 33,735
O'HIGGINS 220 58,527 48,309 3,137 0,000 26,363 78,861 33,777
D. DE ALMAGRO 220 48,754 41,799 3,113 0,000 25,278 73,815 32,660
CARRERA PINTO 220 48,416 41,517 3,122 0,000 25,172 73,320 32,454
CARDONES 220 48,090 41,285 3,191 0,000 25,196 72,846 32,294
MAITENCILLO 220 46,719 39,954 3,049 0,001 24,259 71,005 31,098

<!-- page 14 -->

14

NUDO TENSIÓN
PRECIO BÁSICO DE ENERGÍA POR INTERVALO
TEMPORAL [$/kWh] PRECIO
BÁSICO
PROMEDIO
DE ENERGÍA
[$/kWh]
1 2 3 4 5 6
PUNTA COLORADA 220 46,344 39,662 3,115 0,006 24,240 70,643 30,934
PAN DE AZUCAR 220 46,406 39,940 3,429 0,017 25,170 70,988 31,499
LOS VILOS 220 45,881 39,281 3,300 0,051 26,742 69,722 30,935
NOGALES 220 43,795 39,028 3,846 0,114 30,065 67,803 30,734
QUILLOTA 220 44,709 38,232 3,665 0,081 25,801 69,206 30,296
POLPAICO 220 44,915 38,009 3,660 0,095 26,039 69,170 27,552
EL LLANO 220 44,358 38,228 3,789 0,092 26,050 68,687 30,708
LOS MAQUIS 220 44,298 38,197 3,789 0,092 26,052 68,453 30,653
LAMPA 220 46,505 40,347 4,373 0,110 16,577 69,403 27,646
CERRO NAVIA 220 43,416 36,724 3,694 0,099 26,183 69,374 27,288
MELIPILLA 220 45,022 38,534 3,908 0,081 23,421 70,623 28,815
RAPEL 220 43,357 37,399 3,772 0,070 22,907 70,019 28,187
CHENA 220 43,301 36,629 3,705 0,100 26,201 69,276 27,252
MAIPO 220 42,330 35,889 3,585 0,095 25,741 67,934 29,429
ALTO JAHUEL 220 41,873 35,848 3,755 0,098 26,020 67,917 29,595
ITAHUE 220 41,861 36,267 4,412 0,071 18,377 61,551 26,012
ANCOA 220 40,764 34,854 3,487 0,080 23,149 59,172 26,334
CHARRUA 220 37,883 32,691 3,474 0,100 21,586 55,806 24,892
COLBUN 220 40,766 34,855 3,487 0,080 23,151 59,180 26,337
CANDELARIA 220 43,284 36,635 3,606 0,084 25,402 66,994 28,881
HUALPEN 220 38,809 33,430 4,448 1,186 23,574 57,773 26,172
LAGUNILLAS 220 38,633 33,259 4,761 1,589 24,016 57,718 26,302
CAUTÍN 220 36,644 32,344 3,626 0,084 21,304 52,810 23,431
TEMUCO 220 35,092 30,733 3,595 0,143 20,021 51,352 22,122
CIRUELOS 220 23,967 21,260 12,873 16,638 24,517 40,661 23,437
VALDIVIA 220 24,317 20,972 12,889 16,605 24,290 40,713 23,528
RAHUE 220 23,132 21,508 14,203 18,294 24,795 39,337 23,423
PUERTO MONTT 220 22,877 20,237 13,292 17,137 23,843 39,009 22,648
MELIPULLI 220 22,878 20,238 13,292 17,138 23,844 39,010 22,649
CHILOE 220 23,714 21,105 14,092 18,015 24,167 39,893 23,412

<!-- page 15 -->

15

3.2 DETERMINACIÓN BANDA DE PRECIOS DE MERCADO Y COMPARACIÓN
PRECIO MEDIO TEÓRICO CON PRECIO MEDIO DE MERCADO

3.2.1 Determinación Precio Medio Básico
Conforme a lo establecido en el subcapítulo 2.2 el Precio Medio Básico (PMB) resulta ser igual a:
Tabla 4: Precio Medio Básico 3
Precio Medio Básico  SEN
Precio Básico Energía (PBEp) [$/kWh] 27,552
Precio Básico Potencia (PBP) [$/kW/mes] 7.931,51
Precio Medio Básico (PMB) [$/kWh] 41,478

3.2.2 Determinación de Banda de Precios
Según lo establecido en el subcapítulo 2.2, para la determinación de la Banda de Precios de Mercado
(𝐵𝑃𝑀), se determinó la diferencia porcentual ( ∆𝑃𝑀𝐵/ 𝑃𝑀𝑀%) entre el Precio Medio Básico,
calculado en el punto anterior, y el Precio Medio de Mercado (𝑃𝑀𝑀). Esta comparación se muestra
en la Tabla 5 siguiente.
Tabla 5: Comparación Precio Medio Básico – Precio Medio de Mercado
Precio Medio Básico  SEN
Precio Medio Básico [$/kWh] 41,478
Precio Medio de Mercado [$/kWh] 103,408
Δ PMB / PMM (%)4 -59,90%
El procedimiento para determinar la Banda de Precios de Mercado ( 𝐵𝑃𝑀) se describe a
continuación:
𝐵𝑃𝑀=
{


 5% ;𝑠𝑖|∆𝑃𝑀𝐵
𝑃𝑀𝑀|%<30%
2
5|∆𝑃𝑀𝐵
𝑃𝑀𝑀|%−2% ;𝑠𝑖 30%≤|∆𝑃𝑀𝐵
𝑃𝑀𝑀|%<80%
30% ;𝑠𝑖 80%≤|∆𝑃𝑀𝐵
𝑃𝑀𝑀|%

De la aplicación del procedimiento descrito anteriormente, el límite inferior de la 𝐵𝑃𝑀 para la
presente fijación resulta igual a 22,0% 5 en el SEN.

3 Barra del Precio Básico de Energía, factor de carga y Precio Básico Potencia igual al indicado en el ITD PNCP.
4 Diferencias en el cálculo se deben a aproximaciones por redondeo.
5 Diferencias en el cálculo se deben a aproximaciones por redondeo.

<!-- page 16 -->

16

3.2.3 Comparación Precio Medio Teórico – Precio Medio de Mercado
De acuerdo a lo estipulado en el subcapítulo 2.2, el Precio Medio Teórico ha sido calculado como el
cuociente entre la facturación teórica que resulta de valorar los suministros a clientes libres y
distribuidoras a los precios de nudo de energía y potencia determinados en el presente informe,
incorporando los cargos destinados a remunerar el sistema de transmisión nacional y zonal.
De esta forma, conforme al procedimiento estipulado en el artículo 25° del DS 88/2020, la diferencia
porcentual entre el Precio Medio de Mercado y el Precio Medio Teórico resulta ser igual a:
Tabla 6: Comparación Precio Medio Teórico – Precio Medio de Mercado
Precio Medio Teórico   SEN
Precio Medio Teórico [$/kWh] 47,656
Precio Medio de Mercado [$/kWh] 103,408
Diferencia (%)6 -53,91%
En el SEN d icha diferencia porcentual es menor al límite inferior de la 𝐵𝑃𝑀 calculado en el punto
anterior. Por lo tanto, según lo señalado en el subcapítulo 2.2 del presente informe, se determina el
“Precio Medio Teórico Ajustado”, el cual presenta la misma estructura que el PMT ya calculado, no
obstante, a su componente de energía, en cada punto de suministro, se debe adicionar o sustraer
un valor único y constante, de modo que el Precio Medio Teórico Ajustado alcance el límite más
próximo, superior o inferior, de la banda de precios de mercado.  El resultado es presentado en la
Tabla 7.
Tabla 7: Comparación Precio Medio Teórico Ajustado – Precio Medio de Mercado
Precio Medio Teórico Ajustado SEN
Precio Medio Teórico Ajustado [$/kWh] 80,659
Precio Medio de Mercado [$/kWh] 103,408
Diferencia (%)7 -22,0%
Como resultado del proceso anterior, para efectos de determinar los precios estabilizados, el valor
que se debe adicionar a la componente de energía corresponde a 32,195 [$/kWh], con el fin de
alcanzar el límite más próximo de la Banda de Precios de Mercado. En virtud de lo anterior, y de
acuerdo con lo establecido en el inciso final artículo 25° del DS 88/2020, los precios estabilizados se
calcularon como los Precios Básicos de Energía por intervalo temporal adicionando un valor igual a
32,195 [$/kWh].

6  Diferencias en el cálculo se deben a aproximaciones por redondeo.
7 Diferencias en el cálculo se deben a aproximaciones por redondeo.

<!-- page 17 -->

17

3.3 PRECIOS ESTABILIZADOS
Con el a juste de la banda señalado previamente , los precios estabilizados resultantes son los
presentados en la Tabla 8 a continuación.
Tabla 8: Precios estabilizados por intervalo temporal

NUDO TENSIÓN
[kV]
PRECIO ESTABILIZADO POR INTERVALO TEMPORAL [$/kWh]
1 2 3 4 5 6
PARINACOTA 220 95,245 84,543 34,869 32,195 61,082 117,718
POZO ALMONTE 220 92,945 82,944 35,250 32,195 60,202 114,688
CONDORES 220 93,671 83,301 35,011 32,195 60,393 115,687
TARAPACA 220 92,060 81,936 34,994 32,195 59,211 114,283
LAGUNAS 220 91,593 81,566 34,978 32,195 59,003 113,618
NUEVA VICTORIA 220 91,332 81,355 34,957 32,195 58,892 113,244
CRUCERO 220 88,640 78,847 35,493 32,195 58,476 109,411
ENCUENTRO 220 89,521 80,319 35,474 32,195 58,845 109,980
CHUQUICAMATA 220 90,274 80,833 35,577 32,195 59,064 111,296
CALAMA 220 89,954 80,432 35,204 32,195 60,366 111,070
EL TESORO 220 90,688 81,200 35,452 32,195 59,413 111,571
ESPERANZA SING 220 90,680 81,193 35,452 32,195 59,410 111,560
ATACAMA 220 88,603 78,838 35,105 32,195 59,816 110,302
EL COBRE 220 89,859 81,170 35,320 32,195 58,876 110,116
LABERINTO 220 90,491 80,488 35,311 32,195 58,629 110,969
O'HIGGINS 220 90,722 80,504 35,332 32,195 58,558 111,056
D. DE ALMAGRO 220 80,949 73,994 35,308 32,195 57,473 106,010
CARRERA PINTO 220 80,611 73,712 35,317 32,195 57,367 105,515
CARDONES 220 80,285 73,480 35,386 32,195 57,391 105,041
MAITENCILLO 220 78,914 72,149 35,244 32,196 56,454 103,200
PUNTA
COLORADA 220 78,539 71,857 35,310 32,201 56,435 102,838
PAN DE AZUCAR 220 78,601 72,135 35,624 32,212 57,365 103,183
LOS VILOS 220 78,076 71,476 35,495 32,246 58,937 101,917
NOGALES 220 75,990 71,223 36,041 32,309 62,260 99,998
QUILLOTA 220 76,904 70,427 35,860 32,276 57,996 101,401
POLPAICO 220 77,110 70,204 35,855 32,290 58,234 101,365
EL LLANO 220 76,553 70,423 35,984 32,287 58,245 100,882
LOS MAQUIS 220 76,493 70,392 35,984 32,287 58,247 100,648
LAMPA 220 78,700 72,542 36,568 32,305 48,772 101,598

<!-- page 18 -->

18

NUDO TENSIÓN
[kV]
PRECIO ESTABILIZADO POR INTERVALO TEMPORAL [$/kWh]
1 2 3 4 5 6
CERRO NAVIA 220 75,611 68,919 35,889 32,294 58,378 101,569
MELIPILLA 220 77,217 70,729 36,103 32,276 55,616 102,818
RAPEL 220 75,552 69,594 35,967 32,265 55,102 102,214
CHENA 220 75,496 68,824 35,900 32,295 58,396 101,471
MAIPO 220 74,525 68,084 35,780 32,290 57,936 100,129
ALTO JAHUEL 220 74,068 68,043 35,950 32,293 58,215 100,112
ITAHUE 220 74,056 68,462 36,607 32,266 50,572 93,746
ANCOA 220 72,959 67,049 35,682 32,275 55,344 91,367
CHARRUA 220 70,078 64,886 35,669 32,295 53,781 88,001
COLBUN 220 72,961 67,050 35,682 32,275 55,346 91,375
CANDELARIA 220 75,479 68,830 35,801 32,279 57,597 99,189
HUALPEN 220 71,004 65,625 36,643 33,381 55,769 89,968
LAGUNILLAS 220 70,828 65,454 36,956 33,784 56,211 89,913
CAUTÍN 220 68,839 64,539 35,821 32,279 53,499 85,005
TEMUCO 220 67,287 62,928 35,790 32,338 52,216 83,547
CIRUELOS 220 56,162 53,455 45,068 48,833 56,712 72,856
VALDIVIA 220 56,512 53,167 45,084 48,800 56,485 72,908
RAHUE 220 55,327 53,703 46,398 50,489 56,990 71,532
PUERTO MONTT 220 55,072 52,432 45,487 49,332 56,038 71,204
MELIPULLI 220 55,073 52,433 45,487 49,333 56,039 71,205
CHILOE 220 55,909 53,300 46,287 50,210 56,362 72,088
3.4 FORMULA DE INDEXACIÓN DE LOS PRECIOS ESTABILIZADOS
En concordancia con lo establecido en el ITD PNCP, y el mecanismo de indexación para el precio de
nudo de energía, el precio estabilizado  por intervalo de cada nodo será indexado respecto de las
variaciones que experimente el Precio Medio de Mercado de acuerdo a la siguiente expresión:
𝑃𝑟𝑒𝑐𝑖𝑜 𝑒𝑠𝑡𝑎𝑏𝑖𝑙𝑖𝑧𝑎𝑑𝑜 𝑑𝑒 𝑒𝑛𝑒𝑟𝑔í𝑎𝑡=𝑃𝑟𝑒𝑐𝑖𝑜 𝑏𝑎𝑠𝑒𝑡 [𝑃𝑀𝑀𝑖
𝑃𝑀𝑀0
]
Dónde:
𝑃𝑟𝑒𝑐𝑖𝑜 𝑒𝑠𝑡𝑎𝑏𝑖𝑙𝑖𝑧𝑎𝑑𝑜 𝑑𝑒 𝑒𝑛𝑒𝑟𝑔í𝑎𝑡: Precio estabilizado de energía del nodo, para el intervalo
temporal t, de conformidad a los intervalos definidos en el
subcapítulo 2.1.

<!-- page 19 -->

19

𝑃𝑟𝑒𝑐𝑖𝑜 𝑏𝑎𝑠𝑒𝑡: Precio estabilizado base de energía del nodo, para el intervalo temporal t,
correspondiente a los indicados en la Tabla 8, del subcapítulo 3.3.
𝑃𝑀𝑀𝑖 : Precio Medio de Mercado determinado con los precios medios de los contratos de clientes
libres y ventas efectuadas a precio de nudo de largo plazo de las empresas distribuidoras
según corresponda, informados a la Comisión por las empresas generadoras,
correspondientes a la ventana de cuatro meses que finaliza el tercer mes anterior a la fecha
de publicación de este precio.
𝑃𝑀𝑀0 : Precio Medio de Mercado determinado con los precios medios de los contratos de clientes
libres y ventas efectuadas a precio de nudo de largo plazo de las empresas distribuidoras
según corresponda, informados a la Comisión por las empresas generadoras ,
correspondientes a la ventana de cuatro meses establecida en la normativa vigente. Este
valor se encuentra establecido en el ITD PNCP.
Dentro de los primeros cinco días de cada mes, la Comisión publicará en su sitio web, el valor del
𝑃𝑀𝑀𝑖 respectivo, para efectos de la aplicación de la fórmula anterior.
