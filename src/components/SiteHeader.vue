<script setup>
const nav = [
  { to: '/experience', label: 'Experience' },
  { to: '/projects', label: 'Projects' },
  { to: '/extras', label: 'Extras' },
]
</script>

<template>
  <header>
    <div class="wrap bar">
      <RouterLink to="/" class="mark">Michael Melichar</RouterLink>
      <nav>
        <RouterLink v-for="item in nav" :key="item.to" :to="item.to">{{ item.label }}</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
header {
  border-bottom: 1px solid var(--line);
  background: var(--snow);
  position: sticky;
  top: 0;
  z-index: 10;
}

.bar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1.5rem;
  padding-block: 1.15rem;
}

.mark {
  font-weight: 600;
  letter-spacing: -0.01em;
  text-decoration: none;
}

nav {
  display: flex;
  gap: clamp(1rem, 3vw, 2rem);
  font-size: 0.9375rem;
  color: var(--ink-soft);
}

nav a {
  position: relative;
  text-decoration: none;
  padding-bottom: 0.55rem;
}

nav a:hover {
  color: var(--ink);
}

nav a.router-link-active {
  color: var(--ink);
}

nav a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 5px;
  height: 5px;
  margin-left: -2.5px;
  background: var(--diamond);
  transform: rotate(45deg);
}
</style>
