<script setup>
import TopoLines from '@/components/TopoLines.vue'
import TrailSign from '@/components/TrailSign.vue'
import { profile } from '@/content/profile'

const { coords, elevation } = profile.marker
const year = new Date().getFullYear()
</script>

<template>
  <footer>
    <TopoLines class="topo" align="xMidYMax" />
    <div class="wrap bar">
      <div>
        <TrailSign />
        <p class="kicker plaque">
          {{ profile.location }} · {{ coords }} · {{ elevation }}
        </p>
      </div>
      <ul>
        <li v-for="link in profile.links" :key="link.href">
          <a :href="link.href" rel="me noopener">{{ link.label }}</a>
        </li>
        <li class="kicker year">{{ year }}</li>
      </ul>
    </div>
  </footer>
</template>

<style scoped>
footer {
  position: relative;
  overflow: hidden;
  border-top: 1px solid var(--line);
  margin-top: 5rem;
}

/* Fills the footer, cut only by the rule above it and the bottom of the page.
   Framed on the southern slopes so it is not the same crop as the hero. */
.topo {
  position: absolute;
  inset: 0;
}

.bar {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem 2rem;
  padding-block: 2.5rem 3.25rem;
}

.plaque {
  margin-top: 0.85rem;
}

ul {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 1.5rem;
  font-size: 0.9375rem;
}

.year {
  color: var(--ink-faint);
}
</style>
