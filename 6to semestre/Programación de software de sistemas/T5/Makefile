# Si desea agregar un programa con archivos test-ejemplo.c, ejemplo.c y
# ejemplo.h, agregue un par de reglas que digan:
# test-ejemplo.o ejemplo.o: ejemplo.h
# test-ejemplo: test-ejemplo.o ejemplo.o

RISCV = /opt/riscv
TARGET = riscv64-unknown-elf
CC = ${RISCV}/bin/${TARGET}-gcc
CXX = ${RISCV}/bin/${TARGET}-g++
AS = ${RISCV}/bin/${TARGET}-as
LD = ${RISCV}/bin/${TARGET}-ld
STRIP = ${RISCV}/bin/${TARGET}-strip
GDB = ${RISCV}/bin/${TARGET}-gdb
PK = ${RISCV}/${TARGET}/bin/pk
DUMP= ${RISCV}/${TARGET}/bin/objdump
QEMU32=qemu-riscv32

SHELL=bash -o pipefail
MAK=make --no-print-directory

COMFLAGS= -Wall -pedantic -std=c2x -march=rv32im -mabi=ilp32

CFLAGS= -g ${COMFLAGS}
LDFLAGS= -g
LDLIBS=

readme:
	@less README.txt

sort-rv: test-sort.o sort-rv.o

sort-c: test-sort.o sort-c.o

sort-rv-esp: test-sort.o sort-rv-esp.o

sort-c-esp: test-sort.o sort-c-esp.o

zip:
	@if grep -P '\t' sort-c-esp.c ; then echo "Su archivo sort-c-esp.c contiene tabs.  Reemplacelos por espacios en blanco!" ; false ; else true; fi
	@rm -f resultados.txt sort-esp.zip
	@echo "Sistema operativo utilizado" > resultados.txt
	@uname -a >> resultados.txt
	@cat resultados.txt
	@echo ==== make sort-c-esp.run ==== | tee -a resultados.txt
	@$(MAK) -B sort-c-esp.run | tee -a resultados.txt
	@echo ==== make sort-rv-esp.run ==== | tee -a resultados.txt
	@$(MAK) -B sort-rv-esp.run | tee -a resultados.txt
	@echo ==== zip ====
	zip -r sort-esp.zip resultados.txt sort-c-esp.c sort-rv-esp.s
	@echo "Entregue por u-cursos el archivo sort-esp.zip"
	@echo "Descargue de u-cursos lo que entrego, descomprimalo y revise"
	@echo "que estan sus ultimas versiones de sort-c-esp.c y sort-rv-esp.s"


clean:
	rm -f *.o sort-rv sort-rv-esp sort-c sort-c-esp

%.o: %.c
	${CC} -g -c ${COMFLAGS} $< -o $@

%.s: %.c
	${CC} -O -S ${COMFLAGS} $<

%.ddd: %
	qemu-riscv32 -g 1234 $(*F) &
	ddd --debugger ${GDB} --command target.gdb $(*F)

%.o: %.s
	${CC} -c ${COMFLAGS} $< -o $@

%: %.o
	${CC} ${COMFLAGS} ${LDFLAGS} $^ ${LDLIBS} -o $@

%.run: %
	qemu-riscv32 $(*F)

%.dump: %
	${DUMP} -S $(*F) | less
