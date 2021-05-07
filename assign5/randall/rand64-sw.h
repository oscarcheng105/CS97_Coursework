#ifndef RAND64_SW
#define RAND64_SW

#include <stdio.h>
#include <stdlib.h>

extern char* filename;
extern FILE *urandstream;

void software_rand64_init (void);
unsigned long long software_rand64 (void);
void software_rand64_fini (void);

#endif