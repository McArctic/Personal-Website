---
name: personal-website
description: Orientation for this repo — a Vue 3 + Vite single-page portfolio built around a ski-mountain metaphor, deployed to Cloudflare. Use when working on the home page bands, the scroll/descent system, the contour and sky-plot SVG animations, the markdown-driven project pages, the intro sequence, design tokens, or the Python regeneration tools. Explains the descent model, the content pipeline, the plotted-data drawing language and its Chromium traps, and the repo's commit and branch conventions.
user-invocable: true
---

# Personal Website — Orientation

Michael's portfolio at **michaelmelichar.com**. Vue 3 (`<script setup>`), Vue Router 4, Vite 6, no state library and no CSS framework. Everything is one long scroll down a mountain: the page starts at the **summit** (dark, above the treeline) and descends to the **valley** (light). That metaphor is not decoration — it is the actual architecture, and most of the code reads better once you hold it.

- Plain JavaScript, not TypeScript. No test suite.
- `@` is aliased to `./src` (see `vite.config.js`).
- Deployed as static assets on Cloudflare via `wrangler.jsonc`, SPA fallback to `index.html`.
- Fonts (Archivo + JetBrains Mono) come from Google Fonts and are **render-blocking** — this matters more than it sounds, see the intro section.

---

## Layout — `src/`

```
main.js            createApp + router + the v-rise directive + base.css
App.vue            IntroSequence / SiteHeader / ElevationRail / RouterView / SiteFooter
descent.js         the one scroll listener for the whole site
rise.js            v-rise, fade-a-block-up-on-first-view directive
intro.js           whether the opening plot plays (session-scoped)
router/index.js    routes, old paths redirected to home-page hashes, title handling
styles/base.css    design tokens + the .dark band remap
views/             HomeView (the whole descent), ProjectView, NotFoundView
components/        see below
content/           all copy and data lives here, never in the views
```

### Components

| File | Role |
|---|---|
| `TopoLines.vue` | The Killington contour map. Resting background, or an animated plot. **Read its section below before touching it.** |
| `PassPlot.vue` | Polar sky plot of a satellite pass. Same thin plotted-data language, pointed up. |
| `IntroSequence.vue` | The opening: contours plot in while an elevation readout climbs to 1273 m. |
| `ElevationRail.vue` | Fixed vertical rail showing descent progress and the station marks. |
| `SiteHeader.vue` | Fixed header; recolours itself from the band behind it. |
| `ProjectCard.vue`, `TrailMark.vue`, `TrailSign.vue` | Project tiles and the green/blue/diamond difficulty rating. |
| `ExperienceTimeline.vue`, `SkillGroup.vue` | Experience and skills blocks. |
| `ProseText.vue` | Renders the inline-link markdown used in `profile.js` copy. |
| `ImageLightbox.vue` | Opened by `#stack` galleries in project markdown. |
| `SiteFooter.vue` | Base of the mountain. |

---

## The descent — `src/descent.js`

**One** scroll listener serves the whole site. The header and the rail both need to know how far down you are and what is behind them; two listeners would fight. Never add a second scroll listener — opt into this one instead.

Any element can take part through two data attributes:

- `data-zone="dark|light"` — what sits behind the fixed furniture at this point
- `data-station="Label"` — a junction worth marking on the elevation rail

Exported refs: `progress`, `stations`, `activeStation`, `headerZone`, `railZone`, `scrolled`.

Two things that look redundant but are not:

- `remeasureDescent()` measures **twice** on purpose — once synchronously, because the header must not spend a frame light over the dark hero, then again on the next frame to catch offsets that only settle once webfonts and images land. `App.vue` calls it on every route change.
- `goToStation(id)` scrolls by hand and only then writes the hash. Vue Router owns history and scroll restoration here, which leaves plain fragment links doing nothing.

`watchDescent` / `stopDescent` are refcounted, so mounting twice is safe.

---

## Home page bands — `src/views/HomeView.vue`

The whole descent is one file, seven `<section class="band">` elements, in order:

| id | zone | station |
|---|---|---|
| `summit` | dark | Summit |
| `about` | dark | About |
| `work` | light | Work |
| `experience` | light (shaded) | Experience |
| `now` | light | Now |
| `ski` | light (shaded) | Off the clock |
| `contact` | dark | Contact |

Adding a band means adding the section with its `data-zone` / `data-station` and nothing else — the rail and header pick it up automatically.

---

## Content — `src/content/`

Copy and data never live in the views.

- `profile.js` — name, role, lead, about paragraphs, bench photos. About copy supports inline markdown links, rendered by `ProseText`.
- `experience.js` — `education` and `experience` arrays.
- `skills.js` — grouped lists. Deliberately short.
- `killington.js` — **generated**, do not hand-edit. Contour polylines in the 1280×900 viewBox plus `summitElevation`.
- `projects.js` — the markdown pipeline.
- `projects/*.md` — one file per project.

### Project markdown

Drop a `.md` in `src/content/projects/` and it becomes a project. There is **no index and no route to update**; `import.meta.glob` picks it up and the slug is the filename. Sorting is featured first, then newest year.

Required frontmatter: `title`, `year`, `summary`, `stack`, `difficulty` (`green` / `blue` / `diamond`), `cover`. Optional: `repo`, `download`, `status`, `featured`.

The custom `marked` renderer gives images a small layout language. An image alone in a paragraph becomes a figure; two or more become a gallery with one shared caption:

```
![Caption](/img/slug/shot.jpg)         figure at column width
![Caption](/img/slug/shot.jpg#small)   narrower, for detail shots
![Caption](/img/slug/shot.jpg#tall)    upright, for phone shots
![Caption](/img/slug/shot.jpg#wide)    breaks out past the text column
![front](/img/a.jpg#stack) ![b](/img/b.jpg)   fanned deck, opens the lightbox
```

Tokens are read across a whole group, so one image can carry the mode and another the size. An image mid-sentence stays inline. The full contract is documented in the comment block at the top of `projects.js` — keep it current if you change the renderer.

---

## The plotted-data language — `TopoLines.vue`, `PassPlot.vue`

Thin accent-coloured strokes over a dark field, as if something were being plotted on paper. `TopoLines` renders the contours from `killington.js`, smoothed from polylines to Catmull-Rom Béziers so the simplified data still reads as terrain, and optionally animates them on.

Props: `align` (the `preserveAspectRatio` anchor), `draw`, `drawTime`, `interactive`. Interactive instances run a pointer-following gaussian deform; instances that do not need it opt out, because the deform costs a frame loop.

The plot staggers by elevation — lowest contour first, summit ring last — so terrain fills from the outside in. Each line takes 60% of the budget and the starts spread across the other 40%, so the last stroke lands exactly on `drawTime`.

### Two traps, both paid for in blood

**1. `vector-effect: non-scaling-stroke` cannot be combined with a dash.** Chromium measures a dashed path in user units but strokes it in screen units, so the dash falls `1/scale` short and every contour simply stops before its end — a fifth of each line missing at scale 1.25, a third at 1.5. Firefox gets it right, so it only shows up in Chrome, and only above scale 1, which makes it maddening to reproduce. Plotted paths therefore set `vector-effect: none` and recover the hairline with `stroke-width: calc(1px / var(--topo-scale))`, where `--topo-scale` is measured from `getScreenCTM()`. Resting (undashed) instances keep the vector effect and need no JS.

**2. CSS animations do not start when you think.** They wait on first style resolution, which waits on the render-blocking webfont stylesheet. Anything timing the plot from mount runs ahead of it, and `getAnimations()` on an early frame answers with nothing yet — indistinguishable from nothing left to wait for. `TopoLines` counts `animationstart` / `animationend` events instead and emits `plotstart` / `plotted`.

---

## The intro — `src/intro.js`, `IntroSequence.vue`

Plays **once per tab**, gated on `sessionStorage['intro-played']`, and skipped entirely under `prefers-reduced-motion`. Coming back from a project page should not make you sit through it again.

`IntroSequence` hangs its elevation readout and its exit on TopoLines' events, not on a stopwatch. Two backstops, because one timer cannot do both jobs: `NEVER_STARTED` (5 s from mount) for a plot that never begins, and `PLOT_TIME + SLOW_MARGIN` from `plotstart` for one that began and is slow.

`finish()` is the single way out — timeline ran its course, visitor skipped (pointerdown / keydown / **wheel**, so a stray scroll counts), or a backstop fired. It awaits `TopoLines.settle()` first, which races any unfinished strokes home at a shared raised `playbackRate` so the map always fades out whole. `settle()` is capped and hard-lands stragglers with `animation.finish()`, because a tab nobody is painting never advances its animations and would otherwise hang the intro forever.

### Testing the intro

Replay it without reloading or clearing storage — the dev server serves live ES modules, so you get the same module instance:

```js
const m = await import('/src/intro.js')
m.introDone.value = false
m.introPlaying.value = true
```

Beware: **a hidden browser pane freezes its animation timeline**, so `document.timeline.currentTime` stays 0, no animation events fire, and the backstop trips. Timing measured from a hidden pane is worthless. Check `document.timeline.currentTime > 0` before trusting any run.

---

## Design tokens — `src/styles/base.css`

Two palettes, one semantic layer. Components read **only** the semantic names (`--bg`, `--fg`, `--fg-body`, `--fg-soft`, `--fg-faint`, `--rule`, `--accent`, `--topo-opacity`); the `.dark` class remaps them to the summit palette. Never reach past the semantic layer to `--snow` or `--summit-ink` in a component.

Other tokens: `--mono`, `--gutter` (fluid page gutter), `--measure` (text column). Callers set `--topo-opacity` rather than `opacity` on TopoLines.

Everything honours `prefers-reduced-motion`.

---

## Tools — `tools/*.py`

Regeneration scripts, run by hand, not part of the build. Each has a docstring with its invocation.

| Script | Does |
|---|---|
| `killington-contours.py` | Rebuilds `src/content/killington.js` from USGS 3DEP elevation data via api.opentopodata.org. |
| `og-image.py` | Rebuilds `public/og.jpg`, the link preview card — the hero, flattened. |
| `favicon.py` | Rebuilds the favicon set from the "mm." monogram whose full stop is a black diamond. |
| `logo-tile.py` | Squares an arbitrary logo into a tile the site renders as a circle. Takes a path argument. |

---

## Build, run, deploy

```bash
npm run dev       # vite, port 5173
npm run build     # -> dist/
npm run preview   # serve the built output
```

The live domain is written down in exactly one place: `SITE_URL` in `vite.config.js`, which replaces `__SITE_URL__` in `index.html` for the OG tags. Change it there and the card follows.

`wrangler.jsonc` serves `./dist` with `not_found_handling: single-page-application`, because deep links like `/projects/openturret` are routes the client router owns.

---

## Git conventions

- `prod` is the main branch and the deploy target. `dev` is the integration branch. Work happens on descriptive feature branches (`fix-intro-handover`, `fix-rail-alignment`, `rework-alpine`), merged by PR.
- **The history carries no attribution trailers.** Nine PRs in, there is not one `Co-Authored-By` or "Generated with" line. Do not add them unless Michael asks.
- Commit messages are prose, not changelog bullets: an imperative subject that says what the code now does ("Hand the intro over when the plot has actually finished"), then a body explaining what was wrong and why the fix is right — **with the measurement that proves it** where there is one. Read a few with `git log` before writing one.
- Merge commit messages are short, a subject plus a line or two.

---

## Working style

- The codebase is heavily commented, and the comments explain *why*, in full sentences, often with the failed approach that preceded them. Match that. A comment that restates the code is worse than none.
- Prose voice throughout — in comments, copy and commit messages alike. No bullet-point fragments where a sentence works.
- Changes stay scoped. Do not fold in cleanup or unrelated fixes.
- Verify in a browser before claiming something works, and prefer a measurement over a screenshot. Both intro bugs looked fine to the eye and were caught by counting pixels or reading computed style.

---

## Quick lookup cheatsheet

| I want to… | Look at |
|---|---|
| Add a project | Drop a `.md` in `src/content/projects/` with frontmatter. Nothing else. |
| Change project image layout | The renderer and its comment block in `src/content/projects.js` |
| Add a band to the home page | `src/views/HomeView.vue` — section with `data-zone` + `data-station` |
| Change what the rail or header tracks | `src/descent.js` |
| Touch the contour drawing | `src/components/TopoLines.vue` — read both traps first |
| Change the opening | `src/components/IntroSequence.vue` + `src/intro.js` |
| Add a fade-up on scroll | `v-rise` on the element, `v-rise="2"` to stagger |
| Change colours | `src/styles/base.css`, semantic layer only |
| Regenerate the contours / OG card / favicon | `tools/*.py` |
| Change the live URL | `SITE_URL` in `vite.config.js` |
| Edit copy | `src/content/` — never the views |
