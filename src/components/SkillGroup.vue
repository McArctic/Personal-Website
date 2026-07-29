<script setup>
defineProps({
  heading: { type: String, required: true },
  items: { type: Array, required: true },
})
</script>

<template>
  <div>
    <h3>{{ heading }}</h3>
    <ul>
      <li v-for="item in items" :key="item.name" :class="{ bare: !item.icon }">
        <svg v-if="item.icon" viewBox="0 0 24 24" aria-hidden="true">
          <path :d="item.icon.path" />
        </svg>
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
h3 {
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 400;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 1rem;
}

ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.75rem 0.4rem 0.6rem;
  border: 1px solid var(--line);
  border-radius: 2px;
  font-size: 0.875rem;
  background: var(--snow);
}

/* no logo, so even the padding back out */
.bare {
  padding-left: 0.75rem;
}

svg {
  width: 1rem;
  height: 1rem;
  fill: var(--ink-soft);
}
</style>
