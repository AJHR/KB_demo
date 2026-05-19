---
pdf_source: sources/regulation-cne-obras-nuevas-urgentes/ITP-Precio-Estabilizado-Sep2023.pdf
pdf_sha256: e9a541beb26faffdfaa5d2ea5138de6b720b75c89efdf87070011720145b71fe
pdf_pages: 19
extracted_pages: 19
extracted_chars: 34250
extracted_at: 2026-05-19T13:21:33Z
extractor: pypdf
---

# ITP Precio Estabilizado Sep2023

<!-- page 1 -->

DETERMINACIÓN DE PRECIOS
ESTABILIZADOS


INFORME TÉCNICO PRELIMINAR
SEPTIEMBRE 2023

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
Atendido que, con fecha 11 de agosto de 2023, se comunicó la Resolución Exenta Nº 365 de la
Comisión, de la misma fecha, que aprueba el  Informe Técnico Definitivo, de julio de 2023, para la
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
Se utiliza el mismo tipo de cambio utilizado en el ITD PNCP, que corresponde a 798,64 $/USD.
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
PARINACOTA 220 104,232 77,153 2,549 0,001 43,295 126,149 56,905
POZO ALMONTE 220 100,484 74,983 2,893 0,001 42,052 121,954 58,112
CONDORES 220 101,126 74,917 2,681 0,002 42,285 122,535 54,584
TARAPACA 220 98,781 73,302 2,638 0,001 40,711 120,855 55,678
LAGUNAS 220 97,990 72,741 2,622 0,001 40,389 119,837 55,229
NUEVA VICTORIA 220 97,489 72,382 2,560 0,001 40,201 119,199 54,940
CRUCERO 220 93,005 68,645 3,528 0,002 39,363 113,531 53,994
ENCUENTRO 220 94,155 70,674 3,450 0,002 39,812 113,971 54,653
CHUQUICAMATA 220 95,413 71,385 3,581 0,003 40,079 115,936 55,389
CALAMA 220 94,167 69,920 3,210 0,002 42,183 115,103 55,817
EL TESORO 220 97,099 70,964 3,224 0,002 40,125 116,503 55,221
ESPERANZA SING 220 97,079 70,954 3,224 0,002 40,122 116,477 55,211
ATACAMA 220 92,305 67,744 2,914 0,002 41,345 113,945 53,006
EL COBRE 220 94,408 71,336 3,283 0,002 39,713 113,597 51,775
LABERINTO 220 95,740 70,692 3,367 0,002 39,094 114,369 50,798
O'HIGGINS 220 95,685 70,606 3,401 0,002 38,984 113,966 50,701
D. DE ALMAGRO 220 76,410 59,454 3,227 0,002 36,887 104,113 47,479
CARRERA PINTO 220 75,882 59,063 3,229 0,003 36,718 103,412 47,176
CARDONES 220 75,365 58,739 3,340 0,003 36,728 102,736 46,937
MAITENCILLO 220 72,814 56,616 3,231 0,003 35,324 99,687 45,001

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
PUNTA COLORADA 220 72,255 56,246 3,307 0,010 35,316 99,285 44,790
PAN DE AZUCAR 220 72,548 56,798 3,575 0,021 36,466 100,064 45,669
LOS VILOS 220 70,858 55,488 3,447 0,063 37,921 97,985 44,266
NOGALES 220 64,268 52,670 4,158 0,170 41,605 93,498 42,669
QUILLOTA 220 66,690 52,517 3,835 0,117 35,971 95,281 42,341
POLPAICO 220 68,039 52,459 3,916 0,137 36,508 96,076 38,701
EL LLANO 220 67,031 53,113 3,968 0,134 36,729 95,193 43,429
LOS MAQUIS 220 66,905 53,058 3,970 0,134 36,714 94,864 43,339
LAMPA 220 70,306 56,679 4,573 0,151 23,185 97,617 39,720
CERRO NAVIA 220 62,113 49,151 3,967 0,143 36,418 94,952 37,411
MELIPILLA 220 65,616 52,820 4,169 0,114 32,511 96,381 39,897
RAPEL 220 65,411 52,658 4,140 0,111 32,325 96,044 39,749
CHENA 220 61,151 48,679 3,979 0,145 36,321 94,165 37,092
MAIPO 220 58,617 47,260 3,836 0,137 35,631 91,557 39,735
ALTO JAHUEL 220 57,791 46,994 3,937 0,144 36,144 91,397 39,869
ITAHUE 220 58,496 48,852 4,775 0,100 25,436 83,800 35,486
ANCOA 220 56,322 46,194 3,725 0,115 32,033 80,459 35,655
CHARRUA 220 52,202 43,327 3,644 0,142 29,736 76,171 33,725
COLBUN 220 56,324 46,195 3,725 0,115 32,035 80,469 35,658
CANDELARIA 220 60,000 48,420 3,837 0,121 35,075 90,209 38,933
HUALPEN 220 53,258 44,195 4,640 1,643 31,380 78,258 35,086
LAGUNILLAS 220 52,929 43,916 4,957 2,199 31,583 77,965 35,122
CAUTÍN 220 51,282 43,490 3,879 0,130 29,224 70,745 31,650
TEMUCO 220 49,006 41,273 3,810 0,178 27,428 68,905 29,894
CIRUELOS 220 39,217 33,488 14,856 14,159 30,975 58,213 31,736
VALDIVIA 220 39,693 32,944 15,063 14,635 30,993 58,433 31,620
RAHUE 220 36,932 33,355 16,322 15,646 30,316 55,667 30,839
PUERTO MONTT 220 37,016 31,665 15,499 14,870 29,612 55,367 30,154
MELIPULLI 220 37,017 31,666 15,500 14,870 29,613 55,369 30,155
CHILOE 220 38,121 32,852 16,268 15,555 29,835 56,476 31,012

<!-- page 15 -->

15

3.2 DETERMINACIÓN BANDA DE PRECIOS DE MERCADO Y COMPARACIÓN
PRECIO MEDIO TEÓRICO CON PRECIO MEDIO DE MERCADO

3.2.1 Determinación Precio Medio Básico
Conforme a lo establecido en el subcapítulo 2.2 el Precio Medio Básico (PMB) resulta ser igual a:
Tabla 4: Precio Medio Básico 3
Precio Medio Básico  SEN
Precio Básico Energía (PBEp) [$/kWh] 38,701
Precio Básico Potencia (PBP) [$/kW/mes] 7.306,95
Precio Medio Básico (PMB) [$/kWh] 51,530

3.2.2 Determinación de Banda de Precios
Según lo establecido en el subcapítulo 2.2, para la determinación de la Banda de Precios de Mercado
(𝐵𝑃𝑀), se determinó la diferencia porcentual ( ∆𝑃𝑀𝐵/ 𝑃𝑀𝑀%) entre el Precio Medio Básico,
calculado en el punto anterior, y el Precio Medio de Mercado (𝑃𝑀𝑀). Esta comparación se muestra
en la Tabla 5 siguiente.
Tabla 5: Comparación Precio Medio Básico – Precio Medio de Mercado
Precio Medio Básico  SEN
Precio Medio Básico [$/kWh] 51,530
Precio Medio de Mercado [$/kWh] 106,496
Δ PMB / PMM (%)4 -51,60%
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
presente fijación resulta igual a 18,6% 5 en el SEN.

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
Precio Medio Teórico [$/kWh] 61,627
Precio Medio de Mercado [$/kWh] 106,496
Diferencia (%) -42,13%
En el SEN d icha diferencia porcentual es menor al límite inferior de la 𝐵𝑃𝑀 calculado en el punto
anterior. Por lo tanto, según lo señalado en el subcapítulo 2.2 del presente informe, se determina el
“Precio Medio Teórico Ajustado”, el cual presenta la misma estructura que el PMT ya calculado, no
obstante, a su componente de energía, en cada punto de suministro, se debe adicionar o sustraer
un valor único y constante, de modo que el Precio Medio Teórico Ajustado alcance el límite más
próximo, superior o inferior, de la banda de precios de mercado.  El resultado es presentado en la
Tabla 7.
Tabla 7: Comparación Precio Medio Teórico Ajustado – Precio Medio de Mercado
Precio Medio Teórico Ajustado SEN
Precio Medio Teórico Ajustado [$/kWh] 86,688
Precio Medio de Mercado [$/kWh] 106,496
Diferencia (%)6 -18,6%
Como resultado del proceso anterior, para efectos de determinar los precios estabilizados, el valor
que se debe adicionar a la componente de energía corresponde a 24,610 [$/kWh], con el fin de
alcanzar el límite más próximo de la Banda de Precios de Mercado. En virtud de lo anterior, y de
acuerdo con lo establecido en el inciso final artículo 25° del DS 88/2020, los precios estabilizados se
calcularon como los Precios Básicos de Energía por intervalo temporal adicionando un valor igual a
24,610 [$/kWh].

6 Diferencias en el cálculo se deben a aproximaciones por redondeo.

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
PARINACOTA 220 128,842 101,763 27,159 24,611 67,905 150,759
POZO ALMONTE 220 125,094 99,593 27,503 24,611 66,662 146,564
CONDORES 220 125,736 99,527 27,291 24,612 66,895 147,145
TARAPACA 220 123,391 97,912 27,248 24,611 65,321 145,465
LAGUNAS 220 122,600 97,351 27,232 24,611 64,999 144,447
NUEVA VICTORIA 220 122,099 96,992 27,170 24,611 64,811 143,809
CRUCERO 220 117,615 93,255 28,138 24,612 63,973 138,141
ENCUENTRO 220 118,765 95,284 28,060 24,612 64,422 138,581
CHUQUICAMATA 220 120,023 95,995 28,191 24,613 64,689 140,546
CALAMA 220 118,777 94,530 27,820 24,612 66,793 139,713
EL TESORO 220 121,709 95,574 27,834 24,612 64,735 141,113
ESPERANZA SING 220 121,689 95,564 27,834 24,612 64,732 141,087
ATACAMA 220 116,915 92,354 27,524 24,612 65,955 138,555
EL COBRE 220 119,018 95,946 27,893 24,612 64,323 138,207
LABERINTO 220 120,350 95,302 27,977 24,612 63,704 138,979
O'HIGGINS 220 120,295 95,216 28,011 24,612 63,594 138,576
D. DE ALMAGRO 220 101,020 84,064 27,837 24,612 61,497 128,723
CARRERA PINTO 220 100,492 83,673 27,839 24,613 61,328 128,022
CARDONES 220 99,975 83,349 27,950 24,613 61,338 127,346
MAITENCILLO 220 97,424 81,226 27,841 24,613 59,934 124,297
PUNTA COLORADA 220 96,865 80,856 27,917 24,620 59,926 123,895
PAN DE AZUCAR 220 97,158 81,408 28,185 24,631 61,076 124,674
LOS VILOS 220 95,468 80,098 28,057 24,673 62,531 122,595
NOGALES 220 88,878 77,280 28,768 24,780 66,215 118,108
QUILLOTA 220 91,300 77,127 28,445 24,727 60,581 119,891
POLPAICO 220 92,649 77,069 28,526 24,747 61,118 120,686
EL LLANO 220 91,641 77,723 28,578 24,744 61,339 119,803
LOS MAQUIS 220 91,515 77,668 28,580 24,744 61,324 119,474
LAMPA 220 94,916 81,289 29,183 24,761 47,795 122,227
CERRO NAVIA 220 86,723 73,761 28,577 24,753 61,028 119,562

<!-- page 18 -->

18

NUDO TENSIÓN
[kV]
PRECIO ESTABILIZADO POR INTERVALO TEMPORAL [$/kWh]
1 2 3 4 5 6
MELIPILLA 220 90,226 77,430 28,779 24,724 57,121 120,991
RAPEL 220 90,021 77,268 28,750 24,721 56,935 120,654
CHENA 220 85,761 73,289 28,589 24,755 60,931 118,775
MAIPO 220 83,227 71,870 28,446 24,747 60,241 116,167
ALTO JAHUEL 220 82,401 71,604 28,547 24,754 60,754 116,007
ITAHUE 220 83,106 73,462 29,385 24,710 50,046 108,410
ANCOA 220 80,932 70,804 28,335 24,725 56,643 105,069
CHARRUA 220 76,812 67,937 28,254 24,752 54,346 100,781
COLBUN 220 80,934 70,805 28,335 24,725 56,645 105,079
CANDELARIA 220 84,610 73,030 28,447 24,731 59,685 114,819
HUALPEN 220 77,868 68,805 29,250 26,253 55,990 102,868
LAGUNILLAS 220 77,539 68,526 29,567 26,809 56,193 102,575
CAUTÍN 220 75,892 68,100 28,489 24,740 53,834 95,355
TEMUCO 220 73,616 65,883 28,420 24,788 52,038 93,515
CIRUELOS 220 63,827 58,098 39,466 38,769 55,585 82,823
VALDIVIA 220 64,303 57,554 39,673 39,245 55,603 83,043
RAHUE 220 61,542 57,965 40,932 40,256 54,926 80,277
PUERTO MONTT 220 61,626 56,275 40,109 39,480 54,222 79,977
MELIPULLI 220 61,627 56,276 40,110 39,480 54,223 79,979
CHILOE 220 62,731 57,462 40,878 40,165 54,445 81,086
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
𝑃𝑟𝑒𝑐𝑖𝑜 𝑏𝑎𝑠𝑒𝑡: Precio estabilizado base de energía del nodo, para el intervalo temporal t,
correspondiente a los indicados en la Tabla 8, del subcapítulo 3.3.

<!-- page 19 -->

19

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
