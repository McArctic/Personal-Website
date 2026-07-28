---
title: 'Create: Civilization'
logo: /logos/create-civilization.png
year: 2024
summary: A modded Minecraft server that went from two friends to 680+ players, and everything that had to get built to keep up with it.
stack: [Java, Kotlin, Python, React, SQLite]
status: Running · 99.8% uptime
---

It started as a server for me and a friend, with no goal beyond building the exact
modded experience we wanted to play. We opened it to the public mostly to see what
would happen. Within a day we had hundreds of people applying.

## Whitelisting by hand

Every player had to be in our Discord. That was deliberate: it meant announcements
reached everyone and moderation stayed in one place. Applications came in through a
Google Sheet.

Each one went like this. Open the sheet, check the Minecraft username was real, check
the person was actually in the Discord, whitelist them, then message them to say it
had gone through. That is fine for ten people. At a few hundred it is a second job,
and the server had not even officially launched yet. Once the semester started it
stopped being sustainable.

> Worth adding: roughly how long one application took, and the worst backlog you hit.
> A number here makes the next section land much harder.

## The bot

So I wrote a Discord bot to take the whole thing over. A player types `/whitelist`,
and Discord opens a form asking for their Minecraft username and how they found us.
The bot validates the name against Mojang's API, pulls the account UUID, whitelists
it, and stores the record against the Discord account it came from.

Tying those two identities together is what made everything after it possible.
Leaving the Discord or getting banned now revokes the whitelist on its own.
Punishments handed out in game appear in Discord, and punishments handed out in
Discord apply in game. A queue of manual steps became one command.

## Nobody could find us

Growth was entirely word of mouth, which put a hard ceiling on it. So we built a
website.

The best thing on it is a live map of the world. You can zoom into builds in 3D and
watch where players are in real time without joining the Discord or the server at
all. That turned out to be what brought people in, and it brought in far more of them
than we had planned for.

## Making it hold up

More players than the game server could take, and performance fell over.

Fixing it took weeks. Tuning JVM flags and garbage collection behaviour. Patching
mods by hand where they leaked memory, because those fixes did not exist upstream.
Reworking chunk loading so it happened asynchronously instead of blocking the main
server tick.

> Worth adding: tick time or concurrent player count, before and after. This is the
> most technical work on the page and a number would prove it.

## Season two

A year of this, and now we are rebuilding. Same idea, done properly the second time,
with everything the first year taught us about what actually breaks.
