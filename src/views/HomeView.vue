<script setup>
import { computed, onMounted } from 'vue'
import ExperienceTimeline from '@/components/ExperienceTimeline.vue'
import ProjectCard from '@/components/ProjectCard.vue'
import ProseText from '@/components/ProseText.vue'
import SkillGroup from '@/components/SkillGroup.vue'
import TopoLines from '@/components/TopoLines.vue'
import { profile } from '@/content/profile'
import { projects } from '@/content/projects'
import { skills } from '@/content/skills'
import { goToStation, remeasureDescent } from '@/descent'
import { introDone } from '@/intro'

const hasShots = computed(() => profile.ski.shots.length > 0)

// landing straight on /#work from a write-up has to put you there
onMounted(() => {
  // these bands are what the header and the rail read
  remeasureDescent()

  const id = location.hash.slice(1)
  if (id) requestAnimationFrame(() => goToStation(id))
})
</script>

<template>
  <!-- summit ---------------------------------------------------------- -->
  <section id="summit" class="band dark hero" data-zone="dark" data-station="Summit">
    <TopoLines class="topo" align="xMidYMax" />

    <div class="wrap inner" :class="{ ready: introDone }">
      <h1>
        Michael<br />
        Melichar<span class="stop">.</span>
      </h1>

      <p class="lead">{{ profile.lead }}</p>

      <div class="cta">
        <a class="button primary" href="#work" @click.prevent="goToStation('work')"
          >View work</a
        >
        <a class="button" href="#contact" @click.prevent="goToStation('contact')"
          >Get in touch</a
        >
      </div>
    </div>

    <p class="kicker descend" :class="{ ready: introDone }" aria-hidden="true">
      Scroll for more
      <span class="drop" />
    </p>
  </section>

  <!-- about ----------------------------------------------------------- -->
  <section id="about" class="band dark" data-zone="dark" data-station="About">
    <div class="wrap">
      <header v-rise class="band-head">
        <h2>About.</h2>
      </header>

      <div class="about-grid">
        <div v-rise class="prose">
          <ProseText v-for="(para, i) in profile.about" :key="i" :text="para" />
        </div>

        <ul v-rise="1" class="bench">
          <li v-for="shot in profile.bench" :key="shot.src">
            <img :src="shot.src" :alt="shot.alt" loading="lazy" decoding="async" />
            <p class="kicker">{{ shot.caption }}</p>
          </li>
        </ul>
      </div>

      <div v-rise class="columns">
        <SkillGroup v-for="group in skills" :key="group.heading" v-bind="group" />
      </div>
    </div>
  </section>

  <!-- work ------------------------------------------------------------ -->
  <section id="work" class="band" data-zone="light" data-station="Projects">
    <p class="treeline" aria-hidden="true">
      <span>Treeline</span>
      <span class="hair" />
      <span>1067 m</span>
    </p>

    <div class="wrap">
      <header v-rise class="band-head">
        <h2>Projects.</h2>
      </header>

      <div class="cards">
        <ProjectCard
          v-for="(project, i) in projects"
          :key="project.slug"
          v-rise="i % 2"
          :project="project"
        />
      </div>
    </div>
  </section>

  <!-- experience ------------------------------------------------------- -->
  <section id="experience" class="band shaded" data-zone="light" data-station="Experience">
    <div class="wrap">
      <header v-rise class="band-head">
        <h2>Experience.</h2>
      </header>

      <div v-rise>
        <ExperienceTimeline />
      </div>
    </div>
  </section>

  <!-- now -------------------------------------------------------------- -->
  <section id="now" class="band" data-zone="light" data-station="Working on">
    <div class="wrap">
      <div class="now-grid">
        <header v-rise class="band-head">
          <h2>What I am working on.</h2>
          <p class="note">{{ profile.now.note }}</p>
        </header>

        <ul v-rise="1" class="now-list">
          <li v-for="(item, i) in profile.now.items" :key="i">
            <ProseText :text="item" />
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- off the clock ----------------------------------------------------- -->
  <section id="ski" class="band shaded" data-zone="light" data-station="Personal">
    <div class="wrap">
      <header v-rise class="band-head">
        <h2>Personal.</h2>
      </header>

      <div class="ski-grid">
        <div v-rise>
          <p class="prose">{{ profile.ski.note }}</p>
          <a class="button ski-link" :href="profile.ski.channel.href" rel="noopener">
            {{ profile.ski.channel.label }} <span aria-hidden="true">↗</span>
          </a>
        </div>

        <ul v-rise="1" class="shots" :class="{ empty: !hasShots }">
          <li v-for="shot in profile.ski.shots" :key="shot.src">
            <img :src="shot.src" :alt="shot.alt ?? ''" loading="lazy" decoding="async" />
            <p v-if="shot.caption" class="kicker">{{ shot.caption }}</p>
          </li>
          <li v-if="!hasShots" class="placeholder">
            <TopoLines align="xMidYMid" :interactive="false" />
            <p class="kicker">Photos going here</p>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- base ------------------------------------------------------------- -->
  <section id="contact" class="band dark base" data-zone="dark" data-station="Contact">
    <TopoLines class="topo" align="xMidYMin" />

    <div class="wrap">
      <header v-rise class="band-head">
        <h2>Contact.</h2>
      </header>

      <div v-rise="1" class="base-grid">
        <p class="lead">{{ profile.contact.line }}</p>

        <ul class="channels">
          <li v-for="link in profile.links" :key="link.href">
            <a :href="link.href" rel="me noopener">
              {{ link.label }}<span class="arrow" aria-hidden="true">↗</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* hero -------------------------------------------------------------- */

.hero {
  display: grid;
  align-content: center;
  overflow: hidden;
  min-height: min(100svh, 56rem);
  padding-block: clamp(6rem, 16vh, 9rem) clamp(5rem, 12vh, 7rem);
}

.topo {
  position: absolute;
  inset: 0;
}

/* the intro hands over, and only then does the hero come up */
.inner > * {
  opacity: 0;
  transform: translateY(1.4rem);
}

.inner.ready > * {
  opacity: 1;
  transform: none;
  transition: opacity 0.75s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.75s cubic-bezier(0.22, 1, 0.36, 1);
}

.inner.ready > :nth-child(2) {
  transition-delay: 0.08s;
}
.inner.ready > :nth-child(3) {
  transition-delay: 0.16s;
}
h1 {
  font-size: clamp(2.9rem, 10vw, 6.5rem);
  letter-spacing: -0.045em;
  margin-bottom: 1.75rem;
}

.stop {
  color: var(--accent);
}

.cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2.25rem;
}

.descend {
  position: absolute;
  bottom: clamp(1.5rem, 4vh, 2.5rem);
  left: 50%;
  translate: -50% 0;
  display: grid;
  justify-items: center;
  gap: 0.75rem;
  opacity: 0;
  transition: opacity 0.6s 0.5s;
}

.descend.ready {
  opacity: 1;
}

.drop {
  width: 1px;
  height: 2.25rem;
  background: linear-gradient(var(--summit-faint), transparent);
}

/* buttons ------------------------------------------------------------ */

.button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.1rem;
  border: 1px solid var(--rule);
  border-radius: 2px;
  font-size: 0.9375rem;
  text-decoration: none;
  color: var(--fg);
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.button:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.button.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--summit);
}

.button.primary:hover {
  background: transparent;
  color: var(--accent);
}

/* about -------------------------------------------------------------- */

.about-grid {
  display: grid;
  gap: clamp(2.5rem, 6vw, 4.5rem);
}

@media (min-width: 60rem) {
  .about-grid {
    grid-template-columns: minmax(0, 1fr) minmax(0, 0.8fr);
  }
}

/* the hardware the words are actually about */
.bench {
  display: grid;
  gap: 1.25rem;
  align-content: start;
}

@media (min-width: 34rem) and (max-width: 59.99rem) {
  .bench {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.bench img {
  width: 100%;
  object-fit: cover;
  border: 1px solid var(--rule);
  border-radius: 2px;
  background: var(--bg-raise);
}

.bench li:first-child img {
  aspect-ratio: 4 / 5;
}

.bench li:last-child img {
  aspect-ratio: 4 / 3;
}

.bench .kicker {
  margin-top: 0.6rem;
}

.columns {
  display: grid;
  gap: 2rem;
  align-content: start;
  margin-top: clamp(3rem, 7vw, 5rem);
  padding-top: clamp(2rem, 4vw, 3rem);
  border-top: 1px solid var(--rule);
}

@media (min-width: 34rem) {
  .columns {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 2.5rem;
  }
}

/* work --------------------------------------------------------------- */

/* the seam where the dark band meets the light one */
.treeline {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem var(--gutter) 0;
  font-family: var(--mono);
  font-size: 0.625rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

.treeline .hair {
  flex: 1;
  height: 1px;
  background: var(--line);
}

.cards {
  display: grid;
  gap: clamp(2.5rem, 5vw, 3.5rem) 2.5rem;
}

@media (min-width: 52rem) {
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.shaded {
  background: var(--shade);
}

/* now ---------------------------------------------------------------- */

.now-grid {
  display: grid;
  gap: clamp(1.5rem, 4vw, 3rem);
}

@media (min-width: 60rem) {
  .now-grid {
    grid-template-columns: minmax(0, 0.8fr) minmax(0, 1fr);
  }

  .now-grid .band-head {
    margin-bottom: 0;
  }
}

.note {
  color: var(--fg-faint);
  font-size: 0.9375rem;
  margin-top: 0.9rem;
}

.now-list {
  display: grid;
  gap: 1.1rem;
  align-content: start;
  max-width: var(--measure);
}

.now-list li {
  padding-bottom: 1.1rem;
  border-bottom: 1px solid var(--rule);
  color: var(--fg-body);
}

.now-list li:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

/* off the clock -------------------------------------------------------- */

.ski-grid {
  display: grid;
  gap: clamp(2rem, 5vw, 3.5rem);
  align-items: start;
}

@media (min-width: 60rem) {
  .ski-grid {
    grid-template-columns: minmax(0, 0.75fr) minmax(0, 1fr);
  }
}

.ski-link {
  margin-top: 1.75rem;
}

.shots {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
}

.shots img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border: 1px solid var(--rule);
  border-radius: 2px;
}

.shots .kicker {
  margin-top: 0.5rem;
}

/* holds the shape of the row until there are real photos to put in it */
.placeholder {
  position: relative;
  display: grid;
  place-items: center;
  aspect-ratio: 16 / 9;
  border: 1px dashed var(--rule);
  border-radius: 2px;
  overflow: hidden;
  color: var(--fg-faint);
}

.placeholder :deep(svg) {
  position: absolute;
  inset: 0;
  --topo-opacity: 0.18;
}

.placeholder .kicker {
  position: relative;
  margin: 0;
}

/* base ---------------------------------------------------------------- */

.base {
  overflow: hidden;
}

.base-grid {
  display: grid;
  gap: 2.5rem;
  align-items: start;
}

@media (min-width: 60rem) {
  .base-grid {
    grid-template-columns: minmax(0, 1fr) auto;
  }
}

.channels {
  display: grid;
  gap: 0.6rem;
  font-size: 1.0625rem;
}

@media (min-width: 60rem) {
  .channels {
    justify-items: end;
  }
}

.channels a {
  text-decoration: none;
  color: var(--fg-soft);
  transition: color 0.2s;
}

.channels a:hover {
  color: var(--accent);
}

.arrow {
  display: inline-block;
  margin-left: 0.45rem;
  font-size: 0.8em;
  color: var(--fg-faint);
  transition: translate 0.2s;
}

.channels a:hover .arrow {
  translate: 2px -2px;
}

@media (prefers-reduced-motion: reduce) {
  .inner.ready > *,
  .descend,
  .button,
  .channels a,
  .arrow {
    transition: none;
  }
}
</style>
