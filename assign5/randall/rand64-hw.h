#ifndef RAND64_HW
#define RAND64_HW

#include <immintrin.h>

void hardware_rand64_init (void);
unsigned long long hardware_rand64 (void);
void hardware_rand64_fini (void);

#endif