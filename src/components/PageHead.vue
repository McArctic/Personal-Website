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
    <h1>{{ title }}</h1>
    <p v-if="note" class="lead">{{ note }}</p>
  </header>
</template>

<style scoped>
header {
  position: relative;
  overflow: hidden;
  padding-block: clamp(3rem, 9vw, 5.5rem) clamp(1.5rem, 4vw, 2.5rem);
}

/* Fainter than the hero; these pages are read, not landed on. Fills the header so
   the cut lands on the rule below it. */
.topo {
  --topo-opacity: 0.08;
  position: absolute;
  inset: 0;
}

h1,
.lead {
  position: relative;
}

h1 {
  font-size: clamp(2rem, 4.5vw, 2.9rem);
  margin-bottom: 0.75rem;
}
</style>
