---
title: Overpass
year: 2026
summary: A two-axis ground station that tracks satellites across the sky and holds an antenna on them long enough to talk.
stack: [Python, C++, Servos, SDR]
difficulty: diamond
cover: pass-plot
featured: true
status: In progress
---

I spend my weeks writing flight software for a cubesat I will never get to talk to. The
satellite goes up, someone else's ground station talks to it, and my part of the job
ends at the bench. I wanted the other half of that link. So I'm building the ground
station: a rotator that tracks a satellite across the sky and keeps an antenna pointed
at it for the few minutes it's up there.

There are a lot of satellites overhead that will talk to anyone who asks. Weather
birds broadcasting images in the clear, amateur radio payloads, beacons putting out
telemetry on a published frequency. None of it needs permission. It just needs you to
be pointing the right way at the right time.

## The hard part isn't the radio

A pass is short. A low-orbit satellite clears the horizon, climbs, and is gone again in
something like ten minutes, and for most of that it's moving fast enough that a fixed
antenna with any real gain will miss it. So the problem splits in two: work out where
the thing is going to be, and physically get the antenna there before it is.

The first half is math I can do on a laptop. Orbital elements for anything interesting
are published and updated daily, and propagating them forward gives you azimuth and
elevation for every second of a pass before it happens. You know when the satellite
comes up, where it comes up, how high it gets, and where it sets. That's the plot on
the project card — the arc is a real pass, horizon at the rim, straight overhead in the
middle.

The second half is the part I'm actually building. Two axes: azimuth spins the whole
assembly through a full circle, elevation tilts the antenna from the horizon to
straight up. Both have to move smoothly and both have to know where they are, because
an antenna that's five degrees off is an antenna that heard nothing.

## Where it is right now

I'm on the mechanical side. I have the servos and I'm working through the drive parts
to get the two axes moving under command before anything gets pointed at the sky. Right
now it's a lot of fitting and refitting and finding out that the thing I printed is two
millimetres too small.

The split I'm planning mirrors what I did on the turret: something with a real operating
system does the orbital math and decides where to point, and something small and
boring takes angles and makes the motors go there. Keeping the prediction away from the
motor loop means neither one can ruin the other's day.

After that it's the radio, and then the only measure of success that counts — pointing
it at something overhead and getting a signal back down.

I'll put build photos here as it comes together.
