---
title: OpenTurret
year: 2026
summary: A two-axis turret that aims an airsoft gun at a moving target, splitting vision and prediction on a Pi 5 from motor control on a Pico.
stack: [C++, Pico SDK, CMake, TMC2209]
difficulty: square
cover: /img/openturret/workbench.jpg
repo: https://github.com/McArctic/OpenTurret
status: Back burner
---

OpenTurret is a two-axis turret built on an old airsoft gun that aims at a moving
target. I started it to get hands-on with hardware and vision models at the same time.

The work splits across two computers. A Raspberry Pi 5 runs the vision model and the
prediction math, works out where the target is heading, and sends over a pair of angles.
The Pico does the rest: microstepping, and driving the steppers to those angles.

## Hardware

A Pico driving TMC2209s over UART. Pin mode is simpler to wire but gives you two
microstep settings and a potentiometer for current; UART gives finer microstepping,
current in software, and lets me change either on the fly.

The TMC2209 has pins labeled RX and TX, but only RX is real and it carries both
directions on one wire. The Pico's TX goes into it through a 1k resistor, the Pico's RX
connects to the same pin directly, and anything sent comes back as an echo that has to
be cleared before the driver's reply can be read. The register values were garbage after
that, which turned out to be my own memcpy assuming little-endian when the driver is
big-endian.

![A Pico and a TMC2209 on a breadboard with a scope probe clipped on](/img/openturret/driver-bench.jpg#tall) ![An oscilloscope showing a square wave at 998 Hz and 50 percent duty](/img/openturret/step-pulse.jpg "Pico into a TMC2209, and the step output coming off it at 998 Hz")

## Status

The Pico side is the only part built. The vision model, the prediction math, the link
between the Pi and the Pico, and the mount the whole thing sits on are all still ahead.

On the back burner for now. The TMC2209 work carries straight over to
[Overpass](/projects/overpass), which needs the same two axes and the same drivers.
