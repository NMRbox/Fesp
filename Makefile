.DEFAULT_GOAL := build 
.PHONY: build  clean wheel

#virtual environments are not relocatable, so we must create it where we want it installed
IDIR := /usr/software/fesp

$(IDIR):
	#create virtual environment
	python3.8 -m venv $(IDIR) 

dist/Fesp*whl: | $(IDIR)
	$(IDIR)/bin/pip install -U pip build
	$(IDIR)/bin/python -m build .

# make target that can be invoked from command line, for testing
wheel: dist/Fesp*whl

/usr/software/fesp/lib/python3.8/site-packages/attrdict:
	$(IDIR)/bin/pip install -r prerequirements.txt

$(IDIR)/bin/Fesp:  dist/Fesp*whl | /usr/software/fesp/lib/python3.8/site-packages/attrdict
	$(IDIR)/bin/pip install --force-reinstall dist/Fesp-*.whl

# we can't (or don't know how to) override rules because we have two debian/*install files,
# so copy virtual environment into local directory should dh_install can find it
Fesp: | $(IDIR)/bin/Fesp 
	cp -r $(IDIR) Fesp

Fesp/fest.py: Fesp 
	ln 
build: Fesp 
	
clean:
	rm -fr $(IDIR)  dist
	
