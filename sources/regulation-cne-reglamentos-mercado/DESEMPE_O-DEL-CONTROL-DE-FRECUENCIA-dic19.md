---
pdf_source: sources/regulation-cne-reglamentos-mercado/DESEMPE_O-DEL-CONTROL-DE-FRECUENCIA-dic19.pdf
pdf_sha256: 9a937f9ae4c052ed91cbd2844779d276f85947511c984c09449eded839e2e09a
pdf_pages: 6
extracted_pages: 6
extracted_chars: 7784
extracted_at: 2026-05-19T13:22:08Z
extractor: pypdf
---

# DESEMPE O DEL CONTROL DE FRECUENCIA dic19

<!-- page 1 -->

ANEXO TÉCNICO:

Desempeño del Control de
Frecuencia

<!-- page 2 -->

ANEXO TÉCNICO: DESEMPEÑO DEL CONTROL DE FRECUENCIA
COMISIÓN NACIONAL DE ENERGÍA

2 de 6
TÍTULO I. ASPECTOS GENERALES
Artículo 1 Objetivo

El objetivo del presente Anexo Técnico es definir la metodología para calcular el Factor de
Eficiencia del Control de Frecuencia (FECF) que permite evaluar el desempeño del Control de
Frecuencia del SI, de acuerdo a lo señalado en el TÍTULO 5-13 de la presente Norma.

Artículo 2 Obligaciones

En la operación real, el Coordinador debe evaluar el desempeño del Control de Frecuencia del
SI calculando para cada hora el valor del FECF de acuerdo con lo estipulado en el Artículo 5-
62 de la presente Norma.

Artículo 3 Periodicidad de la Evaluación

La evaluación de desempeño del Control de Frecuencia del SI será efectuada en períodos
mensuales denominados períodos de evaluación, de acuerdo con lo estipulado en el Artículo
5-70 de la presente Norma.

El Coordinador deberá publicar dichos cálculos en su sitio Web, a más tardar el día 10 de cada
mes, de acuerdo con lo estipulado en el Artículo 5-71 de la presente Norma.

Artículo 4 Medición de la frecuencia

Las medidas de frecuencia se obtendrán de las mediciones disponibles en el Sistema de
Información en Tiempo Real (SITR), según lo dispuesto en inciso segundo del Artículo 5-70 de
la presente Norma.

<!-- page 3 -->

ANEXO TÉCNICO: DESEMPEÑO DEL CONTROL DE FRECUENCIA
COMISIÓN NACIONAL DE ENERGÍA

3 de 6
TÍTULO II. METODOLOGÍA DE CÁLCULO DE FECF
Artículo 5 Cálculo del FECF

El FECF para cada hora “k” se define a través de la siguiente expresión de acuerdo con lo
estipulado en el Artículo 5-62 de la presente Norma:
    ( )   |
 ( )
     ( )|
Donde,


 ( ): corresponde a la desviación máxima instantánea del valor filtrado de
medición de la frecuencia.
      ( ): corresponde a la desviación máxima de frecuencia en estado permanente
que agota la totalidad de la reserva asociada al Control Primario de Frecuencia (CPF) y
Control Rápido de Frecuencia (CRF).

Cuando se agota la reserva asociada al CPF y al CRF, la desviación máxima instantánea del
valor filtrado de medición de la frecuencia iguala la desviación máxima de frecuencia en estado
permanente que agota la totalidad de la reserva asociada al CPF y al CRF por lo tanto, el
FECF será nulo. En cambio, cuando la desviación filtrada de la frecuencia coincide con la
frecuencia nominal el FECF será igual a uno.

Artículo 6 Cálculo de la desviación máxima instantánea del valor filtrad o de
medición de la frecuencia

El método de cálculo de la desviación máxima instantánea del valor filtrado de medición de la
frecuencia, según lo establece el Artículo 5-68 de la presente Norma es el siguiente:

Para cada hora “k” se realiza la medición de la frecuencia con un intervalo de muestreo de 10
segundos.

Para cada intervalo de muestreo denominado “i” se determina el valor filtrado de la frecuencia
mediante un filtro digital de promedio móvil de 6 minutos, de acuerdo a la siguiente expresión:
           ∑


Para cada intervalo “i” se determina el valor absoluto resultante de la desviación filtrada de la
frecuencia, respecto a la frecuencia nominal (50 Hz) de acuerdo a la siguiente expresión:


Para cada hora “k” se determina la desviación máxima instantánea del valor fil trado de
medición de la frecuencia como el promedio de los valores absolutos resultantes de las
desviaciones filtradas de la frecuencia, de acuerdo a la siguiente expresión:

<!-- page 4 -->

ANEXO TÉCNICO: DESEMPEÑO DEL CONTROL DE FRECUENCIA
COMISIÓN NACIONAL DE ENERGÍA

4 de 6

  (   )
 ( ) ∑


   ⁄

Artículo 7 Cálculo de la desviación de frecuencia en estado permanente que
agota la totalidad de la reserva asociada al CPF y al CRF

Se debe calcular el valor de la desviación de frecuencia en estado permanente que agota la
totalidad de la reserva asociada al CPF y al CRF como el promedio de los valores obtenidos
cada 5 minutos
     ( ) ∑

(
( ))

(   )
  ⁄

Donde,


( ) : corresponde la desviación de frecuencia individual que agota la reserva
para CPF y al CRF correspondiente a la instalación “n”, en el intervalo de tiempo “i”.
  : número de instalaciones presentes en el despacho.

Dado que en régimen permanente la frecuencia en todas las barras del SI es
aproximadamente la misma y la reserva para el CPF y CRF se agota cuando todas las
instalaciones han consumido su reserva para el CPF y CRF individual, se requiere examinar
los valores individuales de desviación de frecuencia que agotan la reserva de cada una de las
instalaciones que participan en la regulación de frecuencia y que cuentan con reserva en giro.
Luego, se debe seleccionar la máxima desviación de frecuencia individual para calcular el valor
de la desviación máxima de frecuencia en estado permanente que agota la totalidad de la
reserva asociada al CPF y CRF.

El proceso de análisis individual requiere considerar las características potencia - velocidad
estáticas del algoritmo de control incorporado en cada regulador de velocidad de las
instalaciones que participan en el CPF y CRF. Para estas unidades se pueden identificar dos
características típicas asociadas a la banda muerta (Ver Figura 1).

Para cada caso (Ver Figura 1. a y Figura 1.b) es posible determinar la desviación de frecuencia
individual de cada instalación que agota su reserva para el CPF y CRF (igual al valor de
reserva para CPF y CRF del mes en el cual se calcula el índice ), evaluando la  reserva
disponible para el CPF y CRF de cada instalación en su respectiva característica potencia-
velocidad estática, tal como lo indica la Figura 1.a y Figura 1.b.

La Figura 1 muestra, de manera gráfica y algebraica, el proceso descrito previamente para
determinar la máxima desviación de frecuencia individual que agota la reserva para el CPF y
CRF de la respectiva instalación.

<!-- page 5 -->

ANEXO TÉCNICO: DESEMPEÑO DEL CONTROL DE FRECUENCIA
COMISIÓN NACIONAL DE ENERGÍA

5 de 6

Figura 1: Características típicas de banda muerta

Donde,
    : corresponde a la banda muerta de la instalación i en [Hz].
   : corresponde al estatismo porcentual de la instalación i, en base propia respecto de
la potencia activa nominal de la unidad.
         : corresponde a la consigna de frecuencia de operación del SI, igual a 50 [Hz].
     : corresponde al valor máximo de capacidad de reserva para CPF y CRF de la
instalación i en [MW].
     : corresponde a la potencia activa nominal de la instalación i.

<!-- page 6 -->

ANEXO TÉCNICO: DESEMPEÑO DEL CONTROL DE FRECUENCIA
COMISIÓN NACIONAL DE ENERGÍA

6 de 6
TÍTULO III. INFORMACIÓN A LOS COORDINADOS
Artículo 8 Información a los coordinados

El Coordinador deberá informar trimestralmente a los Coordinados:

a) Todas las instalaciones que puedan participan en el CPF y/o CRF en el SI, de acuerdo
a la normativa que corresponda,  junto con sus respectivas potencias máximas
consideradas para el cálculo de la desviación máxima de frecuencia en estado
permanente que agota la reserva para CPF y CRF correspondiente a la unidad n.

b) El valor mínimo del FECF, el cual, de acuerdo con lo establecido en el Artículo 5-69 de
la presente Norma, no debe ser menor que 0.45.

c) El valor de la desviación máxima de frecuencia en estado permanente que agota la
totalidad de la reserva asociada al CPF y CRF.

Artículo 9 Publicación de Resultados

Para efectos de los cálculos estadísticos que se deberán realizar mensualmente conforme lo
establece la presente Norma, el Coordinador deberá publicar los valores horarios calculados
del factor FECF en su sitio Web, a más tardar el día 10 de cada mes.
