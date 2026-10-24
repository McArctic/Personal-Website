<script setup>
import { onBeforeUnmount, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ElevationRail from '@/components/ElevationRail.vue'
import IntroSequence from '@/components/IntroSequence.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/SiteHeader.vue'
import { remeasureDescent, stopDescent, watchDescent } from '@/descent'
import { introPlaying } from '@/intro'

const route = useRoute()

onMounted(watchDescent)
onBeforeUnmount(stopDescent)

// a new route is a different set of bands, so the rail has to be re-read
watch(() => route.fullPath, remeasureDescent)
</script>

<template>
  <IntroSequence v-if="introPlaying" />
  <SiteHeader />
  <ElevationRail />
  <main id="main">
    <RouterView />
  </main>
  <SiteFooter />
</template>

<style>
#app {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
