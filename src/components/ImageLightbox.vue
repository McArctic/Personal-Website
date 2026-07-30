<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  images: { type: Array, required: true },
  start: { type: Number, default: 0 },
})

const emit = defineEmits(['close'])

const index = ref(props.start)
const closeButton = ref(null)

const current = computed(() => props.images[index.value] ?? null)
const many = computed(() => props.images.length > 1)

const step = (by) => {
  index.value = (index.value + by + props.images.length) % props.images.length
}

function onKey(event) {
  if (event.key === 'Escape') return emit('close')
  if (!many.value) return
  if (event.key === 'ArrowRight') step(1)
  if (event.key === 'ArrowLeft') step(-1)
}

watch(
  () => props.start,
  (value) => {
    index.value = value
  },
)

// the overlay owns the keyboard while it is up, and the page behind it
// holds its scroll position instead of jumping to the top
let opener = null
let scrollbarGap = 0

onMounted(() => {
  opener = document.activeElement
  scrollbarGap = window.innerWidth - document.documentElement.clientWidth
  document.body.style.overflow = 'hidden'
  if (scrollbarGap > 0) document.body.style.paddingRight = `${scrollbarGap}px`
  window.addEventListener('keydown', onKey)
  closeButton.value?.focus()
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
  document.body.style.paddingRight = ''
  if (opener instanceof HTMLElement) opener.focus()
})
</script>

<template>
  <div
    class="backdrop"
    role="dialog"
    aria-modal="true"
    aria-label="Image gallery"
    tabindex="-1"
    @click.self="emit('close')"
  >
    <button ref="closeButton" type="button" class="close" aria-label="Close gallery" @click="emit('close')">
      ✕
    </button>

    <button
      v-if="many"
      type="button"
      class="arrow prev"
      aria-label="Previous image"
      @click="step(-1)"
    >
      ‹
    </button>

    <figure v-if="current" class="frame">
      <img :src="current.src" :alt="current.alt" />
      <figcaption>
        <span v-if="current.alt">{{ current.alt }}</span>
        <span v-if="many" class="count">{{ index + 1 }} / {{ images.length }}</span>
      </figcaption>
    </figure>

    <button v-if="many" type="button" class="arrow next" aria-label="Next image" @click="step(1)">
      ›
    </button>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: clamp(0.5rem, 2vw, 1.5rem);
  padding: clamp(1rem, 4vw, 3rem);
  background: rgb(17 20 24 / 0.92);
}

.frame {
  grid-column: 2;
  display: grid;
  justify-items: center;
  gap: 1rem;
  min-width: 0;
}

.frame img {
  max-width: 100%;
  /* leaves room for the caption under the tallest image */
  max-height: calc(100vh - 9rem);
  object-fit: contain;
  border-radius: 2px;
}

figcaption {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.25rem 1rem;
  max-width: var(--measure);
  color: #c9d1d7;
  font-size: 0.9375rem;
  text-align: center;
}

.count {
  font-family: var(--mono);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  color: #8b959d;
  align-self: center;
}

button {
  background: none;
  border: 0;
  color: #e8edf1;
  cursor: pointer;
  font-family: inherit;
  line-height: 1;
  transition: color 0.15s, background-color 0.15s;
}

button:hover {
  color: #fff;
}

.close {
  position: absolute;
  top: clamp(0.75rem, 3vw, 1.75rem);
  right: clamp(0.75rem, 3vw, 1.75rem);
  font-size: 1.25rem;
  padding: 0.5rem 0.65rem;
  border-radius: 2px;
}

.close:hover {
  background: rgb(255 255 255 / 0.1);
}

.arrow {
  font-size: 2.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 2px;
}

.arrow:hover {
  background: rgb(255 255 255 / 0.1);
}

.prev {
  grid-column: 1;
}

.next {
  grid-column: 3;
}

:focus-visible {
  outline: 2px solid #fff;
  outline-offset: 2px;
}
</style>
