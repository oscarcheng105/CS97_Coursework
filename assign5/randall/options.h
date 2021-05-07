#ifndef OPTIONS_FILE
#define OPTIONS_FILE

#include <stdbool.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <cpuid.h>
#include <unistd.h>

/* Description of the current CPU.  */
struct cpuid { unsigned eax, ebx, ecx, edx; };

struct options {
  bool valid;
  long long nbytes;
  bool iflag;
  char *option1;
  bool oflag;
  char *option2;
};

void parseOptions(int argc, char **argv, struct options* opt);
_Bool rdrand_supported (void);
struct cpuid cpuid (unsigned int leaf, unsigned int subleaf);

#endif