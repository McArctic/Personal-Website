<script setup>
import PageHead from '@/components/PageHead.vue'
import TrailMark from '@/components/TrailMark.vue'
import { extras } from '@/content/extras'
</script>

<template>
  <div class="wrap">
    <PageHead title="Extras" note="The part of the resume that doesn't fit on the resume." />

    <ul>
      <li v-for="(item, i) in extras" :key="item.href">
        <a :href="item.href" rel="noopener">
          <span class="kicker"><TrailMark :step="i" />{{ item.label }}</span>
          <span class="title">{{ item.title }}</span>
          <span class="note">{{ item.note }}</span>
          <span class="arrow" aria-hidden="true">↗</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  border-top: 1px solid var(--line);
}

li {
  border-bottom: 1px solid var(--line);
}

a {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 0.25rem 1rem;
  padding-block: 1.75rem;
  text-decoration: none;
}

.kicker {
  grid-column: 1 / -1;
}

.title {
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  transition: color 0.15s;
}

.note {
  grid-column: 1;
  color: var(--ink-soft);
  font-size: 0.9375rem;
  max-width: var(--measure);
}

.arrow {
  grid-row: 2;
  color: var(--ink-faint);
  transition: transform 0.15s, color 0.15s;
}

a:hover .title {
  color: var(--alpine);
}

a:hover .arrow {
  color: var(--alpine);
  transform: translate(2px, -2px);
}
</style>
