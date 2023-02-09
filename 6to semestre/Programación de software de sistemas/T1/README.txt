==========================================================
Esta es la documentación para compilar y ejecutar su tarea
==========================================================

Se está ejecutando el comando: less README.txt

***************************
*** Para salir: tecla q ***
***************************

Para avanzar a una nueva página: tecla <page down>
Para retroceder a la página anterior: tecla <page up>
Para avanzar una sola línea: tecla <enter>
Para buscar un texto: tecla / seguido del texto (/...texto...)
         por ejemplo: /ddd

-----------------------------------------------

Ud. debe crear el archivo borrar-bits.c y programar ahí la función buscar.
Ya hay una plantilla para borrar-bits.c en borrar-bits.c.plantilla.

Pruebe su tarea bajo Debian 11 de 64 bits nativo o virtualizado.  Quedan
excluidos WSL 1 y WSL 2 para hacer las pruebas.  Estos son los requerimientos
para aprobar su tarea:

+ make run-san debe felicitarlo.
+ make run-g debe felicitarlo.
+ make run debe felicitarlo por aprobar este modo de ejecución.  Esta
  prueba será rechazada si su solución es 80% más lenta que la solución
  del profesor.

Cuando pruebe su tarea con make run en su computador asegúrese de que
que está configurado en modo alto rendimiento y que no estén corriendo
otros procesos intensivos en uso de CPU al mismo tiempo.  De otro modo
podría no lograr la eficiencia solicitado.

Invoque el comando make zip para ejecutar todos los tests y generar un
archivo borrar-bits.zip que contiene borrar-bits.c, con su solución,
y resultados.txt, con la salida de make run, make run-g y make run-san.

Para depurar use: make ddd

Video con ejemplos de uso de ddd: https://youtu.be/FtHZy7UkTT4
Archivos con los ejemplos: https://www.u-cursos.cl/ingenieria/2020/2/CC3301/1/novedades/r/demo-ddd.zip

-----------------------------------------------

Entrega de la tarea

Ejecute: make zip

Entregue por U-cursos el archivo borrar-bits.zip

A continuación es muy importante que descargue de U-cursos el mismo
archivo que subió.  Luego examine el archivo borrar-bits.c revisando
que es el correcto.  Es frecuente que no lo sea producto de un defecto
de U-cursos.

-----------------------------------------------

Limpieza de archivos

make clean

Hace limpieza borrando todos los archivos que se pueden volver
a reconstruir a partir de los fuentes: *.o binarios etc.

-----------------------------------------------

Acerca del comando make

El comando make sirve para automatizar el proceso de compilación asegurando
recompilar el archivo binario ejecutable cuando cambió uno de los archivos
fuentes de los cuales depende.

A veces es útil usar make con la opción -n para que solo muestre
exactamente qué comandos va a ejecutar, sin ejecutarlos de verdad.
Por ejemplo:

   make -n ddd

También es útil usar make con la opción -B para forzar la recompilación
de los fuentes a pesar de que no han cambiado desde la última compilación.
Por ejemplo:

   make -B run
