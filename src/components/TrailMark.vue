<script setup>
// A single trail marker, sized to sit inline with the mono kickers. Shape and
// colour are paired the way real signage pairs them, so the marker reads as a
// waypoint down the page rather than a rating of anything.
const shapes = {
  circle: { d: 'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16Z', fill: 'var(--green)' },
  square: { d: 'M5 5h14v14H5Z', fill: 'var(--blue)' },
  diamond: { d: 'M12 3l9 9-9 9-9-9Z', fill: 'var(--diamond)' },
}

const order = ['circle', 'square', 'diamond']

const props = defineProps({
  shape: { type: String, default: '' },
  // Convenience for v-for: pass the loop index and get the next marker along.
  step: { type: Number, default: 0 },
})

const mark = () => shapes[props.shape] ?? shapes[order[props.step % order.length]]
</script>

<template>
  <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path :d="mark().d" :fill="mark().fill" />
  </svg>
</template>

<style scoped>
svg {
  display: inline-block;
  width: 0.62em;
  height: 0.62em;
  margin-right: 0.62em;
  vertical-align: baseline;
}
</style>
