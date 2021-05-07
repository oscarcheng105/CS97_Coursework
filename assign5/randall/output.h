#ifndef OUTPUT_FILE
#define OUTPUT_FILE

#include <stdbool.h>
#include <stdio.h>
#include <limits.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

bool writebytes (unsigned long long x, int nbytes);
void bytesWritten(unsigned long long (*r) (void), int required, int bufferSize);

#endif