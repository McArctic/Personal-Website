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
