<script setup>
defineProps({
  heading: { type: String, required: true },
  items: { type: Array, required: true },
  step: { type: Number, default: 0 },
})

const pad = (n) => String(n).padStart(2, '0')
</script>

<template>
  <div class="group">
    <p class="kicker">/ {{ pad(step + 1) }}</p>
    <h3>{{ heading }}</h3>
    <ul>
      <li v-for="item in items" :key="item">{{ item }}</li>
    </ul>
  </div>
</template>

<style scoped>
.group {
  padding-top: 1.25rem;
  border-top: 1px solid var(--rule);
}

.kicker {
  color: var(--accent);
  margin-bottom: 0.9rem;
}

h3 {
  font-size: 1.125rem;
  margin-bottom: 1rem;
  color: var(--fg);
}

ul {
  display: grid;
  gap: 0.45rem;
  font-size: 0.9375rem;
  color: var(--fg-soft);
}
</style>
