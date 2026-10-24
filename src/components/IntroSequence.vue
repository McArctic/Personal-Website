<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import TopoLines from '@/components/TopoLines.vue'
import { summitElevation } from '@/content/killington'
import { endIntro } from '@/intro'

const PLOT_TIME = 1.5
// a beat on the finished map before it hands over
const HOLD = 650
// if the plot never reports back, leave anyway rather than trap anyone here
const BACKSTOP = 6000
const BASE_ELEVATION = 352

const elevation = ref(BASE_ELEVATION)
const leaving = ref(false)

let frameId = 0
let timers = []
let startedAt = 0

const ease = (t) => 1 - Math.pow(1 - t, 3)

function climb(now) {
  const progress = Math.min((now - startedAt) / (PLOT_TIME * 1000), 1)
  elevation.value = Math.round(
    BASE_ELEVATION + (summitElevation - BASE_ELEVATION) * ease(progress),
  )
  if (progress < 1) frameId = requestAnimationFrame(climb)
}

// one way out, whether the timeline ran its course or the visitor cut it short
function finish() {
  if (leaving.value) return
  leaving.value = true
  elevation.value = summitElevation
  cancelAnimationFrame(frameId)
  timers.forEach(clearTimeout)
  timers = [setTimeout(endIntro, 620)]
}

// the readout climbs with the strokes, so it starts when they do
function onPlotStart() {
  startedAt = performance.now()
  cancelAnimationFrame(frameId)
  frameId = requestAnimationFrame(climb)
}

function onPlotted() {
  if (leaving.value) return
  timers.push(setTimeout(finish, HOLD))
}

onMounted(() => {
  // nothing underneath is ready to be looked at yet
  document.body.style.overflow = 'hidden'
  startedAt = performance.now()
  frameId = requestAnimationFrame(climb)
  timers.push(setTimeout(finish, BACKSTOP))

  addEventListener('pointerdown', finish)
  addEventListener('keydown', finish)
  addEventListener('wheel', finish, { passive: true })
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  cancelAnimationFrame(frameId)
  timers.forEach(clearTimeout)
  removeEventListener('pointerdown', finish)
  removeEventListener('keydown', finish)
  removeEventListener('wheel', finish)
})
</script>

<template>
  <div class="intro dark" :class="{ leaving }">
    <!-- same framing as the hero, so the lines do not jump on handover -->
    <TopoLines
      class="topo"
      align="xMidYMax"
      draw
      :draw-time="PLOT_TIME"
      :interactive="false"
      @plotstart="onPlotStart"
      @plotted="onPlotted"
    />

    <div class="readout">
      <p class="kicker">Killington Peak · Vermont</p>
      <p class="elevation">
        {{ elevation }}<span class="unit">m</span>
      </p>
    </div>

    <p class="kicker hint">Press anything to skip</p>
  </div>
</template>

<style scoped>
.intro {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: grid;
  place-items: center;
  background: var(--summit);
  transition: opacity 0.6s ease, visibility 0.6s;
}

.intro.leaving {
  opacity: 0;
  visibility: hidden;
}

.topo {
  position: absolute;
  inset: 0;
  --topo-opacity: 0.28;
}

.readout {
  position: relative;
  text-align: center;
  animation: settle 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.elevation {
  font-family: var(--mono);
  font-size: clamp(2.5rem, 9vw, 5rem);
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.03em;
  color: var(--summit-ink);
  /* the digits are tabular, so the number never jitters as it climbs */
  font-variant-numeric: tabular-nums;
  margin-top: 0.75rem;
}

.unit {
  font-size: 0.32em;
  letter-spacing: 0.1em;
  margin-left: 0.4em;
  color: var(--alpine-lit);
}

.hint {
  position: absolute;
  bottom: clamp(1.5rem, 5vw, 2.75rem);
  color: var(--summit-faint);
  animation: settle 0.5s 0.9s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes settle {
  from {
    opacity: 0;
    transform: translateY(0.6rem);
  }
}

@media (prefers-reduced-motion: reduce) {
  .readout,
  .hint {
    animation: none;
  }
}
</style>
