---
title: Overpass
year: 2026
summary: A pan/tilt mount that keeps an antenna pointed at a satellite for a full pass, instead of tracking it by hand.
stack: [C, FreeRTOS, Pico, TMC2209, SGP4]
difficulty: diamond
cover: pass-plot
featured: true
status: In progress
---

Overpass is a pan/tilt mount that keeps an antenna pointed at a satellite for a full
pass, instead of tracking it by hand. It came out of a night testing a satellite radio
for UBNL, where hand-tracking cost us most of the pass.

The target is any satellite passing overhead. GPS gives the mount its own location and
the time, the compass gives it which way it's facing, and from those it works out the
angles to the satellite and drives the steppers to hold the antenna there. Both axes
home at startup, and it keeps reading the GPS in case the mount gets moved. The orbit
math is an existing SGP4 library rather than my own implementation.

The plot on the card is a pass seen from the ground: the rim is the horizon, the centre
is straight overhead.

## Hardware

A Pico running FreeRTOS, two NEMA 17 steppers for pan and tilt, TMC2209 drivers, a GPS
for time and position, and a compass for heading.

The drivers are the same ones I used on [OpenTurret](/projects/openturret), and the UART
work from that project carries straight across. That overlap is most of why OpenTurret
is on the back burner.

FreeRTOS is there to keep everything running together, and to make it easier to
prioritize tasks.

## Status

Early. I'm getting FreeRTOS onto the Pico with both motors moving before anything points
at the sky. After that it's tracking a simulated pass indoors, where the math can be
checked against a known input, then an outdoor test on something like the ISS.

Build photos going here as it comes together.
