#define _XOPEN_SOURCE 500

#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include "fav.h"

#ifdef OPT
#define N_INTENTOS 5
#else
#define N_INTENTOS 1
#endif

#define TOLERANCIA 1.5

int leer(int fd, void *vbuf, int n) {
  char *buf= vbuf;
  do {
    int rc= read(fd, buf, n);
    if (rc<=0)
      return 1; /* fracaso: error o fin del archivo/pipe/socket */
    n-= rc; /* descontamos los bytes leídos */
    buf+= rc; /* avanzamos el buffer para no reescribir lo leido previamente */
  } while (n>0); /* mientras no leamos todo lo que esperamos */
  return 0; /* exito */
}

// ----------------------------------------------------
// Funcion que entrega el tiempo transcurrido desde el lanzamiento del
// programa en milisegundos

static long long getUSecsOfDay() {
    struct timeval Timeval;
    gettimeofday(&Timeval, NULL);
    return (long long)Timeval.tv_sec*1000000+Timeval.tv_usec;
}

static int time0= 0;

static int getTime0() {
    return getUSecsOfDay()/1000;
}

static void resetTime() {
  time0= getTime0();
}

static int getTime() {
  return getTime0()-time0;
}

// ----------------------------------------------------
// Generacion de numeros aleatorios
//
// Es correcto usar la funcion estandar random, que genera buenos
// numeros aleatorios.  Pero es ineficiente.  La funcion random pide un
// mutex para evitar dataraces.  Pero este problema invoca random
// demasiado frecuentemente, provocando asi tanta contencion en la solucion
// paralela que hasta se podria demorar mas que la secuencial.
// Por eso tuve que programar mi propia version de la generacion de
// numeros aleatorios, que no sea compartida por los distintos threads.
// Es decir cada thread genera su propia secuencia de numeros.  El
// estado necesario para la generacion de los numeros se almacena en la
// estructura RandGen.  Cada thread maneja su propia instancia de RandGen
// para evitar dataraces.  Aun asi la semilla inicial para cada instancia
// de RandGen se genera con random.

#define MAXBITS 31

// Sacado de: http://en.wikipedia.org/wiki/Multiply-with-carry

#define PHI 0x9e3779b9

typedef struct {
  uint32_t Q[4096], c; // Para rand_cmwc
  int32_t cur;         // Para random0or1
  int bit;
} RandGen;

static void init_rand(RandGen *gen, uint32_t seed) {
    uint32_t x= seed;
    int i;

    gen->c= 362436;
    gen->Q[0] = x;
    gen->Q[1] = x + PHI;
    gen->Q[2] = x + PHI + PHI;

    for (i = 3; i < 4096; i++)
            gen->Q[i] = gen->Q[i - 3] ^ gen->Q[i - 2] ^ PHI ^ i;
}

static uint32_t rand_cmwc(RandGen *gen) {
    uint64_t t, a = 18782LL;
    uint32_t i = 4095;
    uint32_t x, r = 0xfffffffe;
    i = (i + 1) & 4095;
    t = a * gen->Q[i] + gen->c;
    gen->c = (t >> 32);
    x = t + gen->c;
    if (x < gen->c) {
            x++;
            gen->c++;
    }
    return (gen->Q[i] = r - x);
}

int random0or1(RandGen *gen) {
  // Codigo copiado de srand, pero sin soporte para threads
  if (gen->bit>=MAXBITS) {
    gen->cur = rand_cmwc(gen) & 0x7fffffff;
  }
  int res= gen->cur & 1;
  gen->cur >>= 1;
  gen->bit++;
  return res;
}

int rand_int(int i, int j, RandGen *gen) {
  return (rand_cmwc(gen)%(j-i+1))+i;
}

// ----------------------------------------------------
// Version secuencial de favorables

static RandGen gen;
static int seed= 0;

void init_rand_seed(void) {
  seed= random();
  init_rand(&gen, random()+getUSecsOfDay());
}

int favorables(int n, int sum, int rep) {
  pid_t pid= getpid();
  printf("Semilla inicial para proceso %d es %d\n", pid, seed);
  fflush(stdout);
  int fav= 0;    // número de casos favorables
  for (int i= 0; i<rep; i++) {
    int s= 0;  // suma de los dados
    for (int j= 0; j<n; j++)
      s+= rand_int(1,6, &gen); // entrega entero aleatorio en [1,6]
    if (s==sum)  // caso favorable: los dados suman sum
      fav++;
  }
  printf("Casos favorables con %d repeticiones para proceso %d=%d\n",
         rep, pid, fav);
  return fav;
}

int main() {

  srandom(getUSecsOfDay());
  init_rand_seed();

  printf("Test 1: Un ejemplo pequeño con nlanz=2 sum=7 rep=1000000\n");
  {
    int nlanz= 2;
    int sum= 7;
    int rep= 1000000;
    printf("Calculando en paralelo\n");
    fflush(stdout);
    int fav= favorables_par(nlanz, sum, rep, 8);
    double pbb= (double)fav/rep;
    double delta= fabs(pbb-1./6);
    printf("fav=%d  pbb=%f  delta=%f\n", fav, pbb, delta);
    if (delta>0.002) {
      fprintf(stderr, "La probabilidad debio ser un sexto aprox.\n");
      exit(1);
    }
    printf("Test 1 aprobado\n");
    printf("\n--------------------------------------------------\n\n");
  }

  printf("Test 2: Un ejemplo grande con nlanz=10 sum=30 rep=10000000\n");
  {
    int nlanz= 10;
    int sum= 30;
#ifdef SAN
    int rep= 2000000;
#else
    int rep= 20000000;
#endif
    int tiempo_sec, tiempo_par;
    double speedUp= 0;
    int i;
    printf("Precalentando secuencialmente\n");
    int fav= favorables(nlanz, sum, rep/100);
    double pbb= (double)fav/(rep/100);
    printf("fav=%d pbb=%f\n", fav, pbb);
 
    printf("Calculando secuencialmente con rep=%d\n", rep);
    resetTime();
    fav= favorables(nlanz, sum, rep);
    tiempo_sec= getTime();
    pbb= (double)fav/rep;
    printf("Tiempo= %d, fav=%d pbb=%f\n", tiempo_sec, fav, pbb);
 
    for (i= 1; i<=N_INTENTOS; i++) {
      printf("\n-----\n");
      printf("Calculando en paralelo con rep=%d, intento %d\n", rep, i);
      fflush(stdout),
      resetTime();
      int fav_par= favorables_par(nlanz, sum, rep,4);
      tiempo_par= getTime();
      double pbb_par= (double)fav_par/rep;
      speedUp= (double)tiempo_sec/tiempo_par;
      double delta= fabs((pbb-pbb_par)/pbb);
      printf("Tiempo= %d  speedup= %g  fav=%d  pbb=%f  delta=%f\n", 
           tiempo_par, speedUp, fav_par, pbb_par, delta);
 
      if (delta>0.02) {
        fprintf(stderr, "las probabilidades secuencial y paralela difieren\n");
        exit(1);
      }
      if (speedUp>=TOLERANCIA)
        break;
    }
#ifdef OPT
    if (i>N_INTENTOS) {
      fprintf(stderr, "Despues de %d intentos no obtuvo un speedup de %gx\n",
              N_INTENTOS, TOLERANCIA);
      fprintf(stderr, "Revise la paralelizacion.\n");
      exit(1);
    }
    printf("Test 2 aprobado: speedup >= %gx\n\n", TOLERANCIA);
#else
    printf("Test 2 aprobado\n\n");
#endif
  }

  printf("Felicitaciones: su tarea funciona\n");
  
  return 0;
}
