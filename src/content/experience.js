export const experience = [
  {
    org: 'Linde',
    logo: '/logos/linde.png',
    place: 'Buffalo, NY',
    role: 'Software Engineering Intern',
    period: 'May to Aug 2026',
    notes: [
      'Built a customer-facing web app in C# and Blazor showing live and historical readings from cryogenic freezers, so customers can check temperature and fill levels themselves.',
      'Wrote pipelines pulling historical weather data from public APIs into Microsoft Fabric, feeding a forecasting model that covers 8,000+ plant locations.',
      'Modeled and structured the ingested data in Fabric so reporting and downstream analysis had something stable to sit on.',
    ],
  },
  {
    org: 'UB Nanosatellite Laboratory',
    logo: '/logos/ubnl.png',
    place: 'University at Buffalo',
    role: 'Flight Software Engineer',
    period: 'Sept 2025 to present',
    notes: [
      "Write flight software in C on NASA's core Flight System, handling telemetry and command messages routed over the cFS Software Bus.",
      'Built test applications in C that send health packets over UART through the EyeStar radio to verify connectivity with the Globalstar satellite network.',
      "Integrated message passing between the flight computer and an onboard NVIDIA Jetson using the lab's payload communication API.",
      'Bench-tested sensor and radio hardware on Linux flight computers, debugging serial links and confirming packet integrity end to end.',
    ],
  },
  {
    org: 'UB SEDS',
    logo: '/logos/ub-seds.png',
    place: 'University at Buffalo',
    role: 'Avionics Software Engineer',
    period: 'Aug 2024 to present',
    notes: [
      'Wrote ground support system firmware in C/C++ on an STM32 running FreeRTOS, controlling nitrous oxidizer fill and umbilical retraction for a hybrid rocket.',
      'Drove the fill solenoids and the stepper that retracts the umbilical line at launch, and built the igniter firing driver.',
      'Built abort and safety handling as FreeRTOS tasks that watch for fault conditions and bring the fill and ignition sequence down cleanly.',
      'Prototyped a Kalman filter in C++ for IMU-based state estimation, validated against simulated accelerometer and gyroscope data.',
    ],
  },
]

export const education = [
  {
    org: 'University at Buffalo',
    place: 'Buffalo, NY',
    role: 'B.S. Computer Science',
    period: 'Aug 2024 to Dec 2027',
    notes: [],
  },
]
