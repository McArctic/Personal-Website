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

Overpass exists because of a night last winter testing a satellite radio for UBNL. It
was freezing, we were out there for hours, and we never got a solid track on anything.
A satellite in low orbit crosses the whole sky in a few minutes, which is way too fast
to follow by hand. You catch it for a second, lose it, and spend the rest of the pass
trying to find it again before it drops back under the horizon. Getting a good link is
hard enough without fighting the antenna the entire time.

So I decided to build the thing that fixes it. A pan/tilt mount that finds the
satellite and follows it horizon to horizon, so the antenna is actually pointed at it
the whole time it's up there. The plot on the card is what a pass looks like from the
ground, the rim is the horizon and the middle is straight overhead.

## The hardware

A Pico running FreeRTOS, two NEMA 17 steppers for pan and tilt, and TMC2209 drivers to
run them. There's a GPS for time and location, and a compass so it knows which way it's
facing.

Those are the same drivers I was using on [OpenTurret](/projects/openturret), which is
most of the reason that one is on the back burner now. All the UART work I did over
there carries straight across. Two axes and the same drivers, just pointed at the sky
instead of across a room.

## Three things it has to know

The part I didn't think about until I started is that pointing at a satellite means
knowing three things: what time it is, where you are, and which way north is. Miss any
one of them and the mount is aimed at empty sky with no way of telling that it's wrong.
So it homes both axes on startup, reads the compass to find north, and keeps watching
the GPS in case someone picks the whole thing up and sets it down somewhere else.

The orbit math itself is an existing SGP4 library. That one is a solved problem and I
wasn't going to write it from scratch just to say I had.

## Why FreeRTOS

Everything after that is timing. The motors can't be late, because if the mount falls
behind the satellite the link drops, and a pass is only a few minutes long to begin
with. On a plain superloop the step timing would share the main loop with the GPS
reads and the orbit math, and any one of those running long pushes the steps late.

With FreeRTOS the stepping gets its own task at a fixed rate above everything else, so
the slower work can take as long as it needs without touching it. The downside is that
I now have a scheduler to configure and task priorities to get right, which is a lot
more setup than a loop would have been.

## Where it's at

Still early. Right now I'm getting FreeRTOS onto the Pico and both motors moving, and
nothing is getting pointed at the sky until that part is solid. After that it's
tracking a simulated pass indoors, where I can check the math against something I
control. Then the only test that really counts, which is taking it outside and putting
it on something like the ISS.

Build photos going here as it comes together.
