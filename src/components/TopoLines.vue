<script setup>
import { onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { contours } from '@/content/killington'

// Real contour lines of Killington Peak, Vermont, from the USGS 10 m elevation
// dataset. See src/content/killington.js for the source and how it was derived.
// The cursor pushes the terrain out near where it is and leaves the rest alone.
const REACH = 240 // how far the cursor's influence carries, in viewBox units
const LIFT = 20 // how far the nearest stretch of contour is pushed

// Which part of the mountain to frame. The svg fills its container and crops with
// `slice`, so lines only ever get cut at the container's own border, never mid-air.
defineProps({ align: { type: String, default: 'xMidYMid' } })

// 'M x y L x y L ...' into points, once, at module load.
const lines = contours.map((c) =>
  c.d
    .slice(2)
    .split(' L ')
    .map((pair) => pair.split(' ').map(Number)),
)

const round = (n) => Math.round(n * 10) / 10

// Catmull-Rom through the sampled points, as cubic Béziers. The contours are
// simplified polylines, so this is what keeps them reading as terrain rather
// than as a chain of straight segments.
function toPath(pts) {
  const n = pts.length
  if (n < 3) return `M ${pts.map((p) => `${round(p[0])} ${round(p[1])}`).join(' L ')}`
  let d = `M ${round(pts[0][0])} ${round(pts[0][1])}`
  for (let i = 0; i < n - 1; i++) {
    const [x0, y0] = pts[i === 0 ? 0 : i - 1]
    const [x1, y1] = pts[i]
    const [x2, y2] = pts[i + 1]
    const [x3, y3] = pts[Math.min(i + 2, n - 1)]
    d +=
      ` C ${round(x1 + (x2 - x0) / 6)} ${round(y1 + (y2 - y0) / 6)},` +
      ` ${round(x2 - (x3 - x1) / 6)} ${round(y2 - (y3 - y1) / 6)},` +
      ` ${round(x2)} ${round(y2)}`
  }
  return d
}

const REST = lines.map(toPath)

function build(mx, my, strength) {
  if (strength <= 0.001) return REST
  return lines.map((pts) =>
    toPath(
      pts.map(([x, y]) => {
        const dx = x - mx
        const dy = y - my
        const d2 = dx * dx + dy * dy
        // Gaussian falloff: only the stretch of contour near the cursor moves.
        const push = LIFT * strength * Math.exp(-d2 / (REACH * REACH))
        if (push < 0.05) return [x, y]
        const dist = Math.sqrt(d2) || 1
        return [x + (dx / dist) * push, y + (dy / dist) * push]
      }),
    ),
  )
}

const svg = shallowRef(null)
const paths = ref(REST)
const emphasis = ref(1)

const still = !matchMedia('(prefers-reduced-motion: reduce)').matches
const target = { x: 640, y: 450, s: 0 }
const eased = { x: 640, y: 450, s: 0 }
let frame = 0

function tick() {
  // Trail the pointer instead of snapping to it, so the terrain settles rather
  // than twitches.
  eased.x += (target.x - eased.x) * 0.16
  eased.y += (target.y - eased.y) * 0.16
  eased.s += (target.s - eased.s) * 0.09

  paths.value = build(eased.x, eased.y, eased.s)
  emphasis.value = 1 + eased.s * 0.9

  // Once the pointer is gone and the terrain has all but flattened, snap to rest
  // and park the loop rather than easing forever against a rounding error.
  if (target.s === 0 && eased.s < 0.002) {
    eased.s = 0
    paths.value = REST
    emphasis.value = 1
    frame = 0
    return
  }
  frame = requestAnimationFrame(tick)
}

function run() {
  if (!frame) frame = requestAnimationFrame(tick)
}

function onMove(e) {
  // Going through the screen matrix rather than the bounding box, so the viewBox
  // scale and any CSS transform on the svg (the footer copy is flipped) are both
  // accounted for. Otherwise the bulge lands mirrored against the cursor.
  const ctm = svg.value.getScreenCTM()
  if (!ctm) return
  const local = new DOMPoint(e.clientX, e.clientY).matrixTransform(ctm.inverse())
  target.x = local.x
  target.y = local.y
  target.s = 1
  run()
}

function onLeave() {
  target.s = 0
  run()
}

let host = null

onMounted(() => {
  if (!still) return
  // Listening on the containing section, not the svg, so the contours never take
  // the mouse away from the text and links sitting over them.
  host = svg.value.parentElement
  host.addEventListener('pointermove', onMove)
  host.addEventListener('pointerleave', onLeave)
})

onBeforeUnmount(() => {
  if (frame) cancelAnimationFrame(frame)
  host?.removeEventListener('pointermove', onMove)
  host?.removeEventListener('pointerleave', onLeave)
})
</script>

<template>
  <svg
    ref="svg"
    viewBox="0 0 1280 900"
    :preserveAspectRatio="`${align} slice`"
    aria-hidden="true"
    focusable="false"
    :style="{ '--topo-emphasis': emphasis }"
  >
    <path
      v-for="(d, i) in paths"
      :key="i"
      :d="d"
      fill="none"
      stroke="currentColor"
      stroke-width="1"
      stroke-linecap="round"
      vector-effect="non-scaling-stroke"
    />
  </svg>
</template>

<style scoped>
svg {
  display: block;
  width: 100%;
  height: 100%;
  color: var(--alpine);
  /* Callers tune --topo-opacity; --topo-emphasis is driven by the cursor above. */
  opacity: calc(var(--topo-opacity, 0.13) * var(--topo-emphasis, 1));
  shape-rendering: geometricPrecision;
  pointer-events: none;
}
</style>
