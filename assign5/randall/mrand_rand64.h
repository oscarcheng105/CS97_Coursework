#ifndef MRAND_RAND64
#define MRAND_RAND64

#include <stdlib.h>
#include <time.h>

void mrand_rand64_init(void);
unsigned long long mrand_rand64(void);
void mrand_rand64_fini(void);

#endif