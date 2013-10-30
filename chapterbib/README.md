Small example to successfully have an individual reference list (based on the
same bibliography file) for each chapter.

To make it work, change the `\cite` commands in each included file
([Introduction](introduction.tex), [Materials & Methods](material.tex),
[Results](results.tex) and [Discussion](discussion.tex)), supply your own
library.bib file in the `\bibliography{library.bib}` and typeset the
[main file](main.tex) with your preferred editor (or `pdftex main.tex` in the
terminal).

Then read page two for a small how-to (you have to run `bibtex` on each of the
`.aux` files for each chapter).
