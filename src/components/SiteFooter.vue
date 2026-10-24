<script setup>
import TrailSign from '@/components/TrailSign.vue'
import { profile } from '@/content/profile'

const { coords, elevation } = profile.marker
const year = new Date().getFullYear()
</script>

<template>
  <footer class="dark" data-zone="dark">
    <div class="wrap bar">
      <div class="sign">
        <TrailSign />
        <p class="kicker plaque">
          {{ profile.location }} · {{ coords }} · {{ elevation }}
        </p>
      </div>

      <p class="kicker colophon">
        Contours plotted from USGS 3DEP data · {{ year }}
      </p>
    </div>
  </footer>
</template>

<style scoped>
footer {
  border-top: 1px solid var(--rule);
}

.bar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem 2rem;
  padding-block: 2.25rem 2.75rem;
}

.plaque {
  margin-top: 0.85rem;
}

.colophon {
  color: var(--fg-faint);
  opacity: 0.7;
}
</style>
