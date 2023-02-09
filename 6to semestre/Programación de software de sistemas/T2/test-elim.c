// _DEFAULT_SOURCE se necesita para usar random
#define _DEFAULT_SOURCE 1

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "elim.h"

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
// Verifica que el resultado coincida con el valor de referencia
//

static void check_eliminar_espacios(char *s, char *ref) {
  char copia[strlen(s)+1];
  strcpy(copia, s);
  eliminar_espacios(copia);
  if (strcmp(copia, ref)!=0) {
    fflush(stdout);
    fprintf(stderr, "Valor incorrecto para s=\"%s\"\n"
                    "el resultado fue \"%s\"\n"
                    "el resultado debio ser \"%s\"\n", s, copia, ref);
    exit(1);
  }
}

static void check_eliminacion_espacios(char *s, char *ref) {
  char *result= eliminacion_espacios(s);
  if (strcmp(result, ref)!=0) {
    fflush(stdout);
    fprintf(stderr, "Valor incorrecto para s=\"%s\"\n"
                    "el resultado fue \"%s\"\n"
                    "el resultado debio ser \"%s\"\n", s, result, ref);
    exit(1);
  }
  free(result);
}

static void tests_unitarios(void (*check)(char *s, char *ref)) {
  check("", "");
  check(" "," ");
  check("  ", " ");
  check("   ", " ");
  check("    ", " ");
  check("         ", " ");
  check("a", "a");
  check(" b", " b");
  check("  cd", " cd");
  check("        efg", " efg");
  check("h ", "h ");
  check("ij  ", "ij ");
  check("klm       ", "klm ");
  check("  1  ", " 1 ");
  check("        *     ", " * ");
  check("  +-/&|  ", " +-/&| ");
  check("   hola   que     tal     ", " hola que tal ");
  check("los    4     puntos    cardinales    son   3:    "
        "el   norte     y  el   sur",
        "los 4 puntos cardinales son 3: el norte y el sur");
}

static char *w[] = {NULL, "los", "4", "puntos", "cardinales", "son", "3:",
              "el", "norte", "y", "el", "sur", NULL};
static int err_san= 0;

static void tests_lentos(int check, int ns) {
  struct rusage ru;
  char **all_res= malloc(ns*sizeof(char*));
  int nw= 1, lenw= 0;
  while (w[nw]!=NULL) {
    lenw += strlen(w[nw++]);
  }
  nw--;
  int len_w[ns+1];
  int len_ref= lenw+nw+1;
  char *ref= malloc(len_ref);
  int pos_ref= 0;
  for (int idx= 1; idx<=nw; idx++) {
    int len_widx= strlen(w[idx]);
    len_w[idx]= len_widx;
    ref[pos_ref++]= ' ';
    if (pos_ref+len_widx>=len_ref) {
      fprintf(stderr, "bug!\n");
      exit(1);
    }
    strcpy(&ref[pos_ref], w[idx]);
    pos_ref += len_widx;
  }
  ref[pos_ref++]= 0;
  if (pos_ref!=len_ref) {
    fprintf(stderr, "bug!\n");
    exit(1);
  }
  int len= 0;
  for (int i= 1; i<=ns; i++) {
    len= lenw + i*nw + (nw-1)*nw/2 + 1;
    char *s= malloc(len);
    int pos= 0;
    int j= i;
    for (int idx= 1; idx<=nw; idx++) {
      for (int k= 0; k<j; k++) {
        // if (pos>=len)
        //   exit(1);
        s[pos++]= ' ';
      }
      if (pos+len_w[idx]>=len)
        exit(1);
      strcpy(&s[pos], w[idx]);
      pos += len_w[idx];
      j++;
    }
    s[pos++]= 0;
    if (pos!=len) {
      fprintf(stderr, "bug!\n");
      exit(1);
    }
    if (check) {
      check_eliminacion_espacios(s, ref);
      check_eliminar_espacios(s, ref);
    }
    else {
      all_res[i-1]= eliminacion_espacios(s);
      eliminar_espacios(s);
    }
    free(s);
    if (i>1000) {
      int rc= getrusage(RUSAGE_SELF, &ru);
      if (rc!=0) {
        perror("getrusage");
        exit(1);
      }
      if (ru.ru_maxrss>100000) {
        printf("%ld KBytes usados\n", ru.ru_maxrss);
        fprintf(stderr, "Esta solicitando mas memoria de lo necesario "
                        "en eliminacion_espacios\n");
        exit(1);
      }
    }
  }
  free(ref);
  if (!check) {
#ifdef SANITIZE
    if (err_san) {
      all_res[ns-1][len_ref]= 0;
    }
#endif
#if 1
    for (int k= 0; k<ns; k++)
      free(all_res[k]);
#endif
  }
  int rc= getrusage(RUSAGE_SELF, &ru);
  if (rc!=0) {
    perror("getrusage");
    exit(1);
  }
  printf("%ld KBytes usados\n", ru.ru_maxrss);

  free(all_res);
}

static void bench_elim(int check, int ns) {
  int nw= 1, lenw= 0;
  while (w[nw]!=NULL) {
    lenw += strlen(w[nw++]);
  }
  nw--;
  int len_w[ns+1];
  int len_ref= lenw+nw+1;
  char *ref= malloc(len_ref);
  int pos_ref= 0;
  for (int idx= 1; idx<=nw; idx++) {
    int len_widx= strlen(w[idx]);
    len_w[idx]= len_widx;
    ref[pos_ref++]= ' ';
    if (pos_ref+len_widx>=len_ref) {
      fprintf(stderr, "bug!\n");
      exit(1);
    }
    strcpy(&ref[pos_ref], w[idx]);
    pos_ref += len_widx;
  }
  ref[pos_ref++]= 0;
  if (pos_ref!=len_ref) {
    fprintf(stderr, "bug!\n");
    exit(1);
  }
  int len= 0;
  for (int i= 1; i<=ns; i++) {
    len= lenw + i*nw + (nw-1)*nw/2 + 1;
    char *s= malloc(len);
    int pos= 0;
    int j= i;
    for (int idx= 1; idx<=nw; idx++) {
      for (int k= 0; k<j; k++) {
        // if (pos>=len)
        //   exit(1);
        s[pos++]= ' ';
      }
      if (pos+len_w[idx]>=len)
        exit(1);
      strcpy(&s[pos], w[idx]);
      pos += len_w[idx];
      j++;
    }
    s[pos++]= 0;
    if (pos!=len) {
      fprintf(stderr, "bug!\n");
      exit(1);
    }
    if (check) {
      check_eliminar_espacios(s, ref);
    }
    else {
      eliminar_espacios(s);
    }
    free(s);
  }
  free(ref);
}

#ifdef OPT
#define NS 30000
#else
#define NS 1000
#endif
#define NINTENTOS 5

int main(int argc, char *argv[]) {
  char *cmd;
  if (argc==2) {
    cmd= argv[1];
    if (strcmp(cmd,"err")==0) {
      err_san= 1;
      cmd= "debug";
    }
  }
  else {
#ifdef OPT
    cmd= "bench";
#else
    cmd= "debug";
#endif
  }

  printf("Tests de eliminar_espacios\n");
  tests_unitarios(check_eliminar_espacios);
  printf("Tests de eliminacion_espacios\n");
  tests_unitarios(check_eliminacion_espacios);
  printf("Tests largos\n");
  tests_lentos(1, 1000);

  if (strcmp(cmd, "ref")==0) {
    resetTime();
    tests_lentos(0, NS);
    int tiempo= getTime();
    FILE *out= fopen("tiempo-ref.txt", "w");
    if (out==NULL) {
      perror("tiempo-ref.txt");
      exit(1);
    }
    fprintf(out, "%d\n", tiempo);
    fclose(out);
  }
  else if (strcmp(cmd, "bench-elim")==0) {
    resetTime();
    bench_elim(0, NS);
    int tiempo= getTime();
    printf("Tiempo para eliminar_espacios= %d\n", tiempo);
  }
  else if (strcmp(cmd, "debug")==0) {
    resetTime();
    tests_lentos(0, NS);
    int tiempo= getTime();
    printf("Tiempo de cpu usado por su version: %d milisegundos\n", tiempo);
  }
  else {
    int tiempo_ref= atoi(cmd);
    printf("Tiempo de cpu usado por la versión del profesor: "
           "%d milisegundos\n", tiempo_ref);
    int i= 1;
    while (i<=NINTENTOS) {
      printf("Intento %d\n", i);
      resetTime();
      tests_lentos(0, NS);
      int tiempo= getTime();
      printf("Tiempo de cpu usado por su version: %d milisegundos\n", tiempo);
      double q= (double)tiempo/(double)tiempo_ref;
      int sobrecosto= (q-1.)*100;
      printf("Porcentaje de sobrecosto: %d %%\n", sobrecosto);
      if (sobrecosto<=50)
        break;
      i++;
    }
    if (i>NINTENTOS) {
      fflush(stdout);
      fprintf(stderr, "Lo siento: su solucion es mas del 50%% mas lenta\n");
      exit(1);
    }
  }
  printf("Aprobado\n");

  printf("Felicitaciones, todos los tests funcionan correctamente\n");
  return 0;
}
