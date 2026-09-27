# DnD 5e LaTeX Template

[![Latest release](https://img.shields.io/github/release/rpgtex/DND-5e-LaTeX-Template/all.svg)](https://github.com/rpgtex/DND-5e-LaTeX-Template/releases/latest)
[![Build Status](https://img.shields.io/circleci/project/github/rpgtex/DND-5e-LaTeX-Template/master.svg?style=flat)](https://circleci.com/gh/rpgtex/DND-5e-LaTeX-Template)

This is a LaTeX template for typesetting documents in the style of the fifth edition of the "world's greatest roleplaying game".

## Features

* Color schemes, fonts, and layout are close to the core books (but not exactly the same).
* TeX Live includes the default fonts.
* Works with pdfTeX, LuaTeX, and XeTeX.

![Preview](scrot.jpg)

## Installation

There are three options for using this project; choose the one that's
right for you.

### User install using `TEXMFHOME` (recommended)

This will install the template for your current user in one of the following locations:

* Linux: `~/.texmf/tex/latex`
* OS X / macOS: `~/Library/texmf/tex/latex`
* Windows: `C:\Users\{username}\texmf\tex\latex`

LaTeX will find the package automatically.

1. Prepare your `TEXMFHOME` directory.

    ```sh
    mkdir "$(kpsewhich -var-value TEXMFHOME)/tex/latex/"
    ```

2. Download the [latest release](https://github.com/rpgtex/DND-5e-LaTeX-Template/releases/latest) and extract it in `$TEXMFHOME/tex/latex/`.

    ```sh
    wget https://github.com/rpgtex/DND-5e-LaTeX-Template/archive/master.zip
    unzip -d "$(kpsewhich -var-value TEXMFHOME)/tex/latex/" master.zip
    cd "$(kpsewhich -var-value TEXMFHOME)/tex/latex/"
    mv DND-5e-LaTeX-Template-master dnd
    ```

    Alternatively, clone the repo to the same location:

    ```sh
    git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git "$(kpsewhich -var-value TEXMFHOME)/tex/latex/dnd"
    ```

### Using Overleaf

[Overleaf](https://overleaf.com) is an online TeX editor -- think
about it like Google Docs for TeX documents.  This option does not
require a local TeX installation and is an ideal approach for one-off
projects.

1. Download this GitHub repository as a ZIP archive using the *Clone
   or download* link above.
2. On Overleaf, click the *New Project* button and select *Upload
   Project*.  Upload the ZIP archive you downloaded from this
   repository.

### Project install using `TEXINPUTS`

You can also clone a copy of the repository to each LaTeX project. For example, to clone the repository to a `lib/` directory in your project:

```sh
mkdir lib/
git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git lib/dnd
```

LaTeX will not find the template automatically. Set `TEXINPUTS` when compiling your project to locate the package:

```sh
TEXINPUTS=./lib//: pdflatex project.tex
```

## Usage

### Class (recommended)

Load the `dndbook` class in your preamble:

```tex
\documentclass[10pt,twoside,twocolumn,openany,nodeprecatedcode]{dndbook}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}

\begin{document}
% ...
```

### Package

You can also load the `dnd` package directly to use it with another class.
Note that the package has only been tested with the `book` class.

```tex
\documentclass[10pt,twoside,twocolumn,openany]{book}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}

\usepackage[layout=true]{dnd}

\begin{document}
% ...
```

### Options

| Option         | Package `dnd`   | Class `dndbook`   |
| -------------- | :-------------: | :---------------: |
| `bg`           | ✓               | ✓                 |
| `fonts`        | ✓               | ✓                 |
| `fontpath`     | ✓               | ✓                 |
| `img`          | ✓               | ✓                 |
| `stats`        | ✓               | ✓                 |
| `bleed`        | ✓               | ✓                 |
| `cropmarks`    | ✓               | ✓                 |
| `colormodel`   | ✓               | ✓                 |
| `cover`, `spine` | ✓             | ✓                 |
| `index`        | ✓               | ✓                 |
| `hyperref`     | ✓               | ✓                 |
| `links`        | ✓               | ✓                 |
| `bookmarksdepth` | ✓             | ✓                 |
| `srd`          | ✓               | ✓                 |
| `printerfriendly`, `edition` | ✓ | ✓                 |
| `justified`    | ✓               | ✓                 |
| `blankpages`   | ✓               | ✓                 |
| `hyphenate`    | ✓               | ✓                 |
| `balance`      | ✓               | ✓                 |
| `layout`       | ✓               |                   |
| `nomultitoc`   | ✓               | ✓                 |
| `nodeprecatedcode`   | ✓               | ✓                 |

The `dndbook` class also supports all the options of the `book` class.

#### `bg`

Declare how to load background and footer images. This is a key-value option with the following possible values:

* `full`: Load both background and footer images. (**default**)
* `eberron`: Eberron-style backgrounds and footers.
* `none`: Removes both background and footer images.
* `print`: Loads only the footer images.

#### `fonts`

Choose the font set:

* `plain`: Free fonts that ship with TeX Live and work with every engine. (**default**)
* `solbera`: Solbera's free imitations of the fonts in the 2014 core books. This is the closest free match to the official look. Requires XeLaTeX or LuaLaTeX; run `bin/get-solbera-fonts` once to download the fonts into `fonts/solbera/`.
* `wotc`: The fonts used in the official books. You must buy and install them; requires XeLaTeX or LuaLaTeX.
* `dmsguild`: The free fonts from the DMs Guild creator resources; requires XeLaTeX or LuaLaTeX.

Scaly Sans, used for tables and stat blocks with `fonts=solbera`, has no en dash (`--`). Use an em dash (`---`) for empty table cells, as the core books do, and `\DndMinus` for negative numbers.

Solbera's fonts are licensed [CC BY-SA 4.0](https://github.com/jonathonf/solbera-dnd-fonts). You may sell documents typeset with them, but credit Solbera, Ryrok, Ners and LUCASTUCIOUS, and do not sell the fonts themselves.

#### `fontpath`

Folder that holds font files for `fonts=solbera`, relative to the document. Defaults to `fonts/solbera/`.

#### `img`

* `final`: Include images. (**default**)
* `draft`: Replace `\DndImage` images with placeholders for faster builds.

#### `stats`

* `classic`: 2014 Monster Manual stat blocks. (**default**)
* `modern`: 2024 Monster Manual stat blocks.

#### `bleed`

Extra paper added to every side of the page for printing, e.g. `bleed=0.125in`. The paper size you choose (`letterpaper`, `a4paper`, ...) becomes the trim size, the text layout stays on the trimmed page, and backgrounds and full-page art extend into the bleed. Each PDF page gets a TrimBox and BleedBox. Defaults to `0pt`.

#### `cropmarks`

Draw crop marks at the trim size. Most print-on-demand services do not want them.

#### `colormodel`

* `rgb`: Colors are RGB, best for screen PDFs. (**default**)
* `cmyk`: Convert the template's colors to CMYK for print. Convert your images to CMYK separately.

#### `hyperref`

Load `hyperref` and `bookmark` for links, PDF bookmarks and metadata; see [PDF navigation](#pdf-navigation).

* `auto`: Load them with the class, and with the package when `layout=true`. (**default**)
* `true`: Always load them.
* `false`: Never load them.

#### `links`

* `hidden`: Links look like normal text, as in the printed books. (**default**)
* `color`: Links are colored dark red, for screen editions.

#### `bookmarksdepth`

The deepest heading level shown in the PDF bookmarks panel: `part`, `chapter`, `section` (**default**, the same as the table of contents), `subsection`, ... Area headings are subsections by default, so use `bookmarksdepth=subsection` to list every area.

#### `srd`

The System Reference Document your book takes material from. It sets the attribution statement on the credits page and the text chosen by `\DndIfSRD`. See [Credits and legal page](#credits-and-legal-page).

* `none`: No SRD material. (**default**)
* `5.1`: SRD 5.1, the 2014 rules.
* `5.2`: SRD 5.2, the 2024 rules.
* `5.2.1`: SRD 5.2.1, the 2024 rules with errata. This is the current release of SRD 5.2.

#### `printerfriendly`

An edition for printing at home. It leaves out the page background and footer scroll (whatever `bg` says), `\DndPageBackground`, `\DndPartArt` and `\DndChapterArt`, and lightens the fills of boxes, tables and stat blocks. Images in the text, maps, full-page images and covers stay, since they carry content. Use `\DndIfPrinterFriendly{<printer-friendly>}{<other editions>}` to change anything else.

#### `edition`

The name of the edition being built. `bin/build` sets it to `screen`, `print`, `printer-friendly` or `cover`; the default is `screen`. `\DndIfEdition{screen, printer-friendly}{<true>}{<false>}` tests it, for example to leave the cover pages out of the print interior.

#### `justified`

Justify column copy.

#### `hyphenate`

Hyphenate words at line ends, as the core books do (default). `hyphenate=false` never hyphenates, as the template did before; lines are then more ragged and justified text gets wider gaps. The body typography follows measurements of the 2014 books; see [docs/typography.md](docs/typography.md).

#### `balance`

End the two columns at the same height on the last page of each chapter and part, and of the document (default). `balance=false` fills the left column first, as before.

#### `blankpages`

How to fill the page left blank before a chapter or part that starts on a right-hand page (with `twoside,openright`): `background` (default) keeps the paper background, `empty` leaves the page white. Either way the page has no footer or page number. See [Book structure](#book-structure).

#### `layout`

Controls whether loading the `dnd` package also modifies the document layout (geometry, colors, typography, etc.).
This is a boolean option with the following possible values:

* `true`: Modify the document layout.
* `false`: Do not modify the document layout.

The default value is `true` for backwards compatibility with early releases.
This will change in a future release.

#### `nomultitoc`

Disable multi-column table of contents.

#### `nodeprecatedcode`

Excludes all deprecated code from the build process.

## PDF navigation

The class loads `hyperref` and `bookmark` at `\begin{document}`, after your own packages, so you do not have to load them. The PDF opens with a bookmarks panel that mirrors the table of contents, plus bookmarks for the covers, the contents page, `\DndListOfMaps` and the index. The contents, `\DndMapRef`, map area numbers, `\DndAreaRef` and page references are links.

The PDF title and author come from `\title` and `\author`. Set the rest with `\DndSetMetadata` anywhere in the preamble or document:

```latex
\DndSetMetadata{
  subject  = {An adventure for four to six characters of 1st level},
  keywords = {D\&D, 5e, adventure},
  % title and author override \title and \author; any other hyperref key
  % such as pdflang or pdfcopyright is passed on
}
```

To give `hyperref` options of your own, or to use a package that must be loaded after it (such as `cleveref`), load `hyperref` yourself in the preamble. The template's defaults still apply unless you set those options yourself.

A `\\` or `\newline` in a heading breaks the line in the heading itself, and shows as a space in the table of contents, the bookmarks and the footer. To show a different title there, give a short title: `\section[Short title]{Long\\title}`.

Cover pages made with `\DndFrontCover` and `\DndBackCover` are not counted in the page numbers, and are labelled "Cover" and "Back Cover" in the PDF reader's page box.

## Credits and legal page

`\DndCreditsPage` sets a page of credits, usually on the page after the title page, with the legal notices at the foot of the page:

```latex
\DndCreditsPage{
  \DndCredit{design}{A. Writer}
  \DndCredit{cover-art}{B. Artist}
  \DndCredit{cartography}{C. Mapper}
  \DndCredit{Sensitivity Reading}{D. Reader}
  \DndCreditsHeading{Playtesters}
  \DndCredit{thanks}{E. Player, F. Player}
  \DndLegalText{Text required by your publisher, e.g. DMsGuild.}
  \DndCreditsLogo{img/publisher-logo}
}
```

* `\DndCredit{role}{names}` prints one credit. These roles are translated with the document language: `design`, `development`, `writing`, `editing`, `art-direction`, `cover-art`, `interior-art`, `cartography`, `layout`, `playtesting`, `thanks` and `fonts`. Any other role is printed as you wrote it.
* `\DndCreditsHeading{text}` separates groups of credits.
* `\DndLegalText{text}` adds a paragraph to the legal notices. Use it in the preamble or inside the page.
* `\DndCreditsLogo[height]{file}` adds a logo to a row under the legal notices (default height `.5in`).

The page adds two notices by itself:

* **SRD attribution.** With the `srd` class option, the page prints the attribution statement that the SRD's own legal page asks for, word for word. The statement follows the document language when Wizards of the Coast publishes a translated SRD with its own statement (German, Spanish, French and Italian for SRD 5.1 and 5.2.1), and is in English otherwise.
* **Font credit.** Solbera's fonts are licensed CC BY-SA 4.0, which requires crediting their authors. With `fonts=solbera` the page credits all of them; `fonts=dmsguild` and `fonts=wotc` each use one of Solbera's fonts, so it credits that one. The other font sets need no credit.

Options: `\DndCreditsPage[title=Credits, columns=2, fonts=auto, srd-language=auto, pagestyle=empty]`. `title={}` drops the heading, `columns=1` sets the credits in one column, `fonts=none` leaves out the font credit, and `srd-language=english` (or `german`, `spanish`, `french`, `italian`) picks the statement's language instead of following the document. The page is one column wide in a two-column document.

`\DndSRDAttribution[language]` and `\DndFontCredits` print those notices on their own, for example on the back cover.

### One book, two editions

The SRD version is a build option, so the same source can produce a 2014 (SRD 5.1) and a 2024 (SRD 5.2) edition. Build each with `SRD` (see [Publishing your book](#publishing-your-book)):

```sh
make all-editions BOOK=book.tex SRD=5.1     # book-screen-srd5.1.pdf, ...
make all-editions BOOK=book.tex SRD=5.2.1   # book-screen-srd5.2.1.pdf, ...
```

This works without editing `book.tex`, and overrides any `srd` option in its `\documentclass`. To build by hand, define `\DndBuildOptions` before the document is read; it takes any class options and overrides the document's:

```latex
% book-srd5.2.1.tex
\def\DndBuildOptions{srd=5.2.1}
\input{book}
```

Use `\DndIfSRD` for text that differs between the editions. A shorter version matches every release under it, so `5.2` matches `5.2` and `5.2.1`:

```latex
Choose a \DndIfSRD{5.2}{species}{race} for your character.
```

`\DndSRDVersion` prints the version of the current build.

### Before you publish

This is not legal advice. The template copies the statements as published, but whether your product needs them, and what else it needs, depends on what you use and where you sell it. Check the sources yourself:

* [SRD downloads and FAQ](https://www.dndbeyond.com/srd): each SRD PDF starts with a "Legal Information" page that gives the statement. It also asks you not to include any other attribution to Wizards of the Coast.
* [Solbera's fonts](https://github.com/jonathonf/solbera-dnd-fonts) and the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/legalcode).
* DMsGuild products use the legal text and logos that DMsGuild supplies to creators under its Community Content Agreement. Put its text in `\DndLegalText` and its logos in `\DndCreditsLogo`; they are not included here.
* Artists, cartographers and asset packs often ask for specific wording. Add it with `\DndCredit` or `\DndLegalText`.

Each statement's source and the date it was checked are recorded next to it in `lib/dndcredits.sty`.

## Publishing your book

A product for sale usually ships several files built from the same source. Each one is a build command, and each writes its own PDF next to the book, so they never overwrite each other:

| Command | File | What it is |
| ------- | ---- | ---------- |
| `make screen` | `book-screen.pdf` | For reading on screen: no bleed, with bookmarks and links |
| `make print` | `book-print.pdf` | Print interior: bleed and TrimBox for the print service |
| `make printer-friendly` | `book-printer-friendly.pdf` | For home printing: the [`printerfriendly`](#printerfriendly) option |
| `make cover` | `book-cover.pdf` | Print cover spread, built from `cover.tex` next to the book |
| `make all-editions` | all of the above | |
| `make preflight` | all of the above | Builds every edition and checks each one |

Set the book and the print settings with variables:

```sh
make all-editions BOOK=mybook/book.tex ENGINE=xelatex BLEED=0.125in SPINE=0.42in
```

| Variable | Default | Meaning |
| -------- | ------- | ------- |
| `BOOK` | `example.tex` | The book. It can be in any folder; it finds the template without installing it. |
| `COVER` | `cover.tex` next to the book | The cover document for `make cover` |
| `ENGINE` | `pdflatex` | `pdflatex`, `xelatex` or `lualatex` |
| `BLEED` | `0.125in` | Bleed for the print interior and cover; check your printer |
| `SPINE` | `0.25in` | Spine width, from your printer's cover calculator |
| `CMYK` | off | `CMYK=1` converts print and cover colors to CMYK |
| `PAGE_MULTIPLE` | `1` | Page count the printer needs a multiple of, checked by preflight |
| `SRD` | the document's | Build for another SRD version; adds `-srd<version>` to the file names |
| `OPTIONS` | none | More class options for every edition, e.g. `OPTIONS=img=draft` |

The screen edition includes the covers, but the print service wants them as a separate file. Leave them out of the print interior with `\DndIfEdition`:

```latex
\DndIfEdition{screen, printer-friendly}{\DndFrontCover[title=...]{art/cover}}{}
```

### Without make

The Makefile runs `bin/build`, a `texlua` script. `texlua` comes with every TeX distribution, so on Windows (or anywhere without `make`) run it directly:

```sh
texlua bin/build --engine=xelatex all mybook/book.tex
texlua bin/build --bleed=3mm --cmyk print cover mybook/book.tex
texlua bin/build --help
```

### Preflight checks

`bin/preflight` checks a PDF and its log for problems that get files rejected by print services or look unprofessional. `make preflight` (or `bin/build --preflight`) runs it on every edition, with the print checks for the print interior and cover:

```sh
texlua bin/preflight book-screen.pdf
texlua bin/preflight --print --bleed=0.125in --page-multiple=2 book-print.pdf
```

It exits with an error if anything fails, and prints warnings for things worth a look:

| Check | Result | How to fix it |
| ----- | ------ | ------------- |
| LaTeX errors | fail | Read the log; the message names the input line |
| Undefined references and citations | fail | Fix the label, or rebuild so references resolve |
| Missing characters | fail | The font lacks a glyph (e.g. the en dash in Scaly Sans); use another character |
| Fonts not embedded | fail | Use fonts that can be embedded; all the template's font sets can |
| No bleed, or a bleed other than `--bleed` (print) | fail | Build with the `bleed` option (`make print` does) |
| Pages of different trim sizes (print) | fail | Keep every page the same paper size |
| Page count not a multiple of `--page-multiple` (print) | fail | Add or remove pages; many printers need an even count or a multiple of 4 |
| Images below `--min-ppi` (default 200) at their printed size (print) | fail | Use a larger image, or print it smaller |
| RGB images with `--cmyk` (print) | fail | Convert them with `bin/prepare-images --cmyk` |
| Images below `--warn-ppi` (default 300) (print) | warn | 300 ppi is the usual recommendation |
| Overfull boxes wider than `--overfull` (default 1pt) | warn | Reword, or allow a break (e.g. in long `\texttt` or URLs) |
| Font shapes the font does not have | warn | Usually harmless, e.g. slanted set as italic |
| Type 3 (bitmap) fonts | warn | Use a vector font |
| Bleed in a file that is not checked for print | warn | Upload the print edition to the printer, and the screen edition to stores |

The PDF checks need `pdfinfo`, `pdffonts` and `pdfimages` from Poppler. MiKTeX includes them; on Linux install `poppler-utils`, and on macOS `brew install poppler`.

### Example books

The [`examples`](examples) folder has three short books that show different options together, and how to build every edition of each. `make examples` builds and checks them all.

## Book structure

A printed book is read in spreads: chapters start on a right-hand (odd) page, and the left-hand page before a chapter holds art or is left blank on purpose. Use the `twoside` and `openright` class options for print:

```latex
\documentclass[letterpaper,twoside,twocolumn,openright,nodeprecatedcode]{dndbook}
```

A page left blank before a chapter or part has no footer or page number, so it doesn't look like a mistake. It keeps the paper background, or is white with `blankpages=empty`.

| Command | Result |
| ------- | ------ |
| `\maketitle` | A title page in the book's fonts, from `\title`, `\author` and, if you set it, `\date`. |
| `\DndSubtitle{text}` | A line under the title on the title page. |
| `\DndFacingArt[fade=..., graphics={...}]{file}` | Put before `\chapter` or `\part`: full-page art on the left-hand page facing it, instead of a blank page. If the text ends on a left-hand page, a blank right-hand page comes first so the art still faces the chapter. Left out of the printer-friendly edition. |
| `\DndSectionBreak[color]` | A centered ornament between two passages of the same section; the text after it starts without an indent. |
| `\DndOrnament[width][color]` | The ornament on its own, e.g. on a title or credits page. |

The core books put the front and back matter in this order; each item starts on a right-hand page unless noted:

1. Front cover (`\DndFrontCover`, screen editions only; print services take the cover as its own file)
2. Title page (`\maketitle`)
3. Credits and legal page (`\DndCreditsPage`), on the back of the title page
4. Contents (`\tableofcontents`) and list of maps (`\DndListOfMaps`)
5. Introduction and chapters (`\mainmatter`)
6. Appendices (`\appendix`), then player handouts
7. Index (`\DndPrintIndex`, with the `index` class option)
8. Back cover (`\DndBackCover`, screen editions only)

The [book starter](https://github.com/risadams/DND-5e-LaTeX-starter) follows this order.

## Artwork

Art is scaled to fill its space and cropped at the centre, so it is never stretched. `fade` blends an edge into the page: `none`, `bottom`, `top`, `left`, `right`, `sides` or `all`. `graphics={...}` passes options to `\includegraphics`, e.g. `graphics={trim=0 0 0 2in, clip}`.

| Command | Result |
| ------- | ------ |
| `\DndChapterArt[height=.4\paperheight, fade=bottom]{file}` | Put before `\chapter`: art across the top of the chapter's first page, edge to edge, with the title below it. |
| `\DndPartArt{file}` | Put before `\part`: full-page art behind the part title. |
| `\DndFullPageImage{file}` | A page holding only the image, such as a map or a splash illustration. |
| `\DndPageBackground{file}` | Art behind the current page's text. |
| `\DndFadedImage[fade=bottom]{file}` | An image in the column that fades into the page. `\DndFadedImage*` spans the full text width. |
| `\DndSpanImage[t]{file}` | An image across both columns at the top (`t`) or bottom (`b`) of a page. Bottom placement needs `\usepackage{stfloats}`. |
| `\DndImage{file}`, `\DndCaptionedImage{caption}{file}` | Images in a box sized to the column (`*` for full width), with an optional caption. |

### Covers

`\DndFrontCover` and `\DndBackCover` add full-bleed cover pages to a book:

```latex
\DndFrontCover[title=The Sunless Citadel, subtitle=An Adventure for Levels 1--3,
               author=A. Writer, title-position=top]{art/cover}
...
\DndBackCover[blurb={Deep beneath the earth lies a fortress...}]{art/back}
```

Options: `title-position` (`top` or `bottom`), `title-size` (default `54pt`; the subtitle and author are 40% of it), `title-color`, `outline-color`, and `guides` to show the trim line and the safe area where printers want text kept.

Print-on-demand services want the cover as a separate PDF with the back cover, spine and front cover on one sheet. Make a second document for it, using the spine width from your printer's calculator (it depends on page count and paper):

```latex
\documentclass[cover, spine=0.6in, bleed=0.125in, fonts=solbera]{dndbook}
\begin{document}
\DndCoverSpread[title=The Sunless Citadel, author=A. Writer,
                blurb={Deep beneath the earth...},
                art=art/cover, back-art=art/back, guides]
\end{document}
```

Use `wrap-art=<file>` instead of `art` and `back-art` for one image across the whole spread. The spine is filled with `spine-color` (default `titlered`) and gets the title and author in `spine-text-color` when it is wider than 0.25in. Remove `guides` before sending the file to print.

Cut-out art (a PNG with a transparent background) works with every command. Save PNGs as 8-bit: XeLaTeX cannot show 16-bit PNGs with transparency. `bin/prepare-images SRC DEST` converts a folder of images to 8-bit, lists the largest size each can print at 300 dpi, and with `--cmyk PROFILE.icc` converts them to CMYK for print.

Text cannot flow around irregular art shapes. Place cut-out art in a column, or use a faded image, instead.

## Maps

`DndMap` places a map, numbers it by chapter ("Map 1.1") and draws the area numbers on it. The numbers come from `\DndArea` and `\DndSubArea`, so the map stays correct when you add or reorder areas. Export maps from your mapping tool without room numbers.

```latex
\begin{DndMap}[caption=Cragmaw Hideout, label=cragmaw,
               scale={1 square = 5 feet}, compass, placement=wide]{maps/cragmaw}
  \DndMapArea{0.42,0.61}{Cave Mouth}       % the area titled "Cave Mouth"
  \DndMapSubArea{0.30,0.20}{Twin Pools}
  \DndMapArea[region=B]{0.7,0.4}{Kennel}    % an area in another region
  \DndMapText{0.80,0.10}{To Phandalin}     % on every version
  \DndMapText*{0.55,0.75}{Secret door}     % DM map only
\end{DndMap}
```

Positions are fractions of the image, from `0,0` at the bottom left to `1,1` at the top right. Add the `coordinates` option to overlay a 0.1 grid while you place labels.

| Option | Meaning |
| ------ | ------- |
| `caption`, `label` | Caption text, and the name for `\DndMapRef` and `\DndPlayerMap` |
| `placement` | `column` (default, in place), `wide` (across both columns, floated), `page` (a page of its own) or `sideways` (a page of its own, turned sideways for a landscape map; PDF viewers show it upright). The text stops at the end of the page before a sideways map, so put one where a page break is fine, such as the end of a section. |
| `float` | Float position: `t`, `b`, `h` or `p` |
| `scale` | Scale note in the bottom-left corner |
| `compass` | Compass rose; give an angle (`compass=30`) if north is not up |
| `labels` | `false` hides area numbers and DM-only text |

`\DndMapRef{cragmaw}` prints "Map 1.1" (`\DndMapRef*` prints just "1.1"), `\DndListOfMaps` lists every map, and `\DndPlayerMap[placement=page]{cragmaw}` reprints a map without area numbers or DM-only text, for a handout. `\DndSetMapOptions{labels=false}` turns labels off in the whole document. Restyle the labels with `\tikzset{dnd map label/.append style={...}}` (also `dnd map text` and `dnd map scale`).

`\DndPlayerMap[appendix]{cragmaw}` puts the player map in the handout appendix instead (see [Player handouts](#player-handouts)).

## Player handouts

Letters, notes and posters for the players. A handout appears in the text and, with `appendix`, again at full page size in a handout appendix that the DM can print and cut out.

```latex
\begin{DndHandout}[style=letter, title={The Mayor's Letter}, label=mayor, appendix]
  To whoever finds this, ...
\end{DndHandout}

Give the players \DndHandoutRef{mayor}.      % "Handout 1"

\appendix
\DndHandoutAppendix                           % "Appendix A: Handouts"
```

| Option | Meaning |
| ------ | ------- |
| `style` | `letter` (paper and handwriting, default), `note` (a torn scrap, handwriting) or `poster` (a bordered sheet with a large title) |
| `title` | Caption ("Handout 1: The Mayor's Letter") and poster title |
| `label` | Name for `\DndHandoutRef` |
| `art` | Poster only: image under the title |
| `appendix` | Also print the handout full page in `\DndHandoutAppendix` |
| `inline=false` | Leave the handout out of the text (use with `appendix`) |

- Handouts are numbered through the book. `\DndHandoutRef{mayor}` prints "Handout 1" (`\DndHandoutRef*` prints "1"), and `\DndListOfHandouts` lists them with the page of the full-page copy.
- `\DndPlayerMap[appendix]{<map label>}` adds a player map to the appendix as a numbered handout; refer to it with `\DndHandoutRef{<map label>}`. A map with `placement=sideways` gets a sideways page there too.
- `\DndHandoutAppendix` prints every handout marked `appendix`, one per page, in one column, under `\chapter{Handouts}`. Give another heading command with `\DndHandoutAppendix[\section*]`, or none with `\DndHandoutAppendix*`.
- `\DndSetHandoutOptions{appendix}` sets options for every handout.
- Handwriting uses the font set's handwritten face: Zatanna Misdirection with `fonts=solbera` and `fonts=dmsguild`, DaiVernon Misdirect with `fonts=wotc`, and URW Chancery with the default fonts. Change it with `\DndSetFonts[handout-family=..., handout-style=...]`, and restyle the boxes with `\tcbset{dnd handout letter/.append style={...}}` (also `note` and `poster`).

## Class tables, spell lists and the index

`DndClassTable` makes a full-width class table. Stripes start after `header-rows` rows, and `\multicolumn` works in any row. `float` is `t` (default), `b`, `p` or `none`.

```latex
\begin{DndClassTable}[title=The Wizard, header-rows=2]{ccXccc}
  \DndClassTableGroup{3}{3}{Spell Slots per Spell Level} % 3 empty cells, then 3 spanned
  \DndClassTableHeader{Level & Proficiency Bonus & Features & 1st & 2nd & 3rd}
  1st & +2 & Spellcasting, Arcane Recovery & 2 & -- & -- \\
\end{DndClassTable}
```

`DndSpellList` lists a class's spells by level. Levels `0`–`9` get the translated level names; any other text is used as is. Spells are sorted alphabetically unless you pass `sort=false`, and `heading` picks the sectioning level of the title (default `subsection`, or `none`).

```latex
\begin{DndSpellList}{Bard Spells}
  \DndSpellListLevel{0}{Vicious Mockery, Blade Ward, Dancing Lights}
  \DndSpellListLevel{1}{Healing Word, Bane, Charm Person}
\end{DndSpellList}
```

With the `index` class option, mark entries with `\index{term}`, `\index{parent!child}` or `\index{term|see{other}}` and print the index with `\DndPrintIndex`. Entries are grouped under letter headings. `latexmk` runs `makeindex` for you.

## Dependencies

If you don't have LaTeX installed, we recommend installing a complete [TeX Live distribution](https://www.tug.org/texlive/).

### Ubuntu

```sh
sudo apt-get install texlive-full
```

### Arch

```sh
sudo pacman -S texlive-bin texlive-core texlive-latexextra
```

### OSX

MacTex has its own [installer](https://www.tug.org/mactex/), but you can install it through brew cask:

#### Full version

```sh
brew cask install mactex
```

#### Slightly smaller version without GUI

```sh
brew cask install mactex-no-gui
```

#### Minimal version

Use `tlmgr` to install packages as needed, see this [answer](https://tex.stackexchange.com/a/470285) for more information

```sh
brew cask install basictex
brew cask install tex-live-utility
```

After any of this, use the following such that the texlive directory doesn't require admin rights.

```sh
sudo chown -R myuser:mygroup /usr/local/texlive
```

For more information about MacTex permissions, see the following StackExchange [post](https://tex.stackexchange.com/questions/3744/how-do-i-set-up-mactex-so-admin-rights-arent-necessary)

## Known issues and solutions

### Stat block text color does not survive page breaks

This is a known issue in `tcolorbox`. According to the `tcolorbox` 4.12 manual (p. 363):

> If your text content contains some text color changing commands, your color will not survive the break to the next box.

You can use LuaTeX to compile the document.

```sh
lualatex main.tex
```

### Wrapping `monsterbox` in float disrupts spacing inside stat block

Wrapping a `monsterbox` (or `monsterboxnobg`) in a floating figure adds extra space between stat block elements:

```latex
\begin{figure}[b]
  \begin{monsterbox}{Orc Warden}
    % ...
  \end{monsterbox}
\end{figure}
```

Instead, use the `tcolorbox` `float` parameter:

```latex
\begin{monsterbox}[float=b]{Orc Warden}
  % ...
\end{monsterbox}
```

Refer to the `tcolorbox` documentation (section 4.13) for more float parameters.

## Contributing

### Style

We use [EditorConfig](https://editorconfig.org/) to enforce consistent formatting.
Install the appropriate plugin for your editor.

### Preparing a new release

1. Run `./bin/bump-version` to tag the new version.

    ```sh
    ./bin/bumpversion <version>
    ```

2. Compile the example PDF.
3. Save the first page of the PDF as scrot.jpg.
4. Update the change log for the new release; commit your changes.
5. Push changes.

    ```sh
    git push && git push --tags
    ```

6. [Create a new release](https://help.github.com/articles/creating-releases/) and attach the PDF and scrot.

## Credits

* Background image from [Lost and Taken](https://lostandtaken.com/)
* `fonts=solbera` uses fonts by Solbera, Ryrok, Ners and LUCASTUCIOUS, [CC BY-SA 4.0](https://github.com/jonathonf/solbera-dnd-fonts)

## License

MIT
