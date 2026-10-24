<script setup>
import { computed, ref, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { findProject } from '@/content/projects'
import ImageLightbox from '@/components/ImageLightbox.vue'
import PassPlot from '@/components/PassPlot.vue'
import TrailMark from '@/components/TrailMark.vue'

const props = defineProps({ slug: { type: String, required: true } })

const router = useRouter()

const project = computed(() => findProject(props.slug))

// same three cover kinds the cards handle: a file, a drawing, or nothing
const cover = computed(() => project.value?.cover)
const isPlot = computed(() => cover.value === 'pass-plot')
const isImage = computed(() => Boolean(cover.value) && !isPlot.value)

// the body is v-html, so the deck's click is caught here by delegation
const lightbox = ref(null)

function onBodyClick(event) {
  // marked writes plain anchors, so links between write-ups would reload
  const link = event.target.closest('a[href^="/"]')
  if (link && !/\.\w+$/.test(link.getAttribute('href'))) {
    event.preventDefault()
    router.push(link.getAttribute('href'))
    return
  }

  const deck = event.target.closest('.stack')
  if (!deck) return

  const cards = [...deck.querySelectorAll('.card')]
  const images = cards.map((card) => {
    const img = card.querySelector('img')
    return { src: img.getAttribute('src'), alt: img.alt }
  })
  if (!images.length) return

  // opens on whichever card was actually clicked, not always the front
  const clicked = cards.indexOf(event.target.closest('.card'))
  lightbox.value = { images, start: clicked < 0 ? 0 : clicked }
}

watchEffect(() => {
  document.title = project.value
    ? `${project.value.title} · Michael Melichar`
    : 'Not found · Michael Melichar'
})
</script>

<template>
  <div v-if="project" class="page" data-zone="light">
    <div class="wrap">
      <RouterLink to="/#work" class="back kicker">← All work</RouterLink>

      <header>
        <p class="kicker eyebrow">
          <TrailMark v-if="project.difficulty" :shape="project.difficulty" />{{ project.year }} ·
          {{ project.status }}
        </p>
        <h1>{{ project.title }}</h1>
        <p class="lead">{{ project.summary }}</p>
      </header>

      <figure v-if="cover" class="cover" :class="{ plot: isPlot }">
        <img v-if="isImage" :src="cover" alt="" />
        <PassPlot v-else :label="`${project.title} pass plot`" />
      </figure>

      <dl>
        <div>
          <dt class="kicker">Stack</dt>
          <dd>{{ project.stack.join(', ') }}</dd>
        </div>
        <div v-if="project.repo">
          <dt class="kicker">Source</dt>
          <dd><a :href="project.repo" rel="noopener">Repository</a></dd>
        </div>
        <div v-if="project.download">
          <dt class="kicker">Download</dt>
          <dd><a :href="project.download" rel="noopener">Modrinth</a></dd>
        </div>
      </dl>

      <article class="body" v-html="project.html" @click="onBodyClick" />
    </div>

    <Teleport to="body">
      <ImageLightbox
        v-if="lightbox"
        :images="lightbox.images"
        :start="lightbox.start"
        @close="lightbox = null"
      />
    </Teleport>
  </div>

  <div v-else class="page" data-zone="light">
    <div class="wrap missing">
      <h1>No such project</h1>
      <p class="lead">That one isn't here. <RouterLink to="/#work">Back to the list.</RouterLink></p>
    </div>
  </div>
</template>

<style scoped>
.page {
  background: var(--snow);
  padding-bottom: clamp(3rem, 8vw, 5rem);
}

.cover {
  margin-block: clamp(1.5rem, 4vw, 2.5rem) 0;
  border: 1px solid var(--rule);
  border-radius: 2px;
  overflow: hidden;
  background: var(--bg-raise);
}

.cover img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.cover.plot {
  display: grid;
  place-items: center;
  padding: clamp(1.5rem, 4vw, 3rem);
  color: var(--fg-soft);
}

.cover.plot :deep(svg) {
  max-width: 26rem;
}

.eyebrow {
  display: flex;
  align-items: baseline;
  margin-bottom: 0.9rem;
}

.back {
  display: inline-block;
  padding-block: 2.5rem 0;
  text-decoration: none;
}

.back:hover {
  color: var(--accent);
}

header {
  padding-block: 1.25rem clamp(1.5rem, 4vw, 2.5rem);
}

h1 {
  font-size: clamp(2rem, 4.5vw, 2.9rem);
  margin-bottom: 0.75rem;
}

dl {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  gap: 1.25rem 2rem;
  padding-block: 1.5rem;
  border-block: 1px solid var(--rule);
}

dd {
  margin: 0;
  margin-top: 0.3rem;
  font-size: 0.9375rem;
}

.body {
  max-width: var(--measure);
  padding-block: clamp(2rem, 5vw, 3rem);
  color: var(--fg-soft);
}

.body :deep(h2) {
  color: var(--fg);
  font-size: 1.25rem;
  margin-top: 2.5rem;
  margin-bottom: 0.6rem;
}

.body :deep(p + p),
.body :deep(ul) {
  margin-top: 1em;
}

/* images ------------------------------------------------------------ */

.body :deep(figure) {
  margin-block: 1.75rem;
}

.body :deep(img) {
  width: 100%;
  border: 1px solid var(--rule);
  border-radius: 2px;
  /* holds the space while the file is still coming down */
  background: var(--bg-raise);
}

.body :deep(figcaption) {
  margin-top: 0.55rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--fg-faint);
}

/* capped both ways, so a tall photo can't run away down the page */
.body :deep(.shot-small) {
  width: fit-content;
  max-width: min(20rem, 100%);
}

.body :deep(.shot-small img) {
  width: auto;
  max-width: 100%;
  max-height: 22rem;
}

.body :deep(.gallery) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
  gap: 0.75rem;
}

/* the shared note sits under the whole row, not beside the last tile */
.body :deep(.gallery figcaption) {
  grid-column: 1 / -1;
  margin-top: 0;
}

/* a common frame keeps a row of mismatched shots from looking ragged */
.body :deep(.gallery img) {
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.body :deep(.gallery-small) {
  max-width: 26rem;
}

/* upright frames, so a row of phone photos keeps its subject */
.body :deep(.gallery-tall) {
  max-width: 32rem;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
}

.body :deep(.gallery-tall img) {
  aspect-ratio: 3 / 4;
}

/* stacked deck ------------------------------------------------------- */

.body :deep(.gallery-stack) {
  display: block;
  max-width: 30rem;
  /* the back cards fan up and right, so keep that corner clear */
  margin-top: 3rem;
  padding-right: 2.5rem;
}

.body :deep(.gallery-stack.gallery-small) {
  max-width: 22rem;
}

.body :deep(.stack) {
  display: block;
  position: relative;
  width: 100%;
  padding: 0;
  border: 0;
  background: none;
  cursor: pointer;
}

.body :deep(.stack .card) {
  position: absolute;
  inset: 0;
  transition: transform 0.28s ease;
}

/* the front card is the only one in flow, so it sets the deck's height */
.body :deep(.stack .card:first-child) {
  position: relative;
  z-index: 3;
}

.body :deep(.stack .card:nth-child(2)) {
  z-index: 2;
  transform: translate(4%, -4%) rotate(2deg);
}

.body :deep(.stack .card:nth-child(3)) {
  z-index: 1;
  transform: translate(7%, -7%) rotate(4deg);
}

/* anything past the third only ever shows up in the lightbox */
.body :deep(.stack .card:nth-child(n + 4)) {
  display: none;
}

.body :deep(.stack img) {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  /* the back cards read as separate photos, not one bleeding edge */
  box-shadow: 0 1px 8px rgb(17 20 24 / 0.12);
}

.body :deep(.stack:hover .card:nth-child(2)),
.body :deep(.stack:focus-visible .card:nth-child(2)) {
  transform: translate(9%, -9%) rotate(5deg);
}

.body :deep(.stack:hover .card:nth-child(3)),
.body :deep(.stack:focus-visible .card:nth-child(3)) {
  transform: translate(16%, -16%) rotate(9deg);
}

@media (prefers-reduced-motion: reduce) {
  .body :deep(.stack .card) {
    transition: none;
  }
}

/* only break out of the text column once there is room to the right */
@media (min-width: 68rem) {
  .body :deep(.shot-wide),
  .body :deep(.gallery-wide) {
    width: 54rem;
  }
}

.body :deep(code) {
  font-family: var(--mono);
  font-size: 0.875em;
  background: var(--bg-raise);
  padding: 0.1em 0.35em;
  border-radius: 2px;
}

.body :deep(pre) {
  background: var(--bg-raise);
  padding: 1rem;
  border-radius: 2px;
  overflow-x: auto;
  margin-top: 1em;
}

.body :deep(pre code) {
  background: none;
  padding: 0;
}

.missing {
  padding-block: 6rem;
}
</style>
