<script setup>
import { computed } from 'vue'
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
</script>

<template>
  <header :class="[headerZone, { lifted: scrolled }]">
    <div class="wrap bar">
      <RouterLink to="/" class="mark">
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

      <a class="resume" href="/pdf/resume.pdf" rel="noopener">
        Resume<span class="arrow" aria-hidden="true">↗</span>
      </a>
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
  .arrow {
    transition: none;
  }
}
</style>
