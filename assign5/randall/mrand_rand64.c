#include "mrand_rand64.h"

void mrand_rand64_init(void)
{}

unsigned long long mrand_rand64(void)
{
    long int x;
    struct drand48_data buf = {0};
    srand48_r(time(NULL), &buf);
    mrand48_r(&buf, &x);
    unsigned long long y = x;
    return y;
}

void mrand_rand64_fini(void)
{}