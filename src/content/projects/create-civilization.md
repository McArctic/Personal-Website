---
title: 'Create: Civilization'
year: 2024
summary: A modded Minecraft server that went from two friends to 680+ players, and everything that had to get built to keep up with it.
stack: [Java, Kotlin, Python, React, SQLite]
status: Active
---

Create: Civilization started as a server for me and my friends, with the only goal
of making it our dream server. Once we started building it, we realized we didn't
have enough friends to make it feel the way we wanted, so we decided to make it
public. After one week we suddenly had 100 players in our Discord, waiting for the
server to release.

## Applications

One of the things we did to help with server moderation was require players to
"apply" to join. That added a layer of friction on purpose. Normally more friction
is a bad idea, but for a server like ours it helped keep out players who just want
to join and cause problems. Players like that tend to act on impulse and lose
interest fast, so even a slight barrier filtered them out and left us with the most
dedicated, interested players.

Another reason for the application process was to make sure every player who joined
was also in our Discord. One of the server's major gameplay features was the ability
to wage war on another player's claim. Declaring war meant posting in a dedicated
channel at least 24 hours in advance, so everyone had time to see it and prepare.
Having every player able to see and post in that channel was fundamental to the
gameplay.

These applications came in through Google Forms, which fed into a Google Sheet for
manual review. The sheet quickly ballooned as new players kept joining. For each one
I had to check that the Minecraft username was valid and that the Discord account was
actually in our server. That took about five minutes per application, and by the
time we were approaching 200 of them, it was eating up a huge chunk of my day. I knew
it wasn't sustainable, which is what led me to build a Discord bot to automate the
whole thing.

## The bot

I spent about a week writing the first version of the bot, and the way it worked was
pretty elegant. A new player would see a message prompting them to type `/whitelist`
in any channel, which used Discord's bot API to pop up a quick form asking for their
Minecraft username, why they wanted to join, and where they found us (that last one
was purely so I could see what was actually driving people to join). Once they
submitted it, the bot called Mojang's API to check the username was valid, then sent
a call to the server to whitelist it and logged an entry in our whitelist database.

Tying a player's Minecraft account to their Discord account this way turned out to be
huge, because it meant we could finally sync punishments between the two. If someone
was rowdy in Discord chat, muting them there would also mute them in Minecraft. That
saved a ton of time, since before the bot every punishment meant manually
cross-checking the sheet.

Once whitelisting was handled, we also added a ticket system so players could report
issues without flooding a channel or DMing whoever happened to be online. When that
first real ticket came in, it was such a relief knowing the headaches from before the
bot were finally solved.

## Nobody could find us

Now that applications were sorted out and automated, we wanted to expand again.
Before this point we'd pulled all our advertising on purpose, to let things catch
up and slow down. That left growth entirely word of mouth, which showed. To fix
that, we decided to build a website, both to pick up some Google SEO and to come
off as more "professional."

The website was built by one of our team members, at my request and under my
oversight. It gave us a solid homepage where players could check the rules and new
players could find us on Google and get to the Discord. But I always felt it was
missing something.

I decided to add a map of the server to the website. It started as a static image,
but eventually became a live 3D map, updating in real time as players moved around,
showing builds and other features as they happened. Players loved it, current
players and new ones alike. We started seeing applications where people said they'd
found us through the website and specifically mentioned the map. That's when I knew
it was actually working.

## Making it hold up

As the map started pulling in more players, concurrent players crept up with it, we
were regularly hitting 20 at once. The whole server ran off my own hardware at home,
and it started to show. We knew something had to give the moment we got around 20
tickets in a single day, all complaining about performance during peak hours. Being
a broke college student, I couldn't just throw more hardware at the problem, so the
fix had to be entirely software.

![Day one player count.](/img/create-civilization/pre-release-players.png#wide)

We hit the easy stuff first, switching to Aikar's flags and moving to ZGC for
garbage collection. Then we profiled with Spark to find where actual bottlenecks
were, and most of it traced back to chunk loading. We used Spark again to hunt down
memory leaks in specific mods. We didn't have upstream fixes to rely on, so we pulled
the source ourselves, patched them, and built our own fixed versions. Some of those
patches got merged back into the original repos, others we never heard back on.

The hardest part was chunk loading itself. We were running NeoForge, so we didn't
have any async chunk loading built in. So we built it ourselves, loading chunks on
their own CPU thread instead of blocking the main server tick.

All told, this took about three months, with different team members tackling
different pieces along the way. Flags came first, async chunk loading came last,
since it was the hardest problem of the bunch. By the end, server TPS was back up
from 13 to a steady 20, which let us take max concurrent players from the low 20s
up into the 30s.

## Season two

A year of this, and season two is now in active development, no ETA yet. The
website is being rebuilt in Vue. The bot is being rewritten in Java too, since all
our Minecraft modding work is already in Java and the team is built around it. The
gameplay itself is getting reworked into a harder survival experience, with a much
bigger focus on player cooperation and resource scarcity, using everything the
first year taught us about what breaks.