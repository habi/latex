## Makefile based on http://git.io/GIs6og

## Define standard Markdown extension
MEXT = md

## All markdown files in the working directory
SRC = $(wildcard *.$(MEXT))

## Bibliography
BIB = /afs/psi.ch/user/h/haberthuer/Documents/library.bib

## Get last commit hash
ID := $(shell git log --oneline --no-color | cut -c -6 | head -n 1)

## File names
PDFS=$(SRC:.md=.pdf)
HTML=$(SRC:.md=.html)
TEX=$(SRC:.md=.tex)
DOC=$(SRC:.md=.docx)

## Targets
all:	$(PDFS) $(HTML) $(TEX) $(DOC)

pdf:	clean $(PDFS)
html:	clean $(HTML)
tex:	clean $(TEX)
doc:	clean $(DOC)

%.html:	%.md
	pandoc -w html5 -s -S --bibliography=$(BIB) -o $@ $<
	rename.ul .html _$(ID).html *.html

%.tex:	%.md
	pandoc -w latex -s -S --bibliography=$(BIB) -o $@ $<
	rename.ul .tex _$(ID).tex *.tex

%.pdf:	%.md
	pandoc -s -S --bibliography=$(BIB) -o $@ $<
	rename.ul .pdf _$(ID).pdf *.pdf

%.docx:	%.md
	pandoc -s -S --bibliography=$(BIB) -o $@ $<
	rename.ul .docx -$(ID).docx *.docx

clean:
	rm -f *.html *.pdf *.tex *.docx
