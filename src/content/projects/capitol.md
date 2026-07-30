---
title: Capitol
year: 2025
summary: A claims and permissions mod for Minecraft, built standalone first, backed by SQLite, with borders you can actually see instead of a popup name tag.
stack: [Java, NeoForge, SQLite]
repo: https://github.com/Create-Civilization/Capitol
download: https://modrinth.com/mod/capitol
status: In progress
---

Capitol exists because of Open Parties and Claims (OPAC), the claim mod we were running
in Season 1 of Create: Civilization. It wasn't just a Civ problem either, I'd run into
the same frustrations on my own personal worlds for a while. Permissions were messy and
unorganized, painful for anyone who wasn't technical. Teams felt sloppy, no real role
structure, you couldn't define who could do what beyond a couple of fixed tiers. And
claims themselves weren't visual, there was nothing on screen that actually showed you
where a border was. I wanted something better for my own use, and Civilization just
gave me a reason to actually build it.

## Standalone first

Even though Capitol lives under the Civilization umbrella, my rule for every mod I
build for the server is that it has to work standalone first. Integration with the
server comes after. That's a constraint I hold myself to on purpose, it keeps the mod
useful outside of just our one server, and it keeps me honest about building something
actually good instead of something propped up by the rest of our infrastructure.

## Why SQLite

Most Minecraft claim mods store their data in .dat files, or embed it directly into
Minecraft's own chunk data. I didn't want either. I wanted a real database, so I built
Capitol around SQLite. That made it way easier to add features fast and link tables
together as the mod grew, instead of fighting a storage format never meant to hold this
much relational data.

I started simple, basic chunk claiming, just storing chunk coordinates and dimension
in the database. Everything else got built on top of that.

## Roles that actually mean something

One of the things OPAC got wrong was roles, teams were stuck with a couple of fixed
tiers and no way to actually customize who could do what. Capitol lets teams create
their own roles and assign whatever permissions they want to each one, instead of
forcing everyone into a rigid structure that doesn't fit how the team actually works.

## Making claims visible

Old claim mods show you where you are with a text popup, something like "Blah's Claim"
flashing on your screen when you cross a border. I never liked that. It's too in your
face and it breaks immersion.

Instead I built borders you can actually see. Chunk boundaries get a thin line
rendered along the top of blocks, using NeoForge's rendering API, so you get a clean
outline of exactly where a claim starts and ends without anything popping up on your
screen. That works fine on the ground, but it falls apart if you're flying in from
above, a thin line on the ground is hard to spot from altitude. So I added a
semi-transparent wall along the boundary that fades in as you get close and fades back
out as you move away. It's just some math checking whether the area being rendered
falls inside a claim's boundaries, then checking your distance to decide how visible
the wall should be. Between the two, you always know where a border is without the
game ever telling you outright.

![A border at ground level, drawn as a thin line along the tops of the blocks](/img/capitol/borders-ground.png#stack "In-game claim examples") ![The same borders from altitude, where each claim renders in its own color](/img/capitol/borders-aerial.png)

## Subclaims

The subclaims came out of a problem I kept running into with my own builds. I like
making player shops, but if you want other players to interact with blocks inside your
shop, normal claim mods force a bad choice. Either the shop can't be inside your claim
at all, or you give players full permissions to that entire chunk. Neither of those
worked for me.

So Capitol supports 3D subclaims, smaller claim regions nested inside a bigger one,
each with their own permissions separate from the parent claim. As far as I know,
nobody else has built this for Minecraft. It works through a subclaims table that links
back to its parent claim and to the specific chunks it covers, which lets Capitol check
permissions at the subclaim level instead of just the chunk level. That means I can
lock down my whole claim and still let players freely use just the shop inside it.

## Claiming blocks that aren't really there

Sable, a very popular physics mod within the community, adds "sublevels," physics
blocks that exist off the normal grid entirely. Technically those blocks live millions
of blocks away in something Sable calls a plot yard, and get projected into the world
so they look like they're where you're standing. Making Capitol work with that meant
doing a different kind of check. I had to figure out where a player is actually
aiming, whether that hit lands on a projected block, and trace it back to the real
plot yard location to run the normal permission checks against. It's one of the
harder compatibility problems in the mod so far, since none of the normal chunk-based
logic applies once a block isn't really where it appears to be.

## Wars, still unfinished

The last big piece is wars, and it's still a work in progress. The idea is King of the
Hill style capture. Instead of a claim falling the moment someone walks in, attackers
capture it one chunk at a time, starting from the border chunks and working inward.
It's meant to feel like an actual siege with real borders, instead of a fight that's
over the second someone steps inside.

## Where it's at

Right now claims, permissions, teams, roles, and subclaims are all working, including
compatibility with Sable's off-grid blocks. Wars and the KOTH capture system are what's
left before this is ready for Civilization Season 2.