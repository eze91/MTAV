all:
	make -C swig all
	cp swig/glpkpi.py python/glpkpi.py
	python setup.py build

install: all
	python setup.py install

clean:
	make -C swig clean
	rm -rf build
	rm -f *.pyc *.pyo _glpkpi.so glpkpi.py
	rm -f python/*.pyc python/*.pyo python/_glpkpi.so python/glpkpi.py

.PHONY: all install clean
