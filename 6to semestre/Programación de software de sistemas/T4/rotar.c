#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define SIZELIN 10

int main(int argc, char *argv[]){
  if (argc<=1) {
    fprintf(stderr, "Uso: %s <archivo> <l1> <l2> <l3> ...\n", argv[0]);
    
    exit(1);
  }
  char *nom= argv[1];  // El nombre del archivo
  // l0 es atoi(argv[2]), l1 es atoi(argv[3]), ..., ln es atoi(argv[argc-1])

  FILE *f = fopen(nom, "r+");
  int cont = 1;
  int offset;
  int poslo=10*atoi(argv[2]);
  char buf0[10]; //10 por caracteres + el final,  guardara lo q lee l0
  char bufn[10]; //10 por caracteres + el final,  guardara lo q lee ln
  if (argc==2 || argc==3){
    return 0;
  }
  while (cont!=argc-2){
    
    fseek(f,poslo,SEEK_SET); // 1 por SEEK_SET (Partir desde el principio)
    fread(&buf0,10,1,f);

    offset=10*atoi(argv[2+cont]);
    fseek(f,offset,SEEK_SET); // 1 por SEEK_SET (Partir desde el principio)
    fread(&bufn,10,1,f);
    
    fseek(f,offset,SEEK_SET); // 1 por SEEK_SET (Partir desde el principio)
    fwrite(&buf0 , 1 , sizeof(buf0) , f );

    fseek(f,poslo,SEEK_SET); // 1 por SEEK_SET (Partir desde el principio)
    fwrite(&bufn , 1 , sizeof(bufn) , f );
    cont++;
  }
  fclose(f);
  return 0;
}
