# poop-tube

**A dog poop bag holder that doesn't break.** It's a stiff PETG tube with a bayonet lid and a
big, strong eyelet that takes a real carabiner. It prints in two parts with no supports.

Designed to hang from a leash on a
[DMM XSRE Mini carabiner](https://madrock.com/products/dmm-xsre-mini-carabiner) (6.16 mm wire).

## Motivation

Every bag holder I've tried fails in one of these ways:

- **Cordura pouches** have no shape. The roll flops around and the bag won't feed out cleanly.
- **ABS/hard plastic holders** crack.
- **Tiny eyelets** are sized for cheap keychain clips. A real carabiner either doesn't fit through
  them or snaps them off.

This one is a rigid tube, sized to the same bag rolls, with an eyelet built for a real carabiner.

## Files

| File | What |
|---|---|
| `poop_tube.py` | The model ([build123d](https://github.com/gumyr/build123d)). Every dimension is a named constant at the top. Running it rebuilds everything and runs a fit check. |
| `body.stl` | Body, in print orientation (bottom down). |
| `lid.stl` | Lid, in print orientation (plug end down). |
| `assembly.step` | Both parts assembled and locked, for checking fit in CAD. |

```
python poop_tube.py
```

## Printing

- PETG, no supports.
- 4+ perimeters on both parts: they carry the eyelet pull, the posts and the groove rails.
- Body: closed bottom on the bed. Lid: plug end on the bed, eyelet pointing up.

## Using it

Drop the roll in, feed a bag out of the side hole. Then close the lid: **push down, turn
clockwise (seen from the top), let go.** To open: push down, turn back, lift.

## Design decisions

**Dimensions come from the old holder that worked.** The bore is 36.95 mm, the same as the old
holder's, so the rolls fit. The cavity is 67 mm deep for a 62.4 mm roll, leaving room for fat
rolls. The dispensing hole is the same 26.4 mm circle. It's round on purpose: you tear the bags
off by hand, and that works fine with a round hole.

**PETG.** It's tougher and less brittle than ABS or PLA, and it shrugs off cold, sun and being
stepped on.

**Bayonet, not threads.** Threads came first and were dropped:

- *Faster:* a quarter turn opens and closes it, one-handed with gloves on, while the dog pulls.
  A printed thread takes several turns and can cross-thread.
- *Grit-tolerant:* grooves shed dirt and sand; thread flanks pack with it and bind.
- *Forgiving:* a post in a groove works even if the print is a few tenths off. A printed thread
  has to get pitch, flank angle and clearance right all at once.
- *Positive lock:* you can feel it seat, where a thread only goes snug and can back off.

**Gravity is the lock.** Each groove drops from the rim, runs 50 degrees clockwise, then ends in
a pocket that hooks 2 mm *up* toward the rim. Hanging from the eyelet, the body's weight pulls
it down, which lifts the posts into the pockets. Nothing needs to flex or snap over a bump.
A pocket that hooked down would let the weight pull the posts back out.

**Blind grooves, solid skin.** The grooves are cut into the bore from the inside, 3 mm deep, with
1.6 mm of solid wall outside them. Through-slots would leave the rail between the groove and the
rim hanging off the wall at one end, ready to snap. With a solid skin, the rails are part of the
wall. The grooves don't need flex, so the skin costs nothing.

**Rounded rail corners and a flared entry.** The two corners the post is pushed around (entry into
run, run into pocket) are rounded to 1.5 mm. The groove mouths flare 45 degrees at the rim so the
posts find them without looking.

**No ramp in the run (yet).** A helical run would clamp the lid down as you turn it, which
would stop any rattle. But the hanging weight would then try to back the posts up the ramp,
which fights the gravity lock. The run is flat for now. If the lid rattles on the leash, a
short, shallow ramp at the end of the run can be added later.

**The eyelet is a thick arch on top of the lid.** A side tab was tried first and rejected: it
hung the holder off-axis. On top, the pull runs across the print's layer lines, which is the weak
direction, so the arch is built heavy:

- 10 mm thick, with 5 mm of material around the hole;
- a 3 mm fillet where it meets the lid, to spread the load;
- a 9 mm round hole: the 6.16 mm carabiner wire plus room to swing and clip on with gloves.

**Everything prints without supports.**

- The lid's cap meets the plug through a 45-degree cone instead of a flat overhang.
- The plug's bottom edge is chamfered: it's a lead-in, and it hides elephant's foot.
- The body's bottom edge is chamfered for the same reason.

**The fit is checked in CAD.** `poop_tube.py` places the lid at each step of the open/close
path and checks it doesn't hit the body. It also checks that the locked lid can't be lifted or
turned back, and that it can't turn at the entry without being pushed down first.

## Tuning after a print

| Symptom | Knob |
|---|---|
| Plug tight or loose in the bore | `PLUG_CLEARANCE` (0.3) |
| Posts bind or slop in the grooves | `SLOT_CLEARANCE` (0.3) |
| Lock too shallow or too fussy | `HOOK` (2.0) |
| Groove roofs sag and bind the posts | `GROOVE_DEPTH` (3.0) or `SLOT_CLEARANCE` |
| Lid rattles | add a shallow ramp at the end of the run |
| Different carabiner | `EYELET_HOLE_D` (9.0) |
| Different bag roll | `INNER_D`, `CAVITY_DEPTH` |
