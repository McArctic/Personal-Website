<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { activeStation, goToStation, headerZone, scrolled, stations } from '@/descent'

const nav = [
  { id: 'work', label: 'Work' },
  { id: 'about', label: 'About' },
  { id: 'experience', label: 'Experience' },
  { id: 'contact', label: 'Contact' },
]

const route = useRoute()

// on a write-up there is nothing to scroll to, so the links go home first
const here = computed(() => stations.value[activeStation.value]?.id)
const isHome = computed(() => route.name === 'home')

/* Below the nav's breakpoint the links collapse into a panel under the bar.
   The breakpoint is duplicated here because the panel has to close itself if
   the viewport grows past it, otherwise it stays open behind a nav that is
   already back. */
const WIDE = '(min-width: 52rem)'

const open = ref(false)
const toggleEl = ref(null)
const panelEl = ref(null)

const close = () => {
  open.value = false
}

function pick(id) {
  close()
  goToStation(id)
}

function onKeydown(event) {
  if (event.key !== 'Escape' || !open.value) return
  close()
  toggleEl.value?.focus()
}

const wide = matchMedia(WIDE)
const onWide = (event) => {
  if (event.matches) close()
}

// the panel is the only thing on screen worth tabbing to once it is open
watch(open, async (isOpen) => {
  if (!isOpen) return
  await nextTick()
  panelEl.value?.querySelector('a')?.focus({ preventScroll: true })
})

onMounted(() => {
  addEventListener('keydown', onKeydown)
  wide.addEventListener('change', onWide)
})

onBeforeUnmount(() => {
  removeEventListener('keydown', onKeydown)
  wide.removeEventListener('change', onWide)
})
</script>

<template>
  <header :class="[headerZone, { lifted: scrolled, open }]">
    <div class="wrap bar">
      <RouterLink to="/" class="mark" @click="close">
        <span class="mono">mm<span class="dot">.</span></span>
        <span class="full">Michael Melichar</span>
      </RouterLink>

      <nav>
        <!-- already home, so jump between bands instead of routing -->
        <template v-for="item in nav" :key="item.id">
          <a
            v-if="isHome"
            :href="`#${item.id}`"
            :class="{ on: here === item.id }"
            @click.prevent="goToStation(item.id)"
            >{{ item.label }}</a
          >
          <RouterLink v-else :to="`/#${item.id}`">{{ item.label }}</RouterLink>
        </template>
      </nav>

      <div class="end">
        <a class="resume" href="/pdf/resume.pdf" rel="noopener">
          Resume<span class="arrow" aria-hidden="true">↗</span>
        </a>

        <button
          ref="toggleEl"
          type="button"
          class="toggle"
          :aria-expanded="open"
          :aria-label="open ? 'Close menu' : 'Open menu'"
          aria-controls="site-menu"
          @click="open = !open"
        >
          <span class="bars" aria-hidden="true"><span /><span /><span /></span>
        </button>
      </div>
    </div>

    <!-- the same junctions as the nav, stacked for a thumb -->
    <div id="site-menu" class="menu">
      <div ref="panelEl" class="wrap">
        <template v-for="item in nav" :key="item.id">
          <a
            v-if="isHome"
            :href="`#${item.id}`"
            :class="{ on: here === item.id }"
            @click.prevent="pick(item.id)"
            >{{ item.label }}</a
          >
          <RouterLink v-else :to="`/#${item.id}`" @click="close">{{ item.label }}</RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid transparent;
  transition: background 0.4s, border-color 0.4s, color 0.4s;
  color: var(--summit-ink);
  /* the header sits in flow above the first band, so without a background
     of its own the page canvas shows through and the text lands on it */
  background: var(--summit);
}

header.light {
  color: var(--ink);
  background: var(--snow);
}

/* once it is over content it goes translucent and picks up a rule */
header.lifted {
  background: color-mix(in srgb, var(--summit) 86%, transparent);
  border-bottom-color: var(--summit-line);
  backdrop-filter: blur(10px);
}

header.light.lifted {
  background: color-mix(in srgb, var(--snow) 86%, transparent);
  border-bottom-color: var(--line);
}

.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding-block: 1rem;
}

.mark {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  text-decoration: none;
  white-space: nowrap;
}

.mono {
  font-family: var(--mono);
  font-weight: 500;
  font-size: 1.05rem;
  letter-spacing: -0.04em;
}

.dot {
  color: var(--alpine-lit);
}

header.light .dot {
  color: var(--alpine);
}

.full {
  font-size: 0.9375rem;
  font-weight: 500;
  opacity: 0.72;
}

nav {
  display: none;
  gap: clamp(1rem, 2.6vw, 2rem);
  font-size: 0.9375rem;
}

@media (min-width: 52rem) {
  nav {
    display: flex;
  }
}

nav a {
  position: relative;
  text-decoration: none;
  opacity: 0.62;
  transition: opacity 0.2s;
}

nav a:hover,
nav a.on {
  opacity: 1;
}

/* the active junction gets a trail diamond, same as the rail */
nav a.on::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 50%;
  width: 4px;
  height: 4px;
  margin-left: -2px;
  rotate: 45deg;
  background: currentColor;
}

.resume {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.42rem 0.85rem;
  border: 1px solid currentColor;
  border-radius: 2px;
  font-size: 0.8125rem;
  text-decoration: none;
  opacity: 0.72;
  white-space: nowrap;
  transition: opacity 0.2s, background 0.2s, color 0.2s;
}

.resume:hover {
  opacity: 1;
  background: var(--alpine-lit);
  border-color: var(--alpine-lit);
  color: var(--summit);
}

header.light .resume:hover {
  background: var(--alpine);
  border-color: var(--alpine);
  color: var(--snow);
}

.arrow {
  font-size: 0.9em;
  transition: translate 0.2s;
}

.resume:hover .arrow {
  translate: 1px -1px;
}

/* stretch, not center: the toggle takes its height from the resume button
   beside it, so adding it does not make the bar any taller. descent.js reads
   the zone at a fixed 72px below the top of the viewport, and the first band
   starts about two pixels under that, so a bar that grows at all would push
   the summit out of reach of the probe and leave the header light over it. */
.end {
  display: flex;
  align-items: stretch;
  gap: 0.35rem;
}

/* the menu ------------------------------------------------------------ */

.toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  /* the icon is mostly whitespace, so the box hangs into the gutter to put
     the bars themselves on the same line as the text above and below */
  margin-right: -0.5rem;
  padding: 0;
  border: 0;
  border-radius: 2px;
  background: none;
  color: inherit;
  cursor: pointer;
}

.bars {
  position: relative;
  width: 18px;
  height: 12px;
}

.bars span {
  position: absolute;
  left: 0;
  width: 100%;
  height: 1px;
  background: currentColor;
  transition: translate 0.24s, rotate 0.24s, opacity 0.14s;
}

.bars span:nth-child(1) {
  top: 0;
}
.bars span:nth-child(2) {
  top: 50%;
}
.bars span:nth-child(3) {
  top: 100%;
}

header.open .bars span:nth-child(1) {
  translate: 0 6px;
  rotate: 45deg;
}

header.open .bars span:nth-child(2) {
  opacity: 0;
}

header.open .bars span:nth-child(3) {
  translate: 0 -6px;
  rotate: -45deg;
}

/* The panel hangs out of flow on purpose. The header is sticky but still in
   flow, so a panel inside it pushes every band down by its own height, and
   descent.js reads the zone at a fixed depth below the top of the viewport:
   the bands slide past that depth, the lookup finds nothing above it and
   falls back to light, and the header turns white over the dark hero.

   0fr to 1fr still animates to the panel's own height, which a max-height
   guess would only ever approximate. */
.menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  display: grid;
  grid-template-rows: 0fr;
  background: var(--summit);
  backdrop-filter: blur(10px);
  transition: grid-template-rows 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

header.light .menu {
  background: var(--snow);
}

header.open .menu {
  grid-template-rows: 1fr;
  border-bottom: 1px solid var(--summit-line);
}

header.light.open .menu {
  border-bottom-color: var(--line);
}

.menu > .wrap {
  overflow: hidden;
  /* this is also what keeps the links out of the tab order while it is shut,
     so the panel has to stay hidden until the collapse has finished */
  visibility: hidden;
  transition: visibility 0s 0.3s;
}

header.open .menu > .wrap {
  visibility: visible;
  transition: visibility 0s;
}

.menu a {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding-block: 0.95rem;
  border-top: 1px solid var(--summit-line);
  font-size: 1.0625rem;
  text-decoration: none;
  opacity: 0.72;
}

header.light .menu a {
  border-top-color: var(--line);
}

/* the panel clips itself while it opens, so a ring standing off the row
   loses its top edge against the first junction. It goes inside instead. */
.menu a:focus-visible {
  outline-offset: -3px;
}

.menu a.on {
  opacity: 1;
}

/* the active junction gets a trail diamond, same as the rail and the nav.
   It is always in the row so the labels do not shift as you move down. */
.menu a::before {
  content: '';
  width: 5px;
  height: 5px;
  rotate: 45deg;
  background: currentColor;
  opacity: 0;
}

.menu a.on::before {
  opacity: 1;
}

/* padding on the clipped box would not collapse with it, so the gap under
   the last junction belongs to the link */
.menu a:last-child {
  padding-bottom: 1.5rem;
}

@media (min-width: 52rem) {
  .toggle,
  .menu {
    display: none;
  }
}

/* the full name is already the first thing in the hero */
@media (max-width: 34rem) {
  .full {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  header,
  nav a,
  .resume,
  .arrow,
  .bars span,
  .menu {
    transition: none;
  }
}
</style>
