<script setup>
import TopoLines from '@/components/TopoLines.vue'
import SkillGroup from '@/components/SkillGroup.vue'
import TrailMark from '@/components/TrailMark.vue'
import { profile } from '@/content/profile'
import { skills } from '@/content/skills'
</script>

<template>
  <div class="hero">
    <TopoLines class="topo" />
    <div class="wrap inner">
      <p class="kicker">{{ profile.role }} · {{ profile.location }}</p>
      <h1>{{ profile.name }}</h1>
      <p class="lead">{{ profile.lead }}</p>
      <ul class="links">
        <li v-for="link in profile.links" :key="link.href">
          <a :href="link.href">{{ link.label }}</a>
        </li>
      </ul>
    </div>
  </div>

  <div class="wrap">
    <section>
      <div class="spine">
        <p class="kicker"><TrailMark shape="circle" />About</p>
        <div class="prose">
          <p v-for="(para, i) in profile.about" :key="i">{{ para }}</p>
        </div>
      </div>
    </section>

    <section>
      <div class="spine">
        <p class="kicker"><TrailMark shape="square" />Skills</p>
        <div class="groups">
          <SkillGroup v-for="group in skills" :key="group.heading" v-bind="group" />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--line);
}

/* fills the hero, so the lines only ever get cut by its borders */
.topo {
  position: absolute;
  inset: 0;
}

.inner {
  position: relative;
  padding-block: clamp(4rem, 14vw, 8.5rem) clamp(3rem, 8vw, 5rem);
}

h1 {
  margin-block: 0.6rem 1.25rem;
}

.links {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 2rem;
  font-size: 0.9375rem;
}

.groups {
  display: grid;
  gap: 2rem;
}
</style>
