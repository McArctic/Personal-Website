import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/* Link previews need absolute URLs, so the one place the live domain is
   written down is here. Change it and the card follows. */
const SITE_URL = 'https://michaelmelichar.com'

/* Cloudflare Web Analytics. Grab the token from the dashboard under
   Analytics & Logs > Web Analytics, add the site, and paste the value out of
   the data-cf-beacon snippet it hands you. Empty means no beacon, which is
   also what happens in dev, so local page loads never reach Cloudflare. */
const CF_ANALYTICS_TOKEN = ''

const siteUrl = () => ({
  name: 'site-url',
  transformIndexHtml: (html) => html.replaceAll('__SITE_URL__', SITE_URL),
})

const analytics = () => ({
  name: 'cf-analytics',
  transformIndexHtml(html, ctx) {
    // ctx.server is only set by the dev server
    if (ctx.server || !CF_ANALYTICS_TOKEN) return
    return {
      tags: [
        {
          tag: 'script',
          attrs: {
            defer: true,
            src: 'https://static.cloudflareinsights.com/beacon.min.js',
            'data-cf-beacon': JSON.stringify({ token: CF_ANALYTICS_TOKEN }),
          },
          injectTo: 'body',
        },
      ],
    }
  },
})

export default defineConfig({
  plugins: [vue(), siteUrl(), analytics()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
