<script setup>
import { computed } from 'vue'
import { summitElevation } from '@/content/killington'
import { activeStation, goToStation, progress, railZone, stations } from '@/descent'

/* The rail is the trail map's spine: scrolling the page is the descent, so
   the readout drops from the summit to the base as you go. */

const BASE_ELEVATION = 352

const elevation = computed(() =>
  Math.round(summitElevation - (summitElevation - BASE_ELEVATION) * progress.value),
)
</script>

<template>
  <aside v-if="stations.length" class="rail" :class="`over-${railZone}`" aria-hidden="true">
    <p class="readout">{{ elevation }}<span>m</span></p>

    <div class="track">
      <span class="fill" :style="{ transform: `scaleY(${progress})` }" />
      <a
        v-for="(station, i) in stations"
        :key="station.id"
        class="tick"
        :class="{ on: i === activeStation }"
        :href="`#${station.id}`"
        :style="{ top: `${station.at * 100}%` }"
        tabindex="-1"
        @click.prevent="goToStation(station.id)"
      >
        <span class="dot" />
        <span class="label">{{ station.label }}</span>
      </a>
    </div>

    <p class="foot">Base</p>
  </aside>
</template>

<style scoped>
.rail {
  position: fixed;
  left: clamp(1rem, 2.4vw, 2.25rem);
  top: 50%;
  translate: 0 -50%;
  z-index: 8;
  display: none;
  flex-direction: column;
  align-items: center;
  gap: 0.9rem;
  font-family: var(--mono);
  font-size: 0.625rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--rail-dim);

  --rail-dim: #46545f;
  --rail-lit: #9fb4c4;
}

/* against a light band the rail has to darken to stay readable. The zone goes
   on as over-light rather than as the bare class, because .dark is the band
   utility and it paints a background as well as remapping the tokens: worn by
   the rail that put a 32px slab of summit over the valley for as long as the
   two shared a screen. The rail is furniture over the bands, not one of
   them, and it reads the zone for its ink alone. */
.rail.over-light {
  --rail-dim: #ccd4d9;
  --rail-lit: #5a636b;
}

/* The labels run to the right of the rail, into the page margin, so the rail
   only appears once that margin can hold the longest one. Measured at this
   width there is about 19px between the longest label and the text column.
   Lengthen a station name and that is the budget it has to fit in. */
@media (min-width: 88rem) {
  .rail {
    display: flex;
  }
}

.readout {
  font-variant-numeric: tabular-nums;
  font-size: 0.6875rem;
  color: var(--rail-lit);
  transition: color 0.4s;
}

.readout span {
  font-size: 0.8em;
  opacity: 0.6;
  margin-left: 0.15em;
}

.track {
  position: relative;
  width: 1px;
  height: min(42vh, 22rem);
  background: var(--rail-dim);
  transition: background 0.4s;
}

.fill {
  position: absolute;
  inset: 0;
  background: var(--rail-lit);
  transform-origin: top;
  transition: background 0.4s;
}

.tick {
  position: absolute;
  left: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  /* only the dot straddles the rail. A percentage here would resolve against
     the whole row, label included, so every tick would sit a different
     distance left depending on how long its label is. */
  margin-left: calc((1px - 5px) / 2);
  translate: 0 -50%;
  text-decoration: none;
  color: inherit;
}

.dot {
  width: 5px;
  height: 5px;
  background: var(--rail-dim);
  rotate: 45deg;
  transition: background 0.3s, scale 0.3s;
}

.label {
  white-space: nowrap;
  opacity: 0;
  translate: -0.3rem 0;
  transition: opacity 0.3s, translate 0.3s, color 0.4s;
  color: var(--rail-lit);
}

.tick.on .dot {
  background: var(--rail-lit);
  scale: 1.5;
}

.tick.on .label,
.rail:hover .label {
  opacity: 1;
  translate: 0 0;
}

.foot {
  color: var(--rail-dim);
  transition: color 0.4s;
}

@media (prefers-reduced-motion: reduce) {
  .dot,
  .label {
    transition: none;
  }
}
</style>
