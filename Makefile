.PHONY: all clean fonts lint

LATEX ?= pdflatex

all: example.pdf

clean:
	latexmk -C

fonts:
	bin/get-solbera-fonts

lint:
	npx eclint check *.cls *.sty *.tex lib/

%.pdf: %.tex
	latexmk --interaction=nonstopmode --pdf --pdflatex=$(LATEX) $<
