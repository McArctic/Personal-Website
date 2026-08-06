---
title: Capitol
year: 2025
summary: A claims and permissions mod for Minecraft, built standalone first, backed by SQLite, with borders you can actually see instead of a popup name tag.
stack: [Java, NeoForge, SQLite]
repo: https://github.com/Create-Civilization/Capitol
download: https://modrinth.com/mod/capitol
status: In progress
---

Capitol exists because of Open Parties and Claims (OPAC), the claim mod we were using
in Season 1 of Create: Civilization. The mod was amazing but it was always a pain to
use on a large Minecraft server with very dynamic claims. OPAC did a great job
protecting things. It had a detailed config and permission manager but it was painful
to use. Every command had 100s of sub-commands so for non technical users it was a
pain. It also didn't support transferring claims between teams and groups easily so
war was always a mess. I had to make a lot of compromises I didn't want to make. So I
decided if I didn't like what existed I would do it myself.

## Standalone first

Even though Capitol lives under the Civilization umbrella my rule for every mod I
build for the server is that it has to work standalone first. It's important to me
that every mod I work on is applicable outside of the server. I want people to enjoy
what I make and not put my work in a box it can't escape from.

## Why SQLite

Most Minecraft claim mods store their data in .dat files or embed it directly into
Minecraft's own chunk data. I didn't want either. I wanted a real database so I built
Capitol around SQLite. That made it way easier to add features fast and link tables
together as the mod grew instead of fighting a storage format never meant to hold this
much relational data. The downside is I now have to version every database change and
set up migrations for table changes so users can upgrade seamlessly.

## Making claims visible

Old claim mods show you where you are with a text popup, something like "Blah Blah's Claim"
flashing on your screen when you cross a border. I never liked that. It's too in your
face and it breaks immersion.

Instead I built borders you can actually see. Chunk boundaries get a thin line
rendered along the top of blocks using NeoForge's rendering API. That gives you a
clean outline of exactly where a claim starts and ends without anything popping up on
your screen. That works fine on the ground but it falls apart if you're flying in from
above. A thin line is hard to spot from altitude. So I added a semi-transparent wall
along the boundary that fades in as you get close and fades back out as you move away.
It's just some math checking whether the area being rendered falls inside a claim's
boundaries then checking your distance to decide how visible the wall should be.
Between the two you always know where a border is without the game ever telling you
outright.

![The same borders from altitude, where each claim renders in its own color](/img/capitol/borders-ground.jpg#stack "In-game claim examples") ![A border at ground level, drawn as a thin line along the tops of the blocks](/img/capitol/borders-aerial.jpg)

## Subclaims

The subclaims came out of a problem I kept running into with my own builds. I like
making player shops but if you want other players to interact with blocks inside your
shop normal claim mods force a bad choice. Either the shop can't be inside your claim
at all or you give players full permissions to that entire chunk. Neither of those
worked for me.

So Capitol supports 3D subclaims: smaller claim regions nested inside a bigger one,
each with their own permissions separate from the parent claim. As far as I know
nobody else has built this for Minecraft. It works through a subclaims table that
links back to its parent claim and to the specific chunks it covers. That lets Capitol
check permissions at the subclaim level instead of just the chunk level. That means I
can lock down my whole claim and still let players freely use just the shop inside it.

## Blocks that aren't really there

Sable, a popular physics mod in the community, adds "sublevels," physics blocks that
exist off the normal grid entirely. Those blocks actually live millions of blocks away
in what Sable calls a plot yard and get projected into the world so they look like
they're right where you're standing. Making Capitol work with that meant a different
kind of check: figure out where a player is actually aiming, check whether that hit
lands on a projected block, then trace it back to the real plot yard location to run
the normal permission checks. None of the usual chunk-based logic applies once a block
isn't really where it looks like it is. That made this one of the harder compatibility
problems I've hit so far.

## Wars

The last big piece is wars, still a work in progress. The idea is King of the Hill
style capture. Instead of a claim falling the second someone walks in attackers take
it one chunk at a time, starting from the border chunks and working inward. It's meant
to feel like an actual siege with real borders, not a fight that's over the moment
someone steps inside.

## Where it's at

Claims, permissions, teams, roles, and subclaims are all working right now, including
compatibility with Sable's off-grid blocks. Wars and the KOTH capture system are what's
left before this is ready for Civilization Season 2.