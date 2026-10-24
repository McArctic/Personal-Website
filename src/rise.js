/* v-rise — fade a block up the first time it comes into view.

   v-rise          default timing
   v-rise="2"      hold back two steps, for staggering a row of cards    */

const STEP = 90

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches

let observer

function watcher() {
  observer ??= new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('shown')
        // one-shot, nothing fades back out on the way up
        observer.unobserve(entry.target)
      })
    },
    { rootMargin: '0px 0px -8% 0px' },
  )
  return observer
}

export const rise = {
  mounted(el, binding) {
    el.classList.add('rise')
    if (reduced) {
      el.classList.add('shown')
      return
    }
    const step = Number(binding.value) || 0
    if (step) el.style.transitionDelay = `${step * STEP}ms`
    watcher().observe(el)
  },

  unmounted(el) {
    observer?.unobserve(el)
  },
}
