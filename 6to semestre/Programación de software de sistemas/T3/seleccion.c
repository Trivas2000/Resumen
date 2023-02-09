#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "seleccion.h"


int selprim(Nodo **pa, int k) {

  if (*pa==NULL){ //caso base
    return 0;
  }

  Nodo **izq=&(*pa)->izq;
  if (k==0){ //caso base
    Nodo **der=&(*pa)->der;
    int a = selprim(der,0)+selprim(izq,0);
    Nodo* copy=*pa;
    *pa=(*pa)->izq;
    free(copy);
    return a;
  }
  
  int seleccionados=selprim(izq,k); //correr arbol izq
  if (seleccionados==k){
    //liberar nodo actual falta
    Nodo **der=&(*pa)->der;
    selprim(der,0); //liberar parte derecha
    Nodo* copy=*pa;
    *pa=(*pa)->izq;
    free(copy);
    return k;
  }

  else {
    Nodo **der=&(*pa)->der;
    return 1 + selprim(der,k-seleccionados-1) + seleccionados;  //faltan nodos hay q buscarlos
  } 
  
}

Nodo *ultimos(Nodo *a, int *pk) {
  
  if(a==NULL){
   *pk=0;
   Nodo* result=NULL;
   return result;
  }

  int totalDer=*pk;

  Nodo* resder=ultimos(a->der,&totalDer);

  int totalIzq=*pk-totalDer-1;


  if(totalDer==*pk){
    return resder;
  }
  
  else if((totalDer+1)==*pk){
    Nodo* copy=malloc(sizeof(*copy));
    copy->der=resder;
    copy->x=a->x;
    copy->izq=NULL;
    *pk=totalDer+1;
    return copy;

  }

  else{
    Nodo* copy=malloc(sizeof(*copy));
    Nodo *resizq=ultimos(a->izq,&totalIzq);
    copy->izq=resizq;
    copy->der=resder;
    copy->x=a->x;
    *pk=totalDer+totalIzq+1;
    return copy;
  }
  
}