# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Theming class options:
  - Eberron-style header/footers on request
  - Font set options:
    * `fonts=dmsguild` for DMs Guild fonts (freely available).
    * `fonts=wotc` for canonical WotC (paid, fairly expensive) font sets.
    * `fonts=solbera` for Solbera's free imitations of the 2014 core book fonts, including the drop cap face. Run `bin/get-solbera-fonts` to download them; `fontpath` sets where they are loaded from.
    * Leave off the option to get current default fonts.
* Image floats, captioned and standalone, based on `tcolorbox`.
* Stat blocks: small inline ones for sentient weapons, and fully-fledged blocks for vehicles.
* Quotation and aside environments: on a slightly rotated sticky note, with an attribution (quotation) or not (aside).
* Area references:
  - Define ranges (e.g. `Area 10-12: Small prison cells`).
  - Better ways to reach outside the current top-level area to reference things from elsewhere (e.g. reference 'Area A5' from within 'Area C2').
  - `\DndAreaRef` now prints 'C5' instead of 'p. 32'.  Use `\DndAreaPageRef` to get 'p. 32' now.
* Several utility macros:
  - `\DndAbilityCheck` (DC 11 Strength) and `\DndSkillCheck` (DC 11 Strength (Athletics))
  - Ability check macros built on those, e.g. `\DndStrSave{12}` gets 'DC 12 Strength'
  - Skill check macros also built on those, e.g. `\DndAthletics{12}` gets 'DC 12 Strength (Athletics)', or `\DndAthletics[\conname]{12}` gets 'DC 12 Constitution (Athletics)'.
* Print production options: `bleed=<length>` adds bleed on every side and writes PDF TrimBox/BleedBox, `cropmarks` draws trim marks, and `colormodel=cmyk` converts colors for print
* Artwork commands: `\DndChapterArt` (edge-to-edge art at the top of a chapter's first page), `\DndPartArt` (art behind a part title), `\DndFullPageImage` (image-only pages), `\DndPageBackground` (art behind a page's text), `\DndFadedImage` (images that fade into the page) and `\DndSpanImage` (art across both columns). Art fills its space without distortion and extends into the bleed.
* Covers: `\DndFrontCover` and `\DndBackCover` for full-bleed cover pages, and `\DndCoverSpread` with the `cover` and `spine` options for print-on-demand cover spreads (#235)
* `DndClassTable` for full-width class tables with grouped column headings, `DndSpellList` for sorted class spell lists with translated level names, and an `index` option with `\DndPrintIndex` for a styled index
* Maps: `DndMap` numbers maps by chapter and draws area numbers taken from `\DndArea`/`\DndSubArea` onto the image, with DM-only notes, a scale note, a compass rose and a coordinate grid for placing labels. `\DndPlayerMap` reprints a map without DM labels, `\DndMapRef` references maps and `\DndListOfMaps` lists them. Map captions are translated.
* `bin/prepare-images` converts art to 8-bit, reports its printable size at 300 dpi and optionally converts it to CMYK
* `\damagetypename` caption sets the word order of monster attack damage, e.g. "de daño veneno" in Spanish; Spanish, Portuguese and French now put the damage type after the noun (#324, #190)
* `DndMonster` stat blocks can be referenced: `\begin{DndMonster}[label=monster:wolf]{Wolf}` works with `\pageref`, `\nameref` and hyperref links (#337)
* `area-reset` option for `\DndSetAreaOptions` restarts area numbering at each part, chapter or section (#313)
* PDF navigation: `hyperref` and `bookmark` load automatically, so the PDF has a bookmarks panel, a clickable table of contents, and linked map and area references. The `hyperref`, `links=hidden|color` and `bookmarksdepth` options control it, and `\DndSetMetadata` sets the PDF title, author, subject and keywords. Covers, the contents page, the list of maps and the index get bookmarks, and cover pages are no longer counted in the page numbers (risadams/DND-5e-LaTeX-Template#1)
* Credits and legal page: `\DndCreditsPage` with `\DndCredit`, `\DndCreditsHeading`, `\DndLegalText` and `\DndCreditsLogo`. The `srd=5.1|5.2|5.2.1` option adds the SRD attribution statement, copied from Wizards of the Coast's SRDs, in German, Spanish, French or Italian where Wizards publishes one. The active font set is credited automatically when it uses Solbera's fonts. Credit roles are translated (risadams/DND-5e-LaTeX-Template#2)
* Build-time options: `\DndBuildOptions` overrides the document's class options, `make all-editions SRD=5.1` builds for another SRD version, and `\DndIfSRD` selects text for one version
* Editions: `make screen`, `print`, `printer-friendly`, `cover` and `all-editions` build one PDF per file a product ships with, named after the book, from any folder. `bin/build` does the same without `make` (it runs on `texlua`, so it works on Windows). `\DndIfEdition` selects text per edition (risadams/DND-5e-LaTeX-Template#3, rpgtex/DND-5e-LaTeX-Template#340)
* `printerfriendly` option: no page backgrounds, footer scroll, page, part or chapter art, and lighter box fills, for printing at home; `\DndIfPrinterFriendly` selects text for it
* Preflight checks: `bin/preflight` and `make preflight` check the log for errors, undefined references, missing characters and overfull boxes, and the PDF for unembedded fonts, bleed and trim boxes, page counts and image resolution and color (risadams/DND-5e-LaTeX-Template#4)
* `examples` folder with three books (a 2014-style adventure with a cover spread, 2024-style player options and a German A4 gazetteer); `make examples` builds and checks every edition of each
* Portuguese translation
* French translation
* Automatically bolds the first row of tables
* Added optional `proficiency-bonus` item to `\DnDMonsterDetails` that will be displayed next to the monster or NPC's challenge rating, as is the style in Candlekeep Mysteries and dndbeyond.

### Changed
* Moved devops from CircleCI to GitHub Actions
* Page backgrounds are drawn with `eso-pic` behind all page content, so they no longer cover pages inserted with `\includepdf`. A page style that clears the header still suppresses the background (#314, #367)
* Floats on pages holding only floats sit at the top of the page instead of the middle, as in the core books
* Negative modifiers use a true minus sign when the font has one; `\DndMinus` gives the same sign in documents

### Fixed
* `DndReadAloud` no longer typesets a stray `;` (a "Missing character" warning in the log)
* With XeLaTeX and the default fonts, curly quotes, guillemets, dashes, the ellipsis, "œ" and "ß" print correctly instead of going missing (or "ß" printing as "SS")
* `fontpath` is looked up like any input file, so a book in another folder finds the template's `fonts/solbera/`
* `\DndCredit` no longer splits a credit across the columns of the credits page
* `DndReadAloud`, `DndSidebar`, `DndComment`, `DndQuotation` and `DndAside` no longer fail on TeX Live 2026 when the optional argument is omitted (#391)
* Accented characters in translated captions (e.g. Spanish "al día") are no longer garbled under pdfLaTeX (#388)
* Ability scores of 30 no longer wrap onto two lines in monster stat blocks (#373)
* German "ß" prints correctly with LuaLaTeX and the default fonts (#346)
* Documents built without `nodeprecatedcode` (including package mode) no longer stop with "Undefined color `statblockbg'"; the old name is kept as an alias of `statblockbg14`
* `\\` and `\newline` in part, chapter and section titles no longer break the table of contents; they break the line in the heading and show as a space in the contents, bookmarks and footer
* Appendices in an `\include`d file are labeled "Appendix" in the table of contents instead of "Ch."

## [0.8.0] - 2020-04-21

### Added in 0.8.0

* `\DndSetFonts` allows setting of font family and style throughout the document
* Added Spanish captions
* Added styling for the Table of Contents, using the `titletoc` package
* Added styling for `\part`
* Added colors from the 2018 Basic Rules
* Added `nodeprecatedcode` option to exclude deprecated code from building
* Added `\DndFeatHeader`

### Changed in 0.8.0

* Rewrite internals in LaTeX3
* `dndtable` becomes `DndTable`
* `commentbox`, `paperbox`, and `quotebox` become `DndComment`, `DndSidebar`, and `DndReadAloud`
* `\subtitlesection`, `\spellheader`, `\area`, and `\subarea` become `\DndItemHeader`, `\DndSpellHeader`, `\DndArea`, and `\DndSubArea`
* `monsterbox` becomes `DndMonster`
* Separated language files
* Added contour to styling for `\chapter`

## [0.7.1] - 2019-07-18

### Added in 0.7.1

* Added `DndDropCapLine` command to create drop capital letters at chapter beginnings
* Configured CI to compile example document under pdfTeX, LuaTeX, and XeTeX.
* Japanese translation

### Changed in 0.7.1

* Sans serif title font now provided by kp-fonts
* Sans serif body font now provided by gillius
* Overhaul of whitespace and styling

## [0.7.0] - 2019-02-09

### Added in 0.7.0

* Added `bg` package option with `full`, `print`, and `none` as possible values.
* Added boolean `layout` package option to control whether the package formats the document on load.
* Added `nomultitoc` package option to toggle multi-column table of contents.
* Added `dndbook` document class.
* Added low-resolution background file as an option.
* Added Russian localization support.
* Added keycommands to generate text for melee, ranged, and hybrid (melee or ranged) attacks within monsterboxes. Includes localization support for the various phrases used.
* Added commands to generate titled sections for map areas and sub-areas, with associated counters and automatic reference labelling (as `area:<title>`).
* Added commands to help generate spell lists.

### Changed in 0.7.0

* Made `monsterbox` text the width of the column and the background spills into margin and column separator.
* Removed excess space before and after `monsterbox`.
* Challenge rating on `monsterbox` now only needs the CR number.
* `monsterbox` renamed `monsterboxbg`. `monsterbox` is now an alias that maps to `monsterboxbg` or `monsterboxnobg`, depending on the value of the `bg` package option.
* Limited set of pre-loaded `tcolorbox` libraries to `breakable`, `skins`, and `xparse`.
* Title formats for sections now explicitly use `\RaggedRight` to avoid poor layout appearance when using justified output.
* Prevents page breaks immediately following section/subsection/subsubsection titles.
* Removed deprecated `dnditemtable`.
* Removed deprecated `bg-a4` and `bg-letter` package options.
* Removed deprecated `lmss` environment.

### Fixed in 0.7.0

* Display monster elements with hanging indents.
* Allow `\monstersection` before sectioning command(s).
* Removed excess space after `\dice`.
* `monsteraction`: Only add a period to the action name if provided one.
* Set fontlower on all tcolorbox environments.
* Fixed footer scroll and text alignment.
* Added `\xpname` to localization support.
* Added localization to XP number

### Deprecated in 0.7.0

* Deprecated `bg-full`, `bg-none`, and `bg-print` package options. Use `bg` package option instead.
* Deprecated custom `\hline` in stat blocks. Use `\dndline` instead.

## [0.6.0] - 2017-10-12

### Added in 0.6.0

* Added `bg-none` option to disable background image.
* Defined coral-coloured `dnditemtable` environment.
* Added `monsterboxnobg` environment for stat blocks without a background image.
* Defined `\header` command for table headers.
* Defined `\subtitlesection` command to format short object descriptions.
* Customized `\tableofcontents`.
* Added custom centred column type (`Y`) for `dndtable`.
* Defined `\dice` macro to compute average dice roll.
* Added localization support.
* Added Italian localization.
* Defined bold italic `\paragraph` and `\subparagraph` commands.
* Customized `itemize` to match book style.
* Added `themecolor` and customizable box colours.
* Defined additional colours matching core books.
* Defined `spell` environment to format spells.
* Added plain footer style for `bg-none` package option.

### Changed in 0.6.0

* Separate fancyhdr code into separate file.
* Switch layout package from fullpage to geometry.
* `\stat` macro computes modifier automatically.
* Modified `dndtable` to support multiple columns (default: 2).
* Disable "Chapter" prefix for `\chapter`.
* Changed suggested class from `article` to `book`.
* Enabled ragged alignment by default (disable with `justified` package option).
* Separated the footer scroll from the background image.

### Fixed in 0.6.0

* `\stats` tables have stable size inside stat block environments.
* Fixed typos in example image.
* Made odd rows transparent in `dndtable`.
* Fixed paragraph and line spacing.
* Remove `breakable` parameter from `paperbox`.
* Allow commas in newtcolorbox titles.

### Deprecated in 0.6.0

* Deprecated `dnditemtable`.
* Deprecated `bg-a4` and `bg-letter` package options.
* Deprecated `lmss` environment.

## [0.5] - 2016-03-24

### Added in 0.5.0

* Added print variants of background images (`bg-print` package option).
* Added package option to control letter size background images (`bg-letter`).
* Added A4 size background images (`bg-a4` package option).

### Changed in 0.5.0

* Licensed under MIT license.
* Removed dependency on `multicols`; use `twocolumn` option for `book` class instead.

### Fixed in 0.5.0

* Fixed footer positioning.
* Fixed spacing inside and around boxes.
* Disabled indentation after boxes.
* Enabled indentation within boxes.

### Removed in 0.5.0

* Removed `monster` environment.

## [0.2] - 2016-03-07

## Added in 0.2.0

* Added preview to README.
* Defined `monster` and `monsterbox` environments for formatting monster stat blocks.
* Defined `dndtable` environment for formatting tables.
* Defined `quotebox` environment for formatting dialogue.
* Added old paper style background images.
* Added fancy page footers.
* Defined `paperbox` environment to format sidebars.

## Changed in 0.2.0

* Reorganized package layout.
* Matched colours against published PDFs.
* Removed numbering from section titles.
* Set `\raggedcolumns` to flush content to top of column.

## 0.1 - 2015-05-12

### Added in 0.1.0

* Defined green `commentbox` environment.
* Section and subsection titles.

[Unreleased]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.8.0...HEAD
[0.7.1]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.5...v0.6.0
[0.5]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.2...v0.5
[0.2]: https://github.com/rpgtex/DND-5e-LaTeX-Template/compare/v0.1...v0.2
