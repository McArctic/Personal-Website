import yaml from 'js-yaml'
import { marked } from 'marked'

// Every .md file in ./projects becomes a post. Adding one is the whole workflow:
// no index to update, no route to register.
const files = import.meta.glob('./projects/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
})

function split(raw, path) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) throw new Error(`${path} is missing its frontmatter block`)
  return { meta: yaml.load(match[1]), body: match[2] }
}

export const projects = Object.entries(files)
  .map(([path, raw]) => {
    const { meta, body } = split(raw, path)
    return {
      slug: path.slice(path.lastIndexOf('/') + 1, -3),
      html: marked.parse(body),
      ...meta,
    }
  })
  .sort((a, b) => b.year - a.year)

export const findProject = (slug) => projects.find((p) => p.slug === slug)
