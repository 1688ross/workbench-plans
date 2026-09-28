"""Every piece of wood in the bench, computed from tools/model.py.

Part(id, name, step, material, thick, length, width, qty, grain, note)
  material: BB34 (3/4" Baltic birch), BB12, BB14, MDF34, MAPLE (hard maple solid), PINE2x4
  grain: 'L' length along the sheet's 96" axis, 'W' across, 'A' any
Steps match docs/04-build-guide.md.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from model import *

class Part:
    def __init__(self, pid, name, step, material, thick, length, width, qty=1, grain="A", note=""):
        self.id, self.name, self.step, self.material = pid, name, step, material
        self.thick, self.length, self.width, self.qty = thick, round(length, 3), round(width, 3), qty
        self.grain, self.note = grain, note
    @property
    def area(self): return self.length * self.width * self.qty
    def __repr__(self): return f"{self.id} {self.name} {self.length}x{self.width} x{self.qty}"

STEPS = {
    1: "Plinth and levelling feet",
    2: "Carcasses (base cabinets, spine, bays)",
    3: "Downdraft plenum, laser well and vise block",
    4: "Assemble the base",
    5: "Dust ducting",
    6: "Electrical",
    7: "Laminate and machine the top",
    8: "Fit the top, outfeed lip and edging",
    9: "Router station",
    10: "Miter-saw lift station",
    11: "Laser well and tray",
    12: "Drawers, pull-outs and fronts",
    13: "Vise, dogs, lighting and finish",
}

def carcass(parts, key, c, prefix, extra_partitions=()):
    """Frameless carcass from 3/4 BB: two sides full height, top+bottom between, 1/4 back overlay."""
    if c["face"] in ("W", "E"):
        width = c["y1"] - c["y0"]; depth = c["x1"] - c["x0"]
    else:
        width = c["x1"] - c["x0"]; depth = c["y1"] - c["y0"]
    height = c["z1"] - c["z0"]
    parts.append(Part(f"{prefix}-S", f"{key} side", 2, "BB34", PLY, depth, height, 2, "L", f"cabinet {key}: {c['label']}"))
    parts.append(Part(f"{prefix}-TB", f"{key} top/bottom", 2, "BB34", PLY, width - 2 * PLY, depth, 2, "A"))
    parts.append(Part(f"{prefix}-BK", f"{key} back", 2, "BB14", PLY_QTR, width, height, 1, "A", "overlay back, glued + screwed"))
    for (pn, plen, pw, n) in extra_partitions:
        parts.append(Part(f"{prefix}-{pn}", f"{key} {pn}", 2, "BB34", PLY, plen, pw, n, "A"))
    return width, depth, height

def drawer(parts, pid, name, open_w, open_h, depth, step=12, note=""):
    """1/2 BB box on side-mount full-extension slides (1/2" per side); 1/4 bottom in a groove; 3/4 BB front."""
    bw = open_w - 1.0; bh = open_h - 1.5
    parts.append(Part(f"{pid}-DS", f"{name} box side", step, "BB12", PLY_HALF, depth, bh, 2, "L"))
    parts.append(Part(f"{pid}-DF", f"{name} box front/back", step, "BB12", PLY_HALF, bw - 2 * PLY_HALF, bh, 2, "A"))
    parts.append(Part(f"{pid}-DB", f"{name} bottom", step, "BB14", PLY_QTR, depth - 0.5, bw - 0.5, 1, "A", "in 1/4 groove"))
    parts.append(Part(f"{pid}-FR", f"{name} front", step, "BB34", PLY, open_w - 0.125, open_h - 0.125, 1, "L", "full overlay, 1/8 reveal; 30 deg finger-pull chamfer on top edge" + (" " + note if note else "")))

def build():
    P = []
    # ---------------------------------------------------------------- 1 plinth
    ribs = [("W rail", 90.0), ("E rail", 90.0), ("N rail (W of bay)", 30.0), ("N rail (E of bay)", 1.0 + 0.0), ("bay S rail", 30.0),
            ("S rail W", 14.0), ("S rail E", 15.0), ("lift bay side rails", 42.0), ("cross rib y46", 61.0), ("cross rib y66", 37.0), ("cross rib y80", 61.0)]
    for n, L in ribs:
        if L < 2: continue
        P.append(Part("PL-" + n.split()[0] + str(len(P)), f"plinth {n}", 1, "BB34", PLY, L, 4.0, 2 if "lift bay" in n else 1, "L", "4\" tall rib, glued and screwed; toe recess 3\""))
    P.append(Part("PL-KICK", "toe-kick face boards (W, S x2, E)", 1, "BB34", PLY, 90.0, 4.0, 3, "L", "paint black; one 90\" board is cut into the two south pieces"))
    # ---------------------------------------------------------------- 2 carcasses
    carcass(P, "SW", CABS["SW"], "SW", [("leaf-slot divider", 45.0, TOP_UNDER - 4.0, 1)])
    carcass(P, "SE", CABS["SE"], "SE", [("rack/bit divider", 18.0 - 2 * PLY, TOP_UNDER - 12.75, 1)])
    carcass(P, "W1", CABS["W1"], "W1")
    carcass(P, "W2", CABS["W2"], "W2")
    carcass(P, "E2", CABS["E2"], "E2", [("router-box partition", 22.0 - PLY, TOP_UNDER - 12.75, 2)])
    P.append(Part("SP-WALL", "spine duct inner wall (x=55)", 2, "BB34", PLY, 79.0, 8.0, 1, "L", "forms the 5 x 8 duct chase with the SE/E2 west sides"))
    P.append(Part("SP-LID", "duct leg lid (y 76-80)", 2, "BB34", PLY, 18.0, 4.0, 1, "A"))
    P.append(Part("SP-LOW", "SE/E2 lower side extension (z 4-12.75)", 2, "BB34", PLY, 45.0, 8.75, 2, "L", "closes the spine under the raised floors"))
    P.append(Part("BAY-S", "motor bay south wall (y=80)", 2, "BB34", PLY, 30.0, TOP_UNDER - 4.0, 1, "A"))
    P.append(Part("BAY-E", "motor bay east wall (x=64)", 2, "BB34", PLY, 15.0, TOP_UNDER - 4.0, 1, "A"))
    P.append(Part("BAY-NE", "north-east filler panels (x 64-68)", 2, "BB34", PLY, 15.0, TOP_UNDER - 4.0, 2, "A", "east and north faces of the 4\" column"))
    P.append(Part("GAP-W", "service-gap wall (x=41, y 66-80)", 2, "BB34", PLY, 14.0, 22.5, 1, "A", "supports the plenum floor"))
    P.append(Part("GAP-S", "service-gap closure (y=46, x 41-46)", 2, "BB34", PLY, 5.0, TOP_UNDER - 4.0, 1, "A"))
    P.append(Part("LB-FRONT", "lift-bay front panel (removable)", 2, "BB34", PLY, 32.0, TOP_UNDER - 4.0, 1, "A", "hook-on panel; 10 x 8 pedal flap cut in at the bottom"))
    P.append(Part("W-BAND1", "west band panel over W1 (plenum face)", 2, "BB34", PLY, 20.0, TOP_UNDER - 26.5, 1, "A", "with 6 x 4 plenum clean-out hatch"))
    P.append(Part("W-BAND2", "west band panel over W2", 2, "BB34", PLY, 29.0, TOP_UNDER - 24.0, 1, "A"))
    P.append(Part("E-UTIL", "utility column cover (east face y 76-80)", 2, "BB34", PLY, 4.0, TOP_UNDER - 12.0, 1, "A", "removable; ports and inlet mount here"))
    P.append(Part("E-BACK", "east panel beside motor bay (y 80-95)", 2, "BB34", PLY, 15.0, TOP_UNDER - 4.0, 1, "A"))
    # ---------------------------------------------------------------- 3 plenum, well, vise
    pw = PLENUM["x1"] - PLENUM["x0"]; pd = PLENUM["y1"] - PLENUM["y0"]; ph = PLENUM["z1"] - PLENUM["z0"]
    P.append(Part("PLN-F", "plenum floor", 3, "BB34", PLY, pw, pd, 1, "A", "seal all joints with silicone"))
    P.append(Part("PLN-WL", "plenum long walls", 3, "BB34", PLY, pw, ph - PLY, 2, "A"))
    P.append(Part("PLN-WS", "plenum short walls", 3, "BB34", PLY, pd - 2 * PLY, ph - PLY, 2, "A", "east wall gets the 4\" riser hole"))
    P.append(Part("PLN-SP", "spacer frame over W2 (z 24-26.5)", 3, "BB34", PLY, 33.0, 2.5, 4, "A", "two long, two cut to 12\""))
    ww = LASER_WELL["x1"] - LASER_WELL["x0"]; wd = LASER_WELL["y1"] - LASER_WELL["y0"]
    P.append(Part("WELL-WL", "laser well walls (E-W)", 3, "BB34", PLY, ww + 2 * PLY, TOP_UNDER - 24.0, 2, "A"))
    P.append(Part("WELL-WS", "laser well walls (N-S)", 3, "BB34", PLY, wd, TOP_UNDER - 24.0, 2, "A"))
    P.append(Part("WELL-FL", "laser well floor panel (movable)", 3, "BB34", PLY, ww - 0.125, wd - 0.125, 1, "A", "rests on cleats at 2, 4-1/2 or 7 in. below the top"))
    P.append(Part("WELL-CL", "well cleats", 3, "MAPLE", 0.75, wd, 0.75, 6, "L", "3 pairs, 3/4 x 3/4"))
    P.append(Part("WELL-LG", "well insert ledge", 3, "MAPLE", 0.75, ww + wd, 0.75, 2, "L", "3/4 x 3/4, 1-1/2 below the top surface"))
    P.append(Part("VISE-PAD", "vise mounting pad (3 layers)", 3, "BB34", PLY, 13.0, 12.0, 3, "A", "laminated 2-1/4 thick under the top"))
    P.append(Part("VISE-JAW", "vise jaw liners", 3, "MAPLE", 0.75, 9.0, 5.0, 2, "L"))
    # ---------------------------------------------------------------- 7 top
    P.append(Part("TOP-U1", "top upper layer, west piece (x 0-21)", 7, "BB34", PLY, 96.0, 21.0, 1, "L"))
    P.append(Part("TOP-U2", "top upper layer, east piece (x 21-69)", 7, "BB34", PLY, 96.0, 48.0, 1, "L"))
    P.append(Part("TOP-L1", "top lower layer, west piece (x 0-48)", 7, "MDF34", PLY, 96.0, 48.0, 1, "L"))
    P.append(Part("TOP-L2", "top lower layer, east piece (x 48-69)", 7, "MDF34", PLY, 96.0, 21.0, 1, "L"))
    P.append(Part("TOP-DBL", "doubler / plenum lid under dog field", 7, "BB34", PLY, pw, pd, 1, "A", "drill the dog holes through it with the top"))
    P.append(Part("EDGE-W", "maple edge band, west", 8, "MAPLE", 1.5, 96.0 + 3.0, 1.5, 1, "L", "mitred corners"))
    P.append(Part("EDGE-E", "maple edge band, east", 8, "MAPLE", 1.5, 96.0 + 3.0, 1.5, 1, "L"))
    P.append(Part("EDGE-S", "maple edge band, south", 8, "MAPLE", 1.5, 69.0 + 3.0, 1.5, 1, "L"))
    P.append(Part("EDGE-N", "maple edge band, north (outfeed edge)", 8, "MAPLE", 1.5, 69.0, 1.5, 1, "L", "1/8 bevel on the top corner"))
    P.append(Part("LIP", "bridge lip over the rear fence rail", 8, "MAPLE", BRIDGE_LIP["t"], 69.0, BRIDGE_LIP["w"], 1, "L", "MEASURE the rail first"))
    P.append(Part("BEAM", "outfeed beam across the motor bay", 8, "MAPLE", 1.5, 40.0, 3.0, 1, "L", "glued + screwed under the top, x 28-68"))
    P.append(Part("HATCH-LG", "hatch ledge strips", 7, "MAPLE", 1.0, 42.5, 1.5, 2, "L", "plus two at 27\" from the same stock"))
    P.append(Part("HATCH-LG2", "hatch ledge strips (short)", 7, "MAPLE", 1.0, 27.0, 1.5, 2, "L"))
    P.append(Part("HATCH-BAR", "hatch centre bar (removable)", 7, "MAPLE", 1.5, 29.0, 2.0, 1, "L", "sits in notches in the ledge"))
    # ---------------------------------------------------------------- 10 miter lift
    P.append(Part("LIFT-RL", "sub-platform rails", 10, "PINE2x4", 1.5, 41.0, 3.5, 2, "L", "2x4"))
    P.append(Part("LIFT-RB", "sub-platform ribs", 10, "PINE2x4", 1.5, 25.0, 3.5, 3, "L", "2x4"))
    P.append(Part("LIFT-DK", "sub-platform deck", 10, "BB34", PLY, 41.0, 28.0, 1, "A", "saw bolts through this"))
    P.append(Part("HOOD-BK", "hood back", 10, "BB34", PLY, 28.0, MITER_HOOD["h"], 1, "A"))
    P.append(Part("HOOD-SD", "hood sides", 10, "BB34", PLY, 6.0, MITER_HOOD["h"], 2, "A"))
    P.append(Part("HOOD-FL", "hood sloped floor + top", 10, "BB34", PLY, 28.0, 6.5, 2, "A", "floor slopes to the 4\" port"))
    P.append(Part("LEAF", "drop-leaf wings (BB + MDF laminate)", 10, "BB34", PLY, 24.0, 24.0, 2, "A", "laminate to MDF LEAF-M; edge with maple"))
    P.append(Part("LEAF-M", "drop-leaf wings, MDF layer", 10, "MDF34", PLY, 24.0, 24.0, 2, "A"))
    P.append(Part("LEAF-EDGE", "drop-leaf edging", 10, "MAPLE", 1.5, 26.0, 1.5, 6, "L"))
    P.append(Part("STOP", "lift stop blocks", 10, "MAPLE", 1.5, 4.0, 3.0, 4, "L", "with 3/8 leveling bolts"))
    # ---------------------------------------------------------------- 11 laser tray
    P.append(Part("LT-BASE", "laser tray base", 11, "BB34", PLY, 30.0, 29.0, 1, "A", "on 30\" 100 lb full-extension slides"))
    P.append(Part("LT-SIDE", "laser tray sides", 11, "BB12", PLY_HALF, 30.0, 2.0, 2, "L"))
    P.append(Part("LT-END", "laser tray ends", 11, "BB12", PLY_HALF, 28.0, 2.0, 2, "L"))
    P.append(Part("LT-FR", "laser tray front", 12, "BB34", PLY, 29.0 - 0.125, 9.0 - 0.125, 1, "L", "full overlay"))
    # ---------------------------------------------------------------- 12 drawers & pull-outs
    for (face, a0, a1, z0, z1, kind, label) in FRONTS:
        w = a1 - a0; h = z1 - z0
        if kind == "drawer":
            depth = 36.0 if face in ("S", "W") and w < 25 else 30.0
            drawer(P, label.split()[0], label, w, h, depth)
        elif kind == "door":
            P.append(Part("DOOR-" + label.split()[3], label, 12, "BB34", PLY, w - 0.125, h - 0.125, 1, "L", "full overlay; foam-tape gasket on the carcass"))
        elif kind == "pullout":
            if "bit" in label:
                P.append(Part("BIT-BASE", "bit pull-out base + top", 12, "BB34", PLY, 12.0, 15.0 - 1.0, 2, "A"))
                P.append(Part("BIT-UP", "bit pull-out uprights", 12, "BB34", PLY, 12.0, h - 1.5 - 1.5, 2, "A"))
                P.append(Part("BIT-BRD", "bit boards (drilled 1/4 and 1/2)", 12, "BB34", PLY, 12.0, h - 3.0, 3, "A", "holes at 1-1/2 spacing"))
                P.append(Part("BIT-FR", "bit pull-out front", 12, "BB34", PLY, w - 0.125, h - 0.125, 1, "L"))
            elif "clamp" in label:
                P.append(Part("CR-BASE", "clamp rack base + top", 12, "BB34", PLY, 28.0, w - 1.0, 2, "A"))
                P.append(Part("CR-UP", "clamp rack uprights", 12, "BB34", PLY, 28.0, h - 1.5 - 1.5, 2, "A", "notched for the bars"))
                P.append(Part("CR-BAR", "clamp bars", 12, "MAPLE", 1.5, w - 1.0 - 1.5, 1.5, 4, "L", "F-clamps and bar clamps hang here"))
                P.append(Part("CR-FR", "clamp rack front", 12, "BB34", PLY, w - 0.125, h - 0.125, 1, "L"))
        elif kind == "panel":
            pass  # LB-FRONT listed in step 2
    # ---------------------------------------------------------------- 13 misc
    P.append(Part("CRADLE", "pipe-clamp cradles (dog-hole mounted)", 13, "MAPLE", 1.5, 6.0, 3.0, 6, "L", "3/4 dowel peg glued in; notch for 3/4 pipe"))
    return P

def by_material(parts):
    out = {}
    for p in parts: out.setdefault(p.material, []).append(p)
    return out

if __name__ == "__main__":
    P = build()
    for m, ps in by_material(P).items():
        print(m, len(ps), "part lines,", round(sum(p.area for p in ps) / 144, 1), "sq ft")
