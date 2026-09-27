# Example books

Three short books, each showing a different set of options. Build them from the template folder; they find the template there without installing it.

| Book | Look | Shows |
| ---- | ---- | ----- |
| [`adventure`](adventure/adventure.tex) | 2014 core books | Solbera's fonts, the full parchment background, SRD 5.1, covers in the screen editions and a print cover spread ([`cover.tex`](adventure/cover.tex)), chapter art, a drop cap, read-aloud text, numbered areas on a map, a classic stat block |
| [`player-options`](player-options/player-options.tex) | 2024 core books | `style=2024` (white pages, sans-serif headings, modern stat blocks), SRD 5.2.1, text that follows the SRD version (`\DndIfSRD`), justified text, colored links, a class table, a spell list, an index |
| [`gazetteer`](gazetteer/gazetteer.tex) | German, A4 | German captions and SRD attribution, A4 paper, LuaLaTeX, part art, faded images, tables, comments and quotations |

Build every edition of a book, and check each one:

```sh
make fonts   # once, for the adventure's fonts
make preflight BOOK=examples/adventure/adventure.tex ENGINE=xelatex
make preflight BOOK=examples/player-options/player-options.tex
make preflight BOOK=examples/gazetteer/gazetteer.tex ENGINE=lualatex
```

or all three at once with `make examples`. Each writes `<book>-screen.pdf`, `<book>-print.pdf`, `<book>-printer-friendly.pdf` and, for the adventure, `<book>-cover.pdf` next to the book. Build the player options for the 2014 rules from the same source with `SRD=5.1`.

Without `make`, use `texlua bin/build`, e.g. `texlua bin/build --engine=xelatex all examples/adventure/adventure.tex`.

The art in [`art`](art) is placeholder texture generated with ImageMagick, at 300 ppi for letter and A4 pages with bleed.
