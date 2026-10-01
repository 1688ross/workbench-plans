"""Isometric renders: final-look views and one cumulative view per build step."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svg import SVG, Iso
from model import *
from parts import STEPS

OUT = os.path.join(os.path.dirname(__file__), "..", "renders")
COL = {  # kind: (top, front/south, side/west)
    "ply":    ("#f3e6c9", "#e6d3ae", "#d4bf98"),
    "mdf":    ("#e0d2b4", "#cdbd9c", "#bcab8a"),
    "maple":  ("#e2c48f", "#c9a86a", "#b8975c"),
    "top":    ("#e6c992", "#cfae72", "#bd9d63"),
    "dark":   ("#3a3d43", "#2f3136", "#25272b"),
    "front":  ("#2b2d31", "#25272b", "#1f2124"),
    "toe":    ("#1a1b1e", "#151618", "#111214"),
    "duct":   ("#fb923c", "#f97316", "#ea580c"),
    "vac":    ("#fcd34d", "#fbbf24", "#f59e0b"),
    "elec":   ("#fef08a", "#facc15", "#eab308"),
    "steel":  ("#b0b5bd", "#8d939c", "#6b7078"),
    "saw":    ("#ddd6fe", "#c4b5fd", "#a78bfa"),
    "hood":   ("#8b5cf6", "#7c3aed", "#6d28d9"),
    "plenum": ("#dbeafe", "#bfdbfe", "#93c5fd"),
    "laser":  ("#cbd5e1", "#94a3b8", "#64748b"),
    "well":   ("#fde68a", "#fcd34d", "#fbbf24"),
    "red":    ("#f87171", "#ef4444", "#dc2626"),
    "grey":   ("#e5e7eb", "#d1d5db", "#b7bcc4"),
    "glass":  ("#f8fafc", "#e2e8f0", "#cbd5e1"),
    "shell":  ("#3a3d43", "#2f3136", "#25272b"),
    "hole":   ("#1f2124", "#1f2124", "#1f2124"),
}

class Scene:
    def __init__(self): self.boxes = []
    def add(self, step, kind, x0, x1, y0, y1, z0, z1, label=None, lpos=None):
        self.boxes.append(dict(step=step, kind=kind, b=(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)), label=label, lpos=lpos))

def carcass_boxes(S, step, key, c):
    x0, x1, y0, y1, z0, z1 = c["x0"], c["x1"], c["y0"], c["y1"], c["z0"], c["z1"]
    f = c["face"]; t = PLY
    if f in ("W", "E"):   # sides are E-W panels at y0 and y1
        S.add(step, "ply", x0, x1, y0, y0 + t, z0, z1); S.add(step, "ply", x0, x1, y1 - t, y1, z0, z1)
        S.add(step, "ply", x0, x1, y0 + t, y1 - t, z0, z0 + t); S.add(step, "ply", x0, x1, y0 + t, y1 - t, z1 - t, z1)
        bx = (x1 - 0.25, x1) if f == "W" else (x0, x0 + 0.25)
        S.add(step, "ply", bx[0], bx[1], y0, y1, z0, z1)
    else:
        S.add(step, "ply", x0, x0 + t, y0, y1, z0, z1); S.add(step, "ply", x1 - t, x1, y0, y1, z0, z1)
        S.add(step, "ply", x0 + t, x1 - t, y0, y1, z0, z0 + t); S.add(step, "ply", x0 + t, x1 - t, y0, y1, z1 - t, z1)
        S.add(step, "ply", x0, x1, y1 - 0.25, y1, z0, z1)

def build_scene(hero=False, saw_up=False, leaves_up=False, well_open=False, tray_out=False):
    S = Scene()
    # base shell (used when internals are hidden)
    S.add(4, "shell", BASE["x0"], BASE["x1"], BASE["y0"], BASE["y1"], PLINTH_H, TOP_UNDER)
    S.add(4, "shell", MOTOR_BAY["x0"], MOTOR_BAY["x1"], MOTOR_BAY["y0"], MOTOR_BAY["y1"] + 0.01, PLINTH_H, TOP_UNDER)
    # 1 plinth
    for (x0, x1, y0, y1) in [(4, 4.75, 4, 94), (64.25, 65, 4, 94), (4, 34, 93.25, 94), (34, 64, 79.25, 80), (4, 18, 4, 4.75), (50, 65, 4, 4.75),
                             (18, 18.75, 4, 46), (49.25, 50, 4, 46), (4, 65, 45.25, 46), (4, 41, 65.25, 66), (4, 65, 79.25, 80)]:
        S.add(1, "toe", x0, x1, y0, y1, 0.75, PLINTH_H)
    for (x, y) in [(5, 5), (63, 5), (5, 93), (63, 93), (5, 46), (63, 46), (5, 66), (63, 80), (18.5, 5), (49.5, 5)]:
        S.add(1, "steel", x - 0.9, x + 0.9, y - 0.9, y + 0.9, 0, 0.75)
    # 2 carcasses
    for key, c in CABS.items(): carcass_boxes(S, 2, key, c)
    S.add(2, "ply", 50, 68, 29.25, 30, 12.75, TOP_UNDER)                # SE divider
    S.add(2, "ply", 55, 55.75, 1, 80, 4, 12)                            # spine wall
    S.add(2, "ply", 50, 68, 76, 80, 12, 12.75)                          # leg lid
    S.add(2, "ply", 46, 68, 52, 52.75, 12.75, TOP_UNDER); S.add(2, "ply", 46, 68, 71.25, 72, 12.75, TOP_UNDER)   # router box partitions
    S.add(2, "ply", 34, 64, 79.25, 80, 4, TOP_UNDER); S.add(2, "ply", 63.25, 64, 80, 95, 4, TOP_UNDER)            # motor bay walls
    S.add(2, "ply", 64, 68, 94.25, 95, 4, TOP_UNDER); S.add(2, "ply", 67.25, 68, 80, 95, 4, TOP_UNDER)
    S.add(2, "ply", 41, 41.75, 66, 80, 4, 26.5); S.add(2, "ply", 41, 46, 46, 46.75, 4, TOP_UNDER)                  # gap walls
    # 3 plenum, spacer, well, vise pad
    p = PLENUM
    S.add(3, "plenum", p["x0"], p["x1"], p["y0"], p["y1"], p["z0"], p["z1"])
    S.add(3, "ply", 1, 34, 66, 80, 24, 26.5)
    w = LASER_WELL
    S.add(3, "well", w["x0"] - PLY, w["x1"] + PLY, w["y0"] - PLY, w["y1"] + PLY, 24, TOP_UNDER)
    fb = FACE_VISE["block"]; S.add(3, "maple", fb["x0"], fb["x1"], fb["y0"], fb["y1"], fb["z0"], TOP_UNDER)
    # 4 assembly: band panels + lift-bay front + utility cover
    S.add(4, "dark", 1, 1.75, 46, 66, 26.5, TOP_UNDER); S.add(4, "dark", 1, 1.75, 66, 95, 24, TOP_UNDER)
    S.add(4, "dark", 67.25, 68, 76, 80, 12, TOP_UNDER)
    # 5 ducts
    S.add(5, "duct", 50.5, 54.5, 2, 78, 4.5, 8.5); S.add(5, "duct", 50.5, 68, 76, 80, 4.5, 8.5)
    S.add(5, "vac", 51.5, 53.5, 2, 79.5, 9, 11); S.add(5, "vac", 51.5, 68, 78.5, 80.5, 9, 11)
    S.add(5, "duct", 55, 60, 60, 64, 4.5, 8.5); S.add(5, "duct", 56, 60, 60, 64, 8.5, 13.5)      # router drop
    S.add(5, "duct", 41.5, 45.5, 68, 72, 4.5, 31); S.add(5, "duct", 40, 45.5, 68, 72, 27, 31)     # plenum riser
    S.add(5, "duct", 46, 50.5, 28, 32, 4.5, 8.5); S.add(5, "duct", 46, 50.5, 78, 82, 4.5, 8.5)    # miter + saw branches
    S.add(5, "duct", 52.5 - 2, 52.5 + 2, 1, 2, 4.5, 8.5)                                          # floor sweep
    for (x, y, z, sz) in [(52.5, 5, 8.5, 4), (52.5, 30, 8.5, 4), (52.5, 62, 8.5, 4), (52.5, 70, 8.5, 4), (52.5, 78, 8.5, 4)]:
        S.add(5, "red", x - 2.5, x + 2.5, y - 0.6, y + 0.6, z, z + 3.5)
    # 6 electrical
    S.add(6, "elec", 60, 66, 76.5, 79.5, 14, 16); S.add(6, "elec", 66.5, 68, 76.5, 79.5, 18, 22.5)
    S.add(6, "elec", 56.5, 58.5, 2, 78, 12.75, 13.75)                                             # raceway on spine lid
    S.add(6, "elec", 60.5, 62, 63, 66, 26, 28); S.add(6, "elec", 49.2, 50, 36, 40, 12, 15)          # router + miter outlets
    S.add(6, "elec", 1.75, 2.5, 50, 58, 30.5, 32.25); S.add(6, "elec", 56, 64, 1.75, 2.5, 30.5, 32.25)   # flush strips
    S.add(6, "elec", 66.5, 68, 68, 74, 30.5, 32.25)
    # 7 top laminate + doubler
    S.add(7, "mdf", 0, 69, 0, 96, TOP_UNDER, TOP_UNDER + PLY); S.add(7, "top", 0, 69, 0, 96, TOP_UNDER + PLY, TOP_HEIGHT)
    S.add(7, "ply", DOUBLER["x0"], DOUBLER["x1"], DOUBLER["y0"], DOUBLER["y1"], TOP_UNDER - PLY, TOP_UNDER)
    # 8 edging, beam, lip
    S.add(8, "maple", -1.5, 0, -1.5, 96, TOP_UNDER, TOP_HEIGHT); S.add(8, "maple", 69, 70.5, -1.5, 96, TOP_UNDER, TOP_HEIGHT)
    S.add(8, "maple", -1.5, 70.5, -1.5, 0, TOP_UNDER, TOP_HEIGHT); S.add(8, "maple", 0, 69, 96, 97.5, TOP_UNDER, TOP_HEIGHT)
    S.add(8, "maple", 0, 69, 97.5, 100.5, TOP_HEIGHT - 0.5, TOP_HEIGHT)                            # lip
    S.add(8, "maple", 28, 68, 94.5, 96, 30.25, TOP_UNDER)                                          # beam
    # 9 router station (surface details)
    rp = ROUTER_PLATE
    S.add(9, "steel", rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, TOP_HEIGHT - 0.05, TOP_HEIGHT + 0.05)
    for yy in ROUTER_TRACKS["fence_y"]: S.add(9, "dark", ROUTER_TRACKS["fence_x"][0], ROUTER_TRACKS["fence_x"][1], yy - 0.375, yy + 0.375, TOP_HEIGHT - 0.05, TOP_HEIGHT + 0.05)
    S.add(9, "dark", ROUTER_TRACKS["combo_x"] - 0.5, ROUTER_TRACKS["combo_x"] + 0.5, ROUTER_TRACKS["combo_y"][0], ROUTER_TRACKS["combo_y"][1], TOP_HEIGHT - 0.05, TOP_HEIGHT + 0.05)
    S.add(9, "elec", 55, 60, 54, 70, 22, TOP_UNDER)                                                 # DW618 + lift (inside box)
    # 10 miter flip-top
    F = FLIP; ms = MITER_SAW; ay, az = F["axle_y"], F["axle_z"]; hl = F["core_len"] / 2
    S.add(10, "steel", 17.5, 50.5, ay - 0.5, ay + 0.5, az - 0.5, az + 0.5)                          # axle
    for (x0, x1) in ((18, 19.5), (48.5, 50)):
        for yy in (ay - 11, ay + 11): S.add(10, "maple", x0, x1, yy - 1.25, yy + 1.25, az - 2.5, az - 1)   # rest blocks
    if saw_up:
        S.add(10, "ply", 20, 48, ay - hl, ay + hl, az - 1, az + 1)                                    # core
        S.add(10, "saw", 21, 21 + ms["w"], ay - hl + 1, ay - hl + 1 + ms["base_d"], az + 1, az + 1 + ms["deck"])
        S.add(10, "saw", 21, 45.5, ay - hl + 9, ay - hl + 12, az + 1 + ms["deck"], az + 1 + ms["deck"] + 5)
        S.add(10, "saw", 27, 39, ay - hl + 3, ay - hl + 19, az + 1 + ms["deck"] + 5, az + 1 + ms["h_locked"])
        S.add(10, "hood", MITER_HOOD["x0"], MITER_HOOD["x1"], MITER_HOOD["y0"], MITER_HOOD["y1"], az + 1, az + 1 + MITER_HOOD["h"])
        S.add(10, "hole", HATCH["x0"], HATCH["x1"], HATCH["y0"], HATCH["y1"], TOP_HEIGHT - 0.03, TOP_HEIGHT + 0.03)
    else:
        S.add(10, "ply", 20, 48, ay - hl, ay + hl, az - 1, az + 1)                                    # core
        S.add(10, "top", 21, 47, ay - hl, ay + hl, az + 1, TOP_HEIGHT)                                # flush box up
        S.add(10, "saw", 21, 21 + ms["w"], ay - hl + 1, ay - hl + 1 + ms["base_d"], az - 1 - ms["deck"], az - 1)
        S.add(10, "saw", 27, 39, ay - hl + 3, ay - hl + 19, az - 1 - ms["h_locked"], az - 1 - ms["deck"] - 5)
    for side in (-1, 1):
        if leaves_up:
            x0, x1 = (-1.5 - DROP_LEAF["len"], -1.5) if side < 0 else (70.5, 70.5 + DROP_LEAF["len"])
            S.add(10, "top", x0, x1, DROP_LEAF["y0"], DROP_LEAF["y1"], TOP_UNDER, TOP_HEIGHT)
            S.add(10, "steel", x0 + 2, x1 - 4, DROP_LEAF["y0"] + 2, DROP_LEAF["y0"] + 3, TOP_UNDER - 10, TOP_UNDER)
        else:
            x0, x1 = (-1.5 - 1.5, -1.5) if side < 0 else (70.5, 72)
            S.add(10, "front", x0, x1, DROP_LEAF["y0"], DROP_LEAF["y1"], TOP_UNDER - DROP_LEAF["len"], TOP_UNDER)
    # 11 laser well + tray
    if well_open:
        S.add(11, "well", w["x0"], w["x1"], w["y0"], w["y1"], TOP_HEIGHT - 7 - 0.75, TOP_HEIGHT - 7)
        S.add(11, "laser", w["x0"] - 2, w["x1"] + 2, w["y0"] - 4, w["y1"] + 4, TOP_HEIGHT, TOP_HEIGHT + LASER["h"])
    else:
        S.add(11, "top", w["x0"], w["x1"], w["y0"], w["y1"], TOP_HEIGHT - 0.02, TOP_HEIGHT + 0.02)
    if tray_out:
        S.add(11, "ply", -28, 2, 67, 94, 15, 15.75); S.add(11, "laser", -26, 0, 68, 91, 15.75, 15.75 + LASER["h"])
    else:
        S.add(11, "laser", 3, 29, 68, 91, 15.5, 15.5 + LASER["h"])
    # 12 fronts
    for (f, a0, a1, z0, z1, kind, label) in FRONTS:
        k = "front"
        if f == "S": S.add(12, k, a0 + 0.06, a1 - 0.06, 0.25, 1.0, z0 + 0.06, z1 - 0.06)
        elif f == "W": S.add(12, k, 0.25, 1.0, a0 + 0.06, a1 - 0.06, z0 + 0.06, z1 - 0.06)
        elif f == "E": S.add(12, k, 68.0, 68.75, a0 + 0.06, a1 - 0.06, z0 + 0.06, z1 - 0.06)
    S.add(12, "red", 66.5, 68.75, 68, 71, 27.5, 29.5)                                             # router paddle
    S.add(12, "red", 40, 44, 0.25, 1.0, 27, 29)                                                    # miter paddle
    # 13 vise, dogs, cradles, LED
    S.add(13, "steel", -3.5, -1.5, FACE_VISE["y0"], FACE_VISE["y1"], TOP_HEIGHT - 9, TOP_HEIGHT - 0.1)
    S.add(13, "steel", -7, -3.5, 88.5, 89.5, TOP_HEIGHT - 5.5, TOP_HEIGHT - 4.5)
    S.add(13, "elec", -1.5, 70.5, -1.5, 96, TOP_UNDER - 0.3, TOP_UNDER)                              # LED strip line under the overhang
    return S

def render(S, path, title, sub, highlight=None, upto=13, mirror=False, W=1200, H=820, scale=4.6, notes=(), dogs=True, hide_internal=False, wireframe_prev=False):
    s = SVG(W, H, "#f6f5f2")
    s.text(20, 30, title, 16, weight="bold"); s.text(20, 48, sub, 11, "#555")
    iso = Iso(s, scale, 520, 665)
    def T(b):
        x0, x1, y0, y1, z0, z1 = b
        if mirror: x0, x1 = 69 - x1, 69 - x0
        return x0, x1, y0, y1, z0, z1
    # floor shadow
    iso.face([(-8, -8, 0), (78, -8, 0), (78, 104, 0), (-8, 104, 0)], "#ebe9e4", "none")
    # table saw ghost in the hero view
    if upto >= 13 and highlight is None:
        sx0, sx1 = (SAW["x0"], SAW["x1"]) if not mirror else (69 - SAW["x1"], 69 - SAW["x0"])
        iso.box(sx0 + 22, sx1 - 8, SAW["y0"] + 2, SAW["y1"] - 2, 0, 32.5, "#b7bcc4", "#8d939c", "#6b7078")
        iso.box(sx0, sx1, SAW["y0"], SAW["y1"], 32.75, TOP_HEIGHT, "#c9ccd1", "#9aa0a8", "#7b8189")
        iso.box(sx0 - 3, sx1 + 3, SAW["y1"], SAW["y1"] + 2.5, 31, 33.5, "#9aa0a8", "#7b8189", "#5f656d")
        bx = SAW["blade_x"] if not mirror else 69 - SAW["blade_x"]
        iso.face([(bx - .1, SAW["y0"] + 8, TOP_HEIGHT), (bx + .1, SAW["y0"] + 8, TOP_HEIGHT), (bx + .1, SAW["y0"] + 18, TOP_HEIGHT + 3), (bx - .1, SAW["y0"] + 18, TOP_HEIGHT + 3)], "#111", "#111")
    def internal(b):
        x0, x1, y0, y1, z0, z1 = b["b"]
        return x0 >= BASE["x0"] - 0.01 and x1 <= BASE["x1"] + 0.01 and y0 >= BASE["y0"] - 0.01 and y1 <= BASE["y1"] + 0.01 and z1 <= TOP_UNDER + 0.01 and b["kind"] not in ("shell", "toe", "steel")
    boxes = [b for b in S.boxes if b["step"] <= upto]
    if hide_internal:
        boxes = [b for b in boxes if not internal(b) or b["step"] == highlight and highlight not in (12,)]
        boxes = [b for b in boxes if not (b["kind"] == "steel" and internal(b))]
    else:
        boxes = [b for b in boxes if b["kind"] != "shell"]
    boxes.sort(key=lambda b: -(T(b["b"])[1] + T(b["b"])[3] - T(b["b"])[4]))   # far first
    for b in boxes:
        x0, x1, y0, y1, z0, z1 = T(b["b"])
        if highlight is not None and b["step"] != highlight:
            if wireframe_prev:
                iso.box(x0, x1, y0, y1, z0, z1, "none", "none", "none", stroke="#b8bcc4", sw=0.5); continue
            c = COL["grey"] if b["kind"] not in ("toe", "front", "dark", "shell") else ("#d1d5db", "#c4c8cf", "#b1b6bd")
            stroke = "#a1a1aa"
        else:
            c = COL[b["kind"]]; stroke = "#333"
        iso.box(x0, x1, y0, y1, z0, z1, c[0], c[1], c[2], stroke=stroke, sw=0.6)
    if dogs and upto >= 7 and (highlight in (None, 7, 13)):
        g = DOG_GRID
        for i in range(int((g["x1"] - g["x0"]) / g["pitch"]) + 1):
            for j in range(int((g["y1"] - g["y0"]) / g["pitch"]) + 1):
                x = g["x0"] + i * g["pitch"]; x = 69 - x if mirror else x
                iso.dot_top(x, g["y0"] + j * g["pitch"], TOP_HEIGHT + 0.1, 0.5, "#3b2a12")
        for dx in (-SAW["slot_offset"], SAW["slot_offset"]):
            gx = SAW["blade_x"] + dx; gx = 69 - gx if mirror else gx
            iso.line((gx, 96, TOP_HEIGHT + 0.1), (gx, 96 - OUTFEED_GROOVE["len"], TOP_HEIGHT + 0.1), "#6b5330", 1.4)
    # notes
    for i, n in enumerate(notes): s.text(20, H - 20 - (len(notes) - 1 - i) * 16, n, 10, "#444")
    s.save(path)

def hero_views():
    S = build_scene(hero=True)
    render(S, os.path.join(OUT, "10-final-look-sw.svg"), "FINAL LOOK  -  from the south-west, everything stowed",
           "Charcoal Baltic-birch fronts with routed finger pulls, maple-edged 1-1/2\" top at 34-3/4\". Miter saw hangs upside down under its flush box; only the router plate, T-track, dog field and vise show.",
           notes=["West face (left): face vise, dog field, hand-tool drawers, laser tray.  South face (right): long drawers, two flip-bay doors with the miter paddle, clamp-rack pull-out.",
                  "Drop-leaf wings hang flat against both ends. LED strip under the top overhang. The table saw sits against the far (north) edge."], hide_internal=True)
    S2 = build_scene(hero=True, saw_up=True, leaves_up=True, well_open=True)
    render(S2, os.path.join(OUT, "11-final-look-in-use.svg"), "FINAL LOOK  -  in use: miter saw flipped up, drop-leaves up, laser well open",
           "The platform flipped: DWS779 deck flush with the top, hood behind it. Drop-leaves add 24\" of support each side. The laser sits over the open well for rotary work.",
           notes=["The flush box now hangs under the saw. Bay doors are closed again; the 4\" quick-connect and the plug are made inside the bay."], hide_internal=True)
    S3 = build_scene(hero=True)
    render(S3, os.path.join(OUT, "12-final-look-ne.svg"), "FINAL LOOK  -  from the north-east: router station face and outfeed edge",
           "Mirrored view. East face: router-bit pull-out, gasketed router doors with paddle switch, utility column with the 4\" and 2-1/2\" ports and the 20 A inlet. North edge: bridge lip over the saw's rear rail.",
           mirror=True, notes=["The motor bay recess is behind the saw and not visible here; see Sheet 5 and Section C-C."], hide_internal=True)

def step_views():
    subs = {
        1: "Ladder frame of 4\" x 3/4\" Baltic-birch ribs on ten 1,000 lb levelling feet; open under the flip bay (front centre). Recessed 3\" on the S, E, W faces.",
        2: "Five frameless carcasses (SW, SE, W1, W2, E2), the spine duct wall, motor-bay walls, service-gap walls and router-box partitions. SE and E2 have raised floors over the spine.",
        3: "Sealed downdraft plenum on W1/W2 (blue), spacer frame, laser-well box and the laminated vise pad.",
        4: "Carcasses set on the plinth and screwed together; band panels and the utility cover close the faces.",
        5: "4\" main (orange) and 2-1/2\" vac (amber) trunks in the spine, the leg to the east ports, and the five 4\" drops with blast gates (red).",
        6: "Inlet and main strip in the utility column, raceway along the spine lid, tool outlets in the router box and flip bay (through the seat switch), flush strips on three faces.",
        7: "Two-layer top glued up (3/4 BB over 3/4 MDF, seams staggered) with the doubler under the dog field; hatch, well, plate and groove cut-outs made.",
        8: "Top set and screwed from below; maple edging, outfeed beam across the motor bay, bridge lip over the saw's rear rail.",
        9: "Router lift plate recess, two fence T-tracks, combo track, router installed in the sealed box, fence vac port.",
        10: "Flip-top platform on its 1\" axle: core, flush box, saw and hood; rest blocks, plungers, toggle clamps and the seat switch on the bay walls; drop-leaf wings.",
        11: "Laser well insert and movable floor; laser tray on 30\" heavy slides in W2.",
        12: "Drawer boxes and all fronts: long drawers, flip-bay doors, clamp rack, bit pull-out, router doors, W1/W2 drawers, laser tray front, paddle switches.",
        13: "Face vise, dog-hole accessories, pipe-clamp cradles, LED strip and finish.",
    }
    for st in range(1, 14):
        S = build_scene(saw_up=(st == 10), leaves_up=(st == 10), well_open=(st == 11), tray_out=(st == 11))
        render(S, os.path.join(OUT, f"6{st:02d}-step-{st:02d}.svg"), f"BUILD STEP {st}  -  {STEPS[st]}", subs[st], highlight=st, upto=st,
               mirror=(st in (5, 6, 9)), hide_internal=(st >= 7), wireframe_prev=(st in (5, 6)),
               notes=[("Mirrored view from the north-east so the east face and spine are visible." if st in (5, 6, 9) else "View from the south-west.") + "  Parts added in this step are in colour; earlier work is grey" + (" wireframe." if st in (5, 6) else ".")])

if __name__ == "__main__":
    hero_views(); step_views(); print("iso rendered")
