<script setup>
import PageHead from '@/components/PageHead.vue'
import TrailMark from '@/components/TrailMark.vue'
import { extras } from '@/content/extras'
</script>

<template>
  <PageHead title="Extras" note="The part of the resume that doesn't fit on the resume." />

  <div class="wrap">
    <ul>
      <li v-for="(item, i) in extras" :key="item.href">
        <a :href="item.href" rel="noopener">
          <span class="kicker"><TrailMark :step="i" />{{ item.label }}</span>
          <span class="title">{{ item.title }}<span class="arrow" aria-hidden="true">↗</span></span>
          <span class="note">{{ item.note }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
li {
  border-bottom: 1px solid var(--line);
}

a {
  display: grid;
  gap: 0.25rem;
  padding-block: 1.75rem;
  text-decoration: none;
}

.title {
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  transition: color 0.15s;
}

.note {
  color: var(--ink-soft);
  font-size: 0.9375rem;
  max-width: var(--measure);
}

.arrow {
  display: inline-block;
  margin-left: 0.4rem;
  color: var(--ink-faint);
  font-size: 0.875em;
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
