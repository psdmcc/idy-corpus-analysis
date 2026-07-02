#!/bin/bash
# Remove temporary files that cause runaway argument crashes
rm -f main.aux main.toc main.log main.out main.blg main.bbl

# Compile pipeline
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# ... (your existing compilation steps) ...
pdflatex -interaction=nonstopmode main.tex

echo "🚀 Compiling complete! Syncing with GitHub..."
git add .
git commit -m "Auto-update build: $(date)"
git push origin main
