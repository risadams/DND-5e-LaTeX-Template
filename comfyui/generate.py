#!/usr/bin/env python3
"""Generate book art from a jobs file through a local ComfyUI server.

    python comfyui/generate.py jobs.json            # run every job
    python comfyui/generate.py jobs.json --only cover-hero
    python comfyui/generate.py jobs.json --check    # check prompts only

The workflow file (comfyui/workflows/dnd_art_t2i.json by default) is the
single source of truth: the script loads it, fills in each job's subject,
size, seed and print stage, and queues it. Edit the house style, models or
sampler settings in ComfyUI and save the workflow; the script picks them up.

Images come back through the workflow's Preview nodes and are written next
to the jobs file with a .json sidecar (prompt, seed, sizes, models), so
every image can be regenerated. Needs only the Python standard library;
with Pillow installed it also spots the grey "Image blocked by safety
filter" card and retries with a new seed.
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORKFLOW = os.path.join(HERE, "workflows", "dnd_art_t2i.json")
BANNED_FILE = os.path.join(HERE, "banned-terms.txt")

# Generate and print sizes per template command (see README, "Sizes").
PRESETS = {
    "full-page": {"gen": (1232, 1584), "print": (2625, 3375)},
    "chapter":   {"gen": (2016, 1040), "print": (2625, 1350)},
    "span":      {"gen": (1920, 960),  "print": (2100, 1050)},
    "column":    {"gen": (1200, 1600), "print": (1000, 1335)},
    "square":    {"gen": (1344, 1344), "print": (1000, 1000)},
}

# Cover presets: sizes come from the trim size, bleed and spine (inches).
COVER_PRESETS = {"cover-front", "cover-back", "cover-wrap"}
COVER_DEFAULTS = {"trim": [8.5, 11], "bleed": 0.125, "spine": 0.25, "title_position": "top"}
PPI = 300

# Default COMPOSITION text per cover preset and title position.
COMPOSITION = {
    ("cover-front", "top"):
        "Book cover composition: the main subject is large and fills the lower two thirds "
        "of the picture, centred. The top quarter of the picture is calm, uncluttered sky or "
        "shadow with no important detail, reserved for the title. Nothing important near the edges.",
    ("cover-front", "bottom"):
        "Book cover composition: the main subject is large and fills the upper two thirds "
        "of the picture, centred. The bottom third of the picture is calm, uncluttered ground or "
        "shadow with no important detail, reserved for the title. Nothing important near the edges.",
    ("cover-back", None):
        "Back cover composition: a quiet, atmospheric scene with no central figure. The middle "
        "of the picture is calm and evenly toned, suitable for a block of text over it. "
        "The lower right corner is plain.",
    ("cover-wrap", "top"):
        "A very wide panoramic scene for a wraparound book cover. The main subject is large, in "
        "the right half of the picture. The left half continues the same scene quietly, with a "
        "calm, evenly toned area in its middle and no figures there. The top quarter of the right "
        "half is calm sky, reserved for the title. Nothing important in a narrow strip down the "
        "exact centre.",
    ("cover-wrap", "bottom"):
        "A very wide panoramic scene for a wraparound book cover. The main subject is large, in "
        "the upper part of the right half of the picture. The left half continues the same scene "
        "quietly, with a calm, evenly toned area in its middle and no figures there. The bottom "
        "third of the right half is calm ground or shadow, reserved for the title. Nothing "
        "important in a narrow strip down the exact centre.",
}

# Ideogram4Scheduler settings: steps, mu, std.
SCHEDULES = {
    "turbo":   (12, 0.5, 1.75),
    "default": (20, 0.0, 1.75),
    "quality": (48, 0.0, 1.5),
}

# Node titles the script looks for in the workflow.
T_SUBJECT, T_STYLE = "SUBJECT", "HOUSE_STYLE"
T_WIDTH, T_HEIGHT, T_SEED = "GEN_WIDTH", "GEN_HEIGHT", "SEED"
T_PRINT_SCALE = "Scale to print size"
T_COMPOSITION = "COMPOSITION"
SKIP_TYPES = {"MarkdownNote", "Note"}
WIDGET_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"}
MUTED, BYPASSED = 2, 4


def load_banned():
    terms = []
    with open(BANNED_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line)
    return terms


def banned_in(text, terms):
    found = []
    for term in terms:
        if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.IGNORECASE):
            found.append(term)
    return found


class Comfy:
    def __init__(self, url):
        self.url = url.rstrip("/")

    def get(self, path):
        with urllib.request.urlopen(self.url + path) as r:
            return json.load(r)

    def post(self, path, data):
        req = urllib.request.Request(self.url + path, json.dumps(data).encode(),
                                     {"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            return json.load(r)

    def image(self, img):
        q = urllib.parse.urlencode({"filename": img["filename"],
                                    "subfolder": img.get("subfolder", ""),
                                    "type": img.get("type", "temp")})
        with urllib.request.urlopen(f"{self.url}/view?{q}") as r:
            return r.read()


def node_by_title(wf, title, prefix=False):
    for n in wf["nodes"]:
        t = n.get("title", "")
        if t == title or (prefix and t.startswith(title)):
            return n
    raise SystemExit(f"workflow has no node titled {title!r}")


def to_api(wf, info, include_muted):
    """Convert a UI-format workflow to the API format the /prompt endpoint takes."""
    links = {l[0]: (l[1], l[2]) for l in wf["links"]}
    api = {}
    for n in wf["nodes"]:
        if n["type"] in SKIP_TYPES or n.get("mode") == BYPASSED:
            continue
        if n.get("mode") == MUTED and not include_muted:
            continue
        spec = info[n["type"]]["input"]
        order = info[n["type"]].get("input_order", {})
        names = order.get("required", list(spec.get("required", {}))) + \
            order.get("optional", list(spec.get("optional", {})))
        linked = {i["name"]: i["link"] for i in n.get("inputs", []) if i.get("link") is not None}
        values = list(n.get("widgets_values") or [])
        inputs = {}
        for name in names:
            s = spec.get("required", {}).get(name) or spec.get("optional", {}).get(name)
            kind, opts = s[0], (s[1] if len(s) > 1 else {})
            is_widget = isinstance(kind, list) or kind in WIDGET_TYPES
            if is_widget and not opts.get("forceInput"):
                value = values.pop(0) if values else opts.get("default")
                if opts.get("control_after_generate") and values:
                    values.pop(0)
                if name not in linked and value is not None:
                    inputs[name] = value
            if name in linked:
                src, slot = links[linked[name]]
                inputs[name] = [str(src), slot]
        api[str(n["id"])] = {"class_type": n["type"], "inputs": inputs}
    # Drop links to nodes that were left out (e.g. the muted print stage).
    for node in api.values():
        for k, v in list(node["inputs"].items()):
            if isinstance(v, list) and v[0] not in api:
                del node["inputs"][k]
    return api


def workflow_name(path):
    """The workflow path relative to comfyui/, or absolute if it is elsewhere."""
    try:
        rel = os.path.relpath(path, HERE)
    except ValueError:  # another drive on Windows
        return path.replace(os.sep, "/")
    return (path if rel.startswith("..") else rel).replace(os.sep, "/")


def gen_for_ratio(ratio, lo=1.8, hi=2.1):
    """Width and height, multiples of 16 and lo-hi megapixels, closest to ratio."""
    best = None
    for w in range(512, 4096, 16):
        for h in range(512, 4096, 16):
            if lo <= w * h / 1e6 <= hi:
                err = abs(w / h - ratio)
                if best is None or err < best[0]:
                    best = (err, w, h)
    return best[1], best[2]


def cover_geometry(job):
    """Sheet layout of a cover job in inches (see lib/dndcover.sty)."""
    g = {k: job.get(k, v) for k, v in COVER_DEFAULTS.items()}
    tw, th = g["trim"]
    b, s = g["bleed"], g["spine"]
    if job["preset"] == "cover-wrap":
        g["sheet"] = [2 * tw + s + 2 * b, th + 2 * b]
        g["panels"] = {"back": b, "front": b + tw + s}
    else:
        g["sheet"] = [tw + 2 * b, th + 2 * b]
        g["panels"] = {job["preset"][len("cover-"):]: b}
    return g


def job_layout(job):
    """Preset name, generate size, print size, composition text and cover geometry."""
    name = job.get("preset", "full-page")
    geom = None
    if name in COVER_PRESETS:
        geom = cover_geometry(job)
        sw, sh = geom["sheet"]
        gen, prt = gen_for_ratio(sw / sh), (round(sw * PPI), round(sh * PPI))
        pos = None if name == "cover-back" else geom["title_position"]
        composition = COMPOSITION[(name, pos)]
    else:
        gen, prt, composition = PRESETS[name]["gen"], PRESETS[name]["print"], ""
    gen = tuple(job.get("gen", gen))
    prt = tuple(job.get("print_size", prt))
    composition = job.get("composition", composition)
    return name, gen, prt, composition, geom


def draw_guides(png, geom, preset):
    """A smaller copy of a cover image with trim, fold, safe-area and text areas drawn on."""
    try:
        from io import BytesIO
        from PIL import Image, ImageDraw
    except ImportError:
        return None
    im = Image.open(BytesIO(png)).convert("RGB")
    im.thumbnail((1800, 1800))
    sw, sh = geom["sheet"]
    tw, th = geom["trim"]
    b, k = geom["bleed"], im.width / sw
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)

    def box(x0, y0, x1, y1, outline=None, fill=None, width=2):
        # inches from the top-left corner of the sheet
        d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=outline, fill=fill, width=width)

    box(b, b, sw - b, sh - b, outline=(0, 255, 255, 255))  # trim
    if preset == "cover-wrap":
        for x in (b + tw, b + tw + geom["spine"]):  # spine folds
            d.line([x * k, 0, x * k, im.height], fill=(0, 255, 255, 255), width=2)
    for panel, x0 in geom["panels"].items():
        box(x0 + .25, b + .25, x0 + tw - .25, b + th - .25, outline=(255, 0, 255, 255))  # safe area
        if panel == "front":
            if geom["title_position"] == "top":
                title, author = (b + .75, b + 2.35), (b + th - 1.15, b + th - .75)
            else:
                title, author = (b + th - 3.1, b + th - 1.5), (b + .75, b + 1.15)
            for y0, y1 in (title, author):
                box(x0 + .75, y0, x0 + tw - .75, y1, fill=(255, 220, 0, 90))
        else:
            cy = b + .45 * th  # blurb box centre, measured from the top
            box(x0 + .75, cy - 2, x0 + tw - .75, cy + 2, fill=(255, 220, 0, 90))
            box(x0 + tw - .25 - 2, b + th - .25 - 1.2, x0 + tw - .25, b + th - .25,
                fill=(255, 255, 255, 140))  # barcode
    im = Image.alpha_composite(im.convert("RGBA"), over).convert("RGB")
    out = BytesIO()
    im.save(out, "PNG")
    return out.getvalue()


def is_blocked(png):
    try:
        from io import BytesIO
        from PIL import Image, ImageStat
    except ImportError:
        return False
    im = Image.open(BytesIO(png)).convert("L").resize((128, 160))
    return ImageStat.Stat(im).stddev[0] < 12


def run_job(comfy, info, wf, wf_hash, job, out_dir, max_retries):
    preset_name, (gen_w, gen_h), (print_w, print_h), composition, geom = job_layout(job)
    draft = bool(job.get("draft", False))
    schedule = job.get("schedule", "turbo" if draft else None)
    if draft and "gen" not in job:
        gen_w, gen_h = round(gen_w * .7 / 16) * 16, round(gen_h * .7 / 16) * 16  # about half the pixels
    do_print = bool(job.get("print", False))
    fixed_seed = job.get("seed")
    style = node_by_title(wf, T_STYLE, prefix=True)["widgets_values"][0]

    results = []
    for i in range(job.get("count", 1)):
        seed = fixed_seed if fixed_seed is not None else random.randrange(2**50)
        for attempt in range(max_retries + 1):
            node_by_title(wf, T_SUBJECT, prefix=True)["widgets_values"][0] = job["subject"]
            node_by_title(wf, T_COMPOSITION, prefix=True)["widgets_values"][0] = composition
            node_by_title(wf, T_WIDTH)["widgets_values"][0] = gen_w
            node_by_title(wf, T_HEIGHT)["widgets_values"][0] = gen_h
            node_by_title(wf, T_SEED)["widgets_values"][:2] = [seed, "fixed"]
            scale = node_by_title(wf, T_PRINT_SCALE, prefix=True)
            scale["widgets_values"][1:3] = [print_w, print_h]
            if schedule:
                sched = next(n for n in wf["nodes"] if n["type"] == "Ideogram4Scheduler")
                steps, mu, std = SCHEDULES[schedule]
                sched["widgets_values"][0] = steps
                sched["widgets_values"][3:5] = [mu, std]

            api = to_api(wf, info, include_muted=do_print)
            t0 = time.time()
            pid = comfy.post("/prompt", {"prompt": api})["prompt_id"]
            while True:
                time.sleep(2)
                hist = comfy.get(f"/history/{pid}")
                if pid in hist:
                    break
            entry = hist[pid]
            if entry["status"].get("status_str") != "success":
                raise SystemExit(f"{job['name']}: ComfyUI error: {entry['status']}")

            images = {}
            for nid, out in entry["outputs"].items():
                for img in out.get("images", []):
                    title = next((n.get("title", n["type"]) for n in wf["nodes"] if str(n["id"]) == nid), nid)
                    images[title] = comfy.image(img)
            draft = next((v for k, v in images.items() if k.startswith("Draft")), None)
            if draft is not None and is_blocked(draft):
                if fixed_seed is None and attempt < max_retries:
                    print(f"  {job['name']}: seed {seed} gave the grey blocked card, retrying", flush=True)
                    seed = random.randrange(2**50)
                    continue
                print(f"  {job['name']}: seed {seed} gave the grey blocked card", flush=True)
            break

        base = f"{job['name']}_{seed}"
        written = []
        for title, png in images.items():
            suffix = "print" if title.startswith("Print") else "draft"
            path = os.path.join(out_dir, f"{base}_{suffix}.png")
            with open(path, "wb") as f:
                f.write(png)
            written.append(os.path.basename(path))
            if geom is not None:
                guides = draw_guides(png, geom, preset_name)
                if guides is not None:
                    path = os.path.join(out_dir, f"{base}_{suffix}_guides.png")
                    with open(path, "wb") as f:
                        f.write(guides)
                    written.append(os.path.basename(path))
        loras = [n["widgets_values"][:2] for n in wf["nodes"]
                 if n["type"] == "LoraLoaderModelOnly" and n.get("mode", 0) == 0]
        sidecar = {
            "name": job["name"], "subject": job["subject"], "house_style": style,
            "composition": composition, "seed": seed, "preset": preset_name, "cover": geom,
            "generate_size": [gen_w, gen_h], "schedule": schedule or "workflow", "print_size": [print_w, print_h] if do_print else None,
            "loras": loras, "workflow": workflow_name(job["_workflow"]),
            "workflow_sha256": wf_hash, "files": written,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "seconds": round(time.time() - t0),
        }
        with open(os.path.join(out_dir, base + ".json"), "w", encoding="utf-8") as f:
            json.dump(sidecar, f, indent=2, ensure_ascii=False)
        print(f"  {job['name']}: seed {seed}, {sidecar['seconds']}s -> {', '.join(written)}", flush=True)
        results.append(sidecar)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("jobs", help="jobs file (JSON)")
    ap.add_argument("--server", default="http://127.0.0.1:8000", help="ComfyUI URL (default %(default)s)")
    ap.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="UI-format workflow to use")
    ap.add_argument("--only", action="append", help="run only the job with this name (repeatable)")
    ap.add_argument("--check", action="store_true", help="check the prompts for banned terms and stop")
    ap.add_argument("--dry-run", action="store_true",
                    help="show each job's sizes and prompt and build its graph, without generating")
    ap.add_argument("--retries", type=int, default=3, help="new seeds to try after a blocked card (default %(default)s)")
    args = ap.parse_args()

    with open(args.jobs, encoding="utf-8") as f:
        spec = json.load(f)
    jobs = [j for j in spec["jobs"] if not args.only or j["name"] in args.only]
    with open(args.workflow, "rb") as f:
        raw = f.read()
    wf, wf_hash = json.loads(raw), hashlib.sha256(raw).hexdigest()
    style = node_by_title(wf, T_STYLE, prefix=True)["widgets_values"][0]

    terms, bad = load_banned(), False
    for j in jobs:
        if j.get("schedule", "turbo") not in SCHEDULES:
            print(f"{j['name']}: unknown schedule {j['schedule']!r} (use {', '.join(SCHEDULES)})")
            bad = True
        if j.get("preset", "full-page") not in set(PRESETS) | COVER_PRESETS:
            print(f"{j['name']}: unknown preset {j['preset']!r} "
                  f"(use {', '.join(list(PRESETS) + sorted(COVER_PRESETS))})")
            bad = True
            continue
        if j.get("title_position", "top") not in ("top", "bottom"):
            print(f"{j['name']}: title_position must be top or bottom")
            bad = True
            continue
        found = banned_in(j["subject"] + "\n" + job_layout(j)[3] + "\n" + style, terms)
        if found:
            print(f"{j['name']}: banned terms in prompt: {', '.join(found)}")
            bad = True
    if bad:
        sys.exit(1)
    if args.check:
        print(f"{len(jobs)} job(s) OK")
        return

    out_dir = os.path.join(os.path.dirname(os.path.abspath(args.jobs)), spec.get("out", "generated"))
    os.makedirs(out_dir, exist_ok=True)
    comfy = Comfy(args.server)
    info = comfy.get("/object_info")
    if args.dry_run:
        for j in jobs:
            preset_name, gen, prt, composition, geom = job_layout(j)
            wf = json.loads(raw)
            node_by_title(wf, T_COMPOSITION, prefix=True)
            api = to_api(wf, info, include_muted=bool(j.get("print")))
            sheet = "" if geom is None else ", sheet %.3f x %.3f in" % tuple(geom["sheet"])
            print(f"{j['name']}: {preset_name}, generate {gen[0]}x{gen[1]}, "
                  f"print {prt[0]}x{prt[1]}{sheet}, {len(api)} nodes")
            if composition:
                print(f"  composition: {composition}")
        return
    for j in jobs:
        j["_workflow"] = os.path.abspath(args.workflow)
        print(f"{j['name']} ({j.get('preset', 'full-page')}, {j.get('count', 1)} image(s)"
              f"{', draft' if j.get('draft') else ''}{', print' if j.get('print') else ''})", flush=True)
        run_job(comfy, info, json.loads(raw), wf_hash, j, out_dir, args.retries)


if __name__ == "__main__":
    main()
