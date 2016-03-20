PYVERS := 'python2.7'
DIR := $(shell basename `pwd`)

all:	_glpkpi.so glpkpi.py

glpkpi.py:	glpkpi.i glpkpi.c glpkpi.h Makefile
	swig -python  glpkpi.i
	sed -i 's/:in /:_in /g' glpkpi.py

_glpkpi.so:	glpkpi.py glpkpi.o glpkpi_wrap.o
	gcc -Wall -shared glpkpi.o  glpkpi_wrap.o -lm -lglpk  -o _glpkpi.so

glpkpi.o:	glpkpi.c
	gcc -Wall -c -fPIC glpkpi.c -DHAVE_CONFIG_H -I/usr/include/$(PYVERS) -I/usr/lib/$(PYVERS)/config
glpkpi_wrap.o:	glpkpi_wrap.c
	gcc -Wall -c -fPIC glpkpi_wrap.c -DHAVE_CONFIG_H -I/usr/include/$(PYVERS) -I/usr/lib/$(PYVERS)/config
glpkpi_wrap.c:	glpkpi.i glpkpi.c glpkpi.h Makefile
	swig -python  glpkpi.i

clean:
	rm -f *.o *~ *.pyc *.pyo _*.so glpkpi_wrap.c glpkpi.py

