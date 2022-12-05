.DEFAULT_GOAL := build 
.PHONY: build  clean wheel

#virtual environments are not relocatable, so we must create it where we want it installed
IDIR := /git/Fesp/venv

$(IDIR):
	#create virtual environment
	python3.8 -m venv $(IDIR) 

dist/Fesp*whl: | $(IDIR)
	$(IDIR)/bin/pip install -U pip build
	$(IDIR)/bin/python -m build .

# make target that can be invoked from command line, for testing
wheel: dist/Fesp*whl

$(IDIR)/lib/python3.8/site-packages/attrdict:
	$(IDIR)/bin/pip install -r prerequirements.txt

$(IDIR)/bin/Fesp:  dist/Fesp*whl | $(IDIR)/lib/python3.8/site-packages/attrdict
	$(IDIR)/bin/pip install --force-reinstall dist/Fesp-*.whl

# we can't (or don't know how to) override rules because we have two debian/*install files,
# so copy virtual environment into local directory should dh_install can find it
fesp: | $(IDIR)/bin/Fesp 
	cp -r $(IDIR) fesp

fesp/FespReadme.txt: | fesp
	cp src/fesp/FespReadme.txt fesp

fesp/FespSettings.txt: | fesp
	cp src/fesp/FespSettings.txt fesp

fesp/examples: | fesp
	cp -r src/fesp/examples fesp

fesp/scripts: | fesp
	cp -r src/fesp/scripts fesp

build: fesp/FespReadme.txt fesp/FespSettings.txt fesp/examples fesp/scripts

	
clean:
	rm -fr $(IDIR)  dist fesp
	
