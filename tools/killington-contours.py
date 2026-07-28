"""Regenerate src/content/killington.js from real USGS elevation data.

    python tools/killington-contours.py

Fetches a grid of elevations over Killington Peak, Vermont from the USGS 3DEP
National Elevation Dataset (10 m), served in batch by api.opentopodata.org, then
traces contour lines with marching squares and writes them as SVG paths already
placed in the site's 1280x900 viewBox.

The public API allows 100 locations per call at 1 call/sec, so a full run takes
about 90 seconds. Only stdlib is required.
"""

import json
import math
import pathlib
import time
import urllib.parse
import urllib.request

LAT, LON = 43.6042, -72.8203  # Killington Peak summit
LAT_SPAN = 0.028   # ~3.11 km north to south
LON_SPAN = 0.0550  # ~4.43 km east to west, matching the 1280x900 aspect

NX, NY = 96, 68
BATCH = 100
VB_W, VB_H = 1280, 900
INTERVAL = 50   # metres between contour lines
MIN_POINTS = 8  # drop specks
SIMPLIFY = 1.1  # Douglas-Peucker tolerance, in viewBox units

OUT = pathlib.Path(__file__).resolve().parents[1] / "src/content/killington.js"


def fetch_grid():
    lat0, lat1 = LAT - LAT_SPAN / 2, LAT + LAT_SPAN / 2
    lon0, lon1 = LON - LON_SPAN / 2, LON + LON_SPAN / 2
    points = [
        (lat0 + (lat1 - lat0) * j / (NY - 1), lon0 + (lon1 - lon0) * i / (NX - 1))
        for j in range(NY)
        for i in range(NX)
    ]
    print(f"{len(points)} points, {-(-len(points) // BATCH)} requests")

    values = []
    for start in range(0, len(points), BATCH):
        locs = "|".join(f"{la:.6f},{lo:.6f}" for la, lo in points[start : start + BATCH])
        url = "https://api.opentopodata.org/v1/ned10m?" + urllib.parse.urlencode(
            {"locations": locs}
        )
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=60) as resp:
                    data = json.load(resp)
                if data.get("status") != "OK":
                    raise RuntimeError(data.get("error", "bad status"))
                values.extend(r["elevation"] for r in data["results"])
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 3:
                    raise
                print(f"  retry {attempt + 1} after {exc}")
                time.sleep(3)
        time.sleep(1.1)  # respect the published rate limit

    if any(v is None for v in values):
        raise SystemExit("the dataset returned gaps; not writing a partial map")
    return [values[j * NX : (j + 1) * NX] for j in range(NY)]


def smoothed(z, passes=2):
    """Mild blur. The DEM is 10 m data sampled at ~46 m, so raw contours are noisy."""
    for _ in range(passes):
        out = [row[:] for row in z]
        for j in range(1, NY - 1):
            for i in range(1, NX - 1):
                out[j][i] = (
                    z[j][i] * 4
                    + z[j - 1][i] * 2 + z[j + 1][i] * 2 + z[j][i - 1] * 2 + z[j][i + 1] * 2
                    + z[j - 1][i - 1] + z[j - 1][i + 1] + z[j + 1][i - 1] + z[j + 1][i + 1]
                ) / 16
        z = out
    return z


def marching_squares(z, level):
    sx, sy = VB_W / (NX - 1), VB_H / (NY - 1)
    # Row 0 is the southern edge, so y is flipped to put north at the top.
    to_svg = lambda i, j: (i * sx, VB_H - j * sy)
    segs = []

    def lerp(pa, pb, va, vb):
        t = 0.5 if vb == va else (level - va) / (vb - va)
        return (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)

    for j in range(NY - 1):
        for i in range(NX - 1):
            tl, tr = z[j + 1][i], z[j + 1][i + 1]
            bl, br = z[j][i], z[j][i + 1]
            idx = (tl > level) | ((tr > level) << 1) | ((br > level) << 2) | ((bl > level) << 3)
            if idx in (0, 15):
                continue
            top = lerp(to_svg(i, j + 1), to_svg(i + 1, j + 1), tl, tr)
            right = lerp(to_svg(i + 1, j + 1), to_svg(i + 1, j), tr, br)
            bottom = lerp(to_svg(i, j), to_svg(i + 1, j), bl, br)
            left = lerp(to_svg(i, j + 1), to_svg(i, j), tl, bl)
            centre = (tl + tr + bl + br) / 4

            if idx in (1, 14):
                segs.append((left, top))
            elif idx in (2, 13):
                segs.append((top, right))
            elif idx in (3, 12):
                segs.append((left, right))
            elif idx in (4, 11):
                segs.append((right, bottom))
            elif idx in (6, 9):
                segs.append((top, bottom))
            elif idx in (7, 8):
                segs.append((left, bottom))
            elif idx == 5:  # saddle, resolved by the cell average
                segs.extend(
                    [(left, top), (right, bottom)] if centre > level
                    else [(left, bottom), (top, right)]
                )
            elif idx == 10:  # saddle
                segs.extend(
                    [(top, right), (left, bottom)] if centre > level
                    else [(left, top), (right, bottom)]
                )
    return segs


def stitch(segs):
    """Chain segments end to end into polylines."""
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    used = set()
    lines = []
    for idx, (a, b) in enumerate(segs):
        if idx in used:
            continue
        used.add(idx)
        line = [a, b]
        for _ in range(2):
            while True:
                tip, nxt, tail = line[-1], None, None
                for other, (oa, ob) in enumerate(segs):
                    if other in used:
                        continue
                    if key(oa) == key(tip):
                        nxt, tail = other, ob
                        break
                    if key(ob) == key(tip):
                        nxt, tail = other, oa
                        break
                if nxt is None:
                    break
                used.add(nxt)
                line.append(tail)
            line.reverse()
        lines.append(line)
    return lines


def simplify(pts, tol):
    """Douglas-Peucker."""
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay
    span = math.hypot(dx, dy)
    worst, at = 0.0, 0
    for k in range(1, len(pts) - 1):
        px, py = pts[k]
        dist = (
            math.hypot(px - ax, py - ay)
            if span == 0
            else abs(dy * px - dx * py + bx * ay - by * ax) / span
        )
        if dist > worst:
            worst, at = dist, k
    if worst <= tol:
        return [pts[0], pts[-1]]
    return simplify(pts[: at + 1], tol)[:-1] + simplify(pts[at:], tol)


def main():
    z = smoothed(fetch_grid())
    lo = min(min(r) for r in z)
    hi = max(max(r) for r in z)
    levels = range(int(lo // INTERVAL + 1) * INTERVAL, int(hi) + 1, INTERVAL)
    print(f"elevation {lo:.0f} to {hi:.0f} m")

    out = []
    for level in levels:
        for line in stitch(marching_squares(z, level)):
            if len(line) < MIN_POINTS:
                continue
            pts = simplify(line, SIMPLIFY)
            if len(pts) < 4:
                continue
            out.append((level, "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)))
    print(f"{len(out)} polylines")

    body = ",\n".join(f"  {{ level: {lv}, d: '{d}' }}" for lv, d in out)
    OUT.write_text(
        f"// Contour lines of Killington Peak, Vermont, at {INTERVAL} m intervals.\n"
        "//\n"
        "// Derived from real elevation data: USGS 3DEP National Elevation Dataset (10 m),\n"
        "// queried through api.opentopodata.org over a 4.4 x 3.1 km box centred on the\n"
        f"// summit at {LAT}, {LON}. The grid was sampled at {NX}x{NY}, lightly smoothed,\n"
        "// then contoured with marching squares. Coordinates are already in the\n"
        "// 1280x900 viewBox, north up.\n"
        "//\n"
        "// Regenerate with tools/killington-contours.py.\n"
        f"export const summitElevation = {round(hi)}\n\n"
        f"export const contours = [\n{body},\n]\n",
        encoding="utf-8",
    )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
