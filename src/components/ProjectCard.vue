<script setup>
import PassPlot from '@/components/PassPlot.vue'
import TopoLines from '@/components/TopoLines.vue'
import TrailMark from '@/components/TrailMark.vue'

const props = defineProps({
  project: { type: Object, required: true },
  index: { type: Number, required: true },
  total: { type: Number, required: true },
})

const pad = (n) => String(n).padStart(2, '0')

// a cover is either a file, a named drawing, or nothing at all yet
const isPlot = props.project.cover === 'pass-plot'
const isImage = Boolean(props.project.cover) && !isPlot
</script>

<template>
  <RouterLink class="card" :to="`/projects/${project.slug}`">
    <div class="cover" :class="{ plot: isPlot, bare: !project.cover }">
      <img v-if="isImage" :src="project.cover" alt="" loading="lazy" decoding="async" />
      <PassPlot v-else-if="isPlot" :label="`${project.title} pass plot`" />
      <!-- nothing shot yet, so the card falls back to a scrap of the map -->
      <TopoLines v-else class="fallback" align="xMinYMin" :interactive="false" />
    </div>

    <p class="index kicker">
      {{ pad(index + 1) }} <span>/ {{ pad(total) }}</span>
      <span v-if="project.status === 'Back burner'" class="paused">Back burner</span>
    </p>

    <h3 class="title">
      <TrailMark v-if="project.difficulty" :shape="project.difficulty" />{{ project.title }}
      <span class="arrow" aria-hidden="true">↗</span>
    </h3>

    <p class="summary">{{ project.summary }}</p>

    <ul class="stack">
      <li v-for="item in project.stack" :key="item">{{ item }}</li>
    </ul>
  </RouterLink>
</template>

<style scoped>
.card {
  display: block;
  text-decoration: none;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--rule);
}

.cover {
  position: relative;
  overflow: hidden;
  aspect-ratio: 16 / 10;
  margin-bottom: 1.4rem;
  border: 1px solid var(--rule);
  border-radius: 2px;
  background: var(--bg-raise);
}

.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.card:hover .cover img {
  scale: 1.03;
}

/* the drawn covers get room to breathe instead of filling the frame */
.cover.plot {
  display: grid;
  place-items: center;
  padding: 1.25rem;
  color: var(--fg-soft);
}

.cover.plot :deep(svg) {
  max-height: 100%;
  width: auto;
  transition: rotate 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.card:hover .cover.plot :deep(svg) {
  rotate: 3deg;
}

.fallback {
  position: absolute;
  inset: 0;
  --topo-opacity: 0.3;
}

.index {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.7rem;
}

.index span {
  opacity: 0.55;
}

.paused {
  margin-left: auto;
  padding: 0.15rem 0.45rem;
  border: 1px solid var(--rule);
  border-radius: 2px;
  opacity: 1;
  font-size: 0.9em;
}

.title {
  display: flex;
  align-items: baseline;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--fg);
  transition: color 0.2s;
}

.card:hover .title {
  color: var(--accent);
}

.arrow {
  margin-left: 0.5rem;
  font-size: 0.7em;
  color: var(--fg-faint);
  transition: translate 0.2s, color 0.2s;
}

.card:hover .arrow {
  translate: 2px -2px;
  color: var(--accent);
}

.summary {
  margin-block: 0.55rem 1.1rem;
  color: var(--fg-soft);
  font-size: 0.9875rem;
  line-height: 1.6;
  max-width: 34rem;
}

.stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.stack li {
  padding: 0.25rem 0.55rem;
  border: 1px solid var(--rule);
  border-radius: 2px;
  font-family: var(--mono);
  font-size: 0.6875rem;
  letter-spacing: 0.04em;
  color: var(--fg-faint);
}

@media (prefers-reduced-motion: reduce) {
  .cover img,
  .cover.plot :deep(svg),
  .arrow,
  .title {
    transition: none;
  }
}
</style>
