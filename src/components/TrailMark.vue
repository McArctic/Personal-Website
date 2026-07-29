<script setup>
const shapes = {
  circle: { d: 'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16Z', fill: 'var(--green)' },
  square: { d: 'M5 5h14v14H5Z', fill: 'var(--blue)' },
  diamond: { d: 'M12 3l9 9-9 9-9-9Z', fill: 'var(--diamond)' },
}

const cycle = ['circle', 'square', 'diamond']

const props = defineProps({
  shape: { type: String, default: '' },
  // pass a v-for index to walk the cycle instead of naming a shape
  step: { type: Number, default: 0 },
})

const mark = () => shapes[props.shape] ?? shapes[cycle[props.step % cycle.length]]
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
