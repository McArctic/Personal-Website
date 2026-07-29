<script setup>
import TopoLines from '@/components/TopoLines.vue'

defineProps({
  title: { type: String, required: true },
  note: { type: String, default: '' },
})
</script>

<template>
  <header>
    <TopoLines class="topo" align="xMidYMin" />
    <div class="wrap inner">
      <h1>{{ title }}</h1>
      <p v-if="note" class="lead">{{ note }}</p>
    </div>
  </header>
</template>

<style scoped>
header {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--line);
}

/* fainter than the hero, and the cut lands on the rule below */
.topo {
  --topo-opacity: 0.08;
  position: absolute;
  inset: 0;
}

.inner {
  position: relative;
  padding-block: clamp(3rem, 9vw, 5.5rem) clamp(1.5rem, 4vw, 2.5rem);
}

h1 {
  font-size: clamp(2rem, 4.5vw, 2.9rem);
  margin-bottom: 0.75rem;
}
</style>
