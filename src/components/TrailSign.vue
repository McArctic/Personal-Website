<script setup>
// The three trail markers as signage, not as a rating. They sit at the base of
// every lift in the country and they make no claim about anything here.
const marks = [
  { d: 'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16Z', fill: 'var(--green)' },
  { d: 'M5 5h14v14H5Z', fill: 'var(--blue)' },
  { d: 'M12 3l9 9-9 9-9-9Z', fill: 'var(--diamond)' },
]
</script>

<template>
  <svg viewBox="0 0 80 24" aria-hidden="true" focusable="false">
    <g v-for="(mark, i) in marks" :key="i" :transform="`translate(${i * 28} 0)`">
      <path :d="mark.d" :fill="mark.fill" />
    </g>
  </svg>
</template>

<style scoped>
svg {
  width: 3.6rem;
  height: 1.1rem;
  opacity: 0.75;
}
</style>
