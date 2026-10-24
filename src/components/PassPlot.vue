<script setup>
/* A polar sky plot: the view looking straight up, horizon at the rim and
   zenith at the centre, with a satellite pass drawn across it. Same thin
   plotted-data language as the contour map, pointed at the sky instead of
   the ground. */

const SIZE = 400
const CENTRE = SIZE / 2
const RADIUS = SIZE / 2 - 34

defineProps({
  // the arc is the point of the graphic, the rings are scaffolding
  label: { type: String, default: '' },
})

const radians = (degrees) => (degrees * Math.PI) / 180

// elevation 90 is overhead, so it collapses to the middle of the plot
function project(azimuth, elevation) {
  const r = RADIUS * (1 - elevation / 90)
  return [
    CENTRE + r * Math.sin(radians(azimuth)),
    CENTRE - r * Math.cos(radians(azimuth)),
  ]
}

const round = (n) => Math.round(n * 10) / 10

function track(fromAzimuth, sweep, peak, steps = 72) {
  const points = []
  for (let i = 0; i <= steps; i++) {
    const t = i / steps
    // azimuth drifts steadily while elevation rises and falls over the pass
    const azimuth = fromAzimuth + sweep * t
    const elevation = peak * Math.sin(Math.PI * t)
    points.push(project(azimuth, elevation))
  }
  return `M ${points.map(([x, y]) => `${round(x)} ${round(y)}`).join(' L ')}`
}

const rings = [0, 30, 60].map((elevation) => ({
  elevation,
  r: round(RADIUS * (1 - elevation / 90)),
}))

const cardinals = [
  { label: 'N', azimuth: 0 },
  { label: 'E', azimuth: 90 },
  { label: 'S', azimuth: 180 },
  { label: 'W', azimuth: 270 },
].map((point) => {
  const [x, y] = project(point.azimuth, -7)
  return { ...point, x: round(x), y: round(y) }
})

const pass = track(196, 189, 71)
const faint = track(285, 142, 34)

// acquisition and loss of signal, the two ends of the usable window
const aos = project(196, 0)
const los = project(385, 0)
const apex = project(196 + 189 / 2, 71)
</script>

<template>
  <svg :viewBox="`0 0 ${SIZE} ${SIZE}`" role="img" :aria-label="label || 'Satellite pass plot'">
    <g class="grid">
      <circle
        v-for="ring in rings"
        :key="ring.elevation"
        :cx="CENTRE"
        :cy="CENTRE"
        :r="ring.r"
        fill="none"
      />
      <line :x1="CENTRE" :y1="CENTRE - RADIUS" :x2="CENTRE" :y2="CENTRE + RADIUS" />
      <line :x1="CENTRE - RADIUS" :y1="CENTRE" :x2="CENTRE + RADIUS" :y2="CENTRE" />
    </g>

    <text
      v-for="point in cardinals"
      :key="point.label"
      class="cardinal"
      :x="point.x"
      :y="point.y"
      text-anchor="middle"
      dominant-baseline="middle"
    >
      {{ point.label }}
    </text>

    <path class="faint" :d="faint" fill="none" />
    <path class="pass" :d="pass" fill="none" />

    <circle class="node" :cx="aos[0]" :cy="aos[1]" r="3.5" />
    <circle class="node" :cx="los[0]" :cy="los[1]" r="3.5" />
    <circle class="apex" :cx="apex[0]" :cy="apex[1]" r="5" />

    <text class="tag" :x="aos[0] + 10" :y="aos[1] - 6">AOS</text>
    <text class="tag" :x="los[0] - 10" :y="los[1] - 6" text-anchor="end">LOS</text>
    <text class="tag apex-tag" :x="apex[0] + 12" :y="apex[1] + 4">71°</text>
  </svg>
</template>

<style scoped>
svg {
  width: 100%;
  height: auto;
}

.grid circle,
.grid line {
  stroke: currentColor;
  stroke-width: 1;
  opacity: 0.22;
  vector-effect: non-scaling-stroke;
}

.cardinal,
.tag {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.1em;
  fill: currentColor;
  opacity: 0.45;
}

.tag {
  font-size: 10px;
}

.apex-tag {
  opacity: 0.8;
  fill: var(--accent);
}

.faint {
  stroke: currentColor;
  stroke-width: 1;
  opacity: 0.18;
  stroke-dasharray: 3 4;
  vector-effect: non-scaling-stroke;
}

.pass {
  stroke: var(--accent);
  stroke-width: 1.75;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;
}

.node {
  fill: var(--bg);
  stroke: var(--accent);
  stroke-width: 1.5;
  vector-effect: non-scaling-stroke;
}

.apex {
  fill: var(--accent);
}
</style>
