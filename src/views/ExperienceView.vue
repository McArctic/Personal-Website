<script setup>
import PageHead from '@/components/PageHead.vue'
import TrailMark from '@/components/TrailMark.vue'
import { experience, education } from '@/content/experience'

const blocks = [
  { label: 'Work', entries: experience },
  { label: 'Education', entries: education },
]
</script>

<template>
  <div class="wrap">
    <PageHead title="Experience" note="Where I've worked and what I owned there." />

    <section v-for="(block, i) in blocks" :key="block.label">
      <p class="kicker label"><TrailMark :step="i" />{{ block.label }}</p>
      <ol>
        <li v-for="entry in block.entries" :key="entry.org + entry.period">
          <div class="side">
            <img v-if="entry.logo" :src="entry.logo" alt="" />
            <p class="kicker">{{ entry.period }}</p>
          </div>
          <div>
            <h3>{{ entry.role }}</h3>
            <p class="org">{{ entry.org }} <span>· {{ entry.place }}</span></p>
            <ul v-if="entry.notes.length">
              <li v-for="note in entry.notes" :key="note">{{ note }}</li>
            </ul>
          </div>
        </li>
      </ol>
    </section>
  </div>
</template>

<style scoped>
section {
  padding-block: clamp(2rem, 5vw, 3rem);
  border-top: 1px solid var(--line);
}

.label {
  margin-bottom: 1.75rem;
}

ol > li {
  display: grid;
  gap: 0.9rem 2.5rem;
  padding-block: 2rem;
  border-top: 1px solid var(--line);
}

ol > li:first-child {
  border-top: 0;
  padding-top: 0;
}

@media (min-width: 40rem) {
  ol > li {
    grid-template-columns: 8.5rem minmax(0, 1fr);
  }
}

.side {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.8rem;
}

/* The source logos are all different shapes on different backgrounds, so they are
   pre-normalized to square tiles (see the note in the README) and the circle here
   just crops them. The hairline ring is what keeps the light ones from floating. */
.side img {
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--line);
}

h3 {
  margin-top: -0.15rem;
}

.org {
  color: var(--ink-soft);
  margin-bottom: 0.7rem;
}

.org span {
  color: var(--ink-faint);
}

ul {
  max-width: var(--measure);
  color: var(--ink-soft);
}

/* A hairline dash instead of a bullet. Quieter, and it lines up. */
ul li {
  position: relative;
  padding-left: 1.1rem;
}

ul li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.8em;
  width: 0.6rem;
  border-top: 1px solid var(--ink-faint);
}
</style>
