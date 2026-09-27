# The 2024 style (provisional)

What `style=2024` is based on, and what is still unverified. Written for issue #8 on 2026-09-27.

**Status: provisional.** No pages of the 2024 Player's Handbook, Dungeon Master's Guide or Monster Manual were examined for this. Check it against the books before relying on it for a product, and update this document with what you find.

## Sources

1. **WotC's System Reference Document 5.2.1** ([PDF](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf), CC BY 4.0). WotC laid it out in InDesign in a simplified version of the 2024 books' layout. The colors and heading sizes below were measured from it. Its fonts are Cambria (body), Gill Sans (headings, tables), Optima and Scala Sans. Those are probably stand-ins, not the books' own typefaces.
2. **A third-party DMs Guild template that imitates the 2024 books** ([product page](https://www.dmsguild.com/en/product/510078/d-d-5e-2024-indesign-template), [preview PDF](https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/510078-sample.pdf)). It embeds Modesto Condensed, Bookmania, Scala Sans Pro, Mrs Eaves Small Caps and OPTI Pegasus. That is its author's reading of the books, not a WotC source.
3. **Reviews** describe the 2024 PHB as having "a larger, bolder font with higher contrast, offset against brighter white pages" (via web search, 2026-09-27; not checked against a copy).

The typefaces of the 2024 books themselves are not confirmed by any of these.

## Measured from SRD 5.2.1

Colors, sampled from page 5 rendered at 100 and 300 dpi:

| Element | Color | Template color name |
| ------- | ----- | ------------------- |
| Headings | `#881A20` | `titlered24` |
| Rule under subsections | `#CBA95C` | `titlegold24` |
| Sidebars, table stripes | `#E9E9E9` | `boxgray24` |
| Text | `#231F20` | not used (black) |
| Page | white | `bg=none` |

Heading sizes, estimated from cap heights on page 5 at 300 dpi (Gill Sans cap height ≈ 0.68 em), so ±1pt:

| Heading | SRD 5.2.1 | Template (`style=2024`, 10pt body) |
| ------- | --------- | ---------------------------------- |
| Chapter ("Playing the Game") | about 26pt, bold, red | 26pt (`\DndRelativeSize{2.6}`) |
| Section ("Rhythm of Play") | about 18pt, bold, red | 18pt |
| Subsection, with gold rule ("Ability Scores") | about 15pt, bold, red | 15pt |
| Table title ("Ability Descriptions") | about 9.5pt, bold, dark | unchanged table title |
| Subsubsection | not seen on the sampled page | 12pt, bold, black |

Other layout seen in the SRD: headings in upper and lower case (not small caps), no outline on titles; tables in sans serif with a bold header row and gray stripes; gray sidebars with a small-caps title; page number and document title in the footer.

The SRD's page size is 594 × 783pt (8.25 × 10.875in).

## What `style=2024` changes

- `bg=none` (white pages, no footer scroll) and `stats=modern`, unless the document sets `bg` or `stats`
- `titlered`, `titlegold` and the theme color (sidebars, comments, table stripes) take the colors above
- Part, chapter, section, subsection and subsubsection titles and the table of contents use a bold sans-serif face in upper and lower case, at the sizes above: Gillius (a free Gill Sans clone, GPL with the font exception) with the default fonts, and the font set's sans-serif face otherwise (Scaly Sans with `fonts=solbera`)
- Part and chapter titles lose the gray outline

Everything else (maps, covers, class tables, handouts, credits) works unchanged.

## Not done yet

Each needs a look at the books:

- **Typefaces:** confirm the body, heading and sidebar faces and find free, commercially usable substitutes. Solbera's fonts imitate the 2014 books only.
- **Page background:** the books may have a subtle texture rather than plain white.
- **Chapter openers:** art placement and title treatment.
- **Footer:** the SRD shows the page number beside the document title; the books' running footer is unconfirmed. The template keeps its 2014 footer text, without the scroll.
- **Boxes:** read-aloud text, sidebars and notes may differ from the SRD's gray boxes.
