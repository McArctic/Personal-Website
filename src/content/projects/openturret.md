---
title: OpenTurret
year: 2026
summary: A two-axis turret that aims an airsoft gun at a moving target, splitting vision and prediction on a Pi 5 from motor control on a Pico.
stack: [C++, Pico SDK, CMake, TMC2209]
repo: https://github.com/McArctic/OpenTurret
status: In progress · firmware bring-up
---

This has been a dream project of mine for a while. I wanted more hands-on hardware
and vision model experience, and building a turret out of an old airsoft gun seemed
like the obvious way to get both. The idea: something that can find a moving target,
work out where it's actually going to be, and put a round there instead of where the
target used to be.

## The plan

The system splits across two computers. A Raspberry Pi 5 runs the vision model and
does the prediction math, figuring out where a target is heading and what angle the
turret needs to hit it. All the Pi sends over is a pair of angles. The Pico is the
driver. Its only job is turning those angles into actual motor movement: handling
microstepping, moving the steppers, and getting them exactly where they're told to go.

## Where it's at right now

Right now I'm just writing the Pico side, the stepper driver. I've got the Pico
wired up to a TMC2209 stepper driver, and I'm working on the communication layer
between them over UART.

## Why UART instead of just pins

The TMC2209 can run in two modes. Pure pin mode is simpler to wire, but you're stuck
with only two microstep options, and current control means physically turning a
potentiometer on the board. UART mode opens up way more microstep resolution, lets
you set current in software instead of by hand, and lets you change any of it on the
fly instead of committing to a fixed setup. For a project where I want to actually
tune things as I go, that flexibility was worth the extra wiring complexity.

## The UART figured itself out the hard way

The TMC2209 has pins labeled RX and TX, so I wired it up the obvious way. Turned out
that was wrong, the "TX" pin doesn't actually do anything. The driver only has one
real UART pin, the one labeled RX, and it's meant to carry both directions on a
single wire.

So the actual wiring is: the Pico's TX goes through a 1k ohm resistor into that one
UART pin, and the Pico's RX connects to the same pin directly, no resistor. Once I
had that wired correctly, a new problem showed up. Since it's a single wire,
anything I send comes right back to my own RX pin as an echo. I had to clear that
echo out before I could actually read whatever the driver sent back.

## Then the data was wrong

Once I could talk to the driver, I was getting garbage back for its register values.
I put an oscilloscope on the line to check the bits were even moving correctly, and
they were, the driver was responding fine. The actual bug was in my own code, I was
using memcpy assuming little-endian, and the driver expects big-endian. Fixed that
and the data started coming back correctly.

## Still ahead

The vision model, the prediction math, and the link between the Pi and the Pico are
all still unbuilt. So is the mount the whole thing sits on.