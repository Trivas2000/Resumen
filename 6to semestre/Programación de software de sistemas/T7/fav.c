#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "fav.h"



int favorables_par(int n, int sum, int rep, int p) {
  int sons[p];//Crearemos p procesos hijos
  int fds[p][2];//Para las p pipes
  int repHijos=rep/p; //Cuanto debe revisar cada hijo
 
  for (int i=0; i<p; i++) {
    pipe(fds[i]);
    init_rand_seed();
    sons[i] = fork();

    if (sons[i] == 0) {
      close(fds[i][0]);  
      int sumaHijo=favorables(n,sum,repHijos);

      write(fds[i][1], &sumaHijo, sizeof(int));
      exit(0);
    }

    else {
      close(fds[i][1]);
    }
  }
  int res=0;
  for (int i=0; i<p; i++) {
    waitpid(sons[i],NULL,0);
    int res_hijo;
    read(fds[i][0], &res_hijo, sizeof(int));
    res+=res_hijo;
  
  }

  return res;
}
