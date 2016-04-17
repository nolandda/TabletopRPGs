LATEX = latex
PS2PDF = ps2pdf
DVIPS = dvips

# Makefile for Dan Noland's Resume

all: document.pdf charsheet.pdf


%.pdf %.aux %.idx: %.tex
	pdflatex $<
	while grep 'Rerun to get ' $*.log ; do pdflatex $< ; done

clean:
	rm -f *.dvi *.aux *.log *.pdf *.ps *.out
