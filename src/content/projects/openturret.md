---
title: OpenTurret
year: 2026
summary: A two-axis turret that aims an airsoft gun at moving targets, splitting vision and prediction on a Pi 5 from motion control on a Pico.
stack: [C++, Pico SDK, CMake, TMC2209]
repo: https://github.com/McArctic/OpenTurret
status: In progress · firmware bring-up
---

The goal is a turret that finds a target on its own, works out where that target is
going to be, and puts an airsoft round there. Pan and tilt, so two axes of stepper
motion, and a shot that leads the target instead of chasing it.

That last part is what makes it interesting. A round leaves the barrel at a fixed
speed and takes real time to arrive, so aiming where the target is now is aiming
where it used to be. The turret has to solve for where the target and the round meet.

## Two computers, on purpose

A vision model deciding what is a target, and the ballistics behind an intercept, are
not work a microcontroller should be doing. But holding a stepper on a commanded
angle is not work that survives an operating system scheduling something else first.

So the split is by what each side is good at. A Raspberry Pi 5 runs the camera, the
detection model, and the prediction math, and its entire output is a pair of angles:
where the two axes should be pointing. The Pico takes those angles and is responsible
for nothing except getting the motors there and holding them. Everything above the
motion loop can change without touching firmware, and the motion loop cannot be
starved by anything above it.

## Where it actually is

Parts are still coming in. What exists is the Pico end: firmware in C++ against the
Pico SDK, built with CMake and Ninja, flashed as a `.uf2` over BOOTSEL, talking to
TMC2209 stepper drivers.

## Why UART instead of step/dir

TMC2209 drivers will run purely off step and direction pins, and that is where most
projects stop. The features worth having (stall detection, runtime current control,
quiet microstepping) only open up over the driver's UART interface.

Stall detection is the one I want most. A turret that can tell it has hit the end of
its travel, or that something is in the way, does not need limit switches to know
where its own limits are.

## The part that took the longest

The link is half-duplex on a single wire, so every datagram you send comes back at
you as an echo before the reply does. Until you account for that, the read path looks
like it is receiving garbage. On top of it, each datagram carries a CRC, and the
driver silently ignores anything that fails it, so a wrong CRC and a dead wire look
identical from the host side.

> Worth expanding: how you finally got visibility into the line. Debugging something
> that fails silently is a good story and most candidates do not have one.

## Still ahead

The vision model, the prediction, and the link between the Pi and the Pico are all
unbuilt. So is the mount the whole thing sits on.

> Worth adding once you get there: what you picked for detection and why, and how you
> are measuring whether the prediction is any good. An accuracy number against a
> moving target is the number this project is judged on.
