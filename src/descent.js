import { ref } from 'vue'

/* One scroll listener for the whole site. The header and the elevation rail
   both need to know how far down the mountain you are and which band is
   behind them, and two independent listeners would just fight each other.

   Any element can take part:
     data-zone="dark|light"   what sits behind the fixed furniture here
     data-station="Label"     a junction worth marking on the rail         */

export const progress = ref(0)
export const stations = ref([])
export const activeStation = ref(0)
export const headerZone = ref('light')
export const railZone = ref('light')
export const scrolled = ref(false)

const HEADER_DEPTH = 72

let frame = 0
let started = 0
let zoned = []
let marked = []
let observer

function measure() {
  zoned = [...document.querySelectorAll('[data-zone]')]
  marked = [...document.querySelectorAll('[data-station]')]

  const span = Math.max(document.body.scrollHeight - innerHeight, 1)
  stations.value = marked.map((el) => ({
    label: el.dataset.station,
    id: el.id,
    // where this junction lands on the rail, as a fraction of the scroll
    at: Math.min(Math.max((el.offsetTop - innerHeight * 0.3) / span, 0), 1),
  }))
}

const zoneAt = (y) => zoned.findLast((el) => el.offsetTop <= y)?.dataset.zone ?? 'light'

function read() {
  frame = 0
  const span = Math.max(document.body.scrollHeight - innerHeight, 1)
  progress.value = Math.min(Math.max(scrollY / span, 0), 1)

  scrolled.value = scrollY > 24
  headerZone.value = zoneAt(scrollY + HEADER_DEPTH)
  railZone.value = zoneAt(scrollY + innerHeight / 2)

  const middle = scrollY + innerHeight * 0.35
  let index = 0
  marked.forEach((el, i) => {
    if (el.offsetTop <= middle) index = i
  })
  activeStation.value = index
}

function onScroll() {
  if (!frame) frame = requestAnimationFrame(read)
}

// sections grow as fonts and images land, so remeasure instead of trusting
// whatever the first paint happened to report
export function watchDescent() {
  if (started++) return
  measure()
  read()
  addEventListener('scroll', onScroll, { passive: true })
  addEventListener('resize', () => {
    measure()
    read()
  })
  observer = new ResizeObserver(() => {
    measure()
    read()
  })
  observer.observe(document.body)
}

// routes come and go, so the page has to be able to say "the bands changed"
export function remeasureDescent() {
  if (!started) return
  requestAnimationFrame(() => {
    measure()
    read()
  })
}

/* Vue Router owns history and scroll restoration here, which leaves plain
   fragment links on the home page doing nothing, so the jump is done by
   hand and the hash is only written afterwards, for sharing. */
export function goToStation(id) {
  const el = document.getElementById(id)
  if (!el) return false
  const smooth = !matchMedia('(prefers-reduced-motion: reduce)').matches
  el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' })
  history.replaceState(history.state, '', `#${id}`)
  return true
}

export function stopDescent() {
  if (--started > 0) return
  cancelAnimationFrame(frame)
  removeEventListener('scroll', onScroll)
  observer?.disconnect()
}
