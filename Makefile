.PHONY: all clean fonts lint screen print printer-friendly cover all-editions preflight examples test

# The book to build, and its cover document (default: cover.tex next to it)
BOOK ?= example.tex
COVER ?=

# pdflatex, xelatex or lualatex
ENGINE ?= pdflatex

# Print settings; check your printer's requirements
BLEED ?= 0.125in
SPINE ?= 0.25in
CMYK ?=
PAGE_MULTIPLE ?= 1

# Build for another SRD version (5.1, 5.2 or 5.2.1); the files are named
# <book>-<edition>-srd<version>.pdf
SRD ?=

# More class options for every edition, e.g. OPTIONS="img=draft"
OPTIONS ?=

comma := ,
BUILD_OPTIONS = $(if $(SRD),srd=$(SRD)$(if $(OPTIONS),$(comma)))$(OPTIONS)

BUILD = texlua bin/build --engine=$(ENGINE) --bleed=$(BLEED) --spine=$(SPINE) \
	--page-multiple=$(PAGE_MULTIPLE) $(if $(COVER),--cover=$(COVER)) \
	$(if $(CMYK),--cmyk) $(if $(BUILD_OPTIONS),--options=$(BUILD_OPTIONS)) \
	$(if $(SRD),--suffix=-srd$(SRD))

# Example books and the engine each needs
EXAMPLES = examples/adventure/adventure.tex:xelatex \
	examples/player-options/player-options.tex:pdflatex \
	examples/gazetteer/gazetteer.tex:lualatex

all: example.pdf

# Edition outputs of BOOK, by extension (never .tex)
EDITIONS = screen print printer-friendly cover
OUTPUTS = pdf log aux toc out fls fdb_latexmk idx ind ilg lom
BOOK_BASE = $(basename $(BOOK))

clean:
	latexmk -C
	rm -f $(foreach e,$(EDITIONS),$(foreach x,$(OUTPUTS),$(BOOK_BASE)-$(e)*.$(x)))

fonts:
	bin/get-solbera-fonts

lint:
	npx eclint check *.cls *.sty *.tex lib/

%.pdf: %.tex
	latexmk --interaction=nonstopmode --pdf $<

# One PDF per edition: <book>-screen.pdf, <book>-print.pdf, ...
screen print printer-friendly cover:
	$(BUILD) $@ $(BOOK)

all-editions:
	$(BUILD) all $(BOOK)

# Build every edition and check each PDF
preflight:
	$(BUILD) --preflight all $(BOOK)

# Build and check every edition of every example book
examples:
	@status=0; for e in $(EXAMPLES); do \
	  $(MAKE) --no-print-directory preflight BOOK=$${e%%:*} ENGINE=$${e##*:} || status=1; \
	done; exit $$status

# bin/preflight must reject a PDF with known problems
# and the documents in test/ must build
TESTS = deprecated-code package-mode toc-line-breaks appendix-include \
	book-structure handouts

test:
	if texlua bin/build --preflight print test/preflight-fail.tex; then \
	  echo "bin/build passed a PDF that failed preflight"; exit 1; \
	fi
	if texlua bin/preflight --print test/preflight-fail-print.pdf; then \
	  echo "preflight passed a PDF it should have rejected"; exit 1; \
	fi
	@status=0; for t in $(TESTS); do \
	  texlua bin/build --engine=$(ENGINE) screen test/$$t.tex || status=1; \
	done; exit $$status
	@grep -B1 'Monsters' test/appendix-include-screen.toc | head -1 | grep -q tocchapapp || \
	  { echo "the appendix is not labeled Appendix in the contents"; exit 1; }
