typedef struct nodo {
  int x;
  struct nodo *izq, *der;
} Nodo;

int selprim(Nodo **pa, int k);
Nodo *ultimos(Nodo *a, int *pk);
