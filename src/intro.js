import { ref } from 'vue'

/* The opening plot runs once per tab. Coming back from a project page, or
   reloading after a crash, should not make you sit through it again. */

const KEY = 'intro-played'

function played() {
  try {
    return sessionStorage.getItem(KEY) === '1'
  } catch {
    // private mode, blocked storage — just treat it as a first visit
    return false
  }
}

function remember() {
  try {
    sessionStorage.setItem(KEY, '1')
  } catch {
    /* nothing to do, the intro simply plays again next route */
  }
}

const skip = played() || matchMedia('(prefers-reduced-motion: reduce)').matches

export const introPlaying = ref(!skip)
export const introDone = ref(skip)

export function endIntro() {
  if (!introPlaying.value) return
  introPlaying.value = false
  introDone.value = true
  remember()
}
