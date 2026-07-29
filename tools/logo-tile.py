"""Turn a logo of any shape into a square tile the site renders as a circle.

    python tools/logo-tile.py ~/Downloads/acme.png public/logos/acme.png

Requires Pillow (`pip install pillow`).
"""

import sys
from pathlib import Path

from PIL import Image

TILE_SIZE = 256

# the circle clips the corners, so wide marks need more room to breathe
INSET_WIDE = 0.66
INSET_SQUARE = 0.80


def background_colour(image):
    """Most common of the four corner pixels."""
    width, height = image.size
    corners = [
        image.getpixel(p)
        for p in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
    ]
    opaque = [c[:3] for c in corners if len(c) < 4 or c[3] > 128]
    if not opaque:
        return (255, 255, 255)
    return max(set(opaque), key=opaque.count)


def tile(source_path, dest_path):
    image = Image.open(source_path).convert("RGBA")
    aspect = max(image.width, image.height) / min(image.width, image.height)
    inset = INSET_WIDE if aspect > 1.3 else INSET_SQUARE

    scale = min(TILE_SIZE * inset / image.width, TILE_SIZE * inset / image.height)
    mark = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)

    colour = background_colour(image)
    canvas = Image.new("RGB", (TILE_SIZE, TILE_SIZE), colour)
    canvas.paste(mark, ((TILE_SIZE - mark.width) // 2, (TILE_SIZE - mark.height) // 2), mark)
    canvas.save(dest_path)
    print(f"{dest_path}  {TILE_SIZE}x{TILE_SIZE}  bg {colour}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    tile(Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser())
