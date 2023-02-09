#include <string.h>

void sort(char **noms, int n) {
  char **ult= &noms[n-1];
  char **p= noms;
  while (p<ult) {
    ////////////////////////////////////////////
    // Comienza el codigo que Ud. debe modificar
    ////////////////////////////////////////////
    int espaciosp0=0;
    int espaciosp1=0;
    char *a0 = p[0];
    char *a1 = p[1];

    while(*a0 != 0){ //Contamos espacios primera palabra
      if (*a0==' '){
        espaciosp0++;
      }
      a0++;
    }
    
    while(*a1 != 0){ //Contamos espacios segunda palabra
      if (*a1==' '){
        espaciosp1++;
      }
      a1++;
    }
    
    int rc= espaciosp0-espaciosp1;

    ////////////////////////////////////////////
    // Fin del codigo que Ud. debe modificar
    ////////////////////////////////////////////
    if (rc<=0)
      p++;
    else {
      char *tmp= p[0];
      p[0]= p[1];
      p[1]= tmp;
      p= noms;
    }
  }
}
