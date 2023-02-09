#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "seleccion.h"

#pragma GCC diagnostic ignored "-Wunused-function"

// ----------------------------------------------------
// Funcion que entrega el tiempo transcurrido desde el lanzamiento del
// programa en milisegundos

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
// revisar_int: verifica que un entero es un valor especifico

void revisar_int(int n, int nref) {
  if (n!=nref) {
    fprintf(stderr, "El valor retornado debio ser %d, no %d\n", nref, n);
    exit(1);
  }
}

// ----------------------------------------------------
// Funcion que construye un arbol

static Nodo *abb(int x, Nodo *izq, Nodo *der) {
  Nodo *a= malloc(sizeof(*a));
  a->x= x;
  a->izq= izq;
  a->der= der;
  return a;
}

// ----------------------------------------------------
// Funcion que verifica que 2 arboles binarios son iguales

static void revisar_abb(Nodo *a, Nodo *b) {
  if (a==NULL) {
    if (b==NULL)
      return;
    fprintf(stderr, "Arboles distintos: a es NULL, b tiene etiqueta %d\n",
                    b->x);
    exit(1);
  }
  else if (b==NULL) {
    fprintf(stderr, "Arboles distintos: b es NULL, a tiene etiqueta %d\n",
                    a->x);
    exit(1);
  }
  else {
    if (a->x!=b->x) {
      fprintf(stderr, "Etiquetas de arboles son distintas: %d != %d\n",
                      a->x, b->x);
      exit(1);
    }
    revisar_abb(a->izq, b->izq);
    revisar_abb(b->der, b->der);
  }
}

// ----------------------------------------------------
// Funcion que verifica que 2 arboles binarios sean el mismo

static void revisar_mismo_nodo(Nodo *a, Nodo *b) {
  if (a!=b) {
    if (a==NULL || b==NULL)
      fprintf(stderr, "No son el mismo arbol.  Uno es NULL, el otro no\n");
    else
      fprintf(stderr, "No son el mismo arbol.  Etiquetas son %d %d\n",
                      a->x, b->x);
    exit(1);
  }
}

// ----------------------------------------------------
// Funcion que verifica que los campos x de un arbol binario
// desbalanceado por la derecha sean i, i+1, ..., j

static void revisar_des_der(Nodo *a, int i, int j) {
  int ref= i;
  while (ref<=j) {
    if (a==NULL) {
      fprintf(stderr, "El arbol esta incorrectamente vacio\n");
      exit(1);
    }
    if (a->x!=ref) {
      fprintf(stderr, "x es %d, debio ser %d\n", a->x, ref);
      exit(1);
    }
    if (a->izq!=NULL) {
      fprintf(stderr, "Subarbol izquierdo debio ser NULL en nodo %d\n", a->x);
      exit(1);
    }
    a= a->der;
    ref++;
  }
  if (a!=NULL) {
    fprintf(stderr, "El arbol tiene mas nodos de lo que deberia\n");
    exit(1);
  }
}

// ----------------------------------------------------
// Funcion que verifica que los campos x de un arbol binario
// desbalanceado por la derecha sean i, i+1, ...,j

static void revisar_des_izq(Nodo *a, int i, int j) {
  int ref= j;
  while (i<=ref) {
    if (a==NULL) {
      fprintf(stderr, "El arbol esta incorrectamente vacio\n");
      exit(1);
    }
    if (a->x!=ref) {
      fprintf(stderr, "x es %d, debio ser %d\n", a->x, ref);
      exit(1);
    }
    if (a->der!=NULL) {
      fprintf(stderr, "Subarbol derecho debio ser NULL en nodo %d\n", a->x);
      exit(1);
    }
    a= a->izq;
    ref--;
  }
  if (a!=NULL) {
    fprintf(stderr, "El arbol tiene mas nodos de los que deberia\n");
    exit(1);
  }
}

// ----------------------------------------------------
// Revisa que los campos de un arbol sean i, i+1, i+2, etc.

static int revisar_campos(Nodo *a, int i) {
  if (a==NULL) {
    return i;
  }
  int j= revisar_campos(a->izq, i);
  if (a->x!=j) {
    fprintf(stderr, "El nodo con x=%d debio ser %d\n", a->x, j);
    exit(1);
  }
  j= revisar_campos(a->der, j+1);
  return j;
}

// ----------------------------------------------------
// Libera un arbol binario

static void liberar(Nodo *a) {
  if (a!=NULL) {
    liberar(a->izq);
    liberar(a->der);
    free(a);
  }
}

// ----------------------------------------------------
// Crea una copia de un arbol binario

static Nodo *copia(Nodo *a) {
  if (a==NULL)
    return NULL;
 
  Nodo *an= malloc(sizeof(Nodo));
  an->x= a->x;
  an->izq= copia(a->izq);
  an->der= copia(a->der);
  return an;
}

// ----------------------------------------------------
// Entrega el numero de nodos de un arbol binario

static int contar_nodos(Nodo *a) {
  if (a==NULL)
    return 0;
  else
    return 1+contar_nodos(a->izq)+contar_nodos(a->der);
}

// ----------------------------------------------------
// Crea una copia condensada de un arbol binario con un solo malloc

static void duplicar(Nodo *a, Nodo **pdest) {
  Nodo *dest= *pdest;
  (*pdest)++;
  dest->x= a->x;
  if (a->izq==NULL)
    dest->izq=NULL;
  else {
    dest->izq= *pdest;
    duplicar(a->izq, pdest);
  }
  if (a->der==NULL)
    dest->der= NULL;
  else {
    dest->der= *pdest;
    duplicar(a->der, pdest);
  }
}

// ----------------------------------------------------
// Crea un arbol binario de busqueda bien equilibrado en donde 
// los x van de i a j

static Nodo *equilibrado(int i, int j) {
  if (i>j)
    return NULL;
  int k= (i+j+1)/2;
  Nodo *a= malloc(sizeof(Nodo));
  a->x= k;
  a->izq= equilibrado(i, k-1);
  a->der= equilibrado(k+1, j);
  return a;
}

// ----------------------------------------------------
// Crea un arbol binario desequilibrado por la izquierda en donde 
// los x van de i a j

static Nodo *desequilibrado_izq(int i, int j) {
  if (i>j) {
    return NULL;
  }
  Nodo *a= malloc(sizeof(Nodo));
  a->x= j;
  a->izq= desequilibrado_izq(i, j-1);
  a->der= NULL;
  return a;
}

// ----------------------------------------------------
// Crea un arbol binario desequilibrado por la derecha en donde 
// los x van de i a j

static Nodo *desequilibrado_der(int i, int j) {
  if (i>j) {
    return NULL;
  }
  Nodo *a= malloc(sizeof(Nodo));
  a->x= i;
  a->izq= NULL;
  a->der= desequilibrado_der(i+1, j);
  return a;
}

int main(int argc, char *argv[]) {
  printf("====================================\n");
  printf("Tests de la funcion selprim\n");
  printf("====================================\n\n");

  {
    printf("Caso arbol nulo: debe continuar vacio\n");
    Nodo *a= NULL;
    int k= selprim(&a, 3);
    revisar_abb(a, NULL);
    revisar_int(k, 0);
  }

  printf("Caso arbol de un nodo con c='a'\n");
  {
    Nodo *a= abb('a', NULL, NULL);
    Nodo *ref_a= copia(a);
    int k= selprim(&a, 10);
    revisar_abb(a, ref_a);
    revisar_int(k, 1);
    k= selprim(&a, 0);
    revisar_abb(a, NULL);
    revisar_int(k, 0);
    liberar(ref_a);
  }

  printf("Caso arbol 'b' con subnodo 'a' la izquierda\n");
  {
    Nodo *ab= abb('b', abb('a', NULL,NULL), NULL);
    Nodo *ref_a= abb('a', NULL, NULL);
    Nodo *ref_ab= copia(ab);
    Nodo *ab2= copia(ab);
    int k= selprim(&ab, 2);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 2);
    k= selprim(&ab, 1);
    revisar_abb(ab, ref_a);
    revisar_int(k, 1);
    k= selprim(&ab2, 0);
    revisar_abb(ab2, NULL);
    revisar_int(k, 0);
    liberar(ref_a);
    liberar(ref_ab);
    liberar(ab);
  }
    
  printf("Caso arbol 'a' con subnodo 'b' a la derecha\n");    
  {
    Nodo *ab= abb('a', NULL, abb('b', NULL,NULL));
    Nodo *ref_a= abb('a', NULL, NULL);
    Nodo *ref_ab= copia(ab);
    Nodo *ab2= copia(ab);
    int k= selprim(&ab, 2);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 2);
    k= selprim(&ab, 1);
    revisar_abb(ab, ref_a);
    revisar_int(k, 1);
    k= selprim(&ab2, 0);
    revisar_abb(ab2, NULL);
    revisar_int(k, 0);
    liberar(ref_a);
    liberar(ref_ab);
    liberar(ab);
  }
    
  printf("Caso arbol 'b' con subnodo izquierdo 'a' y subnodo derecho 'c'\n");
  {
    Nodo *abc= abb('b', abb('a',NULL, NULL), abb('c', NULL,NULL));
    Nodo *ref_a= abb('a', NULL, NULL);
    Nodo *ref_ab= abb('b', abb('a', NULL, NULL), NULL);
    Nodo *ref_abc= copia(abc);
    Nodo *abc2= copia(abc);
    Nodo *abc3= copia(abc);
    int k= selprim(&abc, 9);
    revisar_abb(abc, ref_abc);
    revisar_int(k, 3);
    k= selprim(&abc, 2);
    revisar_abb(abc, ref_ab);
    revisar_int(k, 2);
    k= selprim(&abc2, 1);
    revisar_abb(abc2, ref_a);
    revisar_int(k, 1);
    k= selprim(&abc3, 0);
    revisar_abb(abc3, NULL);
    revisar_int(k, 0);
    liberar(ref_abc);
    liberar(ref_ab);
    liberar(ref_a);
    liberar(abc);
    liberar(abc2);
  }

  {
    printf("Caso abb del enunciado\n");
    Nodo *a= abb('v',
               abb('s',
                 abb('r', NULL, NULL),
                 abb('u', abb('t', NULL, NULL), NULL) ),
               abb('x', abb('w', NULL, NULL), NULL) );
    Nodo *a_ref= copia(a);
    Nodo *b_ref= abb('s', abb('r', NULL, NULL), abb('t', NULL, NULL));
    int k= selprim(&a, 20);
    revisar_abb(a, a_ref);
    revisar_int(k, 7);
    k= selprim(&a, 3);
    revisar_abb(a, b_ref);
    revisar_int(k, 3);
    liberar(a);
    liberar(a_ref);
    liberar(b_ref);
  }

  {
    int n= 100;
    printf("Caso abbs de %d nodos, equilibrado, desequilibrado por izquierda "
           "y derecha\n", n);
    Nodo *equilib= equilibrado(1, n);
    Nodo *deseq_izq= desequilibrado_izq(1, n);
    Nodo *deseq_der= desequilibrado_der(1, n);
    for (int z=0; z<=n; z++) {
      Nodo *a= copia(equilib);
      int k= selprim(&a, z);
      revisar_int(k, z);
      revisar_int(revisar_campos(a, 1), z+1);
      liberar(a);

      a= copia(deseq_izq);
      k= selprim(&a, z);
      revisar_int(k, z);
      revisar_int(revisar_campos(a, 1), z+1);
      liberar(a);

      a= copia(deseq_der);
      k= selprim(&a, z);
      revisar_int(k, z);
      revisar_int(revisar_campos(a, 1), z+1);
      liberar(a);
    }
    liberar(equilib);
    liberar(deseq_izq);
    liberar(deseq_der);
  }

  printf("=============================\n");
  printf("Tests de la funcion ultimos\n");
  printf("=============================\n\n");

 {
    printf("Caso arbol nulo\n");
    Nodo *a= NULL;
    int k= 3;
    Nodo *r= ultimos(a, &k);
    revisar_abb(r, NULL);
    revisar_int(k, 0);
  }

  printf("Caso arbol de un nodo con c='a'\n");
  {
    Nodo *a= abb('a', NULL, NULL);
    Nodo *ref_a= copia(a);
    int k= 10;
    Nodo *r= ultimos(a, &k);
    revisar_abb(a, ref_a);
    revisar_abb(r, ref_a);
    revisar_int(k, 1);
    liberar(r);

    k= 0;
    r= ultimos(a, &k);
    revisar_abb(a, ref_a);
    revisar_abb(r, NULL);
    revisar_int(k, 0);
    liberar(ref_a);
    liberar(a);
  }

  printf("Caso arbol 'b' con subnodo 'a' la izquierda\n");
  {
    Nodo *ab= abb('b', abb('a', NULL,NULL), NULL);
    Nodo *ref_b= abb('b', NULL, NULL);
    Nodo *ref_ab= copia(ab);
    int k= 2;
    Nodo *r= ultimos(ab, &k);
    revisar_abb(r, ref_ab);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 2);
    liberar(r);

    k= 1;
    r= ultimos(ab, &k);
    revisar_abb(r, ref_b);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 1);
    liberar(r);

    k= 0;
    r= ultimos(ab, &k);
    revisar_abb(r, NULL);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 0);
    liberar(r);
    liberar(ref_b);
    liberar(ref_ab);
    liberar(ab);
  }

 printf("Caso arbol 'a' con subnodo 'b' a la derecha\n");
  {
    Nodo *ab= abb('a', abb('b', NULL,NULL), NULL);
    Nodo *ref_b= abb('a', NULL, NULL);
    Nodo *ref_ab= copia(ab);
    int k= 2;
    Nodo *r= ultimos(ab, &k);
    revisar_abb(r, ref_ab);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 2);
    liberar(r);

    k= 1;
    r= ultimos(ab, &k);
    revisar_abb(r, ref_b);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 1);
    liberar(r);

    k= 0;
    r= ultimos(ab, &k);
    revisar_abb(r, NULL);
    revisar_abb(ab, ref_ab);
    revisar_int(k, 0);
    liberar(r);
    liberar(ref_b);
    liberar(ref_ab);
    liberar(ab);
  }

  printf("Caso arbol 'b' con subnodo izquierdo 'a' y subnodo derecho 'c'\n");
  {
    Nodo *abc= abb('b', abb('a',NULL, NULL), abb('c', NULL,NULL));
    Nodo *ref_c= abb('c', NULL, NULL);
    Nodo *ref_bc= abb('b', NULL, abb('c', NULL, NULL));
    Nodo *ref_abc= copia(abc);
    int k= 9;
    Nodo *r= ultimos(abc, &k);
    revisar_abb(abc, ref_abc);
    revisar_abb(r, ref_abc);
    revisar_int(k, 3);
    liberar(r);

    k= 2;
    r= ultimos(abc, &k);
    revisar_abb(r, ref_bc);
    revisar_abb(abc, ref_abc);
    revisar_int(k, 2);
    liberar(r);

    k= 1;
    r= ultimos(abc, &k);
    revisar_abb(r, ref_c);
    revisar_abb(abc, ref_abc);
    revisar_int(k, 1);
    liberar(r);

    k= 0;
    r= ultimos(abc, &k);
    revisar_abb(r, NULL);
    revisar_abb(abc, ref_abc);
    revisar_int(k, 0);
    liberar(r);

    liberar(abc);
    liberar(ref_c);
    liberar(ref_bc);
    liberar(ref_abc);
  }

  {
    printf("Caso abb del enunciado\n");
    Nodo *a= abb('v',
               abb('s',
                 abb('r', NULL, NULL),
                 abb('u', abb('t', NULL, NULL), NULL) ),
               abb('x', abb('w', NULL, NULL), NULL) );
    Nodo *a_ref= copia(a);
    Nodo *b_ref= abb('v',
                   abb('u', NULL, NULL),
                   abb('x', abb('w', NULL,NULL), NULL) );
    int k= 20;
    Nodo *r= ultimos(a, &k);
    revisar_abb(r, a_ref);
    revisar_abb(a, a_ref);
    revisar_int(k, 7);
    liberar(r);

    k= 4;
    r= ultimos(a, &k);
    revisar_abb(r, b_ref);
    revisar_abb(a, a_ref);
    revisar_int(k, 4);
    liberar(r);
    liberar(a);
    liberar(a_ref);
    liberar(b_ref);
  }

  {
    int n= 100;
    printf("Caso arboles de %d nodos, equilibrado, desequilibrado por "
           "izquierda y derecha\n", n);
    Nodo *equilib= equilibrado(1, n);
    Nodo *ref_equilib= copia(equilib);
    Nodo *deseq_izq= desequilibrado_izq(1, n);
    Nodo *ref_deseq_izq= copia(deseq_izq);
    Nodo *deseq_der= desequilibrado_der(1, n);
    Nodo *ref_deseq_der= copia(deseq_der);
    for (int z=1; z<=n; z++) {
      int k= z;
      Nodo *r= ultimos(equilib, &k);
      revisar_int(revisar_campos(r, n-z+1), n+1);
      revisar_abb(equilib, ref_equilib);
      revisar_int(k, z);
      liberar(r);

      k= z;
      r= ultimos(deseq_izq, &k);
      revisar_int(revisar_campos(r, n-z+1), n+1);
      revisar_abb(deseq_izq, ref_deseq_izq);
      revisar_int(k, z);
      liberar(r);

      k= z;
      r= ultimos(deseq_der, &k);
      revisar_int(revisar_campos(r, n-z+1), n+1);
      revisar_abb(deseq_der, ref_deseq_der);
      revisar_int(k, z);
      liberar(r);
    }
    liberar(equilib);
    liberar(ref_equilib);
    liberar(deseq_izq);
    liberar(ref_deseq_izq);
    liberar(deseq_der);
    liberar(ref_deseq_der);
  }

#ifdef OPT
#define N1 25000
#define N2 10000

  printf("\n==================================\n");
  printf(  "Benchmark de selprim\n");
  printf(  "==================================\n\n");

#else

#define N1 2000
#define N2 1400

#endif

  int tiempo_selprim;

  {
    int n= N1;
    printf("arbol de %d nodos\n", n);
    Nodo *equilib= equilibrado(1, n);
    Nodo *deseq_izq= desequilibrado_izq(1, n);
    Nodo *deseq_der= desequilibrado_der(1, n);
    resetTime();
    for (int z=n; z>=0; z--) {
      int k= selprim(&equilib, z);
      revisar_int(k, z);
      k= selprim(&deseq_izq, z);
      revisar_int(k, z);
      k= selprim(&deseq_der, z);
      revisar_int(k, z);
    }

    tiempo_selprim= getTime();
    liberar(equilib);
    liberar(deseq_izq);
    liberar(deseq_der);
    if (tiempo_selprim!=0) {
      printf("Tiempo selprim = %d milisegundos\n", tiempo_selprim);
    }
  }

#ifdef OPT
  printf("\n======================\n");
  printf(  "Benchmark de ultimos\n");
  printf(  "======================\n\n");
#endif

  int tiempo_ultimos;

  {
    int n= N2;
    printf("arbol de %d nodos\n", n);
    Nodo *equilib= equilibrado(1, n);
    Nodo *deseq_izq= desequilibrado_izq(1, n);
    Nodo *deseq_der= desequilibrado_der(1, n);
    resetTime();
    for (int z=n; z>=0; z--) {
      int k= z;
      Nodo *r= ultimos(equilib, &k);
      liberar(r);
      revisar_int(k, z);
      r= ultimos(deseq_izq, &k);
      liberar(r);
      revisar_int(k, z);
      r= ultimos(deseq_der, &k);
      liberar(r);
      revisar_int(k, z);
    }

    tiempo_ultimos= getTime();
    liberar(equilib);
    liberar(deseq_izq);
    liberar(deseq_der);
    if (tiempo_ultimos!=0) {
      printf("Tiempo ultimos = %d milisegundos\n", tiempo_ultimos);
    }
  }

 if (argc>=2) {
    if (strcmp(argv[1], "ref")==0) {
      FILE *out= fopen("tiempo-ref.txt", "w");
      if (out==NULL) {
        perror("tiempo-ref.txt");
        exit(1);
      }
      fprintf(out, "%d %d\n", tiempo_selprim, tiempo_ultimos);
      fclose(out);
    }
    else if (argc>=3) {
      int tiempo_selprim_ref= atoi(argv[1]);
      int tiempo_ultimos_ref= atoi(argv[2]);
      double q= (double)tiempo_selprim/(double)tiempo_selprim_ref;
      int porciento= (q-1.)*100+0.5;
      printf("Tiempo de referencia para selprim = %d milisegundos\n",
             tiempo_selprim_ref);
      printf("Porcentaje de sobrecosto de selprim: %d %%\n",
             porciento);
      if (porciento>80) {
        fflush(stdout);
        fprintf(stderr, "Lo siento: su solucion es demasiado lenta\n");
        exit(1);
      }
      q= (double)tiempo_ultimos/(double)tiempo_ultimos_ref;
      porciento= (q-1.)*100+0.5;
      printf("Tiempo de referencia para ultimos = %d milisegundos\n",
             tiempo_ultimos_ref);
      printf("Porcentaje de sobrecosto de ultimos: %d %%\n", porciento);
      if (porciento>80) {
        fflush(stdout);
        fprintf(stderr, "Lo siento: su solucion es demasiado lenta\n");
        exit(1);
      }
    }
  }

#ifdef OPT
  printf("Felicitaciones: su solucion es correcta y eficiente\n");
#else
  printf("Felicitaciones: su solucion es correcta\n");
#endif

  return 0;
}
