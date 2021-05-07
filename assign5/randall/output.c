
#include "output.h"

bool writebytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
	return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

void bytesWritten(unsigned long long (*r) (void),int required, int bufferSize)
{
  int total = 0;
  int index = 0;
  char* buf = malloc(bufferSize * sizeof(char));

  unsigned long long x = 0;
  int written = 0;
  //Generate random numbers and print them
  while (total<required)
  {
    x = r();

    if (total+bufferSize > required)
      bufferSize = required - total;

    while (x > 0 && index < bufferSize)
    {
      buf[index] = x;
      index += 1;
      x >>= 8;
    }

    if(index == bufferSize)
    {
      written = write(1,buf,bufferSize);
      total += written;
      index = 0;
    }
  }
}