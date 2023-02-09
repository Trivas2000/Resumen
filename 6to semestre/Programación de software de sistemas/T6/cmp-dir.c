#include <dirent.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <strings.h>
#include <stdbool.h>




int compararArchivosRegulares(char *A,char *B){
  struct stat statbufA; //Statbufs de A y B
  struct stat statbufB;
  stat(A,&statbufA); //Poner stats en buffers
  stat(B,&statbufB);
  int fileSize=statbufA.st_size;

  if (fileSize==statbufB.st_size){ //Si tienen el mismo tamaño
      char bufA[fileSize+1];
      int fdA = open(A,O_RDONLY); //Abrimos A
      
      if (fdA == -1) {
        perror(A);
        exit(1);
        return 1;
      }
      read(fdA,bufA,fileSize); //Leemos A
      close(fdA); //Cerramos A
      
      int fdB = open(B,O_RDONLY); //Abrimos B
      char bufB[fileSize+1];
      
      if (fdB == -1) {
        perror(B);
        exit(1);
        return 1;
      }
      read(fdB,bufB,fileSize); //Leemos B
      close(fdB); //Cerramos B
      int iguales=memcmp(bufA,bufB,fileSize);
      if (iguales==0){
        return 0; //Exito, ambos son iguales
      }

      else{
        printf("Contenidos de %s y %s difieren\n",A,B);
        return 1;
      }
  }
  printf("%s y %s son de distinto tamanno\n",A,B);
  return 2;
}


int comparadorGeneral(char *A,char *B){
  struct stat statbufA; //Statbufs de A y B
  struct stat statbufB;
  int seguirRevisando=0;

  int aexiste=stat(A,&statbufA); //Poner stats en buffers
  int bexiste=stat(B,&statbufB);
  
  int isAdir =S_ISDIR(statbufA.st_mode);
  int isBdir =S_ISDIR(statbufB.st_mode);

  if (!isAdir && !isBdir){  //Ambos no son directorios (Archivos regulares)
    if (aexiste!=0){
      printf("%s no existe\n",A);
      return 6;
    }
    else if (bexiste!=0){
      printf("%s si existe, %s no existe\n",A,B);
      return 7;
    }
    else{
      seguirRevisando=compararArchivosRegulares(A,B);
    }
  }

  else if (isAdir && !isBdir){ //A es directorio, B no
    if (aexiste!=0){
      printf("%s no existe\n",A);
      return 6;
    }
    else if (bexiste!=0){
      printf("%s si existe,%s no existe\n",A,B);
      return 7;
    }
    else{
      printf("%s es directorio, %s no es directorio\n",A,B);
      return 3;
    }
  }

  else if (!isAdir && isBdir){ //A no es directorio, B si
    if (aexiste!=0){
      printf("%s no existe\n",A);
      return 6;
    }
    else if (bexiste!=0){
      printf("%s si existe,%s no existe\n",A,B);
      return 7;
    }
    else{
      printf("%s no es directorio, %s si es directorio\n",A,B);
      return 4;
    }
  }

  else if (isAdir && isBdir){ //A y B son directorios

    struct stat st_nom;
    int rc;
    rc= stat(A, &st_nom);

    if (rc!=0) {
      printf("%s no existe\n", A);
      exit(0);
    }

    DIR *dir = opendir(A);
    if (dir == NULL) {
      perror(A);
      exit(1);
    }
  
    
    for (struct dirent *entry = readdir(dir);
      entry != NULL;
      entry = readdir(dir)) {
        if (strcmp(entry->d_name, ".")==0 || strcmp(entry->d_name, "..")==0) {
          continue;
        }
        char *nom_arch= malloc(strlen(A)+strlen(entry->d_name)+2);
        char *nom_archB= malloc(strlen(A)+strlen(entry->d_name)+2);

        strcpy(nom_arch, A);
        strcat(nom_arch, "/");
        strcat(nom_arch, entry->d_name);
        strcpy(nom_archB, B);
        strcat(nom_archB, "/");
        strcat(nom_archB, entry->d_name);
        seguirRevisando=comparadorGeneral(nom_arch,nom_archB);
        free(nom_arch);
        free(nom_archB);
        if(seguirRevisando!=0){
          break;
        }

      }
    
    closedir(dir);
    }
  
  return seguirRevisando;
}
  


int main(int argc, char *argv[]) {
  if (argc!=3) {
    fprintf(stderr, "uso: %s <arch|dir> <arch|dir>\n", argv[0]);
    exit(2);
  }
  int subconjunto=comparadorGeneral(argv[1],argv[2]); //Iniciamos la comparacion
  if (subconjunto==0){
      printf("Es subconjunto\n");
    }
  return 0;
}
