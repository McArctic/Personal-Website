# portfolio

Personal site. Vue 3 + Vite, static build, deployed on Cloudflare Pages.

```bash
npm install
npm run dev
```

`npm run build` writes to `dist/`.

## Editing content

Nothing about the site's content lives in a component.

- `src/content/profile.js`: name, blurb, about paragraphs, footer links
- `src/content/skills.js`: skill groups, logos come from the `simple-icons` package
- `src/content/experience.js`: work and education entries
- `src/content/extras.js`: links on the Extras page
- `src/content/projects/*.md`: one file per project

Adding a project means adding a markdown file. The slug is the filename, the
route and the listing come along on their own. Frontmatter fields:

```yaml
title: OpenTurret
year: 2026
summary: One sentence for the list page.
stack: [C++, Pico SDK]
repo: https://github.com/...      # optional
logo: /logos/openturret.png       # optional
status: In progress
```

## Contour lines

The contours behind the page headers are the real Killington Peak, Vermont, traced
from the USGS 3DEP National Elevation Dataset (10 m) over a 4.4 x 3.1 km box centred
on the summit. `src/content/killington.js` is generated, not hand-written:

```bash
python tools/killington-contours.py
```

That refetches the elevation grid, traces it with marching squares, and rewrites the
file. It takes about 90 seconds because the elevation API is rate limited to one call
per second. Needs Python with no extra packages.

## Logos

Org logos in `public/logos/` are 256x256 squares, rendered as circles by the CSS.
They have to be square going in. The sources are a mix of wide banners, squares and
transparent PNGs, and a wide one masked to a circle just floats in a white void.

```bash
python tools/logo-tile.py ~/Downloads/acme.png public/logos/acme.png
```

That pads to a square using the logo's own background colour and insets the mark far
enough that the circle does not clip it. Linde was the one exception: it ships as a
2:1 banner, so it was cropped to the wordmark first and then tiled.

## Deploy

Cloudflare Pages, connected to this repo.

- Build command: `npm run build`
- Output directory: `dist`

`public/_redirects` sends unknown paths to `index.html` so deep links like
`/projects/openturret` resolve on a reload.
