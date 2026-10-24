import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'Michael Melichar' } },
  {
    path: '/projects/:slug',
    name: 'project',
    component: () => import('@/views/ProjectView.vue'),
    props: true,
  },

  // the old standalone pages are bands on the home page now
  { path: '/projects', redirect: { path: '/', hash: '#work' } },
  { path: '/experience', redirect: { path: '/', hash: '#experience' } },
  { path: '/extras', redirect: { path: '/', hash: '#ski' } },

  { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to, from, saved) => {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return saved ?? { top: 0 }
  },
})

router.afterEach((to) => {
  const title = to.meta.title
  document.title =
    title && title !== 'Michael Melichar' ? `${title} · Michael Melichar` : 'Michael Melichar'
})

export default router
