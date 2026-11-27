#!/usr/bin/env python3
"""Render entry.png — a one-image broadsheet of 27 November 2026's news.

Reads headlines.json (researched from the day's wire reports) and draws a
dense, old-style newspaper front page at 1024x1024 with PIL:

  * masthead with the edition name, date line and furniture rules
  * the lead story (kicker, headline, deck, source) in large serif type
  * the second story, then a one-row "Day in Numbers" strip
  * six news sections in a three-column grid
  * wire datelines and one-line briefs in three bottom columns
  * a footer with the compilation credit and a fine-print story index

The layout is drawn with a uniform scale factor: the page is first laid
out at natural broadsheet sizes, measured, and — if it would overrun the
square — redrawn at the largest scale that fits, so the type stays
evenly proportioned, just denser, like a real front page's small print.

The paper stock is a fine grain (PIL's effect_noise blended into the
stock colour) and the numbers strip carries a halftone dot screen, so
the image keeps the tactile feel — and byte weight — of newsprint.

Usage:  python3 render.py   (writes entry.png next to this file)
"""

import json
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
FOOTER_TOP = H - 64

PAPER = (246, 242, 230)
INK = (18, 20, 24)
ACCENT = (158, 27, 27)
GREY = (92, 90, 84)
PANEL = (233, 226, 205)
PANEL_LINE = (178, 164, 128)
DOT = (196, 182, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, max(6, int(round(size))))


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, fnt, width, leading, fill=INK, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def letterspaced(draw, xy, text, fnt, spacing, fill=INK, centre=False):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (W - total) / 2 if centre else xy[0]
    for ch, w in zip(text, widths):
        draw.text((x, xy[1]), ch, font=fnt, fill=fill)
        x += w + spacing
    return total


def halftone(draw, box, step=9, rmax=3.1):
    x0, y0, x1, y1 = box
    for yy in range(int(y0) + step // 2, int(y1), step):
        for xx in range(int(x0) + step // 2, int(x1), step):
            t = ((xx - x0) / max(1, x1 - x0) + (yy - y0) / max(1, y1 - y0)) / 2
            r = 0.6 + t * rmax
            draw.ellipse([xx - r, yy - r, xx + r, yy + r], fill=DOT)


def paper():
    base = Image.new("RGB", (W, H), PAPER)
    grain = Image.effect_noise((W, H), 14).convert("RGB")
    return ImageChops.add(base, grain, scale=1.0, offset=-118)


def draw_page(draw, data, S):
    """Draw the whole page at scale S; return the y where content ends."""
    M = 36 * S  # side margin

    def F(path, size):
        return font(path, size * S)

    # ---- masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 5 * S], fill=INK)
    draw.rectangle([0, 9 * S, W, 11 * S], fill=INK)
    f_small = F(SANS, 13)
    draw.text((M, 20 * S), "Vol. I — No. 27", font=f_small, fill=GREY)
    right = "Price: one image"
    draw.text((W - M - draw.textlength(right, font=f_small), 20 * S), right,
              font=f_small, fill=GREY)
    letterspaced(draw, (0, 40 * S), "THE WORLD TODAY", F(SERIF_B, 74), 2 * S,
                 fill=INK, centre=True)
    letterspaced(draw, (0, 126 * S), "O N E   I M A G E   E D I T I O N",
                 F(SANS_B, 16), 3 * S, fill=ACCENT, centre=True)
    draw.rectangle([0, 156 * S, W, 159 * S], fill=INK)
    f_date = F(SERIF, 15)
    date = data["date_line"]
    draw.text(((W - draw.textlength(date, font=f_date)) / 2, 166 * S), date,
              font=f_date, fill=INK)
    draw.text((M, 166 * S), "Late City Final", font=f_small, fill=GREY)
    tail = "All the day in one frame"
    draw.text((W - M - draw.textlength(tail, font=f_small), 166 * S), tail,
              font=f_small, fill=GREY)
    draw.rectangle([0, 192 * S, W, 198 * S], fill=INK)
    y = 212 * S

    # ---- lead story -----------------------------------------------------
    letterspaced(draw, (M, y), data["lead"]["kicker"], F(SANS_B, 14), 2 * S,
                 fill=ACCENT)
    y += 22 * S
    y = block(draw, (M, y), data["lead"]["headline"], F(SERIF_B, 40),
              W - 2 * M, 46 * S)
    y += 3 * S
    y = block(draw, (M, y), data["lead"]["deck"], F(SERIF, 15), W - 2 * M,
              20 * S, fill=(40, 42, 46))
    y += 5 * S
    draw.text((M, y), "— " + data["lead"]["source"], font=F(SANS_B, 11.5),
              fill=GREY)
    y += 24 * S
    draw.rectangle([M, y, W - M, y + 2 * S], fill=INK)
    y += 12 * S

    # ---- second story ---------------------------------------------------
    letterspaced(draw, (M, y), data["second"]["kicker"], F(SANS_B, 12.5),
                 2 * S, fill=ACCENT)
    y += 18 * S
    y = block(draw, (M, y), data["second"]["headline"], F(SERIF_B, 23),
              W - 2 * M, 27 * S)
    y += 2 * S
    y = block(draw, (M, y), data["second"]["deck"], F(SERIF, 13), W - 2 * M,
              17.5 * S, fill=(40, 42, 46))
    y += 4 * S
    draw.text((M, y), "— " + data["second"]["source"], font=F(SANS_B, 11),
              fill=GREY)
    y += 22 * S

    # ---- day in numbers: one shaded strip, eight cells ------------------
    cells = data["numbers"]
    cw = (W - 2 * M) / len(cells)
    strip_h = 74 * S
    draw.rectangle([M, y, W - M, y + strip_h], fill=PANEL)
    halftone(draw, (M + 3, y + 3, W - M - 3, y + strip_h - 3),
             step=max(6, int(9 * S)), rmax=3.1 * S)
    draw.rectangle([M, y, W - M, y + strip_h], outline=PANEL_LINE, width=1)
    for i, item in enumerate(cells):
        num, _, rest = item.partition(" — ")
        x = M + i * cw + 8 * S
        draw.text((x, y + 7 * S), num, font=F(SERIF_B, 16), fill=ACCENT)
        block(draw, (x, y + 30 * S), rest, F(SANS, 9.5), cw - 14 * S, 12 * S,
              fill=INK, max_lines=3)
    y += strip_h + 10 * S
    draw.rectangle([M, y, W - M, y + 2 * S], fill=INK)
    y += 11 * S

    # ---- six sections, three columns by two rows ------------------------
    gap = 22 * S
    col_w = (W - 2 * M - 2 * gap) / 3
    sec_font = F(SERIF, 11)
    for row in range(2):
        heights = []
        for col in range(3):
            sec = data["sections"][row * 3 + col]
            x = M + col * (col_w + gap)
            cy = y
            draw.rectangle([x, cy, x + col_w, cy + 19 * S], fill=INK)
            draw.text((x + 7 * S, cy + 3.5 * S), sec["name"],
                      font=F(SANS_B, 11), fill=PAPER)
            cy += 25 * S
            for item in sec["items"]:
                cy = block(draw, (x, cy), "▪ " + item, sec_font, col_w,
                           13.5 * S)
                cy += 4 * S
            heights.append(cy)
        y = max(heights) + 6 * S
        if row == 0:
            draw.line([M, y - 3 * S, W - M, y - 3 * S], fill=PANEL_LINE,
                      width=1)
    draw.rectangle([M, y, W - M, y + 2 * S], fill=INK)
    y += 11 * S

    # ---- datelines + briefs, three flowing columns ----------------------
    headers = ["FROM THE WIRES", "IN BRIEF", "IN BRIEF · CONTINUED"]
    items = ([("d", c, t) for c, t in data["datelines"]]
             + [("b", c, t) for c, t in data["briefs"]])
    # balance 13 items over 3 columns: 5 / 4 / 4
    columns = [items[:5], items[5:9], items[9:]]
    heights = []
    for col, col_items in enumerate(columns):
        x = M + col * (col_w + gap)
        cy = y
        letterspaced(draw, (x, cy), headers[col], F(SANS_B, 11.5), 1.5 * S,
                     fill=INK)
        cy += 17 * S
        for _, city, text in col_items:
            cy = block(draw, (x, cy), f"{city} — {text}", F(SERIF, 10.5),
                       col_w, 13 * S)
            cy += 3.5 * S
        heights.append(cy)
    y = max(heights)
    return y


def main():
    with open(os.path.join(HERE, "headlines.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    # Measure at natural size, then refine: some elements (hairlines,
    # minimum font sizes) do not shrink linearly, so one correction
    # pass lands the layout much closer to the footer's top edge.
    target = FOOTER_TOP - 10
    scratch = ImageDraw.Draw(Image.new("RGB", (W, H)))
    end = draw_page(scratch, data, 1.0)
    if end <= target:
        S = 1.0
    else:
        # Wrap counts jump in steps as type grows, so bisect for the
        # largest scale whose layout still ends above the target.
        lo, hi = 0.40, 1.0
        for _ in range(24):
            mid = (lo + hi) / 2
            if draw_page(scratch, data, mid) <= target:
                lo = mid
            else:
                hi = mid
        S = lo
    print(f"natural layout ends at y={end:.0f}; drawing at scale {S:.3f}")

    img = paper()
    draw = ImageDraw.Draw(img)
    end = draw_page(draw, data, S)

    draw.rectangle([0, FOOTER_TOP, W, FOOTER_TOP + 3], fill=INK)
    draw.text((36, FOOTER_TOP + 8), data["compiled"], font=font(SANS, 11),
              fill=GREY)
    index = " · ".join(
        [data["lead"]["headline"], data["second"]["headline"]]
        + [it for s in data["sections"] for it in s["items"]]
        + [f"{c}: {t}" for c, t in data["datelines"]]
        + [f"{c}: {t}" for c, t in data["briefs"]])
    block(draw, (36, FOOTER_TOP + 26), index, font(SANS, 8), W - 72, 10,
          fill=GREY, max_lines=2)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out}: {os.path.getsize(out)} bytes; content ends at y={end:.0f}")


if __name__ == "__main__":
    main()
