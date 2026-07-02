#!/bin/bash
# Remove temporary files that cause runaway argument crashes
rm -f main.aux main.toc main.log main.out main.blg main.bbl

# Compile pipeline
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
