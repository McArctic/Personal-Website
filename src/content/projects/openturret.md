---
title: OpenTurret
year: 2026
summary: A two-axis turret on an RP2040, driving TMC2209 stepper drivers over a single-wire UART link.
stack: [C++, Pico SDK, CMake, TMC2209]
repo: https://github.com/McArctic/OpenTurret
status: In progress
---

A pan-and-tilt turret built around a Raspberry Pi Pico. Firmware is C++ against the
Pico SDK, built with CMake and Ninja, flashed as a `.uf2` over BOOTSEL.

## Why UART instead of step/dir

TMC2209 drivers will run purely off step and direction pins, and that is where most
projects stop. The features worth having (stall detection, runtime current control,
quiet microstepping) only open up over the driver's UART interface.

## The part that took the longest

The link is half-duplex on a single wire, so every datagram you send comes back at
you as an echo before the reply does. Until you account for that, the read path looks
like it is receiving garbage. On top of it, each datagram carries a CRC, and the
driver silently ignores anything that fails it, so a wrong CRC and a dead wire look
identical from the host side.

> Worth expanding: how you finally got visibility into the line. Debugging something
> that fails silently is a good story and most candidates do not have one.

## What I would change

> Worth expanding, and worth doing honestly. This is the section that shows you can
> evaluate your own work, and interviewers read it closely.
