"""Poop bag holder: bayonet tube, body + lid, PETG.

Both parts print standing on the bed with no supports:
  body - closed bottom on the bed, two L-grooves cut into the bore from the open top
  lid  - plug end on the bed, posts sticking out its sides, cone + cap above, eyelet arch on top

Bayonet: push the lid down, turn it clockwise (seen from the top) along the slot, let go. Each
slot ends in a pocket that hooks UP toward the rim. Hanging from the eyelet, the body's weight
pulls it down, which lifts the posts into the pockets, so gravity holds it locked. To open:
push down, turn back, lift.

The grooves are blind (cut from the inside, solid skin outside), so the rails between the run
and the rim are part of the wall, not cantilevers that snap off. Nothing needs to flex: the
upward hook is the lock. The rail corners the post turns around are rounded.

The eyelet pulls across the layer lines (the weak direction for prints), so it's a thick arch
with a filleted base: two 5 x 10 mm legs, far more than a bag roll on a leash will ever see.
"""

from build123d import *
from pathlib import Path

OUT = Path(__file__).parent

# Bag roll cavity
INNER_D = 36.95      # same ID as the old holder; the rolls fit it
BAG_LENGTH = 62.4
CAVITY_DEPTH = 67.0  # floor to the bottom of the lid's plug: BAG_LENGTH + 4.6 room for fat rolls

# Walls
FLOOR = 3.0
WALL = 4.6           # 3.0 wall the grooves are cut into + 1.6 solid skin outside them
CAP = 2.0            # lid's flat top above its cone

# Lid plug
PLUG_LENGTH = 12.0
PLUG_CLEARANCE = 0.3  # radial, plug to bore

# Bayonet
POST_D = 5.0
SLOT_CLEARANCE = 0.3  # each side of the post
RUN_DEPTH = 7.0       # rim down to the centre of the horizontal run
TURN = 50.0           # degrees from the entry to the pocket
HOOK = 2.0            # how far the pocket rises above the run: the lock
GROOVE_DEPTH = 3.0    # into the wall from the bore; leaves WALL - 3.0 of solid skin outside
RAIL_CORNER_R = 1.5   # rounding on the rail corners the post is pushed around
ENTRY_CHAMFER = 1.5   # 45 degree flare where each groove meets the rim, so the posts find it

# Dispensing hole in the body's side, same size as the old holder's
HOLE_D = 26.4

# Eyelet for a DMM mini carabiner (6.16 mm wire)
EYELET_HOLE_D = 9.0   # 6.16 wire + ~3 mm room, so it swings freely and clips on with gloves
EYELET_RING = 5.0     # material around the hole
EYELET_THICK = 10.0   # along the hole axis
EYELET_LIFT = 4.0     # lid top to the bottom of the hole
EYELET_FILLET = 3.0   # where the arch meets the lid top: spreads the pull into the cap

# Derived
inner_r = INNER_D / 2
body_r = inner_r + WALL
plug_r = inner_r - PLUG_CLEARANCE
slot_w = POST_D + 2 * SLOT_CLEARANCE
cone_rise = body_r - plug_r            # 45 degree cone from the plug out to the body's OD

# The cone touches the rim's inner edge when the lid is pushed down; locked, it rides HOOK higher.
# Size the body so the cavity under the locked plug is CAVITY_DEPTH.
pushed_cone_z = -PLUG_CLEARANCE        # cone bottom relative to the rim, lid pushed down
locked_cone_z = pushed_cone_z + HOOK
body_height = FLOOR + CAVITY_DEPTH + PLUG_LENGTH - locked_cone_z
run_z = body_height - RUN_DEPTH

# Lid, in its own coordinates: z = 0 at the bottom of the cone
post_z = (run_z - body_height) - pushed_cone_z
lid_top_z = cone_rise + CAP
lid_locked_z = body_height + locked_cone_z   # where the lid's z = 0 sits on the locked body


def up(solid_cls, *args, z=0.0):
    """Primitive sitting on z (base at z, extending up)."""
    return Pos(0, 0, z) * solid_cls(*args, align=(Align.CENTER, Align.CENTER, Align.MIN))


def radial(radius, r_from, r_to, z, angle):
    """Cylinder along the radial direction at `angle` degrees, centred at height z."""
    rod = Pos((r_from + r_to) / 2, 0, z) * Rot(0, 90, 0) * Cylinder(radius, r_to - r_from)
    return Rot(0, 0, angle) * rod


def radial_box(width, r_from, r_to, z_from, z_to, angle):
    """Box spanning r_from..r_to radially, `width` tangentially, z_from..z_to, at `angle`."""
    box = Pos((r_from + r_to) / 2, 0, (z_from + z_to) / 2) * Box(r_to - r_from, width, z_to - z_from)
    return Rot(0, 0, angle) * box


def slot_cutter(entry_angle):
    """One blind L-groove in the bore: down from the rim, clockwise along the run, up into the pocket."""
    r_from, r_to = inner_r - 1, inner_r + GROOVE_DEPTH
    pocket_angle = entry_angle - TURN
    entry = radial_box(slot_w, r_from, r_to, run_z, body_height + 1, entry_angle)
    # Flare: a V in the tangential/Z plane, slot_w wide at ENTRY_CHAMFER below the rim, 45 degree
    # sides running up past the rim, extruded radially through the groove
    half, top = slot_w / 2, body_height + 1
    flare_plane = Plane(origin=(r_from, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    flare_shape = Polygon((-half, top - ENTRY_CHAMFER - 1), (half, top - ENTRY_CHAMFER - 1),
                          (half + ENTRY_CHAMFER + 1, top), (-half - ENTRY_CHAMFER - 1, top),
                          align=None)
    entry += Rot(0, 0, entry_angle) * extrude(flare_plane * flare_shape, amount=r_to - r_from)
    run_section = Plane.XZ * Pos((r_from + r_to) / 2, run_z) * Rectangle(r_to - r_from, slot_w)
    run = Rot(0, 0, pocket_angle) * revolve(run_section, Axis.Z, TURN)
    ends = radial(slot_w / 2, r_from, r_to, run_z, entry_angle) + radial(
        slot_w / 2, r_from, r_to, run_z, pocket_angle)
    pocket = radial_box(slot_w, r_from, r_to, run_z, run_z + HOOK, pocket_angle) + radial(
        slot_w / 2, r_from, r_to, run_z + HOOK, pocket_angle)
    return entry + run + ends + pocket


def make_body():
    body = up(Cylinder, body_r, body_height)
    body -= up(Cylinder, inner_r, body_height, z=FLOOR)

    for angle in (0, 180):
        body -= slot_cutter(angle)

    # Round the rail corners: the radial edges where the run's roof meets the entry and the
    # pocket. They're the only straight edges at the roof's height.
    roof_z = run_z + slot_w / 2
    rail_corners = body.edges().filter_by(GeomType.LINE).filter_by(
        lambda e: abs(e.start_point().Z - roof_z) < 0.01 and abs(e.end_point().Z - roof_z) < 0.01)
    assert len(rail_corners) == 4, f"expected 4 rail corners, found {len(rail_corners)}"
    body = fillet(rail_corners, RAIL_CORNER_R)

    # Dispensing hole through the -Y side, centred on the cavity, clear of the slots
    hole_z = FLOOR + CAVITY_DEPTH / 2
    body -= extrude(Plane.XZ * Pos(0, hole_z) * Circle(HOLE_D / 2), amount=body_r + 2)

    # Break the bed edge so elephant's foot doesn't flare it
    body = chamfer(body.edges().group_by(Axis.Z)[0], 0.6)
    return body


def make_lid():
    """Lid in its own coordinates (z = 0 at the cone bottom), posts on the X axis."""
    plug = up(Cylinder, plug_r, PLUG_LENGTH, z=-PLUG_LENGTH)
    plug = chamfer(plug.edges().group_by(Axis.Z)[0], 1.0)   # lead-in, and kills elephant's foot
    lid = plug + up(Cone, plug_r, body_r, cone_rise) + up(Cylinder, body_r, CAP, z=cone_rise)

    # Posts reach to 0.4 short of the groove bottom
    for angle in (0, 180):
        lid += radial(POST_D / 2, plug_r - 1, inner_r + GROOVE_DEPTH - 0.4, post_z, angle)

    # Eyelet arch: post + round head in the XZ plane, EYELET_THICK along Y
    outer_r = EYELET_HOLE_D / 2 + EYELET_RING
    hole_z = lid_top_z + EYELET_LIFT + EYELET_HOLE_D / 2
    head = (Pos(0, hole_z) * Circle(outer_r)
            + Pos(0, (lid_top_z - 1 + hole_z) / 2) * Rectangle(2 * outer_r, hole_z - lid_top_z + 1))
    lid += extrude(Plane.XZ.offset(-EYELET_THICK / 2) * head, amount=EYELET_THICK)
    base_edges = lid.edges().filter_by(
        lambda e: abs(e.center().Z - lid_top_z) < 0.01 and e.length < 3 * outer_r)
    lid = fillet(base_edges, EYELET_FILLET)

    lid -= extrude(Plane.XZ.offset(-EYELET_THICK) * Pos(0, hole_z) * Circle(EYELET_HOLE_D / 2),
                   amount=2 * EYELET_THICK)
    return lid


def placed(lid, turn, z):
    """Lid on the body: turned `turn` degrees (0 = posts at the entries), cone bottom at z."""
    return Rot(0, 0, turn) * Pos(0, 0, z) * lid


body = make_body()
lid = make_lid()
locked = placed(lid, -TURN, lid_locked_z)

export_stl(body, str(OUT / "body.stl"))
export_stl(Pos(0, 0, PLUG_LENGTH) * lid, str(OUT / "lid.stl"))   # plug end on the bed
# Both on one plate, 10 mm apart, to print together
export_stl(Compound([body, Pos(2 * body_r + 10, 0, PLUG_LENGTH) * lid]), str(OUT / "plate.stl"))
export_step(Compound([body, locked]), str(OUT / "assembly.step"))

print(f"body: OD {2 * body_r:.2f}  height {body_height:.1f}  volume {body.volume / 1000:.1f} cm3")
print(f"lid:  height {PLUG_LENGTH + lid.bounding_box().max.Z:.1f}  volume {lid.volume / 1000:.1f} cm3")
print(f"overall assembled length {locked.bounding_box().max.Z:.1f}")

# Fit check. The open path must be clear; the locked lid must be trapped.
pushed_z = body_height + pushed_cone_z
checks = [
    ("locked", -TURN, lid_locked_z, False),
    ("pushed down in pocket column", -TURN, pushed_z, False),
    ("halfway along the run", -TURN / 2, pushed_z, False),
    ("at the entry", 0, pushed_z, False),
    ("lifting out the entry", 0, pushed_z + RUN_DEPTH, False),
    ("locked, lifted 1 mm (must hit)", -TURN, lid_locked_z + 1, True),
    ("locked, turned back 10 deg (must hit)", -TURN + 10, lid_locked_z, True),
    ("not pushed, turned at the entry (must hit)", -10, pushed_z + HOOK + 1, True),
]
for name, turn, z, should_hit in checks:
    hit = (body & placed(lid, turn, z)).volume
    ok = (hit > 0.01) == should_hit
    print(f"{'ok  ' if ok else 'FAIL'} {name}: overlap {hit:.2f} mm3")
