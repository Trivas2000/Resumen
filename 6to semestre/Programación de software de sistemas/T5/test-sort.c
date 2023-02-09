#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "sort.h"

void resultados(char *s, char *r) {
  printf("Resultado: \"%s\" \"%s\"\n", s, r);
}

int main(int argc, char *argv[]) {
  if (argc==1) {

    printf("Un arreglo bien ordenado: \"a\" \"a\"\n");
    char *strs[]= {"a", "a"};
    sort(strs, 2);
    resultados(strs[0], strs[1]);
    if (strcmp(strs[0], "a")!=0 || strcmp(strs[1], "a")!=0) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

    printf("Otro arreglo bien ordenado: \"a\" \"a a\"\n");
    char *strs2[]= {"a", "a a"};
    sort(strs2, 2);
    resultados(strs2[0], strs2[1]);
    if (strcmp(strs2[0], "a")!=0 || strcmp(strs2[1], "a a")!=0) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

    printf("Un arreglo desordenado: \"a a\" \"a\"\n");
    char *strs3[]= {"a a", "a"};
    sort(strs3, 2);
    resultados(strs3[0], strs3[1]);
    if (strcmp(strs3[0], "a")!=0 || strcmp(strs3[1], "a a")!=0) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

    printf("Otro arreglo desordenado: \"abcd efgh\" \"abcdefgh\"\n");
    char *strs3b[]= {"abcd efgh", "abcdefgh"};
    sort(strs3b, 2);
    resultados(strs3b[0], strs3b[1]);
    if ( strcmp(strs3b[0], "abcdefgh")!=0 ||
         strcmp(strs3b[1], "abcd efgh")!=0 ) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

    printf("Otro arreglo desordenado: \"abc d ef ghi jklm\" "
                                     "\"abcd efghijklm\"\n");
    char *strs3c[]= {"abc d ef ghi jklm", "abcd efghijklm"};
    sort(strs3c, 2);
    resultados(strs3c[0], strs3c[1]);
    if ( strcmp(strs3c[0], "abcd efghijklm")!=0 ||
         strcmp(strs3c[1], "abc d ef ghi jklm")!=0 ) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

    printf("Arreglo con 3 strings desordenados: \"ab bcd e\" \"a\", \"a a\"\n");
    char *strs4[] = {"ab bcd e", "a", "a a"};
    sort(strs4, 3);
    printf("Resultado: \"%s\" \"%s\" \"%s\"\n", strs4[0], strs4[1], strs4[2]);
    if ( strcmp(strs4[0], "a")!=0 ||
         strcmp(strs4[1], "a a")!=0 ||
         strcmp(strs4[2], "ab bcd e")!=0 ) {
      fprintf(stderr, "El resultado es incorrecto\n");
      exit(1);
    }

  }

  printf("Ahora un arreglo de 10 strings\n");
  char *strs10[]= {
                 "ab cde fghi", // 2
                 "abc def gh ij kl", // 4
                 "yz", // 0
                 "mno q r s t v wxy", // 6
                 "d e f g h i j k l m", // 9
                 "l m", // 1
                 "z y x w", // 3
                 "j k l m n o p q r", // 8
                 "s t u v w ", // 5
                 " c d e f g h " // 7
               };

  char *refs[]= {
                 "yz", // 0
                 "l m", // 1
                 "ab cde fghi", // 2
                 "z y x w", // 3
                 "abc def gh ij kl", // 4
                 "s t u v w ", // 5
                 "mno q r s t v wxy", // 6
                 " c d e f g h ", // 7
                 "j k l m n o p q r", // 8
                 "d e f g h i j k l m", // 9
               };

  printf("El arreglo desordenado es:\n");
  printf("--------------------------\n");
  for (int i= 0; i<10; i++) {
    printf("%s\n", strs10[i]);
  }
  sort(strs10, 10);
  printf("\n");
  printf("El arreglo ordenado es:\n");
  printf("-----------------------\n");
  for (int i= 0; i<10; i++) {
    printf("%s\n", strs10[i]);
  }
  for (int i= 0; i<10; i++) {
    if (strcmp(strs10[i],refs[i])!=0) {
      fprintf(stderr, "El %d-esimo elemento es incorrecto\n", i);
      exit(1);
    }
  }

  printf("Felicitaciones: test de prueba aprobado\n");
  return 0;
}
