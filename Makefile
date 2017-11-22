all:
	pdflatex document.tex

clean:
	rm -fv document.aux document.bbl document.blg document.log document.pdf
