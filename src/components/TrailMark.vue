<script setup>
/* Trail difficulty, used as a real rating on a project rather than as a
   bullet: green circle, blue square, black diamond. */

const shapes = {
  circle: { d: 'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16Z', fill: 'var(--green)' },
  square: { d: 'M5 5h14v14H5Z', fill: 'var(--blue)' },
  diamond: { d: 'M12 3l9 9-9 9-9-9Z', fill: 'var(--diamond)' },
}

const props = defineProps({
  shape: { type: String, default: 'circle' },
})

const mark = () => shapes[props.shape] ?? shapes.circle
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
