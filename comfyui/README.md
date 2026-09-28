# Book art workflows (ComfyUI + Ideogram 4)

ComfyUI workflows that generate art for books made with this template, in the style of the 2014 core books. They run **entirely locally** on the Ideogram 4 open weights: no API or partner nodes, no credits and no cloud services. The only network access is downloading the models below once.

Generated images belong in the book's repository (see the starter repo, which keeps art in Git LFS), not here.

## Setup

1. Install [ComfyUI](https://www.comfy.org/) 0.37 or later. The base workflow uses only core nodes, so no custom node packs are needed.
2. Put these models in ComfyUI's `models` folder:

   | Folder | File | Used for |
   | --- | --- | --- |
   | `diffusion_models` | `ideogram4_fp8_scaled.safetensors` | Ideogram 4, conditional |
   | `diffusion_models` | `ideogram4_unconditional_fp8_scaled.safetensors` | Ideogram 4, unconditional (guidance) |
   | `text_encoders` | `qwen_3_8b.safetensors` | Text encoder (CLIP type `ideogram4`) |
   | `vae` | `flux2-vae.safetensors` | VAE |
   | `loras` | `Realism_Engine_Ideogram4_V1.safetensors` | Guard LoRA on both models, strength 1.0 (see below) |
   | `upscale_models` | `RealESRGAN_x4plus.pth` | 4x upscale for print ([Real-ESRGAN v0.1.0](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.1.0), BSD-3) |

3. Drag a workflow from `workflows/` onto the ComfyUI canvas.

## Workflows

| File | Purpose |
| --- | --- |
| `workflows/dnd_art_t2i.json` | Base text-to-image workflow: house style, draft, then print-size output |
| `generate.py` | Runs a jobs file through the workflow (see [Generating from a jobs file](#generating-from-a-jobs-file)) |
| `banned-terms.txt` | Terms `generate.py` refuses in prompts |

The cover, NPC portrait and interior art workflows (issues #16, #17 and #18) build on the base workflow.

## House style

Every workflow joins the scene (**SUBJECT**) and the shared **HOUSE_STYLE** text into one prompt. SUBJECT says what is in the picture. HOUSE_STYLE says how it is painted: an oil-on-canvas look, a warm natural palette, dramatic light, and no text or logos. Change the style in one place, `dnd_art_t2i.json`, and copy it to the other workflows.

Keep HOUSE_STYLE about the painting: medium, palette, lighting and composition. Do not describe figures or armour there. A version with a "Figures: … practical weathered armour and gear" line turned almost every subject into a line-up of armoured heroes facing the viewer: the lich became a living knight, the spot-art sword gained two men holding it, and the sahuagin became humans. A short version without palette, lighting and composition detail got the subjects right but looked flatter and less like the core books.

Keep the line "Every person is fully clothed in period fantasy dress. No nudity." With the short style and the guard LoRA, the model sometimes drew a figure nude when the subject did not mention clothing. In tests with the line, 4 of 4 seeds were clothed, including one that was nude without it.

Tips for SUBJECT:

- Describe unusual creatures instead of only naming them. "An owlbear" came out as a plain bear; "an owlbear, a huge bear with an owl's feathered face and hooked beak" works better.
- For spot art, say "on a plain parchment background, spot illustration".
- The model sometimes adds a small signature scribble in a corner despite "no signature". Crop or retouch it before placing the image.

Rules for prompts:

- No WotC logos, the D&D ampersand, trade dress or product identity (beholders, mind flayers, displacer beasts, Forgotten Realms names and so on). Use SRD creatures and your own setting. `generate.py` refuses prompts that contain any term in `banned-terms.txt`.
- No living artists' names.
- No person-likeness LoRAs.
- No text in images. LaTeX sets titles, captions and labels.

## Guard LoRAs

Without a LoRA on **both** the conditional and the unconditional model, the base Ideogram 4 weights ignore the prompt. They return a grey "Image blocked by safety filter" card, which the model paints itself (it is not a ComfyUI filter), or an unrelated photo. How often this happens depends on the seed and on the total LoRA strength. In tests with the Realism Engine LoRA on both models, 3 of 4 seeds came back blocked at strength 0.6 and 0 of 4 at 1.0, and the house style still made the result painterly. Keep both LoRAs at 1.0 until there is a house-style LoRA of our own to replace them.

## Draft, then print

The workflows show results in Preview nodes and do not write files. Drafts are generated at Ideogram's native size, and **Seed used** shows the seed of the last run. When you like a draft, copy its seed into **SEED**, set it to `fixed`, unmute the **Print** group (select it, then press Ctrl+M) and queue again. The print stage upscales 4x with Real-ESRGAN and then scales to the print size with Lanczos. Right-click the print preview and choose **Save Image** to keep it.

Write down the seed and the SUBJECT of every image you keep. Together with the workflow, they are enough to regenerate the image. `generate.py` does this for you.

## Generating from a jobs file

`generate.py` runs a list of images through the running ComfyUI server. It needs only Python 3; with Pillow installed, it also spots the grey blocked card and retries with a new seed.

```
python comfyui/generate.py mybook/art/jobs.json
python comfyui/generate.py mybook/art/jobs.json --only cover-hero
python comfyui/generate.py mybook/art/jobs.json --check     # banned-terms check only
python comfyui/generate.py mybook/art/jobs.json --dry-run   # sizes and prompts, no images
```

A jobs file lists the images:

```json
{
  "out": "generated",
  "jobs": [
    { "name": "keep-at-dusk", "preset": "chapter", "subject": "A ruined hilltop keep at dusk ...", "count": 4 },
    { "name": "dwarf-cleric", "preset": "column", "subject": "...", "seed": 81762, "print": true }
  ]
}
```

- `preset` is one of `full-page`, `chapter`, `span`, `column` or `square`, or `cover-front`, `cover-back` or `cover-wrap` (see [Sizes](#sizes)). `gen` and `print_size` override the sizes, e.g. `"gen": [1024, 1024]`.
- Cover presets also take `title_position` (`top` or `bottom`, as in `\DndFrontCover`), `trim` (`[8.5, 11]`), `bleed` (`0.125`) and `spine` (`0.25`), in inches. Each cover image also gets a `_guides.png` copy showing the trim (cyan), the spine folds, the safe area (magenta), the title, author and blurb areas (yellow) and a barcode space (white), matching what `\DndCoverSpread[guides]` draws.
- `composition` sets the COMPOSITION text (where things go, what to keep empty). Cover presets fill it in; set it to `""` to leave it empty.
- `count` is the number of images, each with a random seed. `seed` fixes the seed, for example to reproduce a draft.
- `draft: true` is for trying out ideas quickly: the Turbo schedule at 0.7 × the generate size (about half the pixels, roughly a minute per image). Use the same seed without `draft` to get the finished image, which will differ in detail.
- `schedule` is `turbo`, `default` or `quality` (12, 20 or 48 steps). Without it, the job uses the workflow's own setting.
- `print: true` also runs the print stage.
- `out` is the output folder, relative to the jobs file.

The script reads the workflow (`workflows/dnd_art_t2i.json`, or `--workflow`) each time it runs. To change the house style, models or sampler settings, edit them in ComfyUI and save the workflow over that file. The script finds the nodes it fills in by their titles: SUBJECT, COMPOSITION, HOUSE_STYLE, GEN_WIDTH, GEN_HEIGHT, SEED and "Scale to print size". Keep those titles.

Each image is written as `<name>_<seed>_draft.png` (and `_print.png`), with `<name>_<seed>.json` beside it. The JSON records the subject, house style, seed, sizes, LoRAs and a hash of the workflow file: the image's provenance. `comfyui/jobs/example.json` has three sample jobs, `comfyui/jobs/covers.json` has front, back and wraparound covers, and `comfyui/jobs/house-style-test.json` has 12 drafts for judging the house style across characters, scenes, SRD creatures, items and every preset. Their output goes to `comfyui/jobs/generated/`, which git ignores.

## Sizes

Print needs 300 ppi at the final size. The sizes below are for letter paper with the template's layout: 0.75 in side margins, 0.33 in between the columns (so the text is 7.0 in wide and each column 3.335 in), and a 0.125 in bleed on every edge. Set **GEN_WIDTH** and **GEN_HEIGHT** to the Generate size, and the **Scale to print size** node to the Print size. The generate sizes are multiples of 16, about 2 megapixels, and within 0.5% of the print shape; the print stage crops the difference from the centre.

| Command | Generate | Print (px) | Print size (in) |
| --- | --- | --- | --- |
| `\DndFullPageImage`, `\DndPartArt`, `\DndFacingArt`, `\DndPageBackground` | 1232 × 1584 | 2625 × 3375 | 8.75 × 11.25, full bleed |
| `\DndChapterArt` (default `height=.4\paperheight`) | 2016 × 1040 | 2625 × 1350 | 8.75 × 4.5, bleed on top and sides |
| `\DndFadedImage*`, `\DndSpanImage` (2:1) | 1920 × 960 | 2100 × 1050 | 7.0 × 3.5 |
| `\DndFadedImage` in a column, portrait (3:4) | 1200 × 1600 | 1000 × 1335 | 3.335 × 4.45 |
| `\DndFadedImage` in a column, square, or spot art | 1344 × 1344 | 1000 × 1000 | 3.335 × 3.335 |

### Covers

Cover sizes depend on the trim size, bleed and, for the wraparound spread, the spine width from your printer's cover calculator. `generate.py` works them out; the defaults are letter trim, 0.125 in bleed and a 0.25 in spine.

| Preset | Command | Sheet (in) | Print (px) at the defaults |
|---|---|---|---|
| `cover-front` | `\DndFrontCover`, or `art=` of `\DndCoverSpread` | trim + 2 × bleed: 8.75 × 11.25 | 2625 × 3375 |
| `cover-back` | `\DndBackCover`, or `back-art=` | trim + 2 × bleed: 8.75 × 11.25 | 2625 × 3375 |
| `cover-wrap` | `wrap-art=` of `\DndCoverSpread` | 2 × trim width + spine + 2 × bleed: 17.5 × 11.25 | 5250 × 3375 |

Each cover preset fills **COMPOSITION** with where the subject goes and what to keep empty. The template sets the title and subtitle 0.75 in from the top of the trim, and the author 0.75 in from the bottom; with `title-position=bottom` they swap. The back cover's blurb box sits just above the middle, and printers usually put the barcode in the lower right. For a wraparound, the subject goes in the right half (the front cover), and the left half stays quiet for the blurb.

The generated art needs no text: LaTeX sets the title, subtitle, author, blurb and spine text.

For A4 (8.27 × 11.69 in) or another bleed, work out the print size as inches × 300. For full-bleed art, add twice the bleed to the width and to the height.
