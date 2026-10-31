<script setup>
defineProps({
  heading: { type: String, required: true },
  items: { type: Array, required: true },
})
</script>

<template>
  <div class="group">
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
