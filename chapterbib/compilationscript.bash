pdflatex main
for i in `ls *.aux`; do bibtex $i; done
pdflatex main
pdflatex main
