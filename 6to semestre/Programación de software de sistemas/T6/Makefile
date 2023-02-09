# Para revisar las opciones de compilacion y ejecucion,
# ingrese en el terminal el comando: make
#
#

PROB=cmp-dir

SHELL=bash -o pipefail

INCLUDE=
CFLAGS=-Wall -Werror -std=c18 $(INCLUDE)
#CFLAGS=-Wall -Werror -pedantic -std=c18 $(INCLUDE)
LDLIBS=-lm

MAK=make --no-print-directory

readme:
	@less README.txt

$(PROB).bin $(PROB).bin-g $(PROB).bin-san: $(PROB).c

run-san: $(PROB).bin-san
	@echo "Test de igualdad"
	./cmp-dir.bin-san dir1/iguales dir2/iguales |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad con muchos directorios"
	./cmp-dir.bin-san dir1/igualesB dir2/igualesB |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenidos distintos"
	./cmp-dir.bin-san dir1/contenidos-distintos dir2/contenidos-distintos |& tee res.out
	@diff res.out res2.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de tamanos distintos"
	./cmp-dir.bin-san dir1/tamanos-distintos dir2/tamanos-distintos |& tee res.out
	@diff res.out res3.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad de archivos binarios grandes"
	cp cmp-dir.bin-san cmp-dir.bin-copy
	./cmp-dir.bin-san cmp-dir.bin-san cmp-dir.bin-copy |& tee res.out
	@diff res.out res4.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenido distinto de archivos binarios grandes"
	@echo "(difieren en el ultimo byte)"
	cp cmp-dir.bin-copy cmp-dir.bin-copy2
	echo a >> cmp-dir.bin-copy
	echo b >> cmp-dir.bin-copy2
	./cmp-dir.bin-san cmp-dir.bin-copy cmp-dir.bin-copy2 |& tee res.out
	@diff res.out res5.ref && echo "Test aprobado"
	rm cmp-dir.bin-copy cmp-dir.bin-copy2
	@echo "----------------------------------------------"
	@echo "Test de no existencia del 2do. archivo"
	./cmp-dir.bin-san dir1/noexiste2 dir2/noexiste2 |& tee res.out
	@diff res.out res6.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de no existencia del 1er. directorio o archivo"
	./cmp-dir.bin-san dir1/noexiste1 dir2/noexiste1 |& tee res.out
	@diff res.out res7.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de inconsistencia de directorios 1"
	./cmp-dir.bin-san dir1/dir-inconsistente dir2/dir-inconsistente |& tee res.out
	@diff res.out res8.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de inconsistencia de directorios 2"
	./cmp-dir.bin-san dir1/dir-inconsistente2 dir2/dir-inconsistente2 |& tee res.out
	@diff res.out res9.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de error: error de lectura en 2do. archivo"
	chmod a-rwx dir2/error-arch/sin-permiso
	@echo ./cmp-dir.bin-san dir1/error-arch dir2/error-arch
	@ ! ./cmp-dir.bin-san dir1/error-arch dir2/error-arch > res.out >& err.out || ( echo "Codigo de retorno es 0, debe ser distinto de 0" ; false )
	@cat err.out
	@diff res.out res10.ref
	@ ! diff err.out err10.ref >& /dev/null || ( echo "Use la funcion perror para explicar el error en la salida estandar de errores" ; false )
	@echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de error: error de lectura en 1er. directorio"
	chmod a-rwx dir1/error-dir
	@echo ./cmp-dir.bin-san dir1/error-dir dir2/error-dir
	@ ! ./cmp-dir.bin-san dir1/error-dir dir2/error-dir > res.out >& err.out || ( echo "Codigo de retorno es 0, debe ser distinto de 0" ; false )
	@cat err.out
	@diff res.out res11.ref
	@ ! diff err.out err11.ref >& /dev/null || ( echo "Use la funcion perror para explicar el error en la salida estandar de errores" ; false )
	@echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Felicitaciones: todos los tests aprobados"

run: $(PROB).bin
	@echo "Test de igualdad"
	./cmp-dir.bin-san dir1/iguales dir2/iguales |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad con muchos directorios"
	./cmp-dir.bin-san dir1/igualesB dir2/igualesB |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenidos distintos"
	./cmp-dir.bin-san dir1/contenidos-distintos dir2/contenidos-distintos |& tee res.out
	@diff res.out res2.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de tamanos distintos"
	./cmp-dir.bin-san dir1/tamanos-distintos dir2/tamanos-distintos |& tee res.out
	@diff res.out res3.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad de archivos binarios grandes"
	cp cmp-dir.bin-san cmp-dir.bin-copy
	./cmp-dir.bin-san cmp-dir.bin-san cmp-dir.bin-copy |& tee res.out
	@diff res.out res4.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenido distinto de archivos binarios grandes"
	@echo "(difieren en el ultimo byte)"
	cp cmp-dir.bin-copy cmp-dir.bin-copy2
	echo a >> cmp-dir.bin-copy
	echo b >> cmp-dir.bin-copy2
	./cmp-dir.bin-san cmp-dir.bin-copy cmp-dir.bin-copy2 |& tee res.out
	@diff res.out res5.ref && echo "Test aprobado"
	rm cmp-dir.bin-copy cmp-dir.bin-copy2
	@echo "----------------------------------------------"
	@echo "Felicitaciones: todos los tests aprobados"


run-g: $(PROB).bin-g
	@echo "Test de igualdad"
	./cmp-dir.bin-san dir1/iguales dir2/iguales |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad con muchos directorios"
	./cmp-dir.bin-san dir1/igualesB dir2/igualesB |& tee res.out
	@diff res.out res1.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenidos distintos"
	./cmp-dir.bin-san dir1/contenidos-distintos dir2/contenidos-distintos |& tee res.out
	@diff res.out res2.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de tamanos distintos"
	./cmp-dir.bin-san dir1/tamanos-distintos dir2/tamanos-distintos |& tee res.out
	@diff res.out res3.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de igualdad de archivos binarios grandes"
	cp cmp-dir.bin-san cmp-dir.bin-copy
	./cmp-dir.bin-san cmp-dir.bin-san cmp-dir.bin-copy |& tee res.out
	@diff res.out res4.ref && echo "Test aprobado"
	@echo "----------------------------------------------"
	@echo "Test de contenido distinto de archivos binarios grandes"
	@echo "(difieren en el ultimo byte)"
	cp cmp-dir.bin-copy cmp-dir.bin-copy2
	echo a >> cmp-dir.bin-copy
	echo b >> cmp-dir.bin-copy2
	./cmp-dir.bin-san cmp-dir.bin-copy cmp-dir.bin-copy2 |& tee res.out
	@diff res.out res5.ref && echo "Test aprobado"
	rm cmp-dir.bin-copy cmp-dir.bin-copy2
	@echo "----------------------------------------------"
	@echo "Felicitaciones: todos los tests aprobados"

ddd: $(PROB).ddd

ddd-san: $(PROB).ddd-san

zip:
	@if grep -P '\t' $(PROB).c ; then echo "Su archivo $(PROB).c contiene tabs.  Reemplacelos por espacios en blanco!" ; false ; else true; fi
	@rm -f resultados.txt $(PROB).zip
	@echo "Sistema operativo utilizado" > resultados.txt
	@uname -a >> resultados.txt
	@cat resultados.txt
	@echo ==== run-san ==== | tee -a resultados.txt
	@$(MAK) -B run-san | tee -a resultados.txt
	@echo ==== run-g ==== | tee -a resultados.txt
	@$(MAK) -B run-g | tee -a resultados.txt
	@echo ==== run ==== | tee -a resultados.txt
	@$(MAK) -B run | tee -a resultados.txt
	@echo ==== zip ====
	zip -r $(PROB).zip resultados.txt $(PROB).c
	@echo "Entregue por u-cursos el archivo $(PROB).zip"
	@echo "Descargue de u-cursos lo que entrego, descomprimalo y revise"
	@echo "que esta su ultima version de $(PROB).c"

%.bin: %.c
	gcc -O -DOPT=1 $(CFLAGS) $^ $(LDLIBS) -o $@

%.bin-g: %.c
	gcc -g $(CFLAGS) $^ $(LDLIBS) -o $@

%.bin-san: %.c
	gcc -g -DSAN=1 -fsanitize=address -fsanitize=undefined -DSANITIZE $(CFLAGS) $^ $(LDLIBS) -o $@

%.ddd: %.bin-g
	ddd $(*F).bin-g &

%.ddd-san: %.bin-san
	ddd $(*F).bin-san &

clean:
	rm -f *.o *.log *.bin* core *.out
