
#===============================================================================
# Make dependency file for LaTeX/BibTeX documents.
# Original borrowed (gratefully) from Jason McPhate.
# Numerous modifications and updates by Brian Wolven.
#===============================================================================
# To customize this makefile for use with another document, you will
# need to edit the following variables (macros in make-speak):
# The ???Dir variables are provided for convenience - full file names can be
# used in the ???Files variable lists.
#
# Target   : is your primary document name.
# SecDir   : points to location of included TeX files.
# FigDir   : points to location of your figures    (ps or eps files)
# BibDir   : points to location of your .bib files (BibTeX bibliography entries)
# BstDir   : points to location of your .bst files (bibliography style)
# SecFiles : lists actual names of files referenced in your primary document,
#            e.g. with LaTeX's \include command.
# FigFiles : lists actual names of figure files - other paths can be used
#            besides FigDir, as needed.
# BibFiles : lists actual names of .bib files referenced in your
#            document with LaTeX's \bibliography command.
# BstFiles : lists actual name of .bst file referenced in your
#            document with LaTeX's \bibliographystyle command.
#
# Macros which exceed one line in length are joined with a backslash (\)
# at the end of the line. Macros with more than one value, e.g. multiple
# file names, must be surrounded by parentheses, either () or {}.
# Comment out the ???Files line for a given variable assignment if there are
# no file dependencies of that type.
#===============================================================================


 Target   = report
 FigDir   = ./images
 StyDir   = ./TeX
 BibDir   = ./TeX
 BstDir   = ./
 SecFiles = report.tex introduction.tex metric.tex conics.tex abstract.tex testing.tex library.tex
 MungiDir = ../thesis_code/Mungi-1.2/
 GrindDir = ./grind
 GrindFiles = ${GrindDir}/conf.tex ${GrindDir}/iide.idl.tex \
	${GrindDir}/interrupt.idl.tex ${GrindDir}/serial.idl.tex \
	${GrindDir}/inthandler.frag.c.tex ${GrindDir}/pyxis.idl.tex \
	${GrindDir}/imainchip.idl.tex ${GrindDir}/iisaiospace.idl.tex \
	${GrindDir}/pyxishandler.frag.c.tex ${GrindDir}/ipciconfspace.idl.tex \
	${GrindDir}/ipciconfspacerw.idl.tex ${GrindDir}/ipcimemspace.idl.tex ${GrindDir}/ipciiospace.idl.tex \
	${GrindDir}/ipcidevice.idl.tex ${GrindDir}/iisadevice.idl.tex \
	${GrindDir}/ipciinterrupts.idl.tex ${GrindDir}/isource.idl.tex ${GrindDir}/iisainterrupts.idl.tex  \
	${GrindDir}/isink.idl.tex ${GrindDir}/iserial.idl.tex \
	${GrindDir}/iblock.idl.tex ${GrindDir}/ide.idl.tex ${GrindDir}/iideprivate.idl.tex \
	${GrindDir}/icomplete.idl.tex ${GrindDir}/ipacketsource.idl.tex ${GrindDir}/ipacketsink.idl.tex
 FigFiles = 
 StyFiles = ${StyDir}/unswthesis-benno.cls

 BibFiles = report.bib

# BstFiles = (${BstDir}/poster.bst)

grind = lgrind -i

# Depends
all: ${Target}.dvi

${Target}.toc: ${BibFiles} ${SecFiles} ${FigFiles} ${StyFiles} Makefile ${Target}.tex

#===============================================================================
# LaTeX and BibTeX options
# On-screen viewing options (mini and maxi format)
# Either viewing option can be used for either format - but :
#   make view     - will specify convenient options for mini format
#   make maxiview - will specify convenient options for maxi format
#===============================================================================

 LaTeXEnv   = TEXINPUTS=::${StyDir}:${FigDir}:/home/disy/lib/TeX/
 BibTexEnv  = BIBINPUTS=::${BibDir}
 LaTeX      = ${LaTeXEnv} latex  # or regular latex, if you prefer
 BibTeX     = ${BibTexEnv} bibtex
 DVItoPS    = ${LaTeXEnv} dvips -t a4 -Pcmz -Pamz -G1           # "-l 1" option for poster production only
 Paper      = gv -magstep  0   # For normal papers
 Viewer     = gv -magstep  1   # For mini format - scale 1.414
 MaxiViewer = gv -magstep -5   # For maxi format - scale 0.100
 Fig2Dev    = fig2dev

#===============================================================================
# Everthing below here should probably be left alone, unless you know what
# you're doing and have a valid reason for changing them.
#===============================================================================
# Targets, options, and dependencies
#===============================================================================

%.pstex_t: %.pstex
	${Fig2Dev} -L pstex_t -p $< $(patsubst %.pstex,%.fig,$<) $@

%.pstex: %.fig
	${Fig2Dev} -L pstex $< $@

%.ps: %.dvi
	${DVItoPS} $< -o $@

%.pdf: %.ps
	ps2pdf $<


%.dvi: %.toc
	${LaTeX} $(patsubst %.toc,%,$<)

%.toc: %.bbl
	${LaTeX} $(patsubst %.bbl,%,$<)

%.bbl: %.tex
	${LaTeX} $(patsubst %.tex,%,$<)
	${BibTeX} $(patsubst %.tex,%,$<)

clean:
	rm -f *.aux *.toc *.bbl *.blg *.dvi *.log ${FigDir}/*.pstex ${FigDir}/*.pstex_t *~ ${GrindFiles}

realclean: clean
	rm -f *.ps *.tar.gz

#===============================================================================
# Viewing options
#===============================================================================

show: %.ps
	${Paper} $<

%.view: %.ps
	${Viewer} $<

%.viewmaxi: %.ps
	${MaxiViewer} $<

#===============================================================================
# Archive file options
#===============================================================================

%.ps.gz: %.ps
	rm $@
	gzip -9 $<

%.tar.gz: # Create tar archive with all files in current directory.
	 make
	 make clean
	 tar czf $@ .

%.list: %.tar.gz # List files in tar archive.
	 tar tvzf $(patsubst %.list,%,$@).tar.gz

#===============================================================================
# This command too dangerous for casual use!!!
#===============================================================================

#extract: # Extract files from tar archive - overwrites current files!
#	tar -xvf ${Target}.tar

${GrindDir}/conf.tex: ${MungiDir}conf
	${grind} -lsh $< > $@

${GrindDir}/ipciconfspace.idl.tex: ${MungiDir}lib/interfaces/ipci_confspace.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipciconfspacerw.idl.tex: ${MungiDir}lib/interfaces/ipci_confspacerw.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipcimemspace.idl.tex: ${MungiDir}lib/interfaces/ipci_memspace.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipciiospace.idl.tex: ${MungiDir}lib/interfaces/ipci_iospace.idl
	${grind} -lIDL $< > $@


${GrindDir}/iide.idl.tex: ${MungiDir}lib/interfaces/iide.idl
	${grind} -lIDL $< > $@

${GrindDir}/imainchip.idl.tex: ${MungiDir}lib/interfaces/imainchip.idl
	${grind} -lIDL $< > $@

${GrindDir}/iisaiospace.idl.tex: ${MungiDir}lib/interfaces/iisa_iospace.idl
	${grind} -lIDL $< > $@

${GrindDir}/interrupt.idl.tex: ${MungiDir}lib/interfaces/interrupt.idl
	${grind} -lIDL $< > $@

${GrindDir}/serial.idl.tex: ${MungiDir}apps/serial/serial.idl
	${grind} -lIDL $< > $@

${GrindDir}/ide.idl.tex: ${MungiDir}apps/ide/ide.idl
	${grind} -lIDL $< > $@

${GrindDir}/pyxis.idl.tex: ${MungiDir}apps/pyxis/pyxis.idl
	${grind} -lIDL $< > $@

${GrindDir}/iisadevice.idl.tex: ${MungiDir}lib/interfaces/iisa_device.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipcidevice.idl.tex: ${MungiDir}lib/interfaces/ipci_device.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipciinterrupts.idl.tex: ${MungiDir}lib/interfaces/ipci_interrupts.idl
	${grind} -lIDL $< > $@

${GrindDir}/iisainterrupts.idl.tex: ${MungiDir}lib/interfaces/iisa_interrupts.idl
	${grind} -lIDL $< > $@

${GrindDir}/isource.idl.tex: ${MungiDir}lib/interfaces/isource.idl
	${grind} -lIDL $< > $@

${GrindDir}/isink.idl.tex: ${MungiDir}lib/interfaces/isink.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipacketsource.idl.tex: ${MungiDir}lib/interfaces/ipacketsource.idl
	${grind} -lIDL $< > $@

${GrindDir}/ipacketsink.idl.tex: ${MungiDir}lib/interfaces/ipacketsink.idl
	${grind} -lIDL $< > $@


${GrindDir}/iserial.idl.tex: ${MungiDir}lib/interfaces/iserial.idl
	${grind} -lIDL $< > $@

${GrindDir}/iideprivate.idl.tex: ${MungiDir}lib/interfaces/iide_private.idl
	${grind} -lIDL $< > $@

${GrindDir}/iblock.idl.tex: ${MungiDir}lib/interfaces/iblock.idl
	${grind} -lIDL $< > $@

${GrindDir}/icomplete.idl.tex: ${MungiDir}lib/interfaces/icomplete.idl
	${grind} -lIDL $< > $@

${GrindDir}/inthandler.frag.c.tex: int_handler.frag.c
	${grind} -lc $< > $@

${GrindDir}/pyxishandler.frag.c.tex: pyxis_handler.frag.c
	${grind} -lc $< > $@
