# Para revisar las opciones de compilacion y ejecucion,
# ingrese en el terminal el comando: make
#
#

PROB=rotar

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
	cp noms-orig.txt noms.txt
	@echo "Test: sin movimientos"
	./rotar.bin-san noms.txt 3
	@echo diff noms.txt noms-orig.txt
	@diff noms.txt noms-orig.txt && echo "Sin movimientos: test aprobado"
	@echo "Test: 2 movimientos"
	./rotar.bin-san noms.txt 0 5
	@echo diff noms.txt noms-ref2.txt
	@diff noms.txt noms-ref2.txt && echo "2 movimientos: test aprobado"
	@echo "Test: 4 movimientos"
	cp noms-orig.txt noms.txt
	./rotar.bin-san noms.txt 2 5 0 4
	@echo diff noms.txt noms-ref4.txt
	@diff noms.txt noms-ref4.txt && echo "4 movimientos: test aprobado"
	@echo "Test: 6 movimientos"
	cp noms10-orig.txt noms10.txt
	./rotar.bin-san noms10.txt 2 1 7 9 0 3
	@echo diff noms10.txt noms10-ref6.txt
	@diff noms10.txt noms10-ref6.txt && echo "6 movimientos: test aprobado"
	@echo "Felicitaciones: todos los tests aprobados"

run: $(PROB).bin
	cp noms-orig.txt noms.txt
	@echo "Test: sin movimientos"
	./rotar.bin noms.txt 3
	@echo diff noms.txt noms-orig.txt
	@diff noms.txt noms-orig.txt && echo "Sin movimientos: test aprobado"
	@echo "Test: 2 movimientos"
	./rotar.bin noms.txt 0 5
	@echo diff noms.txt noms-ref2.txt
	@diff noms.txt noms-ref2.txt && echo "2 movimientos: test aprobado"
	@echo "Test: 4 movimientos"
	cp noms-orig.txt noms.txt
	./rotar.bin noms.txt 2 5 0 4
	@echo diff noms.txt noms-ref4.txt
	@diff noms.txt noms-ref4.txt && echo "4 movimientos: test aprobado"
	@echo "Test: 6 movimientos"
	cp noms10-orig.txt noms10.txt
	./rotar.bin noms10.txt 2 1 7 9 0 3
	@echo diff noms10.txt noms10-ref6.txt
	@diff noms10.txt noms10-ref6.txt && echo "6 movimientos: test aprobado"
	@echo "Felicitaciones: todos los tests aprobados"


run-g: $(PROB).bin-g
	cp noms-orig.txt noms.txt
	@echo "Test: sin movimientos"
	./rotar.bin-g noms.txt 3
	@echo diff noms.txt noms-orig.txt
	@diff noms.txt noms-orig.txt && echo "Sin movimientos: test aprobado"
	@echo "Test: 2 movimientos"
	./rotar.bin-g noms.txt 0 5
	@echo diff noms.txt noms-ref2.txt
	@diff noms.txt noms-ref2.txt && echo "2 movimientos: test aprobado"
	@echo "Test: 4 movimientos"
	cp noms-orig.txt noms.txt
	./rotar.bin-g noms.txt 2 5 0 4
	@echo diff noms.txt noms-ref4.txt
	@diff noms.txt noms-ref4.txt && echo "4 movimientos: test aprobado"
	@echo "Test: 6 movimientos"
	cp noms10-orig.txt noms10.txt
	./rotar.bin-g noms10.txt 2 1 7 9 0 3
	@echo diff noms10.txt noms10-ref6.txt
	@diff noms10.txt noms10-ref6.txt && echo "6 movimientos: test aprobado"
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
	rm -f *.o *.log *.bin* core
