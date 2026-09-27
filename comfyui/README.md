# Book art workflows (ComfyUI + Ideogram 4)

ComfyUI workflows that generate art for books made with this template, in the style of the 2014 core books. They run **entirely locally** on the Ideogram 4 open weights: no API or partner nodes, no credits and no cloud services. The only network access is downloading the models below once.

Generated images belong in the book's repository (see the starter repo, which keeps art in Git LFS), not here.

## Setup

1. Install [ComfyUI](https://www.comfy.org/) 0.37 or later. The base workflow uses only core nodes, so no custom node packs are needed.
2. Put these models in ComfyUI's `models` folder:

| Folder | File | Used for |
|---|---|---|
| `diffusion_models` | `ideogram4_fp8_scaled.safetensors` | Ideogram 4, conditional |
| `diffusion_models` | `ideogram4_unconditional_fp8_scaled.safetensors` | Ideogram 4, unconditional (guidance) |
| `text_encoders` | `qwen_3_8b.safetensors` | Text encoder (CLIP type `ideogram4`) |
| `vae` | `flux2-vae.safetensors` | VAE |
| `loras` | `Realism_Engine_Ideogram4_V1.safetensors` | Guard LoRA on both models, strength 1.0 (see below) |
| `upscale_models` | `RealESRGAN_x4plus.pth` | 4x upscale for print ([Real-ESRGAN v0.1.0](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.1.0), BSD-3) |

3. Drag a workflow from `workflows/` onto the ComfyUI canvas.

## Workflows

| File | Purpose |
|---|---|
| `workflows/dnd_art_t2i.json` | Base text-to-image workflow: house style, draft, then print-size output |

The cover, NPC portrait and interior art workflows (issues #16, #17 and #18) build on the base workflow.

## House style

Every workflow joins the scene (**SUBJECT**) and the shared **HOUSE_STYLE** text into one prompt. SUBJECT says what is in the picture. HOUSE_STYLE says how it is painted: an oil-on-canvas look, grounded figures, a warm natural palette, dramatic light, and no text or logos. Change the style in one place, `dnd_art_t2i.json`, and copy it to the other workflows.

Rules for prompts:

- No WotC logos, the D&D ampersand, trade dress or product identity (beholders, mind flayers, displacer beasts, Forgotten Realms names and so on). Use SRD creatures and your own setting.
- No living artists' names.
- No person-likeness LoRAs.
- No text in images. LaTeX sets titles, captions and labels.

## Guard LoRAs

Without a LoRA on **both** the conditional and the unconditional model, the base Ideogram 4 weights ignore the prompt. They return a grey "Image blocked by safety filter" card, which the model paints itself (it is not a ComfyUI filter), or an unrelated photo. How often this happens depends on the seed and on the total LoRA strength. In tests with the Realism Engine LoRA on both models, 3 of 4 seeds came back blocked at strength 0.6 and 0 of 4 at 1.0, and the house style still made the result painterly. Keep both LoRAs at 1.0 until there is a house-style LoRA of our own to replace them.

## Draft, then print

The workflows show results in Preview nodes and do not write files. Drafts are generated at Ideogram's native size, and **Seed used** shows the seed of the last run. When you like a draft, copy its seed into **SEED**, set it to `fixed`, unmute the **Print** group (select it, then press Ctrl+M) and queue again. The print stage upscales 4x with Real-ESRGAN and then scales to the print size with Lanczos. Right-click the print preview and choose **Save Image** to keep it.

Write down the seed and the SUBJECT of every image you keep. Together with the workflow, they are enough to regenerate the image.

## Sizes

Print needs 300 ppi at the final size, including bleed.

| Use | Generate | Print | Print size |
|---|---|---|---|
| Full page, full bleed (`\DndFullPageImage`, `\DndPartArt`, `\DndFacingArt`) | 1232 × 1584 | 2625 × 3375 | 8.75 × 11.25 in (letter + 0.125 in bleed) |

More presets come with #16–#18.
