export const profile = {
  name: 'Michael Melichar',
  role: 'Flight software & avionics',
  location: 'Buffalo, NY',
  marker: { coords: '42.89°N 78.88°W', elevation: '183 m' },
  lead: 'Computer science student at the University at Buffalo. I do a bit of everything, from embedded systems to general software and personal projects. But if you get me talking, it\'s probably about hardware-level code for space and defense.',
  about: [
    'I write software that runs close to the hardware, most of it aimed at space and defense. At the UB Nanosatellite Laboratory I write flight software for cubesats for defense research, and at UB SEDS I work on our hybrid rocket for IREC. Last competition I handled ground station systems, things like solenoid drivers for filling the nitrous, safety monitoring, and pulling the umbilical before launch. I really just love building things that are physical. I get so much joy from watching something I worked on at a laptop become real.',
    'Space and defense really pull me in for the same reason. Both end in something tangible, and I get to watch what I do contribute to something bigger. I also just love being at the bleeding edge.',
    'I\'ve always loved software and computer science, outside of school I\'ve built more personal projects than I can count, most lost to time by now. Right now I\'m building [a mount that tracks satellites as they pass overhead](/projects/overpass), because trying to follow one by hand in the cold did not go well. Another one of my bigger projects is my [Minecraft server](/projects/create-civilization), which I\'ve been running since 2024 with 680 members and counting, that one\'s been such a journey. Then in the winter I ALWAYS try to find time to ski.',
  ],

  // the two benches the about section is actually describing
  bench: [
    {
      src: '/img/seds/avionics-bay.jpg',
      alt: 'The SEDS hybrid rocket avionics bay opened up, boards and harness visible',
      caption: 'SEDS · hybrid rocket avionics bay',
    },
    {
      src: '/img/ubnl/flight-board.jpg',
      alt: 'A flight computer development board on the bench, cabled up for testing',
      caption: 'UBNL · flight computer on the bench',
    },
  ],

  // the current-conditions board at the bottom of the mountain
  now: {
    note: 'What I\'m actually working on this month.',
    items: [
      'Getting FreeRTOS onto the Pico for [Overpass](/projects/overpass), with both motors moving before anything gets pointed at the sky.',
      'Flight software at UBNL, and ground support firmware for the SEDS hybrid ahead of the next IREC cycle.',
      'Waiting on enough snow to be worth the drive.',
    ],
  },

  ski: {
    note: 'Skiing is the one thing I\'ll rearrange a week for. I film some of it, mostly badly, and put it up along with whatever else I feel like posting.',
    channel: { label: 'YouTube', href: 'https://www.youtube.com/@MichaelRMelichar' },
    shots: [
      {
        src: '/img/ski/run.jpg',
        alt: 'Me skiing down a tree-lined run',
        caption: 'Somewhere worth the drive',
      },
      {
        src: '/img/ski/gear.jpg',
        alt: 'Skis planted in the snow next to a helmet and pack, snow coming down',
        caption: 'Random hill on campus',
      },
    ],
  },

  contact: {
    line: 'I\'m looking for internships in flight software, embedded, and anything that ends in hardware doing something.',
    note: 'Fastest way to reach me is email.',
  },

  links: [
    { label: 'Email', href: 'mailto:michaelrmelichar@gmail.com' },
    { label: 'GitHub', href: 'https://github.com/McArctic' },
    { label: 'LinkedIn', href: 'https://linkedin.com/in/michaelrmelichar' },
    { label: 'YouTube', href: 'https://www.youtube.com/@MichaelRMelichar' },
    { label: 'Resume', href: '/pdf/resume.pdf' },
  ],
}
