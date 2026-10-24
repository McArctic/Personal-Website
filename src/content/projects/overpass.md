---
title: Overpass
year: 2026
summary: A pan/tilt mount that tracks a satellite across the sky, so the antenna stays pointed at it for the whole pass instead of a few lucky seconds.
stack: [C, FreeRTOS, Pico, TMC2209, SGP4]
difficulty: diamond
cover: pass-plot
featured: true
status: In progress
---

Last winter we were outside testing a satellite radio for UBNL. It was freezing, we
were out there for hours, and we never got a solid track on anything. A satellite in
low orbit crosses the whole sky in a few minutes, way too fast to follow by hand, so
you catch it for a second and then lose it. Getting a good link is hard enough
without that.

So I'm building the thing that fixes it. A pan/tilt mount that finds the satellite
and follows it horizon to horizon, so the antenna is actually pointed at it the whole
time it's up there. The plot on the card is what a pass looks like from the ground,
the rim is the horizon and the middle is straight overhead.

## What it is

A Pico running FreeRTOS, two NEMA 17 steppers for pan and tilt, and TMC2209 drivers
to run them. There's a GPS for time and location, and a compass so it knows which way
it's facing. Same drivers I was using on [OpenTurret](/projects/openturret), which is
most of the reason that one's on the back burner now.

The part I didn't think about until I started is that pointing at a satellite means
knowing three things: the time, where you are, and where north is. Miss any one of
them and you're pointed at nothing. So it homes both axes on startup, reads the
compass to find north, and keeps watching the GPS in case someone picks it up and
puts it somewhere else.

Everything after that is timing. The motors can't be late or the mount falls behind
the satellite and the link drops, so that runs at a fixed rate above everything else.
The orbit math is an existing SGP4 library, I'm not writing that from scratch.

## Where it's at

Early. Right now it's getting FreeRTOS onto the Pico and both motors moving. Then
tracking a simulated pass indoors, and then the only test that actually counts,
taking it outside and pointing it at something like the ISS.

Build photos going here as it comes together.
