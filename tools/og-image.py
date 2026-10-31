"""Regenerate the link preview card.

    python tools/og-image.py

This is the image that shows up when the site gets pasted into LinkedIn, a
Discord server or an email. It is the hero, flattened: the Killington contours
behind the name, framed the same way the summit band frames them.

The site sets its type in Archivo, which is not installed here, so the card
falls back to the nearest system sans. Close enough at this size, but if the
card ever needs to match exactly, drop Archivo into tools/ and point FACES at
it.

Needs Pillow. Writes public/og.jpg.
"""

import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
SUPERSAMPLE = 2
VIEWBOX = (1280, 900)

SUMMIT = (12, 17, 22)
SNOW = (239, 244, 248)
ALPINE = (124, 180, 217)
# The contours sit at about a fifth opacity on the site, flattened here.
# They are drawn in the summit ink rather than the accent, so that the blue
# on this card is only ever the kicker and the full stop.
CONTOUR = (57, 62, 67)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FACES = pathlib.Path(r"C:\Windows\Fonts")


def face(*names, size):
    for name in names:
        path = FACES / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size)


def contours():
    """The polylines out of the generated contour file, as point lists."""
    source = (ROOT / "src/content/killington.js").read_text(encoding="utf-8")
    for d in re.findall(r"d: '([^']+)'", source):
        yield [
            tuple(float(n) for n in pair.split())
            for pair in d[2:].split(" L ")
        ]


def main():
    w, h = WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE
    card = Image.new("RGB", (w, h), SUMMIT)
    draw = ImageDraw.Draw(card)

    # cover the card the way preserveAspectRatio="slice" does, held to the
    # bottom edge like the hero, so the summit sits high in the frame
    scale = max(w / VIEWBOX[0], h / VIEWBOX[1])
    offset_x = (w - VIEWBOX[0] * scale) / 2
    offset_y = h - VIEWBOX[1] * scale

    for points in contours():
        draw.line(
            [(x * scale + offset_x, y * scale + offset_y) for x, y in points],
            fill=CONTOUR,
            width=round(2 * SUPERSAMPLE),
            joint="curve",
        )

    pad = 86 * SUPERSAMPLE
    name = face("segoeuib.ttf", "arialbd.ttf", size=118 * SUPERSAMPLE)
    note = face("segoeui.ttf", "arial.ttf", size=31 * SUPERSAMPLE)

    # the hero dropped its kicker, so the card opens on the name as well. The
    # offset that used to clear the kicker stays: it leaves a little more air
    # above the name than below the note, which is what keeps the block from
    # sitting dead centre.
    top = pad + 62 * SUPERSAMPLE
    draw.text((pad, top), "Michael", font=name, fill=SNOW)
    draw.text((pad, top + 128 * SUPERSAMPLE), "Melichar", font=name, fill=SNOW)

    # the full stop picks up the accent, same as it does in the hero
    stop_x = pad + draw.textlength("Melichar", font=name)
    draw.text((stop_x, top + 128 * SUPERSAMPLE), ".", font=name, fill=ALPINE)

    draw.text(
        (pad, h - pad - 38 * SUPERSAMPLE),
        "Cubesat flight software, rocket avionics, and a satellite ground station.",
        font=note,
        fill=(141, 153, 164),
    )

    card = card.resize((WIDTH, HEIGHT), Image.LANCZOS)
    card.save(ROOT / "public/og.jpg", quality=88, optimize=True, progressive=True)
    print("wrote public/og.jpg")


if __name__ == "__main__":
    main()
