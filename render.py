"""Render the README images into images/ with f3d (apt install f3d)."""

import subprocess
import tempfile
from pathlib import Path

from build123d import *

OUT = Path(__file__).parent
src = (OUT / "poop_tube.py").read_text()
exec(src[:src.index("body = make_body()")])

body = make_body()
lid = make_lid()
# Groove close-up: the half of the wall centred on one groove (entry at 0, pocket at -TURN),
# top 22 mm only, seen from inside
keep = Rot(0, 0, -TURN / 2) * Box(100, 100, 22, align=(Align.MIN, Align.CENTER, Align.MAX))

ORANGE = "1,0.55,0.1"
BLUE = "0.25,0.5,0.9"
views = [
    ("assembled", body + placed(lid, -TURN, lid_locked_z), ORANGE, "0.45,1,-0.35", 1.0),
    ("lid", Pos(0, 0, PLUG_LENGTH) * lid, BLUE, "-1,0.6,-0.5", 1.0),
    ("grooves", body & (Pos(0, 0, body_height + 0.01) * keep), ORANGE, "0.75,-0.1,-0.65", 1.3),
]

(OUT / "images").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for name, part, color, direction, zoom in views:
        stl = Path(tmp) / f"{name}.stl"
        export_stl(part, str(stl))
        subprocess.run([
            "f3d", str(stl), "--up=+Z", "--resolution=1000,1000", "--background-color=1,1,1",
            "-a", "--light-intensity=1.6", f"--color={color}", f"--camera-direction={direction}",
            f"--camera-zoom-factor={zoom}", f"--output={OUT / 'images' / f'{name}.png'}",
        ], check=True, stderr=subprocess.DEVNULL)
        print(OUT / "images" / f"{name}.png")
