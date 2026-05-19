---
pdf_source: sources/regulation-coordinador-reportes-estadisticas/CEN-Manual-de-Usuarios-Finales-v2.3.pdf
pdf_sha256: 48bcfd6ec837e31fca07e3c7abf1e42b533016af2376502777ad9fac110870ee
pdf_pages: 22
extracted_pages: 22
extracted_chars: 8634
extracted_at: 2026-05-19T13:23:06Z
extractor: pypdf
---

# CEN Manual de Usuarios Finales v2.3

<!-- page 1 -->

https://hub.coordinador.cl/ne
MANUAL DE USUARIO

INGRESO UNIFICADO A APLICATIVOS
DEL COORDINADOR
Diciembre 2020

<!-- page 2 -->

Ingreso Unificado a Aplicativos del Coordinador


Página 2 de 22

1. Tabla de Contenidos

1. Tabla de Contenidos 2
2. Resumen Ejecutivo 3
3. Glosario 3
4. Inicio de sesión en el Hub de Aplicaciones 3
5. Acceso a una aplicación y SSO (Single-Sign-On) 6
6. Cierre de sesión 7
7. Reingreso a aplicativo integrado (Cambio de contraseña de una aplicación) 9
8. Necesita cambiar su Contraseña 10
9. Recuperación de contraseña de NAM 17

<!-- page 3 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 3 de 22

2. Resumen Ejecutivo
El presente documento detalla cómo es la interacción entre el usuario final, y la plataforma de
autenticación centralizada basada en Micro Focus Access Manager.

El objetivo principal es presentar en detalle, los distintos escenarios por los cuales un usu ario
puede transitar cuando utilice Access Manager para acceder a sus aplicaciones habituales de
trabajo.


3. Glosario
SSO: Single-Sign-On es un mecanismo de autenticación que permite al usuario acceder a varios
sistemas con una única instancia de identificación.

NAM: NetIQ Access Manager es una solución para el control y gestión de los accesos a distintos
recursos web a través de un proxy reverso facilitando SSO.

AppMark: Es la contracción de “Application Marks”. Se denomina así al portal de SSO visto por
los usuarios luego de ser autenticados. Contiene marcadores de acceso rápido que permiten el
ingreso de los usuarios a las aplicaciones.

Self Service Password Reset (SSPR):   Es una solución de gestión de contraseñas basada en
tecnologías web. Elimina la dependencia de los usuarios de la asistencia de los administradores o
mesa de ayuda para cambiar las contraseñas. Permite asegurar que todas las contraseñas de la
organización cumplan con las políticas de mejores prácticas establecidas. Los usuarios pueden
almacenar respuestas a preguntas de seguridad para luego cambiar o restablecer su contraseña
utilizando la información de respuesta a la pregunta de seguridad configurada.

4. Inicio de sesión en el Hub de Aplicaciones
Usted podrá acceder a la nueva interfaz de inicio de sesión centralizada desde el siguiente
enlace  https://hub.coordinador.cl/ donde se deberán completar las credenciales
correspondientes. En el caso colaboradores del Coordinador utilizaran su clave del Dominio
@coordinador.cl. Para los usuarios coordinados deberán activar su cuenta por primera vez e
ingresar a través del siguiente enlace https://sspr.coordinador.cl/sspr/public/activate
y ahí debe seguir los pasos para activar su cuenta la primera vez y podrán definir su password.

<!-- page 4 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 4 de 22


Si las credenciales ingresadas no son correctas, se visualizará el siguiente mensaje.


Una vez que se ingrese correctamente, se verán los recursos a los cuales se tiene acceso.

<!-- page 5 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 5 de 22


En el margen superior derecho de la pantalla, se observa el nombre de la cuenta con la cual se
ingresó. Al seleccionarla, se despliega la siguiente lista.


Desde aquí se puede cerrar la sesión al seleccionar “Salir”; o modificar el tamaño y modo de
visualización de los iconos de los recursos y aplicaciones.

En la parte central de la pantalla, se muestran todas las aplicaciones y recursos a los cuales usted
tiene acceso, por ejemplo:

<!-- page 6 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 6 de 22


5. Acceso a una aplicación y SSO (Single-Sign-On)
En este ejemplo, se pretende ingresar a la aplicación “SIREP” seleccionando el icono
correspondiente.


Al hacerle clic se abrirá otra pestaña en el navegador, donde observará la página de ingreso al
aplicativo SIREP y deberá completar las credenciales correspondientes para ingresar.

<!-- page 7 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 7 de 22


Una vez dentro del aplicativo, en el margen superior derecho de la pantalla principal, se observa
el nombre de la cuenta con la cual se ingresó.

*Nota:
Este proceso de ingreso por primera vez al aplicativo fue detectado por Access Manager (NAM)
para guardar las credenciales y poder ingresar automáticamente en futuras oportunidades. Es decir,
en los posteriores ingresos en este caso a SIREP, no será nece sario ingresar las credenciales; ya
que realizará SSO.

6. Cierre de sesión
El cierre de sesión en Access Manager (NAM) se puede realizar de dos formas:

1. Utilizar la opción de “Salir” desde el AppMark de NAM:

<!-- page 8 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 8 de 22


2. Desde cualquier aplicación abierta , al cerrar sesión de la aplicación, también se cierra la
sesión de NAM. Al cerrar sesión desde SIREP, por ejemplo.

<!-- page 9 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 9 de 22


7. Reingreso a aplicativo integrado (Cambio de contraseña de una aplicación)
Cuando se realiza el cambio de contraseña desde una aplicación, a la cual se accede desde el
AppMark; este cambio es registrado por NAM para garantizar el SSO del usuario a dicha aplicación.

Si se ingresa al cambio de contraseña de una aplicación, en este caso “REUC”, y se realiza dicha
acción.

<!-- page 10 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 10 de 22


Este proceso es dete ctado por NAM y registra el cambio, para garantizar el SSO a dicha
aplicación. Por lo cual, al ingresar nuevamente a “REUC” desde el Appmark, obtenemos el acceso
directamente.


8. Necesita cambiar su Contraseña
El acceso a la aplicación SSPR, está disponible en el Appmark de l HUB de aplicaciones, luego
del ingreso exitoso por la interfaz de inicio de sesión centralizada desde el siguiente
enlace  https://hub.coordinador.cl/

<!-- page 11 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 11 de 22


Al hacerle clic se abrirá otra pestaña en el navegador, donde se carga la página de ingreso al
aplicativo SSPR y deberá completar las credenciales correspondientes para ingresar.

<!-- page 12 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 12 de 22

<!-- page 13 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 13 de 22

<!-- page 14 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 14 de 22


Cuando el cambio de contraseña es exitoso y cada vez que cambie la contraseña, llegara una
notificación de seguridad del cambio de contraseña.


Otra forma de poder recuperar su contraseña  es previamente configurar sus preguntas de
seguridad.

<!-- page 15 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 15 de 22


Acá, puede seleccionar “Guardar respuestas” para corregir las preguntas y respuestas; o puede
seleccionar “Confirmar respuestas de seguridad” para guardarlas. Cuando confirma, SSPR muestra
el siguiente mensaje:


*Nota:

<!-- page 16 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 16 de 22

Estas preguntas y respuestas son utilizadas por el aplicativo cuando un usuario requiera el servicio
de recuperar contraseña.

Al seleccionar “Continuar”, SSPR carga la página del Appmark de NAM.


En los próximos ingreso s al SSPR, no será necesario cargar las credenciales, ni cargar las
preguntas de desafío; y el aplicativo mostrará su página principal.

<!-- page 17 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 17 de 22

9. Recuperación de contraseña de NAM
Este proceso se realiza con el aplicativo SSPR, y se accede al mismo a través del link “Recuperar
contraseña” en la página de ingreso centralizada.


Al seleccionarlo, se abre una ventana, donde se solicita ingresar el nombre de usuario:


Sí el nombre del usuario ingresado es incorrecto, SSPR muestra el siguiente error:

<!-- page 18 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 18 de 22


Cuando el nombre se ingresa correctamente, SSPR solicita que complete unas preguntas de
desafío o recuperar su contraseña a través de su correo electrónico, para validar su identidad:


*Nota:
Estas preguntas de desafío deben ser completadas por cada usuario, en el primer inicio de sesión
en SSPR.

<!-- page 19 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 19 de 22


La segunda opción es recuperar su contraseña a través de su correo electrónico


Al continuar le llegará una confirmación a su correo electrónico junto un código de verificación

<!-- page 20 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 20 de 22

<!-- page 21 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 21 de 22


Después de seleccionar “Cambiar Contraseña”

<!-- page 22 -->

Ingreso Unificado a Aplicativos del Coordinador

 Página 22 de 22
