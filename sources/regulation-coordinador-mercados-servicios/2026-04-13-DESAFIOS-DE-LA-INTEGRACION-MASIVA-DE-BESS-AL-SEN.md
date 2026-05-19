---
pdf_source: sources/regulation-coordinador-mercados-servicios/2026-04-13-DESAFIOS-DE-LA-INTEGRACION-MASIVA-DE-BESS-AL-SEN.pdf
pdf_sha256: 7b4e7e9f876ccd3601ba6344152f22d7e9e12af24389bd35eb1ccc49d5e30486
pdf_pages: 12
extracted_pages: 11
extracted_chars: 6549
extracted_at: 2026-05-19T13:22:48Z
extractor: pypdf
---

# 2026 04 13 DESAFIOS DE LA INTEGRACION MASIVA DE BESS AL SEN

<!-- page 1 -->

Abril, 2026
Desafíos de la Integración
Masiva de BESS al Sistema Eléctrico
Nacional y la Fortaleza de Red
Víctor Velar
Subgerente de Estudios y Simulación en Tiempo Real
Coordinador Eléctrico Nacional (CEN) - Chile

<!-- page 2 -->

Generación BESS
Se acerca a los 2
GW
Al 2026 se estiman
~4.3 GW BESS en EO
(entrada en
operación)+ PES
(Puesta en servicio)
Al 2031 se estiman más de 8 GW BESS
Contexto Sistema Eléctrico Nacional
Long-term RE
Goals:
 Carbon
Neutrality by 2050
 Decarbonization
by 2035
 100% RE by
2030 (85% VRE)

<!-- page 3 -->

Contexto Sistema Eléctrico Nacional
Transición Acelerada  Se altera radicalmente la dinámica física del sistema eléctrico

<!-- page 4 -->

Despliegue masivo de BESS
Energía
Arbitraje · gestión de vertimiento →
optimización del uso de la energía disponible
en el sistema.
Flexibilidad
Rampas rápidas → servicios operacionales →
soporte a la operación del sistema en tiempo
real.
Rol sistémico
Control del convertidor → influencia directa
en la respuesta dinámica del SEN → rol activo.
Utility Scale: el BESS pasa a ser parte relevante de la dinámica
del sistema
BESS pequeño → efecto despreciable.
BESS utility-scale → control + modelo + validación + atributos GFL/GFM
pasan a ser parte fundamental de la operación segura del SEN.

<!-- page 5 -->

Despliegue masivo de BESS – CEN+Industria - CNE

<!-- page 6 -->

Qué se entiende por fortaleza de red
Propiedad del sistema eléctrico  capacidad de mantener tensiones y frecuencias estables ante
perturbaciones  determinada principalmente por el nivel de cortocircuito sincrónico disponible
(robustez de tensión) y por la inercia sistémica (robustez de frecuencia).

<!-- page 7 -->

Desafío técnico de la integración masiva de BESS
Más BESS → más exigencia técnica al sistema
Menor inercia
Cada MW BESS
reemplazando sincrónica →
reducción de la inercia
equivalente del sistema.
SCR más bajo
BESS concentrados +
sincrónicas fuera de
despacho → SCR reducido en
nodos críticos del norte.
Interacciones IBR
Múltiples IBR en el mismo
nodo → posibles
interacciones de control →
amplificación de oscilaciones.
Implicancia para el pipeline actual de proyectos
~4 GW BESS en tramitación + conexión sin validación adecuada → posible agravamiento de condiciones de fortaleza de red ya
degradadas → posible riesgo sistémico identificado por el CEN.
Ya existe marco normativo para afrontar este desafío
Nuevas métricas
¿Cómo definimos nuevas
métricas que den real cuenta
de la contribución de los
BESS GFM? La Skss puede
subestimar al GFM.

<!-- page 8 -->

Exigencias NTSyCS actualizada - AT IBR para GFM
Naturaleza del Control — lo que define una IBR GFM
Art. 3-1.a
Regula de forma autónoma el fasor de tensión y la
frecuencia en el Punto de Conexión al SI — sin requerir
apoyo de otras unidades generadoras sincrónicas ni
otras IBR GFM.
Art. 3-1.b
Mantiene su Fuente Interna de Voltaje (FIV)
predominantemente constante en el Régimen
Transitorio, controlando el sincronismo y la potencia
activa y reactiva.
Art. 3-1.c
Energía disponible de forma instantánea para el SI —
Tiempo de Reacción < 10 ms; Tiempo de
Establecimiento < 20 ms (valor referencial según
disponibilidad tecnológica, Oficio CNE N°337/2026).
Autonomía y Operación en Isla Eléctrica
Art. 3-1.f /
3-3.a
Opera de manera estable en Red Débil. El Controlador
de Tensión es autónomo: mantiene la tensión dentro
de los límites de la NTSyCS sin apoyo externo.
Art. 3-10
Capacidad de operar en Isla Eléctrica — obligatoria para
todas las IBR GFM. Debe mantener operación estable
junto con otras IBR GFM o GFL, en ausencia de
generación sincrónica.
Art. 3-1.d /
Art. 3-5
Capacidad de sobrecorriente ≥ 1,3 p.u. por 5 s
(exigencia de diseño del PCS). Debe inyectar corriente
de secuencia negativa ante fallas asimétricas para
propender a tensión balanceada.

<!-- page 9 -->

Exigencias NTSyCS actualizada - AT IBR para GFM
Respuestas Dinámicas Características
Art. 3-7
Inercia Sintética: entrega o reduce potencia activa de
forma instantánea (T. Reacción < 10 ms) sin necesidad
de medición de frecuencia, contribuyendo a reducir el
RoCoF del SI.
Art. 3-8
Control activo de Salto de Fase (Potencia por Salto de
Fase): respuesta instantánea; ángulo máximo de salto
de fase ≥ 30° con respuesta lineal y controlada.
Art. 3-9
Amortiguamiento de Oscilaciones Subsíncronas
(Potencia de Amortiguamiento) entre 0,05 Hz y 1 Hz;
ajustable por software sin introducir nuevos modos
oscilatorios inestables.
Interconexión de Sistemas de Almacenamiento (BESS / CRCA)
Art. 3-12
Todo Sistema de Almacenamiento de Energía que se
interconecte al SEN deberá cumplir con ser una IBR
GFM. Lo mismo aplica para la componente de
almacenamiento de una CRCA.
Art. 7-2
En construcción al 3/02/2026 con EO hasta el
3/08/2026: exentos automáticamente del Título 3. Con
EO posterior al 3/08/2026: obligados a cumplir Título 3
completo.
Art. 7-4 /
Oficio 337
Entrega de modelo EMT validado requerida antes de la
Entrada en Operación para obras con EO a partir del 3
de agosto de 2026, conforme al Título 5 del AT IBR.

<!-- page 10 -->

Validación para conexión de GFM BESS
De la especificación a la evidencia - Coordinador
① Capa HIL-EMT
Pérdida última sincrónica
RoCoF → rampas 4 Hz/s
SCR step-down 20 → 1.25
Saltos de fase ±10° · ±30° · ±60°
Impedance scan 0.05–1000 Hz
② Pruebas en terreno
Operación en Isla (apertura breaker PCC)
Sincronización al retornar a red
Black start (si fue declarado)
Monitoreo constante diferentes condiciones
de Fortaleza; respuesta a eventos o
perturbaciones reales
③ Emulador AC (opcional)
RoCoF e inercia virtual
Saltos de fase en terreno
Amortiguamiento armónico
Sobre y subtensión
Prácticamente ningún ISO lo exige (Costos)

<!-- page 11 -->

① BESS no es solo energía
almacenada
Sistema dominado por IBR → el convertidor
del BESS es tan relevante como la batería →
control + modo de operación + modelo
validado forman parte del activo técnico del
sistema.
② GFM es una decisión de diseño
NT 2026 → capacidad GFM obligatoria para
nuevos BESS → el valor está en los servicios
sistémicos habilitados, no solo en el
cumplimiento normativo.
③ La validación cierra el ciclo
Declaración de atributos → necesaria pero no
suficiente. AT IBR → modelo EMT validado +
HIL completado + desempeño en terreno
coherente = evidencia requerida.
El despliegue masivo de BESS GFM en Chile es una realidad
 NT 2026 vigente actualizada para IBR
 ~4 GW BESS en tramitación
 Pilotos en marcha del CEN con la Industria desde hace 3
años
 CEN activo en especificaciones · estudios · validación ·
operación.
Resumen y mensaje final
Condiciones dadas para afrontar
con éxito el desafío de la
integración masiva de BESS 
Acciones deben estar en marcha
ahora mismo.

<!-- page 12 -->
