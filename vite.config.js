import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/* Link previews need absolute URLs, so the one place the live domain is
   written down is here. Change it and the card follows. */
const SITE_URL = 'https://michaelmelichar.com'

const siteUrl = () => ({
  name: 'site-url',
  transformIndexHtml: (html) => html.replaceAll('__SITE_URL__', SITE_URL),
})

export default defineConfig({
  plugins: [vue(), siteUrl()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
