---
pdf_source: sources/regulation-coordinador-mercados-servicios/2026-04-16-CONTROL-DINAMICO-DE-TENSION.pdf
pdf_sha256: 729db585540916e94cf95e049393bb96206b1ad877a12d46612dd9893316fda3
pdf_pages: 17
extracted_pages: 17
extracted_chars: 8436
extracted_at: 2026-05-19T13:22:50Z
extractor: pypdf
---

# 2026 04 16 CONTROL DINAMICO DE TENSION

<!-- page 1 -->

PRESENTACIÓN
Control dinámico de tensión en
parques eólicos, solares y BESS
Eugenio Quintana
Jefe del Departamento Estudios Eléctricos
16 de abril de 2026

<!-- page 2 -->

Presentar:
✓El plan de instrucciones de Control Dinámico de Tensión (CDT)
✓El criterio de selección de plantas
✓El protocolo de instrucciones de CDT
✓Los resultados observados a la fecha
OBJETIVO

<!-- page 3 -->

TEMARIO
1. Contexto
2. Capacidad de CPF y CDT en plantas IBR
3. Propuesta de estándar CDT IBR y
comparación con AT-IBR (NTSyCS)
4. Ranking y priorización
5. Plan de instrucciones
6. Protocolo y resultados preliminares
7. Conclusiones

<!-- page 4 -->

CONTEXTO: CDT ERV Y BESS
Plan de instrucciones de
CDT por seguridad
rapidez suficiente
zonas críticas
tamaño relevante
Medidas del apagón
25F
Inclusión de IBR en
SSCC de CF y CT
Evaluación técnica
Capacidad de CPF y CDT
en 107 parques IBR
Estándar de CDT para
contener sobretensiones

<!-- page 5 -->

CONTEXTO: PROBLEMA Y SOLUCIÓN
Problema que se
quiere resolver:
En un escenario de baja demanda diurna una
operación del EDAC puede producir
sobretensiones transitorias mayores a 1,1 [pu]* en
barras críticas y durante varios segundos
Pueden actuar las protecciones de sobretensión
de plantas IBR, empeorando la caída de
frecuencia
Esta salida de generación también afecta la
tensión, empeorando el problema.
Propuesta:
Identificar recursos de CDT
adecuados ya disponibles en
parques IBR
Diseñar un plan para
disponer de estos recursos
necesarios
Evitar introducir oscilaciones
o conflictos con otros
controles.
* Art. 3-1 AT IBR y Cap. 7.2.2.1 IEEE 2800-2022

<!-- page 6 -->

• Se evaluó la capacidad de CT y CF de
107 PE, PFV y BESS usando sus
modelos dinámicos homologados en
PowerFactory.
• Estos modelos se consolidaron en un
banco de pruebas y se homologaron las
condiciones en el punto de conexión
(SCR).
• Se activaba el CPF y se aplicaba una
señal de sobre y subfrecuencia.
• Se activaban los modos Q/V/FP y se
aplicaba un escalón de la variable de
control.
CAPACIDAD DE CPF Y CDT EN PLANTAS IBR
Para cada modo se
calculó:
reacción
crecimiento
estabilización
sobreoscilación
amortiguamiento
estatismo

<!-- page 7 -->

PROPUESTA DE ESTÁNDAR CDT IBR
Parámetro Propuesta
Coordinador *
Art. 4-3 AT IBR /
NTSyCS feb-2026
Observación
Tiempo de
reacción
≤ 200 ms < 200 ms Prácticamente igual.
Tiempo de
crecimiento
≤ 2,5 s < 1,0 s La propuesta es menos exigente en subida inicial.
Tiempo de
establecimiento
≤ 3,5 s < 5,0 s La propuesta es más exigente en tiempo de
establecimiento.
Oscilación /
amortiguamiento
ζ ≥ 70% Sobreoscilación ≤ 5% La métrica es distinta para ajustarse a definición
del estándar IEEE-2800.
Estatismo
recomendado
2%–7% según barra
y necesidad zonal
2%–10% ajustable Se acota el rango para mayor utilidad y referido a
Qmax.
Compromiso entre rapidez, necesidad del sistema y disponibilidad de los
recursos considerando una performance dinámica sistémica similar
* Tiempos para el SCRmin

<!-- page 8 -->

PROPUESTA DE ESTÁNDAR CDT IBR
1. Se simuló en un escenario de demanda
baja diurna la pérdida intempestiva de
2500 MW de generación sincrónica.
2. Se modeló el EDAC con un monto del
25% y del 30% de la demanda bruta
total.
3. Se activó el CDT en un conjunto de 16
parques totalizando 1530 MVA.
4. Se obtuvo un comportamiento estable y
sin sobretensiones.
Tensión máx. se da a ~ 4 s desde el evento

<!-- page 9 -->

INSTRUCCIÓN DIRECTA DE SC CT
1. Plantas verificadas para SC de CT - individual
• Se inició con las instrucciones directas individuales de CDT de
6 parques que ya estaban verificados para el SC de CT y que
tenían una rapidez suficiente.
• Esto permitió avanzar con menor incertidumbre porque ya
existe un precedente técnico de pruebas adicionales a la
validación del modelo.
Planta Zona Coordinado
PV Malgarida Norte
Chico
Acciona Energía
Chile Holdings S.A.
PE Tolpán sur Sur Acciona Energía
Chile Holdings S.A.
PF Usya Norte
Grande
Acciona Energía
Chile Holdings S.A.
PFV Andes Solar II Norte
Grande AES Andes S.A.
PE San Matías Sur AES Andes S.A.
PE Calama Norte
Grande
Engie Energía Chile
S.A.
2. Plantas verificadas para SC de CT - conjunto
• La segunda etapa consistió en habilitar el CDT en todos los
parques del Norte Grande y del Sur simultáneamente.
• En el caso de PFV Malgarida se evalúo la prestación
simultánea de CDT y CF .

<!-- page 10 -->

RANKING Y PRIORIZACIÓN PARA INSTRUCCIÓN POR SEGURIDAD
37
plantas
4,7 GW
potencia
total
Criterios de ordenamiento
1)Mayor rapidez primero
2)Mayor tamaño primero
3)Zonas Norte Grande y Sur priorizadas
Distribución por zona
Norte
Grande
18 | 2,26 GW
Sur 7 | 0,86 GW
Otro 12 | 1,60 GW
Las zonas Norte Grande y Sur concentran gran parte de las plantas seleccionadas.
Plantas no verificadas para SC de CT
pero que cumple criterios
Se aplicará el mismo esquema anterior a los parques
IBR que cumplan con los siguiente criterios.

<!-- page 11 -->

PLAN: ESQUEMA DE INSTRUCCIÓN DE CDT POR SEGURIDAD
Fase 1 | Individual
• Instrucción de CDT por
seguridad en plantas con
respuesta ad hoc.
• Objetivo: comprobar
efectividad del control,
márgenes de Q y
comportamiento estable en
tiempo real.
Fase 2 | Conjunta entre
plantas
• Instrucciones de CDT por
seguridad en parques de una
misma zona.
• Objetivo: revisar interacción,
reparto de reactivos y
comportamiento agregado.
Fase 3 | Con control de
frecuencia
• Evaluar simultaneidad de
CDT con CPF/CSF y chequear
restricciones.
• Coordinado deberá verificar
la compatibilidad total
revisando documentación de
PPC en cuanto a limitaciones y
prioridad P/Q.

<!-- page 12 -->

PLAN: OTROS ASPECTOS
Aspecto Criterio propuesto Comentario
Quién instruye CDC emite la instrucción y valida su
entendimiento y cumplimiento.
Operadores del CC deben estar preparados.
Registro Toda instrucción y cambio de modo deben
quedar registrado en RIO.
Es la base para análisis posterior.
Tratamiento
económico
Seguir reglas vigentes de instrucciones
directas de SSCC cuando corresponda y,
fuera de ello, reglas de instrucción por
seguridad.
Uso del resultado SCADA/PMU y bitácora alimentan análisis
técnicos.
Instrucciones, registros y análisis quedarán
documentados para referencia futura.

<!-- page 13 -->

PROTOCOLO DE INSTRUCCIÓN
Preparación
CDC valida
señales
SCADA/PMU
Verifica
condiciones
habilitantes: por
ej. sin CPF/CSF
Chequea
disponibilidad
del recurso
primario
Inicio
CDC instruye
encendido de
CDT
Indica Vref en
barra de control
Registra hora y
confirmación
Verifica cambio
efectivo del
control
Ejecución
CDC monitorea
continuamente P ,
Q y V
Supervisa
margen de Q
Solicita cambios
de Vref
Suspensión
Riesgo de
operación de
protecciones
Oscilaciones
sostenidas
Pérdida de
señales
relevantes
Cierre
CDC instruye
retorno a modo
control de
reactivos
Registra todo en
bitácora RIO

<!-- page 14 -->

RESULTADOS PRELIMINARES: PFV MALGARIDA
• Estatismo calculado ≈ 6% en barra 220 kV
• A las 15:00 Bypass de CCSS en S/E Cumbre 500 kV
produce escalones de tensión y se observa que el
comportamiento de Q es coherente con los saltos de V.
• Indicadores ref.:
1. 𝑡_𝑐𝑟𝑒𝑐 <1 s
2. 𝑡_𝑒𝑠𝑡 ~2 s
3. dV/dQ ≈ 0,128 kV/MVAr → estatismo ~6%.

<!-- page 15 -->

✓A partir del análisis de la performance de control de 107 parques, se propone un estándar de
CDT que permita contener sobretensiones transitorias ante caídas de frecuencia que gatillan la
operación del EDAC con los recursos existentes.
✓Considerando los recursos que ya cuentan con un performance adecuado, se busca responder
cómo se disponen para la operación real sin crear nuevos problemas de estabilidad.
✓Se buscar avanzar con una lógica gradual: se partió con las plantas verificadas para el SC de CT
y ahora se darán instrucciones por seguridad con un protocolo único.
✓Se comenzará con instrucciones individuales y luego instrucciones a múltiples plantas y con el
control de frecuencia activo, con trazabilidad CDC–RIO-SCADA–PMU .
✓La viabilidad final depende del cumplimiento de las responsabilidades de cada actor.
CONCLUSIONES

<!-- page 16 -->

GRACIAS

<!-- page 17 -->

PLANTAS SELECCIONADAS
Nombre Nombre Nombre Nombre
PFV Sol del Desierto PE Malleco Sur PE Negrete PE Sierra Gorde Este
PE Cerro Tigre PE Los Olmos PE Atacama PFV Cerro Dominador
PFV Atacama Solar II PE La Cabaña PFV Quilapilún PFV Azabache
PFV Tamaya Solar PE Campo Lindo PFV Sol del Lila PFV Jama
PFV Granja Solar PFV Campos del Sol PFV Huatacondo PFV Uribe Solar
PFV San Pedro PFV Meseta de los Andes PE San Gabriel PFV Finis Terrae
PFV Pampa Tigre PE Alena PE La Flor PFV Valle del Sol
PE Valle de los Vientos PFV La Huella PFV Guanchoi
PE Renaico II PE Lomas de Duqueco PFV Conejo Solar
PE Malleco Norte PE Mesamavida PFV Coya
