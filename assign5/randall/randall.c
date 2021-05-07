/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <string.h>
#include <ctype.h>

#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include "mrand_rand64.h"

/*outputs N bytes of random data.*/

int main (int argc, char **argv)
{
  struct options opt = {
    .valid = false,
    .nbytes = 0,
    .iflag = false,
    .option1 = NULL,
    .oflag = false,
    .option2 = NULL
  };
  
  parseOptions(argc, argv, &opt);

  if (!opt.valid)
    {
      fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      return 1;
    }

  //If there's no work to do, don't worry about which library to use.
  if (opt.nbytes == 0)
    return 0;

  /*Now that we know we have work to do, arrange to use the
     appropriate library.*/
  void (*initialize) (void) = NULL;
  unsigned long long (*rand64) (void) = NULL;
  void (*finalize) (void) = NULL;

  if(opt.iflag)
  {
    const char* hardware = "rdrand";
    const char* mrand = "mrand48_r";
    if(strcmp(opt.option1, hardware) == 0)
    {
      if(rdrand_supported())
      {
        initialize = hardware_rand64_init;
        rand64 = hardware_rand64;
        finalize = hardware_rand64_fini;
      }
      else
      {
        perror("Error: rdrand not supported\n");
        exit(1);
      }

    }
    else if(strcmp(opt.option1, mrand) == 0)
    {
      initialize = mrand_rand64_init;
      rand64 = mrand_rand64;
      finalize = mrand_rand64_fini;
    }
    else if(opt.option1)
    {
      filename = opt.option1;
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }
    else
    {
      perror("Error: input flag error\n");
      exit(1);
    }
  }
  else if (rdrand_supported ())
  {
      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
  }
  else
  {
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
  }


  initialize ();
  int wordsize = sizeof rand64 ();
  int output_errno = 0;

  const char* def = "stdio";

  if((opt.oflag && strcmp(opt.option2, def)==0) || !opt.oflag)
  {
    do
      {
        unsigned long long x = rand64 ();
        int outbytes = opt.nbytes < wordsize ? opt.nbytes : wordsize;
        if (!writebytes (x, outbytes))
        {
          output_errno = errno;
          break;
        }
        opt.nbytes -= outbytes;
      }
    while (0 < opt.nbytes);
  }
  else if(opt.oflag)
  {
    for(int i=0; opt.option2[i]!='\0';i++)
    {
      if(isdigit(opt.option2[i]) == 0)
      {
        perror("Error: N flag needs to be digit\n");
        exit(1);
      }
    }
    bytesWritten(rand64,opt.nbytes,atoi(opt.option2));
  }

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}