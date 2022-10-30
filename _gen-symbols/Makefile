.PHONY: all
all: fraction.html
fraction.html: fraction.tex latexml.preamble.tex latexml.postamble.tex Makefile
	latexmlc fraction.tex --dest=$@ --preamble=latexml.preamble.tex --postamble=latexml.postamble.tex