PACKAGE = bookshelf

DIRS = doc scripts

# Default: build everything
all: ${PACKAGE}.cls bookshelf-svgnam.tex
	for dir in ${DIRS}; do cd $$dir; ${MAKE} $@; cd ..; done

# Build spines PDF from sample.bib
pdf: ${PACKAGE}.cls bookshelf-svgnam.tex
	cd doc && ${MAKE} spines.pdf

# Build SVG from PDF (requires inkscape)
svg: pdf
	cd doc && ${MAKE} bookshelf.svg

# Regenerate font files (run after TeX Live updates or font errors)
fonts:
	cd doc && $(RM) pickfont.tex allfonts && ${MAKE} allfonts pickfont.tex

%.cls: %.ins %.dtx
	pdflatex $<

bookshelf-svgnam.tex:
	./svgnam.sh > bookshelf-svgnam.tex
	$(RM) svgnam.csv

%.pdf: %.dtx
	xelatex $<
	- biber $<
	xelatex $<
	- makeindex -s gind.ist -o $*.ind $*.idx
	- makeindex -s gglo.ist -o $*.gls $*.glo
	xelatex $<
	while ( grep -q '^LaTeX Warning: Label(s) may have changed' $*.log) \
	do xelatex $<; done

# Clean intermediate files
clean:
	$(RM) *.aux *.log *.bbl *.blg *.cls *.dvi *~ pickfont.tex \
	*.bcf *.glo *.gls *.hd *.idx *.ilg *.ind *.our *.xml *.toc \
	*.out  *.pdf *.tgz svgnam.csv
	for dir in ${DIRS}; do cd $$dir; ${MAKE} $@; cd ..; done

# Deep clean including outputs
distclean: clean
	for dir in ${DIRS}; do cd $$dir; ${MAKE} $@; cd ..; done

archive: all clean
	COPYFILE_DISABLE=1 tar -C .. -czvf ../$(PACKAGE).tgz --exclude '*~' --exclude '*.tgz' --exclude '*.zip'  --exclude CVS --exclude '.git*' --exclude books.bib $(PACKAGE); mv ../$(PACKAGE).tgz .

.PHONY: all pdf svg fonts clean distclean archive
