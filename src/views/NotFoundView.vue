<script setup>
import TrailSign from '@/components/TrailSign.vue'
</script>

<template>
  <div class="wrap">
    <TrailSign />
    <p class="kicker">404</p>
    <h1>Off-piste</h1>
    <p class="lead">Nothing here. <RouterLink to="/">Head back to the base.</RouterLink></p>
  </div>
</template>

<style scoped>
div {
  padding-block: clamp(5rem, 14vw, 9rem);
}

.kicker {
  margin-top: 1.5rem;
}

h1 {
  margin-block: 0.6rem 1rem;
}
</style>
