# .latexmkrc configuration
$pdflatex = 'pdflatex -interaction=nonstopmode %O %S';

# Automatically clean up specific extensions after a successful build
$cleanup_mode = 1; 
@generated_exts = (@generated_exts, 'aux', 'toc', 'out', 'log');
