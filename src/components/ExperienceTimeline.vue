<script setup>
import { education, experience } from '@/content/experience'

// work first, then school, on one rail — it reads as one history
const entries = [...experience, ...education]
</script>

<template>
  <ol class="timeline">
    <li v-for="entry in entries" :key="entry.org + entry.period">
      <div class="when">
        <span class="node" aria-hidden="true" />
        <p class="kicker">{{ entry.period }}</p>
        <img v-if="entry.logo" :src="entry.logo" alt="" loading="lazy" />
      </div>

      <div class="what">
        <p v-if="entry.kicker" class="kicker role-kicker">{{ entry.kicker }}</p>
        <h3>{{ entry.role }}</h3>
        <p class="org">{{ entry.org }} <span>· {{ entry.place }}</span></p>

        <ul v-if="entry.notes.length" class="notes">
          <li v-for="note in entry.notes" :key="note">{{ note }}</li>
        </ul>

        <p v-if="entry.restricted" class="restricted">
          <span aria-hidden="true">●</span> {{ entry.restricted }}
        </p>

        <ul v-if="entry.tags.length" class="tags">
          <li v-for="tag in entry.tags" :key="tag">{{ tag }}</li>
        </ul>
      </div>
    </li>
  </ol>
</template>

<style scoped>
.timeline > li {
  display: grid;
  gap: 1rem 2.5rem;
  padding-block: 2.25rem;
  border-top: 1px solid var(--rule);
}

.timeline > li:first-child {
  border-top: 0;
  padding-top: 0;
}

@media (min-width: 46rem) {
  .timeline > li {
    grid-template-columns: 10rem minmax(0, 1fr);
  }
}

.when {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.9rem;
}

/* the junction dot, same diamond the rail and the nav use */
.node {
  position: absolute;
  top: 0.55rem;
  left: -1.35rem;
  width: 5px;
  height: 5px;
  rotate: 45deg;
  background: var(--accent);
}

@media (max-width: 45.99rem) {
  .node {
    display: none;
  }
}

.when img {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--rule);
  background: var(--bg-raise);
}

.role-kicker {
  color: var(--accent);
  margin-bottom: 0.5rem;
}

h3 {
  font-size: 1.375rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.org {
  color: var(--fg-soft);
  font-size: 0.9375rem;
  margin-bottom: 0.9rem;
}

.org span {
  color: var(--fg-faint);
}

.notes {
  max-width: var(--measure);
  color: var(--fg-body);
  font-size: 0.9875rem;
  display: grid;
  gap: 0.5rem;
}

/* hairline dash instead of a bullet */
.notes li {
  position: relative;
  padding-left: 1.1rem;
}

.notes li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.78em;
  width: 0.6rem;
  border-top: 1px solid var(--fg-faint);
}

.restricted {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.9rem;
  font-family: var(--mono);
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--fg-faint);
}

.restricted span {
  color: var(--accent);
  font-size: 0.7em;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 1.1rem;
}

.tags li {
  padding: 0.25rem 0.55rem;
  border: 1px solid var(--rule);
  border-radius: 2px;
  font-family: var(--mono);
  font-size: 0.6875rem;
  color: var(--fg-faint);
}
</style>
