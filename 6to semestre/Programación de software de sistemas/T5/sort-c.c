#include <string.h>

void sort(char **noms, int n) {
  char **ult= &noms[n-1];
  char **p= noms;
  while (p<ult) {
    ////////////////////////////////////////////
    // Comienza el codigo que Ud. debe modificar
    ////////////////////////////////////////////
 
    int rc= strcmp(p[0], p[1]);

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
