"""Regenerate src/content/killington.js from real USGS elevation data.

    python tools/killington-contours.py

Fetches elevations over Killington Peak, Vermont from the USGS 3DEP National
Elevation Dataset (10 m) via api.opentopodata.org, traces contour lines with
marching squares, and writes them as SVG paths in the site's 1280x900 viewBox.

The API allows 100 locations per call at 1 call/sec, so a run takes about 90
seconds. Stdlib only.
"""

import json
import math
import pathlib
import time
import urllib.parse
import urllib.request

SUMMIT_LAT, SUMMIT_LON = 43.6042, -72.8203
LAT_SPAN = 0.028   # ~3.11 km north to south
LON_SPAN = 0.0550  # ~4.43 km east to west, matching the viewBox aspect

COLUMNS, ROWS = 96, 68
BATCH_SIZE = 100
VIEWBOX_W, VIEWBOX_H = 1280, 900
INTERVAL = 50          # metres between contour lines
MIN_POINTS = 8         # anything shorter is a speck, so drop it
SIMPLIFY_TOLERANCE = 1.1

OUTPUT = pathlib.Path(__file__).resolve().parents[1] / "src/content/killington.js"


def fetch_grid():
    lat0, lat1 = SUMMIT_LAT - LAT_SPAN / 2, SUMMIT_LAT + LAT_SPAN / 2
    lon0, lon1 = SUMMIT_LON - LON_SPAN / 2, SUMMIT_LON + LON_SPAN / 2
    coordinates = [
        (lat0 + (lat1 - lat0) * row / (ROWS - 1), lon0 + (lon1 - lon0) * col / (COLUMNS - 1))
        for row in range(ROWS)
        for col in range(COLUMNS)
    ]
    print(f"{len(coordinates)} points, {-(-len(coordinates) // BATCH_SIZE)} requests")

    elevations = []
    for start in range(0, len(coordinates), BATCH_SIZE):
        batch = coordinates[start : start + BATCH_SIZE]
        locations = "|".join(f"{lat:.6f},{lon:.6f}" for lat, lon in batch)
        url = "https://api.opentopodata.org/v1/ned10m?" + urllib.parse.urlencode(
            {"locations": locations}
        )
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    payload = json.load(response)
                if payload.get("status") != "OK":
                    raise RuntimeError(payload.get("error", "bad status"))
                elevations.extend(result["elevation"] for result in payload["results"])
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 3:
                    raise
                print(f"  retry {attempt + 1} after {exc}")
                time.sleep(3)
        time.sleep(1.1)  # their published rate limit

    if any(value is None for value in elevations):
        raise SystemExit("the dataset returned gaps; not writing a partial map")
    return [elevations[row * COLUMNS : (row + 1) * COLUMNS] for row in range(ROWS)]


def smoothed(grid, passes=2):
    """Mild blur. 10 m data sampled at ~46 m gives noisy contours."""
    for _ in range(passes):
        blurred = [row[:] for row in grid]
        for row in range(1, ROWS - 1):
            for col in range(1, COLUMNS - 1):
                blurred[row][col] = (
                    grid[row][col] * 4
                    + grid[row - 1][col] * 2 + grid[row + 1][col] * 2
                    + grid[row][col - 1] * 2 + grid[row][col + 1] * 2
                    + grid[row - 1][col - 1] + grid[row - 1][col + 1]
                    + grid[row + 1][col - 1] + grid[row + 1][col + 1]
                ) / 16
        grid = blurred
    return grid


def marching_squares(grid, level):
    scale_x, scale_y = VIEWBOX_W / (COLUMNS - 1), VIEWBOX_H / (ROWS - 1)
    # row 0 is the southern edge, so y gets flipped to put north at the top
    to_svg = lambda col, row: (col * scale_x, VIEWBOX_H - row * scale_y)
    segments = []

    def crossing(point_a, point_b, value_a, value_b):
        t = 0.5 if value_b == value_a else (level - value_a) / (value_b - value_a)
        return (
            point_a[0] + (point_b[0] - point_a[0]) * t,
            point_a[1] + (point_b[1] - point_a[1]) * t,
        )

    for row in range(ROWS - 1):
        for col in range(COLUMNS - 1):
            top_left, top_right = grid[row + 1][col], grid[row + 1][col + 1]
            bottom_left, bottom_right = grid[row][col], grid[row][col + 1]
            case = (
                (top_left > level)
                | ((top_right > level) << 1)
                | ((bottom_right > level) << 2)
                | ((bottom_left > level) << 3)
            )
            if case in (0, 15):
                continue

            top = crossing(to_svg(col, row + 1), to_svg(col + 1, row + 1), top_left, top_right)
            right = crossing(to_svg(col + 1, row + 1), to_svg(col + 1, row), top_right, bottom_right)
            bottom = crossing(to_svg(col, row), to_svg(col + 1, row), bottom_left, bottom_right)
            left = crossing(to_svg(col, row + 1), to_svg(col, row), top_left, bottom_left)
            average = (top_left + top_right + bottom_left + bottom_right) / 4

            if case in (1, 14):
                segments.append((left, top))
            elif case in (2, 13):
                segments.append((top, right))
            elif case in (3, 12):
                segments.append((left, right))
            elif case in (4, 11):
                segments.append((right, bottom))
            elif case in (6, 9):
                segments.append((top, bottom))
            elif case in (7, 8):
                segments.append((left, bottom))
            elif case == 5:  # saddle, settled by the cell average
                segments.extend(
                    [(left, top), (right, bottom)] if average > level
                    else [(left, bottom), (top, right)]
                )
            elif case == 10:  # saddle
                segments.extend(
                    [(top, right), (left, bottom)] if average > level
                    else [(left, top), (right, bottom)]
                )
    return segments


def stitch(segments):
    """Chain segments end to end into polylines."""
    key = lambda point: (round(point[0], 3), round(point[1], 3))
    used = set()
    polylines = []
    for index, (start, end) in enumerate(segments):
        if index in used:
            continue
        used.add(index)
        line = [start, end]
        for _ in range(2):
            while True:
                tip, found, tail = line[-1], None, None
                for other, (other_start, other_end) in enumerate(segments):
                    if other in used:
                        continue
                    if key(other_start) == key(tip):
                        found, tail = other, other_end
                        break
                    if key(other_end) == key(tip):
                        found, tail = other, other_start
                        break
                if found is None:
                    break
                used.add(found)
                line.append(tail)
            line.reverse()
        polylines.append(line)
    return polylines


def simplify(points, tolerance):
    """Douglas-Peucker."""
    if len(points) < 3:
        return points
    (start_x, start_y), (end_x, end_y) = points[0], points[-1]
    dx, dy = end_x - start_x, end_y - start_y
    span = math.hypot(dx, dy)
    furthest, split_at = 0.0, 0
    for index in range(1, len(points) - 1):
        x, y = points[index]
        distance = (
            math.hypot(x - start_x, y - start_y)
            if span == 0
            else abs(dy * x - dx * y + end_x * start_y - end_y * start_x) / span
        )
        if distance > furthest:
            furthest, split_at = distance, index
    if furthest <= tolerance:
        return [points[0], points[-1]]
    return simplify(points[: split_at + 1], tolerance)[:-1] + simplify(points[split_at:], tolerance)


def main():
    grid = smoothed(fetch_grid())
    lowest = min(min(row) for row in grid)
    highest = max(max(row) for row in grid)
    levels = range(int(lowest // INTERVAL + 1) * INTERVAL, int(highest) + 1, INTERVAL)
    print(f"elevation {lowest:.0f} to {highest:.0f} m")

    contours = []
    for level in levels:
        for line in stitch(marching_squares(grid, level)):
            if len(line) < MIN_POINTS:
                continue
            points = simplify(line, SIMPLIFY_TOLERANCE)
            if len(points) < 4:
                continue
            contours.append((level, "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)))
    print(f"{len(contours)} polylines")

    body = ",\n".join(f"  {{ level: {level}, d: '{d}' }}" for level, d in contours)
    OUTPUT.write_text(
        "// generated by tools/killington-contours.py, don't edit this by hand\n"
        f"// Killington Peak, Vermont at {INTERVAL} m intervals, from the USGS 3DEP 10 m dataset\n"
        "// coordinates are in the 1280x900 viewBox, north up\n"
        f"export const summitElevation = {round(highest)}\n\n"
        f"export const contours = [\n{body},\n]\n",
        encoding="utf-8",
    )
    print("wrote", OUTPUT)


if __name__ == "__main__":
    main()
