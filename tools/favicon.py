"""Regenerate the favicon set from one description of the mark.

    python tools/favicon.py

The mark is a double black diamond, the hardest rating on a trail map and the
same shape the project ratings already use, so the tab icon reads as the site
without spelling anything out. Ski signage is black on white, so the tile is
snow and the diamonds are ink.

Everything is drawn as polygons rather than set in a typeface, because a
favicon has no webfont to fall back on and the system sans differs on every
machine.

The gap between the two diamonds is the whole mark: close it and the pair
reads as one bowtie. It is sized so that at 16 px, the smallest frame in the
.ico, it still lands on a pixel of its own rather than dissolving into the
downsample. That is what fixes RADIUS and GAP below — widen the diamonds and
the gap goes with them.

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

RADIUS = 13  # half the diagonal of one diamond
GAP = 4  # between the two facing vertices; 1 px once scaled to 16
CORNER = 10  # rounding on the tile

CONTENT = RADIUS * 4 + GAP

OUT = pathlib.Path(__file__).resolve().parents[1] / "public"


def layout():
    """The two diamonds, in the 64 unit box, centred."""
    first = (BOX - CONTENT) / 2 + RADIUS
    cy = BOX / 2

    return [
        [(cx, cy - RADIUS), (cx + RADIUS, cy), (cx, cy + RADIUS), (cx - RADIUS, cy)]
        for cx in (first, first + RADIUS * 2 + GAP)
    ]


def render(size):
    """One square icon."""
    scale = size * SUPERSAMPLE / BOX
    big = Image.new("RGBA", (size * SUPERSAMPLE,) * 2, (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    up = lambda v: v * scale

    draw.rounded_rectangle(
        [0, 0, size * SUPERSAMPLE - 1, size * SUPERSAMPLE - 1],
        radius=up(CORNER),
        fill=SNOW,
    )

    for diamond in layout():
        draw.polygon([(up(x), up(y)) for x, y in diamond], fill=INK)

    return big.resize((size, size), Image.LANCZOS)


def svg():
    r = lambda v: round(v, 2)
    shapes = [
        f'<polygon points="{" ".join(f"{r(x)},{r(y)}" for x, y in diamond)}"/>'
        for diamond in layout()
    ]
    marks = "\n    ".join(shapes)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}">\n'
        f'  <rect width="{BOX}" height="{BOX}" rx="{CORNER}" fill="#fbfcfd"/>\n'
        f'  <g fill="#111418">\n    {marks}\n  </g>\n'
        f"</svg>\n"
    )


def write_ico(path, frames):
    """Pack the frames into one .ico, each stored as a PNG.

    Pillow's own ICO writer resizes a single source to the sizes you ask for.
    Each frame here is drawn at its own size instead, so the supersampling and
    the rounding of the tile land correctly at every one.
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
    write_ico(OUT / "favicon.ico", [render(16), render(32), render(48)])

    # the tile's corners are transparent, and iOS masks the icon with its own
    # rounding, so dropping the alpha would paint those corners black on any
    # surface that does not mask. Flatten onto the snow instead.
    apple = Image.new("RGB", (180, 180), SNOW[:3])
    tile = render(180)
    apple.paste(tile, mask=tile)
    apple.save(OUT / "apple-touch-icon.png", optimize=True)

    print("wrote favicon.svg, favicon.ico, apple-touch-icon.png")


if __name__ == "__main__":
    main()
