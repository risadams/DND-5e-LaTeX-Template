.PHONY: all clean fonts lint

LATEX ?= pdflatex

# Class options that override the document's, e.g.
#   make example.pdf DND_OPTIONS="srd=5.2.1"
DND_OPTIONS ?=

SRD_VERSIONS = 5.1 5.2 5.2.1

LATEXMK = latexmk --interaction=nonstopmode --pdf --pdflatex=$(LATEX)

comma := ,

# Build $(2).pdf from $(1).tex with the class options $(3). The options go in
# a wrapper file because latexmk mangles TeX code on the Windows command line.
define build_with_options
	printf '%s\n' '\def\DndBuildOptions{$(3)}' '\input{$(1)}' > $(2).build.tex
	$(LATEXMK) -jobname=$(2) $(2).build.tex; status=$$?; rm -f $(2).build.tex; exit $$status
endef

all: example.pdf

clean:
	latexmk -C
	rm -f $(foreach v,$(SRD_VERSIONS),*-srd$(v).*)

fonts:
	bin/get-solbera-fonts

lint:
	npx eclint check *.cls *.sty *.tex lib/

%.pdf: %.tex
ifeq ($(DND_OPTIONS),)
	$(LATEXMK) $<
else
	$(call build_with_options,$*,$*,$(DND_OPTIONS))
endif

# One book, one PDF per SRD version: make example-srd5.1.pdf example-srd5.2.1.pdf
define srd_rule
%-srd$(1).pdf: %.tex
	$$(call build_with_options,$$*,$$*-srd$(1),srd=$(1)$(if $(DND_OPTIONS),$(comma)$(DND_OPTIONS)))
endef
$(foreach v,$(SRD_VERSIONS),$(eval $(call srd_rule,$(v))))
