<script setup>
import { computed, watchEffect } from 'vue'
import { findProject } from '@/content/projects'

const props = defineProps({ slug: { type: String, required: true } })

const project = computed(() => findProject(props.slug))

watchEffect(() => {
  document.title = project.value
    ? `${project.value.title} · Michael Melichar`
    : 'Not found · Michael Melichar'
})
</script>

<template>
  <div v-if="project" class="wrap">
    <RouterLink to="/projects" class="back kicker">← Projects</RouterLink>

    <header>
      <img v-if="project.logo" :src="project.logo" alt="" />
      <h1>{{ project.title }}</h1>
      <p class="lead">{{ project.summary }}</p>
    </header>

    <dl>
      <div>
        <dt class="kicker">Year</dt>
        <dd>{{ project.year }}</dd>
      </div>
      <div>
        <dt class="kicker">Status</dt>
        <dd>{{ project.status }}</dd>
      </div>
      <div>
        <dt class="kicker">Stack</dt>
        <dd>{{ project.stack.join(', ') }}</dd>
      </div>
      <div v-if="project.repo">
        <dt class="kicker">Source</dt>
        <dd><a :href="project.repo" rel="noopener">Repository</a></dd>
      </div>
    </dl>

    <article class="body" v-html="project.html" />
  </div>

  <div v-else class="wrap missing">
    <h1>No such project</h1>
    <p class="lead">That one isn't here. <RouterLink to="/projects">Back to the list.</RouterLink></p>
  </div>
</template>

<style scoped>
.back {
  display: inline-block;
  padding-block: 2.5rem 0;
  text-decoration: none;
}

.back:hover {
  color: var(--alpine);
}

header {
  padding-block: 1.25rem clamp(1.5rem, 4vw, 2.5rem);
}

header img {
  width: 3.75rem;
  height: 3.75rem;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--line);
  margin-bottom: 1.1rem;
}

h1 {
  font-size: clamp(2rem, 4.5vw, 2.9rem);
  margin-bottom: 0.75rem;
}

/* Spec block: the facts an employer scans for before deciding to read on. */
dl {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  gap: 1.25rem 2rem;
  padding-block: 1.5rem;
  border-block: 1px solid var(--line);
}

dd {
  margin: 0;
  margin-top: 0.3rem;
  font-size: 0.9375rem;
}

.body {
  max-width: var(--measure);
  padding-block: clamp(2rem, 5vw, 3rem);
  color: var(--ink-soft);
}

.body :deep(h2) {
  color: var(--ink);
  font-size: 1.25rem;
  margin-top: 2.5rem;
  margin-bottom: 0.6rem;
}

.body :deep(p + p),
.body :deep(ul) {
  margin-top: 1em;
}

.body :deep(code) {
  font-family: var(--mono);
  font-size: 0.875em;
  background: var(--shade);
  padding: 0.1em 0.35em;
  border-radius: 2px;
}

.body :deep(pre) {
  background: var(--shade);
  padding: 1rem;
  border-radius: 2px;
  overflow-x: auto;
  margin-top: 1em;
}

.body :deep(pre code) {
  background: none;
  padding: 0;
}

.missing {
  padding-block: 6rem;
}
</style>
