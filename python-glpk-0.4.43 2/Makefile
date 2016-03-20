DIR := $(shell basename `pwd`)

deb:	clean
	debuild

new:	clean
	rm -rf debian
	( cd .. && pwd && tar zcvf $(DIR).tar.gz $(DIR)/* )
	cp -p ../$(DIR).tar.gz ../$(DIR).orig.tar.gz

web:	deb
	cp -p ../$(DIR).tar.gz ~/public_html/code/python-glpk
	cp -p ../$(DIR)-*.deb ~/public_html/code/python-glpk

clean:
	make -C src clean

.PHONY: install new deb web clean

