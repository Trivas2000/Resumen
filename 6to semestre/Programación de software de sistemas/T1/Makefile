# Para revisar las opciones de compilacion y ejecucion,
# ingrese en el terminal el comando: make
#
#

PROB=borrar-bits

TEST=test-$(PROB)
HEADER=$(PROB)

SHELL=bash -o pipefail

INCLUDE=
CFLAGS=-Wall -Werror -std=c2x -Wno-unused-function $(INCLUDE)
#CFLAGS=-Wall -Werror -pedantic -std=c2x $(INCLUDE)
LDLIBS=-lm

MAK=make --no-print-directory

readme:
	@less README.txt

$(PROB).bin $(PROB).bin-g $(PROB).bin-san: $(PROB).c $(TEST).c $(HEADER).h

run-san: $(PROB).bin-san
	./$(PROB).bin-san

run-g: $(PROB).bin-g
	./$(PROB).bin-g

prof.ref: $(PROB).bin
	cp $(PROB).bin $@
	strip $@

run: $(PROB).bin
	@echo "Midiendo cuanto demora la solucion del profesor"
	rm -f tiempo-ref.txt
	chmod +x prof.ref
	./prof.ref ref > /dev/null
	@echo "Tiempo de referencia = " `cat tiempo-ref.txt`
	@echo "Verificando y comparando con su solucion"
	./$(PROB).bin `cat tiempo-ref.txt`

ddd: $(PROB).ddd

ddd-san: $(PROB).ddd-san

zip:
	@rm -f resultados.txt borrar-bits.zip
	@echo "Sistema operativo utilizado" > resultados.txt
	@uname -a >> resultados.txt
	@cat resultados.txt
	@echo ==== run ==== | tee -a resultados.txt
	@$(MAK) -B run | tee -a resultados.txt
	@echo ==== run-g ==== | tee -a resultados.txt
	@$(MAK) -B run-g | tee -a resultados.txt
	@echo ==== run-san ==== | tee -a resultados.txt
	@$(MAK) -B run-san | tee -a resultados.txt
	@echo ==== zip ====
	zip -r borrar-bits.zip resultados.txt borrar-bits.c
	@echo "Entregue por u-cursos el archivo borrar-bits.zip"
	@echo "Descargue de u-cursos lo que entrego, descomprimalo y revise"
	@echo "que esta su ultima version de borrar-bits.c"

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
	rm -f *.o *.log *.bin*
