<script setup>
import { onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { contours } from '@/content/killington'

const CURSOR_REACH = 240
const PUSH_DISTANCE = 20

defineProps({ align: { type: String, default: 'xMidYMid' } })

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
  if (!motionAllowed) return
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
    :style="{ '--topo-emphasis': emphasis }"
  >
    <path
      v-for="(path, i) in paths"
      :key="i"
      :d="path"
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
  /* callers set --topo-opacity, not opacity */
  opacity: calc(var(--topo-opacity, 0.13) * var(--topo-emphasis, 1));
  shape-rendering: geometricPrecision;
  pointer-events: none;
}
</style>
