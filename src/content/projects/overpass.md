---
title: Overpass
year: 2026
summary: A pan/tilt mount that finds a satellite and follows it across the sky, so a ground station can hold a link for the few minutes one is actually overhead.
stack: [C, FreeRTOS, Pico, TMC2209, SGP4]
difficulty: diamond
cover: pass-plot
featured: true
status: In progress
---

Last winter we were outside testing a satellite communications module for UBNL. It was
cold, we were out there for hours, and we never got a good track on anything. That is
basically the whole problem in one sentence. A satellite in low orbit crosses the entire
sky in a few minutes, which is way too fast to follow by hand, so you catch it for a
second and then spend the rest of the pass guessing where it went.

Getting a solid uplink and downlink from a ground station is hard enough without that.
If the antenna is actually pointed at the satellite the whole time it is overhead, a lot
of that difficulty goes away. So that is what I am building. A pan/tilt mount that finds
the satellite and follows it horizon to horizon.

The plot on the project card is what a pass looks like from the ground. The rim is the
horizon, the middle is straight up, and the arc is the path the mount has to follow.

## What it is

A Raspberry Pi Pico running FreeRTOS, two NEMA 17 steppers for pan and tilt, and two
TMC2209 drivers to run them. There is a GPS module for accurate time and location, and a
compass module so the thing knows which way it is facing.

The TMC2209s are the same drivers I was working with on [OpenTurret](/projects/openturret),
which is most of the reason that project is on the back burner. I would rather put the
driver work into something I actually need.

## It has to know where it is before it can know where to look

This is the part I did not think about until I started writing the proposal. Pointing at
a satellite means knowing the time, your location, and which direction is north. Miss any
one of those and you are pointing at nothing.

So on startup both motors home themselves using sensorless homing on the drivers, which
means no limit switches to wire or mount. Then the compass gets read to find north. The
GPS gives the time and location, and it keeps checking, because if the mount gets picked
up and put somewhere else the compass has to be read again. That check has some slop in
it on purpose, since GPS drifts a little even when the thing is sitting perfectly still,
and I do not want normal drift to count as somebody moving it.

## I am not writing the orbit math

Satellite positions come from a TLE, which is a short block of text describing an orbit,
and the standard way to turn one into a position is SGP4. That algorithm is decades old
and very well tested, and writing my own version of it would be a worse version of it. So
I am using an existing library and typing the TLE in by hand for now.

## Four things happening at once

This is the part that makes it a real time problem instead of a scripting problem. Four
tasks, different priorities, different rates:

The motor task is the highest priority and runs every 10 ms, because that is the one that
cannot be late. If it stalls, the mount lags behind the satellite and the link drops.

The orbit task runs every 100 ms and works out where the satellite is right now, then
hands the motor task a target angle through a queue.

The GPS task runs once a second and checks for new fix data. If the location moved more
than the slop range, it re-reads the compass.

The input task is the lowest priority and just takes in a new TLE.

The time, location, and heading are shared between the GPS task and the orbit task, so
those are behind a mutex. The drivers' stall signal fires an interrupt that gives a
semaphore to the motor task, which is how homing knows it is done. Everything periodic
uses `vTaskDelayUntil` so the rates stay fixed instead of drifting.

## Where it is right now

This one is for a class, so it has a ten week plan with real checkpoints. First
checkpoint is homing working and the angles coming out correct, checked against an online
tracker. Second is the whole system tracking a simulated pass indoors.

Right now I am at the start of that, getting FreeRTOS running on the Pico and both motors
moving. After the indoor tracking works the real test is taking it outside and pointing it
at something like the ISS, which is the only result that actually counts.

Build photos going here as it comes together.
