<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
})

// splits "some text [label](/target) more text" into plain and linked runs
const parts = computed(() => {
  const link = /\[([^\]]+)\]\(([^)]+)\)/g
  const out = []
  let last = 0
  let match

  while ((match = link.exec(props.text))) {
    if (match.index > last) out.push({ text: props.text.slice(last, match.index) })
    out.push({ text: match[1], href: match[2] })
    last = match.index + match[0].length
  }
  if (last < props.text.length) out.push({ text: props.text.slice(last) })

  return out
})

// a leading slash is a route, unless it points at a real file like /resume.pdf
const isRoute = (href) => href.startsWith('/') && !/\.\w+$/.test(href)
</script>

<template>
  <p>
    <template v-for="(part, i) in parts" :key="i">
      <RouterLink v-if="part.href && isRoute(part.href)" :to="part.href">{{ part.text }}</RouterLink>
      <a v-else-if="part.href" :href="part.href" rel="noopener">{{ part.text }}</a>
      <template v-else>{{ part.text }}</template>
    </template>
  </p>
</template>
