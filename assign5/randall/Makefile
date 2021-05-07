# Make x86-64 random byte generators.

# Copyright 2015, 2020 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE =

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --xz --transform 's,^,randall/,'
TAREXT = txz

default: randall

check: randall test_script.sh
	./test_script.sh

randall: randall.c options.o output.o rand64-hw.o rand64-sw.o mrand_rand64.o
	$(CC) $(CFLAGS) $@.c options.o output.o rand64-hw.o rand64-sw.o mrand_rand64.o -o$@

options.o: options.c options.h
	$(CC) $(CFLAGS) -c options.c

output.o: output.c output.h
	$(CC) $(CFLAGS) -c output.c

rand64-hw.o: rand64-hw.c rand64-hw.h
	$(CC) $(CFLAGS) -c rand64-hw.c

rand64-sw.o: rand64-sw.c rand64-sw.h
	$(CC) $(CFLAGS) -c rand64-sw.c

mrand_rand64.o: mrand_rand64.c mrand_rand64.h
	$(CC) $(CFLAGS) -c mrand_rand64.c

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c options.c options.h output.c output.h \
	rand64-hw.c rand64-hw.h rand64-sw.c rand64-sw.h mrand_rand64.c mrand_rand64.h \
	notes.txt test_script.sh input
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt # More files should be listed here, as needed.
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

.PHONY: default clean assignment submission

clean:
	rm -f options.o output.o rand64-hw.o rand64-sw.o mrand_rand64.o randall
