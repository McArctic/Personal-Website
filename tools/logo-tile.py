"""Turn a logo of any shape into a square tile the site can render as a circle.

    python tools/logo-tile.py ~/Downloads/acme.png public/logos/acme.png

Logos arrive as wide banners, squares, and transparent PNGs on every possible
background. Masking those to circles in CSS alone leaves the wide ones floating as
small rectangles in a white void, so they get normalized to squares here instead:
the background fills the whole tile, and the mark sits inside the inscribed circle.

Requires Pillow (`pip install pillow`).
"""

import sys
from pathlib import Path

from PIL import Image

SIZE = 256

# A circle inscribed in a square clips the corners, so the mark has to sit well
# inside it. Wide marks need more room than square ones.
INSET_WIDE = 0.66
INSET_SQUARE = 0.80


def background(img):
    """Best guess at the tile colour: the most common of the four corners."""
    w, h = img.size
    corners = [img.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    opaque = [c[:3] for c in corners if len(c) < 4 or c[3] > 128]
    if not opaque:
        return (255, 255, 255)
    return max(set(opaque), key=opaque.count)


def tile(src, dest):
    img = Image.open(src).convert("RGBA")
    ratio = max(img.width, img.height) / min(img.width, img.height)
    inset = INSET_WIDE if ratio > 1.3 else INSET_SQUARE

    factor = min(SIZE * inset / img.width, SIZE * inset / img.height)
    mark = img.resize((round(img.width * factor), round(img.height * factor)), Image.LANCZOS)

    canvas = Image.new("RGB", (SIZE, SIZE), background(img))
    canvas.paste(mark, ((SIZE - mark.width) // 2, (SIZE - mark.height) // 2), mark)
    canvas.save(dest)
    print(f"{dest}  {SIZE}x{SIZE}  bg {background(img)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    tile(Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser())
