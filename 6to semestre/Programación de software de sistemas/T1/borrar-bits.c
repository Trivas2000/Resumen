#include <stdio.h>
#include <stdlib.h>

#include "borrar-bits.h"

uint borrar_bits(uint x, uint pat, int len) {
  if( x == pat){  //Caso base 1, cuando x es igual al patron
    return 0;
  }
  if( len == 0){ //Caso base 2, cuando el largo del patron es 0
    return x;
  }
  unsigned mask = ~( ( ~0U ) << ( len-1 ) << 1); //Creamos la mascara
  int i = 0;
  while ( i <= 32-len ) {
    if( ( x & mask ) == pat ){  //Se revisa si el patron coincide
      x = x & ( ~mask );
      i+=len;
      pat = pat << ( len-1 ) <<1;
      mask = mask << ( len-1 ) << 1;
    }
    else{
      i+=1;
      pat<<=1;
      mask<<=1;
    }
  }
  return x; //Retornamos x
}
