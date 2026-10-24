<script setup>
import { computed, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { contours } from '@/content/killington'

const CURSOR_REACH = 240
const PUSH_DISTANCE = 20

const props = defineProps({
  align: { type: String, default: 'xMidYMid' },
  // plot the lines on instead of having them already there
  draw: { type: Boolean, default: false },
  // seconds from the first stroke to the last one landing
  drawTime: { type: Number, default: 1.6 },
  // the cursor deform costs a frame loop, so bands that don't need it opt out
  interactive: { type: Boolean, default: true },
})

const contourPoints = contours.map((contour) =>
  contour.d
    .slice(2)
    .split(' L ')
    .map((pair) => pair.split(' ').map(Number)),
)

const round = (n) => Math.round(n * 10) / 10

// Catmull-Rom to Béziers, so the simplified polylines still read as terrain
function toSmoothPath(points) {
  const count = points.length
  if (count < 3) {
    return `M ${points.map(([x, y]) => `${round(x)} ${round(y)}`).join(' L ')}`
  }
  let path = `M ${round(points[0][0])} ${round(points[0][1])}`
  for (let i = 0; i < count - 1; i++) {
    const [prevX, prevY] = points[i === 0 ? 0 : i - 1]
    const [startX, startY] = points[i]
    const [endX, endY] = points[i + 1]
    const [nextX, nextY] = points[Math.min(i + 2, count - 1)]
    path +=
      ` C ${round(startX + (endX - prevX) / 6)} ${round(startY + (endY - prevY) / 6)},` +
      ` ${round(endX - (nextX - startX) / 6)} ${round(endY - (nextY - startY) / 6)},` +
      ` ${round(endX)} ${round(endY)}`
  }
  return path
}

const restingPaths = contourPoints.map(toSmoothPath)

/* the plot climbs the mountain: the lowest contour starts first and the
   summit ring lands last, so the terrain fills in from the outside */
const levels = contours.map((contour) => contour.level)
const lowest = Math.min(...levels)
const highest = Math.max(...levels)
const bandSpan = highest - lowest || 1

/* Each line takes 60% of the budget to draw and the starts are staggered
   across the other 40%, so the summit ring lands exactly on drawTime. */
const STAGGER = 0.4

const strokeTime = computed(() => props.drawTime * (1 - STAGGER))

const delays = computed(() =>
  levels.map((level) => (((level - lowest) / bandSpan) * props.drawTime * STAGGER).toFixed(2)),
)

function deform(cursorX, cursorY, strength) {
  if (strength <= 0.001) return restingPaths
  return contourPoints.map((points) =>
    toSmoothPath(
      points.map(([x, y]) => {
        const dx = x - cursorX
        const dy = y - cursorY
        const distanceSq = dx * dx + dy * dy
        // gaussian falloff, so only the lines near the cursor move
        const push = PUSH_DISTANCE * strength * Math.exp(-distanceSq / (CURSOR_REACH * CURSOR_REACH))
        if (push < 0.05) return [x, y]
        const distance = Math.sqrt(distanceSq) || 1
        return [x + (dx / distance) * push, y + (dy / distance) * push]
      }),
    ),
  )
}

/* The plot runs on CSS animations, which do not start until the browser
   first styles these paths, and that waits on the render-blocking webfont
   stylesheet. Anything timing the plot from mount therefore runs ahead of it.

   So count the animation events instead. The listeners go on in onMounted,
   before a single stroke can have finished, and animationend bubbles up from
   the paths, so the count cannot be missed however late the plot begins.
   Asking getAnimations() on a frame would not do: on a cold load it answers
   with nothing yet, which reads identically to nothing left to wait for. */
const emit = defineEmits(['plotstart', 'plotted'])

function reportPlot(el) {
  const total = el.querySelectorAll('path').length
  if (!motionAllowed || !total) {
    emit('plotstart')
    emit('plotted')
    return
  }

  let ended = 0
  el.addEventListener('animationstart', () => emit('plotstart'), { once: true })
  el.addEventListener('animationend', () => {
    if (++ended === total) emit('plotted')
  })
}

const svgEl = shallowRef(null)
const paths = ref(restingPaths)
const emphasis = ref(1)

const motionAllowed = !matchMedia('(prefers-reduced-motion: reduce)').matches
const target = { x: 640, y: 450, strength: 0 }
const current = { x: 640, y: 450, strength: 0 }
let frameId = 0

function animate() {
  // trail the pointer a little, otherwise the terrain twitches
  current.x += (target.x - current.x) * 0.16
  current.y += (target.y - current.y) * 0.16
  current.strength += (target.strength - current.strength) * 0.09

  paths.value = deform(current.x, current.y, current.strength)
  emphasis.value = 1 + current.strength * 0.9

  // park the loop once everything has flattened back out
  if (target.strength === 0 && current.strength < 0.002) {
    current.strength = 0
    paths.value = restingPaths
    emphasis.value = 1
    frameId = 0
    return
  }
  frameId = requestAnimationFrame(animate)
}

function startLoop() {
  if (!frameId) frameId = requestAnimationFrame(animate)
}

function onPointerMove(event) {
  // the screen matrix handles the viewBox scale and any css transform for us
  const matrix = svgEl.value.getScreenCTM()
  if (!matrix) return
  const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse())
  target.x = point.x
  target.y = point.y
  target.strength = 1
  startLoop()
}

function onPointerLeave() {
  target.strength = 0
  startLoop()
}

let section = null

onMounted(() => {
  if (props.draw) reportPlot(svgEl.value)
  if (!motionAllowed || !props.interactive) return
  // listen on the section, so the contours never take the mouse from the text
  section = svgEl.value.parentElement
  section.addEventListener('pointermove', onPointerMove)
  section.addEventListener('pointerleave', onPointerLeave)
})

onBeforeUnmount(() => {
  if (frameId) cancelAnimationFrame(frameId)
  section?.removeEventListener('pointermove', onPointerMove)
  section?.removeEventListener('pointerleave', onPointerLeave)
})
</script>

<template>
  <svg
    ref="svgEl"
    viewBox="0 0 1280 900"
    :preserveAspectRatio="`${align} slice`"
    aria-hidden="true"
    focusable="false"
    :class="{ plotting: draw }"
    :style="{ '--topo-emphasis': emphasis, '--topo-draw': `${strokeTime}s` }"
  >
    <path
      v-for="(path, i) in paths"
      :key="i"
      :d="path"
      fill="none"
      stroke="currentColor"
      stroke-width="1"
      stroke-linecap="round"
      pathLength="1"
      vector-effect="non-scaling-stroke"
      :style="draw ? { animationDelay: `${delays[i]}s` } : null"
    />
  </svg>
</template>

<style scoped>
svg {
  display: block;
  width: 100%;
  height: 100%;
  color: var(--accent);
  /* callers set --topo-opacity, not opacity */
  opacity: calc(var(--topo-opacity, 0.13) * var(--topo-emphasis, 1));
  shape-rendering: geometricPrecision;
  pointer-events: none;
}

/* normalised by pathLength, so every contour plots in the same time */
.plotting path {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: plot var(--topo-draw, 1.6s) cubic-bezier(0.33, 0.8, 0.4, 1) forwards;
}

@keyframes plot {
  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .plotting path {
    animation: none;
    stroke-dashoffset: 0;
  }
}
</style>
