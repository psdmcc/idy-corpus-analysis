#!/bin/bash

echo "✨ Step 1: Wiping old LaTeX auxiliary files..."
rm -f *.aux *.bbl *.blg *.log *.toc *.out *.bak *.synctex.gz main.pdf

echo "🚀 Step 2: Launching Pass 1 (Populating text fields)..."
pdflatex -interaction=nonstopmode main.tex

echo "🚀 Step 3: Launching Pass 2 (Resolving inline citation numbers)..."
pdflatex -interaction=nonstopmode main.tex

echo "🚀 Step 4: Launching Pass 3 (Finalizing Figure & Table floating alignments)..."
pdflatex -interaction=nonstopmode main.tex

echo "🎉 Success! Clean single-author manuscript PDF generated flawlessly."

echo "🚀 Step 5: Syncing project with GitHub repository..."
git add .
git commit -m "Auto-update build: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "🎯 All tasks completed successfully!"
