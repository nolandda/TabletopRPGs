LATEX = latex
PS2PDF = ps2pdf
DVIPS = dvips

# Makefile for pdfs
.PHONY: all
all: document.pdf


%.pdf %.aux %.idx: %.tex
	pdflatex $<
	while grep 'Rerun to get ' $*.log ; do pdflatex $< ; done

clean:
	rm -f *.dvi *.aux *.log *.pdf *.ps *.out
