## Makefile based on https://github.com/kjhealy/pandoc-templates/blob/master/examples/starting_from_markdown/Makefile

## Define standard Markdown extension
MEXT = md

## All markdown files in the working directory
SRC = $(wildcard *.$(MEXT))

## Bibliography
BIB = /home/habi/P/Documents/library.bib

## Pandoc options to use
OPTIONS = markdown+simple_tables+table_captions+yaml_metadata_block+smart

## Get last commit hash
ID := $(shell git rev-parse --short HEAD)

## File names
PDFS=$(SRC:.md=.$(ID).pdf)
HTML=$(SRC:.md=.$(ID).html)
TEX=$(SRC:.md=.$(ID).tex)
DOCX=$(SRC:.md=.$(ID).docx)

## Targets
all:	$(PDFS) $(HTML) $(TEX) $(DOC)

pdf:	$(PDFS)
html:	$(HTML)
tex:	$(TEX)
doc:	$(DOCX)

%.$(ID).html: %.md
	pandoc -r $(OPTIONS) -w html5 -s --bibliography=$(BIB) -o $@ $<

%.$(ID).tex: %.md
	pandoc -r $(OPTIONS) -w latex -s --bibliography=$(BIB) -o $@ $<

%.$(ID).pdf: %.md
	pandoc -r $(OPTIONS) --bibliography=$(BIB) -o $@ $<
	
%.$(ID).docx: %.md
	pandoc -r $(OPTIONS) --bibliography=$(BIB) -o $@ $<

clean:
	rm *.html *.pdf *.tex *.docx
