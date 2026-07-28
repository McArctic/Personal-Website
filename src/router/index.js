import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'Michael Melichar' } },
  {
    path: '/experience',
    name: 'experience',
    component: () => import('@/views/ExperienceView.vue'),
    meta: { title: 'Experience' },
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/ProjectsView.vue'),
    meta: { title: 'Projects' },
  },
  {
    path: '/projects/:slug',
    name: 'project',
    component: () => import('@/views/ProjectView.vue'),
    props: true,
  },
  {
    path: '/extras',
    name: 'extras',
    component: () => import('@/views/ExtrasView.vue'),
    meta: { title: 'Extras' },
  },
  { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to, from, saved) => saved ?? { top: 0 },
})

router.afterEach((to) => {
  const title = to.meta.title
  document.title = title && title !== 'Michael Melichar' ? `${title} · Michael Melichar` : 'Michael Melichar'
})

export default router
