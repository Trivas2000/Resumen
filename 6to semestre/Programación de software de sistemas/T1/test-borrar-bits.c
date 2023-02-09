// _DEFAULT_SOURCE se necesita para usar random
#define _DEFAULT_SOURCE 1

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "borrar-bits.h"

// ----------------------------------------------------
// Funcion que entrega el tiempo de CPU usado desde
// que se invoco resetTime()

static long long time0= 0;

static long long getTime0() {
  struct rusage ru;
  int rc= getrusage(RUSAGE_SELF, &ru);
  if (rc!=0) {
    perror("getTime");
    exit(1);
  }
  return (long long)ru.ru_utime.tv_sec*1000000+ru.ru_utime.tv_usec;
}

static void resetTime() {
  time0= getTime0();
}

static int getTime() {
  return (getTime0()-time0+500)/1000;
}

// ----------------------------------------------------
// La misma funcionalidad de recortar pero con
// multiplicaciones, divisiones y modulo
//

static uint borrar_bits_lento(uint x, uint pat, int len) {
  unsigned long long dosElen= pow(2, len);
  uint z= 0;
  int i= 0;
  while (i <= sizeof(uint)*8-len) {
    if (x % dosElen == pat) {
      i += len;
      x /= dosElen;
    }
    else {
      z += (x % 2)*pow(2,i);
      i++;
      x /= 2;
    }
  }
#if 1
  while (i <= sizeof(uint)*8-1) {
    z += (x % 2)*pow(2,i);
    i++;
    x /= 2;
  }
#endif
    
  return z;
}

// ----------------------------------------------------
// Benchmark

static char *to_binary(uint x) {
  int len= 0;
  uint z= x;
  do {
    z >>= 1;
    len++;
  } while (z!=0);
  char *s= malloc(len+1);
  char *end = s+len;
  *end-- = 0;
  z= x;
  do {
    *end-- = '0' + (z&1);
    z >>= 1;
  } while (z!=0);
  return s;
}

// ----------------------------------------------------
// Benchmark
//

typedef struct {
  uint x, pat, ref;
  int len;
} Param;

static uint check(uint x, uint pat, int len, uint ref) {
  uint result= borrar_bits(x, pat, len);
  if (result != ref) {
    fflush(stdout);
    char *x_bin= to_binary(x);
    char *pat_bin= to_binary(pat);
    char *result_bin= to_binary(result);
    char *ref_bin= to_binary(ref);
    fprintf(stderr, "Valor incorrecto para x=0b%s\npat=0b%s len=%d\n",
            x_bin, pat_bin, len);
    fprintf(stderr, "borrar_bits retorna 0b%s\ncuando debio ser 0b%s\n",
            result_bin, ref_bin);
    free(x_bin);
    free(pat_bin);
    free(result_bin);
    free(ref_bin);
    exit(1);
  }
  return result;
}

// ----------------------------------------------------
// Funcion main
//

int main(int argc, char **argv) {
  int tiempo_ref= 0;
  int bench= 0;       // si se hace o no el benchmark
  int ntests= 300000; // numero de tests para cada len
  const int bits_uint= sizeof(uint)*8;

  if (argc==2) {
    bench= 1;
    if (strcmp(argv[1], "ref")!=0)
      tiempo_ref= atoi(argv[1]);
  }

  printf("Tests unitarios\n");
  check(0b00010001001, 0b0, 1, 0b00010001001);
  check(0b00010001001, 0b1, 1, 0);
  check(0b111011001, 0b10, 2, 0b110010001);
  check(0b111011001, 0b101, 3, 0b110001001);
  check(0b111011001, 0b111011001, 9, 0);
  check(0b111011001, 0b11011001, 8, 0b100000000);
  check(0b111011001, 0b111011001, bits_uint, 0);
  check(0b111011001, 0b11011001, bits_uint, 0b111011001);
  printf("Aprobado\n");

  srandom(1000);
  int tot_tests= bits_uint*ntests;

  printf("Test exhaustivo con %d invocaciones de borrar_bits\n", tot_tests);

  Param *params= NULL, *p= NULL;
  if (bench) {
    const size_t size= (size_t)tot_tests*sizeof(Param);
    const size_t MB= 1024*1024;
    int size_mb= (size+MB/2)/MB;
    printf("Reservando %d MB para los benchmarks\n", size_mb);
    params= malloc(size);
    p= params;
  }

  for (int len= 1; len<=bits_uint; len++) {
    for (int k= 0; k<ntests; k++) {
      uint x = (random()<<1) + (random()&1);
      uint pat = ( (uint)( (random()<<1) + (random()&1) ) << (bits_uint-len) )
                 >> (bits_uint-len);
      uint ref = borrar_bits_lento(x, pat, len);
      check(x, pat, len, ref);
      if (bench) {
        p->x= x;
        p->pat= pat;
        p->len= len;
        p->ref= ref;
        p++;
      }
    }
  }
  printf("Aprobado\n");

  if (bench) {
    int niter= 10;
    printf("Corriendo benchmark\n");
    printf("Tiempo de cpu usado por la version del profesor: "
             "%d milisegundos\n", tiempo_ref);
    if (strcmp(argv[1],"ref")!=0) {
      Param *params_top= &params[tot_tests];
      resetTime();
        for (p= params; p<params_top; p++) {
          uint result= borrar_bits_lento(p->x, p->pat, p->len);
          if (result!=p->ref) {
            fflush(stdout);
            fprintf(stderr, "Los resultados son inconsistentes: con los "
                    " mismos\nargumentos se entregan resultados distintos\n");
            exit(1);
          }
        }
      int tiempo_lento= getTime()*niter;
      printf("Tiempo para la version sin operadores de bits (estimado): "
                "%d milisegundos\n", tiempo_lento);
    }
    Param *params_top= &params[tot_tests];
    params_top= &params[tot_tests];
    resetTime();
    for (int k= 0; k<niter; k++) {
      for (p= params; p<params_top; p++) {
        uint result= borrar_bits(p->x, p->pat, p->len);
        if (result!=p->ref) {
          fflush(stdout);
          fprintf(stderr, "Los resultados son inconsistentes: con los "
                  " mismos\nargumentos se entregan resultados distintos\n");
          exit(1);
        }
      }
    }
    int tiempo= getTime();
    free(params);
    printf("Tiempo de cpu usado por su version: %d milisegundos\n", tiempo);
    if (argc==2) {
      if (tiempo_ref!=0) {
        double q= (double)tiempo/(double)tiempo_ref;
        int porciento= (q-1.)*100;
        printf("Porcentaje de sobrecosto: %d %%\n", porciento);
        if (porciento>80) {
          fflush(stdout);
          fprintf(stderr, "Lo siento: su solucion es demasiado lenta\n");
          exit(1);
        }
      }
      else {
        FILE *out= fopen("tiempo-ref.txt", "w");
        if (out==NULL) {
          perror("tiempo-ref.txt");
          exit(1);
        }
        fprintf(out, "%d\n", tiempo);
        fclose(out);
      }
    }
    printf("Aprobado\n");
  }

  printf("Felicitaciones!  Todos los tests aprobados.\n");

  return 0;
}
