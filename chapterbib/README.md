Small example to successfully have an individual reference list (based on *one* bibliography file) for each chapter.

On a *NIX-based system you should be able to just do `bash compilationscript.bash` to compile the example and read the resulting PDF file.
This runs `pdflatex` on the main file, calls `bibtex` for each of the chapter files and runs `pdflatex` several times afterwards.

Or you can read the resulting [PDF](main.pdf) which is present in this sub folder.
