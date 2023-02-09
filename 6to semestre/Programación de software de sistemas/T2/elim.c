#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "elim.h"

void eliminar_espacios(char *s) {
 char *p1=s;
 char *p2=s;
 int leftIsSpace=0; //0 si el de la izq no es espacio, 1 si lo es
 while(*p2!='\0') {
  if( leftIsSpace && *p2 == ' ' ) {
   p2++;
  }
  else {
    *p1=*p2;
    p1++; 
    leftIsSpace=0; 
    if( *p2 == ' ' ) {
      leftIsSpace=1;
    }
    p2++;
  }
 }
 *p1=*p2;
}

 char *eliminacion_espacios(const char *s) {
  char *copia = malloc(strlen(s) + 1);
  strcpy(copia, s);
  eliminar_espacios(copia);


  char *copia2 = malloc(strlen(copia) + 1);
  strcpy(copia2, copia);
  free(copia);
  return copia2; 
 }


