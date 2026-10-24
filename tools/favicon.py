"""Regenerate the favicon set from one description of the mark.

    python tools/favicon.py

The mark is the site's monogram: a lowercase "mm" whose full stop is a black
diamond, the hardest trail rating on a map. Ski signage is a black diamond on
white, so the tile is snow and the marks are ink.

Everything is drawn as rectangles and a polygon rather than set in a typeface,
because a favicon has no webfont to fall back on and the system sans differs
on every machine.

At 16 px the two m's collapse into four grey smudges, so that size in the .ico
carries the diamond on its own. It is the same mark the nav, the rail and the
project ratings already use, so it still reads as the site.

Needs Pillow. Writes public/favicon.ico, public/favicon.svg and
public/apple-touch-icon.png.
"""

import io
import pathlib
import struct

from PIL import Image, ImageDraw

BOX = 64  # the grid everything below is measured in
SUPERSAMPLE = 16

SNOW = (251, 252, 253, 255)
INK = (17, 20, 24, 255)

STEM = 5  # width of one vertical in an m
GAP = 2  # space between those verticals
BAR = 5  # thickness of the bar across the top of an m
XHEIGHT = 19
WORD_GAP = 5  # between the two m's
STOP_GAP = 5  # between the second m and the diamond
RADIUS = 5.5  # half the diagonal of the diamond
CORNER = 10  # rounding on the tile

M_WIDTH = STEM * 3 + GAP * 2
CONTENT = M_WIDTH * 2 + WORD_GAP + STOP_GAP + RADIUS * 2

OUT = pathlib.Path(__file__).resolve().parents[1] / "public"


def layout():
    """Rectangles and one diamond, in the 64 unit box, centred."""
    left = (BOX - CONTENT) / 2
    top = (BOX - XHEIGHT) / 2
    bottom = top + XHEIGHT

    rects = []
    for m in range(2):
        x = left + m * (M_WIDTH + WORD_GAP)
        # the bar closes the top, the three verticals hang off it
        rects.append((x, top, x + M_WIDTH, top + BAR))
        for stem in range(3):
            sx = x + stem * (STEM + GAP)
            rects.append((sx, top, sx + STEM, bottom))

    cx = left + M_WIDTH * 2 + WORD_GAP + STOP_GAP + RADIUS
    cy = bottom - RADIUS
    diamond = [(cx, cy - RADIUS), (cx + RADIUS, cy), (cx, cy + RADIUS), (cx - RADIUS, cy)]
    return rects, diamond


def render(size, *, mark=True, tile=True):
    """One square icon. mark=False leaves just the diamond."""
    scale = size * SUPERSAMPLE / BOX
    big = Image.new("RGBA", (size * SUPERSAMPLE,) * 2, (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    up = lambda v: v * scale

    if tile:
        draw.rounded_rectangle(
            [0, 0, size * SUPERSAMPLE - 1, size * SUPERSAMPLE - 1],
            radius=up(CORNER),
            fill=SNOW,
        )

    rects, diamond = layout()
    if mark:
        for x0, y0, x1, y1 in rects:
            draw.rectangle([up(x0), up(y0), up(x1), up(y1)], fill=INK)
        draw.polygon([(up(x), up(y)) for x, y in diamond], fill=INK)
    else:
        # the diamond alone, grown to carry the whole tile
        cx = cy = size * SUPERSAMPLE / 2
        r = up(RADIUS) * 2.6
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=INK)

    return big.resize((size, size), Image.LANCZOS)


def svg():
    rects, diamond = layout()
    r = lambda v: round(v, 2)
    shapes = [
        f'<rect x="{r(x0)}" y="{r(y0)}" width="{r(x1 - x0)}" height="{r(y1 - y0)}"/>'
        for x0, y0, x1, y1 in rects
    ]
    points = " ".join(f"{r(x)},{r(y)}" for x, y in diamond)
    shapes.append(f'<polygon points="{points}"/>')
    marks = "\n    ".join(shapes)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}">\n'
        f'  <rect width="{BOX}" height="{BOX}" rx="{CORNER}" fill="#fbfcfd"/>\n'
        f'  <g fill="#111418">\n    {marks}\n  </g>\n'
        f"</svg>\n"
    )


def write_ico(path, frames):
    """Pack the frames into one .ico, each stored as a PNG.

    Pillow's own ICO writer resizes a single source to the sizes you ask for,
    which is no good here: the 16 is a different drawing, not a smaller one.
    """
    blobs = []
    for frame in frames:
        buffer = io.BytesIO()
        frame.save(buffer, format="PNG", optimize=True)
        blobs.append(buffer.getvalue())

    offset = 6 + 16 * len(blobs)
    header = struct.pack("<HHH", 0, 1, len(blobs))
    entries = b""
    for frame, blob in zip(frames, blobs):
        side = 0 if frame.width >= 256 else frame.width
        entries += struct.pack("<BBBBHHII", side, side, 0, 0, 1, 32, len(blob), offset)
        offset += len(blob)

    path.write_bytes(header + entries + b"".join(blobs))


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    (OUT / "favicon.svg").write_text(svg(), encoding="utf-8")

    # the .ico holds all three, and the browser picks by the size it needs
    tiny = render(16, mark=False)
    write_ico(OUT / "favicon.ico", [tiny, render(32), render(48)])

    render(180).convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)

    print("wrote favicon.svg, favicon.ico, apple-touch-icon.png")


if __name__ == "__main__":
    main()
