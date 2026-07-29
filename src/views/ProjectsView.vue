<script setup>
import PageHead from '@/components/PageHead.vue'
import { projects } from '@/content/projects'
</script>

<template>
  <PageHead title="Projects" note="Longer write-ups on the things worth explaining." />

  <div class="wrap">
    <ol>
      <li v-for="project in projects" :key="project.slug">
        <RouterLink :to="`/projects/${project.slug}`">
          <p class="meta kicker">{{ project.year }}</p>
          <div>
            <h2>{{ project.title }}</h2>
            <p class="summary">{{ project.summary }}</p>
            <p class="stack kicker">{{ project.stack.join(' · ') }}</p>
          </div>
        </RouterLink>
      </li>
    </ol>
  </div>
</template>

<style scoped>
li {
  border-bottom: 1px solid var(--line);
}

a {
  display: grid;
  gap: 0.5rem 2rem;
  padding-block: 2rem;
  text-decoration: none;
}

@media (min-width: 40rem) {
  a {
    grid-template-columns: 8rem minmax(0, 1fr);
  }
}

.meta {
  padding-top: 0.5rem;
}

h2 {
  font-size: 1.4rem;
  transition: color 0.15s;
}

a:hover h2 {
  color: var(--alpine);
}

.summary {
  color: var(--ink-soft);
  max-width: var(--measure);
  margin-block: 0.4rem 0.75rem;
}

.stack {
  font-size: 0.6875rem;
}
</style>
