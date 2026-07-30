import yaml from 'js-yaml'
import { marked } from 'marked'

// every .md file in here becomes a post, no index or route to update
const markdownFiles = import.meta.glob('./projects/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
})

function parseFrontmatter(raw, path) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) throw new Error(`${path} is missing its frontmatter block`)
  return { meta: yaml.load(match[1]), body: match[2] }
}

/* images -------------------------------------------------------------
   ![Caption](/img/slug/shot.jpg)        figure at column width
   ![Caption](/img/slug/shot.jpg#small)  narrower, for detail shots
   ![Caption](/img/slug/shot.jpg#wide)   breaks out past the text column
   ![](/img/slug/shot.jpg)               no alt, so no caption

   The caption is the alt text, or the quoted title if there is one:
   ![alt](/img/slug/shot.jpg "shown instead of the alt")

   Put two or more on their own line, separated by spaces, and they
   render as a gallery: one frame, one caption underneath. In a gallery
   the alt text stays alt text, so the shared caption has to come from a
   title, and the first #size found sets the whole group. An image
   sitting in the middle of a sentence stays a plain inline image.

   #stack turns a gallery into a fanned deck that opens a lightbox:
   ![front](/img/slug/a.jpg#stack) ![behind](/img/slug/b.jpg#small)
   Tokens are read across the whole group, so one image can carry the
   mode and another the size.                                         */

const SIZES = new Set(['small', 'wide'])
const MODES = new Set(['stack'])

const escapeHtml = (value) =>
  String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;')

function layout(href) {
  const [src, hash] = String(href).split('#')
  return { src, size: SIZES.has(hash) ? hash : '', mode: MODES.has(hash) ? hash : '' }
}

function image({ href, text }) {
  const { src } = layout(href)
  return `<img src="${escapeHtml(src)}" alt="${escapeHtml(text ?? '')}" loading="lazy" decoding="async">`
}

const caption = (text) => (text ? `<figcaption>${escapeHtml(text)}</figcaption>` : '')

function figure(token) {
  const { size } = layout(token.href)
  return `<figure class="shot${size ? ` shot-${size}` : ''}">${image(token)}${caption(token.title || token.text)}</figure>`
}

// one frame around the set, with a single note under all of them
function gallery(tokens) {
  const size = tokens.map((t) => layout(t.href).size).find(Boolean)
  const mode = tokens.map((t) => layout(t.href).mode).find(Boolean)
  const note = tokens.map((t) => t.title).find(Boolean)
  const cls = `gallery${mode ? ` gallery-${mode}` : ''}${size ? ` gallery-${size}` : ''}`

  // a real button, so the deck is focusable and Enter works without any
  // help from the view. ProjectView delegates the click to the lightbox.
  if (mode === 'stack') {
    const cards = tokens.map((t) => `<span class="card">${image(t)}</span>`).join('')
    const label = escapeHtml(`Open gallery, ${tokens.length} images`)
    const deck = `<button type="button" class="stack" aria-label="${label}">${cards}</button>`
    return `<figure class="${cls}">${deck}${caption(note)}</figure>`
  }

  return `<figure class="${cls}">${tokens.map(image).join('')}${caption(note)}</figure>`
}

const renderer = {
  // keeps images inline when they share a paragraph with text
  image(token) {
    return image(token)
  },

  paragraph(token) {
    const images = token.tokens.filter((t) => t.type === 'image')
    const prose = token.tokens.filter((t) => t.type !== 'image' && t.raw.trim())

    if (images.length && !prose.length) {
      return images.length === 1 ? figure(images[0]) : gallery(images)
    }

    return `<p>${this.parser.parseInline(token.tokens)}</p>`
  },
}

marked.use({ renderer })

export const projects = Object.entries(markdownFiles)
  .map(([path, raw]) => {
    const { meta, body } = parseFrontmatter(raw, path)
    return {
      slug: path.slice(path.lastIndexOf('/') + 1, -3),
      html: marked.parse(body),
      ...meta,
    }
  })
  .sort((a, b) => b.year - a.year)

export const findProject = (slug) => projects.find((project) => project.slug === slug)
