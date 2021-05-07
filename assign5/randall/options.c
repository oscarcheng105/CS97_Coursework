#include "options.h"

void parseOptions(int argc, char **argv, struct options* opt)
{
  int option;
  while((option = getopt(argc, argv, "i:o:"))!= -1)
  {
    switch(option)
    {
      case 'i': opt->iflag = true;
                opt->option1 = optarg; break;
      case 'o': opt->oflag = true;
                opt->option2 = optarg; break;
      default: exit(1);
    }
  }

  char *endptr;
  errno = 0;
  opt->nbytes = strtoll (argv[optind], &endptr, 10);
  if (errno)
	      perror (argv[optind]);
  else
	  opt->valid = !*endptr && 0 <= opt->nbytes;
}

/* Hardware implementation.  */

/* Return information about the CPU.  See <http://wiki.osdev.org/CPUID>.  */
struct cpuid cpuid (unsigned int leaf, unsigned int subleaf)
{
  struct cpuid result;
  asm ("cpuid"
       : "=a" (result.eax), "=b" (result.ebx),
	 "=c" (result.ecx), "=d" (result.edx)
       : "a" (leaf), "c" (subleaf));
  return result;
}

/* Return true if the CPU supports the RDRAND instruction.  */
_Bool rdrand_supported (void)
{
  struct cpuid extended = cpuid (1, 0);
  return (extended.ecx & bit_RDRND) != 0;
}