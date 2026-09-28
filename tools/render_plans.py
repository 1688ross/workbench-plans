"""Stage-2 dimensioned drawings: plan, elevations, sections, station details, routing."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from view import View, sheet
from model import *

OUT = os.path.join(os.path.dirname(__file__), "..", "renders")
MAPLE, PLYC, MDFC, DARK, STEEL, ACC = "#e2c48f", "#f1e2c2", "#d9c9a8", "#2f3136", "#9aa0a8", "#c2410c"
GHOST = "stroke-dasharray='4 3'"

def grid_dogs(v, fill="#1d4ed8"):
    g = DOG_GRID
    for i in range(int((g["x1"] - g["x0"]) / g["pitch"]) + 1):
        for j in range(int((g["y1"] - g["y0"]) / g["pitch"]) + 1):
            v.circle(g["x0"] + i * g["pitch"], g["y0"] + j * g["pitch"], g["dia"] / 2, fill=fill, stroke="none")

# ==================================================================== PLAN
def plan():
    k = 6.0; s = sheet("SHEET 1  -  PLAN VIEW (top surface) with base layout below, dashed", "Island 69 x 96 in. North (top of page) is the table-saw side. Blade line, miter slots and outfeed grooves are aligned to the SawStop CNS with the 36\" extension on the west.", 980, 1010)
    v = View(s, k, 120, 900)
    # table saw ghost
    v.rect(SAW["x0"], SAW["x1"], SAW["y0"], SAW["y1"], fill="#e8eaee", stroke="#666", sw=1, extra=GHOST)
    v.rect(SAW["x0"], SAW["ext_x1"], SAW["y0"], SAW["y1"], fill="#f3f4f6", stroke="#666", sw=0.6, extra=GHOST)
    v.line(SAW["blade_x"], SAW["y0"] + 8, SAW["blade_x"], SAW["y0"] + 19, stroke="#111", sw=3)
    for dx in (-SAW["slot_offset"], SAW["slot_offset"]):
        v.line(SAW["blade_x"] + dx, SAW["y0"], SAW["blade_x"] + dx, SAW["y1"], stroke="#555", sw=2)
    v.rect(SAW["x0"] - 4, SAW["x1"] + 3, SAW["y1"], SAW["y1"] + 2.5, fill="#888", stroke="none")
    v.rect(SAW["x0"] - 4, SAW["x1"] + 3, TOP["y1"], SAW["y0"], fill="#888", stroke="none")   # rear rail
    v.label(34, SAW["y1"] - 4, "SawStop CNS + 36\" T-Glide  (operator on this side, feeds south)", size=10, fill="#333")
    v.label(12, SAW["y0"] + 4, "extension table", size=9, fill="#555"); v.label(SAW["blade_x"] + 9, SAW["y0"] + 13, "blade", size=9, fill="#555")
    v.label(34, TOP["y1"] + 0.6, "rear rail  -  bridge lip covers it", size=8, fill="#fff", bg="#555")
    # motor bay + base (dashed)
    v.dashed(BASE["x0"], BASE["x1"], BASE["y0"], BASE["y1"], color="#888")
    v.rect(MOTOR_BAY["x0"], MOTOR_BAY["x1"], MOTOR_BAY["y0"], MOTOR_BAY["y1"], fill="#fee2e2", stroke="#b91c1c", sw=0.8, extra=GHOST)
    v.label(49, 92.5, "MOTOR BAY (recess in base, open to the saw)", size=9, fill="#7f1d1d")
    # top
    v.rect(TOP["x0"], TOP["x1"], TOP["y0"], TOP["y1"], fill="none", stroke="#111", sw=2.2)
    # outfeed grooves
    for dx in (-SAW["slot_offset"], SAW["slot_offset"]):
        gx = SAW["blade_x"] + dx
        v.rect(gx - 0.375, gx + 0.375, TOP["y1"] - OUTFEED_GROOVE["len"], TOP["y1"], fill="#c9c2b2", stroke="#6b5330", sw=0.8)
    v.label(49, 86, "outfeed grooves 3/4 x 3/8, 14\" long", size=8, fill="#6b5330"); v.label(49, 83, "(align to your miter slots)", size=7.5, fill="#6b5330")
    # cabinets dashed + spine
    for key, c in CABS.items():
        v.rect(c["x0"], c["x1"], c["y0"], c["y1"], fill="none", stroke="#9ca3af", sw=0.6, extra=GHOST)
        v.text((c["x0"] + c["x1"]) / 2, (c["y0"] + c["y1"]) / 2 - 1, key, size=9, fill="#6b7280", anchor="middle")
    v.rect(SPINE["x0"], SPINE["x1"], SPINE["y0"], SPINE["y1"], fill="#ffedd5", stroke="#c2410c", sw=0.6, extra=GHOST)
    v.rect(DUCT_LEG["x0"], DUCT_LEG["x1"], DUCT_LEG["y0"], DUCT_LEG["y1"], fill="#ffedd5", stroke="#c2410c", sw=0.6, extra=GHOST)
    v.text(52.5, 20, "duct", size=7.5, fill=ACC, anchor="middle"); v.text(52.5, 17, "spine", size=7.5, fill=ACC, anchor="middle")
    # plenum + dog field
    v.rect(PLENUM["x0"], PLENUM["x1"], PLENUM["y0"], PLENUM["y1"], fill="#eff6ff", stroke="#1d4ed8", sw=0.8, extra=GHOST)
    grid_dogs(v)
    v.label(1.5, 81.6, "plenum below", size=7.5, fill="#1d4ed8", anchor="start")
    v.label(21, 41.2, "81 dog holes 3/4\", 4\" grid  -  clamping station", size=9, fill="#1d4ed8")
    # laser well
    lw = LASER_WELL
    v.rect(lw["x0"], lw["x1"], lw["y0"], lw["y1"], fill="#fef3c7", stroke="#92400e", sw=1.2)
    v.label(23, 85, "LASER WELL 22 x 15", size=9, fill="#78350f"); v.label(23, 81.5, "flush insert; floor drops to 7\"", size=8, fill="#78350f")
    # vise
    fv = FACE_VISE
    v.rect(-2.5, 0, fv["y0"], fv["y1"], fill="#94a3b8", stroke="#334155")
    v.label(-8, 89, "face vise", size=9, fill="#334155")
    # router station
    rp = ROUTER_PLATE; rt = ROUTER_TRACKS
    for yy in rt["fence_y"]: v.rect(rt["fence_x"][0], rt["fence_x"][1], yy - 0.375, yy + 0.375, fill="#4b5563", stroke="none")
    v.rect(rt["combo_x"] - 0.5, rt["combo_x"] + 0.5, rt["combo_y"][0], rt["combo_y"][1], fill="#4b5563", stroke="none")
    v.rect(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, fill="#fff7ed", stroke="#b45309", sw=1.5)
    v.circle(rp["cx"], rp["cy"], 1.75, fill="#fde68a", stroke="#b45309")
    v.rect(ROUTER_BOX["x0"], ROUTER_BOX["x1"], ROUTER_BOX["y0"], ROUTER_BOX["y1"], fill="none", stroke="#b45309", sw=0.8, extra=GHOST)
    v.label(55, 77.2, "fence T-track (E-W)", size=8, fill="#7c2d12"); v.label(55, 46.8, "fence T-track (E-W)", size=8, fill="#7c2d12")
    v.label(57, 58.5, "ROUTER LIFT", size=9, fill="#7c2d12"); v.label(57, 54.5, "plate 9-1/4 x 11-3/4", size=8, fill="#7c2d12")
    v.label(64.5, 44.2, "combo track", size=7.5, fill="#7c2d12")
    v.circle(ROUTER_FENCE_PORT["x"] + 1.5, ROUTER_FENCE_PORT["y"], 1.25, fill="#fff", stroke="#7c2d12"); v.label(78, 65, "2-1/2\" vac port", size=8, fill="#7c2d12")
    # miter hatch
    h = HATCH
    v.rect(h["x0"], h["x1"], h["y0"], h["y1"], fill="#f5f3ff", stroke="#6d28d9", sw=1.4)
    v.line(h["x0"], (h["y0"] + h["y1"]) / 2, h["x1"], (h["y0"] + h["y1"]) / 2, stroke="#6d28d9", sw=1)
    v.rect(LIFT_BAY["x0"], LIFT_BAY["x1"], LIFT_BAY["y0"], LIFT_BAY["y1"], fill="none", stroke="#6d28d9", sw=0.8, extra=GHOST)
    v.label(34, 34, "MITER HATCH 29 x 42-1/2 (two lift-off leaves)", size=9, fill="#4c1d95")
    v.label(34, 12, "DWS779 rises on a scissor lift", size=9, fill="#4c1d95"); v.label(34, 8.5, "fence line E-W, operator south", size=8, fill="#4c1d95")
    v.rect(MITER_HOOD["x0"], MITER_HOOD["x1"], MITER_HOOD["y0"], MITER_HOOD["y1"], fill="none", stroke="#6d28d9", sw=1, extra=GHOST)
    v.label(34, 40.8, "hood (rides with the lift)", size=8, fill="#4c1d95")
    v.rect(LEAF_SLOT["x0"], LEAF_SLOT["x1"], LEAF_SLOT["y0"], LEAF_SLOT["y1"], fill="#ede9fe", stroke="#6d28d9", sw=0.6, extra=GHOST)
    # drop leaves (extended, ghost)
    for (x0, x1) in ((-DROP_LEAF["len"], 0), (TOP["x1"], TOP["x1"] + DROP_LEAF["len"])):
        v.rect(x0, x1, DROP_LEAF["y0"], DROP_LEAF["y1"], fill="#f5f3ff", stroke="#6d28d9", sw=0.8, extra=GHOST)
    v.label(-12, 16, "drop-leaf 24 x 24", size=8, fill="#4c1d95"); v.label(81, 16, "drop-leaf 24 x 24", size=8, fill="#4c1d95")
    v.circle(TOP["x1"] + 2, 78, 1.8, fill="#f97316", stroke="#7c2d12"); v.label(84, 81.5, "4\" + 2-1/2\" ports, 20 A inlet", size=8, fill="#7c2d12")
    # face labels
    v.label(34.5, -6, "SOUTH FACE  -  miter operator, long drawers, clamp rack", size=10, fill="#111")
    v.label(-14, 60, "WEST FACE", size=10, fill="#111"); v.label(-14, 56.5, "hand-work station", size=8.5, fill="#111")
    v.label(84, 60, "EAST FACE", size=10, fill="#111"); v.label(84, 56.5, "router station", size=8.5, fill="#111")
    # dimensions
    v.dim_h(0, 69, -12, "69\"", size=11); v.dim_v(-20, 0, 96, "96\"", size=11)
    v.dim_h(0, SAW["blade_x"], 100.5, "47-1/8\" to blade", size=9)
    v.dim_h(h["x0"], h["x1"], -3, "29\"", size=9); v.dim_v(76, h["y0"], h["y1"], "42-1/2\"", size=9)
    v.dim_v(76, MOTOR_BAY["y0"], MOTOR_BAY["y1"], "15\"", size=9); v.dim_h(MOTOR_BAY["x0"], MOTOR_BAY["x1"], 97.5, "30\" bay", size=9)
    v.dim_h(lw["x0"], lw["x1"], 76, "22\"", size=9); v.dim_v(9, lw["y0"], lw["y1"], "15\"", size=9)
    v.dim_v(-5, DOG_GRID["y0"], DOG_GRID["y1"], "32\"", size=9)
    s.save(os.path.join(OUT, "20-plan.svg"))

# ==================================================================== ELEVATIONS
def face_fronts(v, face, flip=False):
    """draw drawer/door fronts on a face; u = position along face"""
    for (f, a0, a1, z0, z1, kind, label) in FRONTS:
        if f != face: continue
        u0, u1 = (a0, a1) if not flip else (-a1, -a0)
        col = {"drawer": "#25272b", "door": "#25272b", "pullout": "#2b2d31", "panel": "#33363c", "slot": "#111"}[kind]
        v.rect(u0 + 0.0625, u1 - 0.0625, z0 + 0.0625, z1 - 0.0625, fill=col, stroke="#15161a", sw=0.5)
        if kind in ("drawer", "pullout", "door"):
            v.line(u0 + 2, z1 - 1.2, u1 - 2, z1 - 1.2, stroke="#8f949c", sw=1.2)   # finger-pull chamfer line
        v.text((u0 + u1) / 2, (z0 + z1) / 2 - 0.6, label if len(label) < 30 else label.split("(")[0], size=7.5, fill="#c9ccd1", anchor="middle")

def elevation(name, face):
    k = 6.0; L = 69.0 if face in ("S", "N") else 96.0
    s = sheet(f"SHEET {dict(S=2, E=3, W=4, N=5)[face]}  -  {name}", "Base is 33-1/4 tall on a 4\" recessed plinth; top is 1-1/2 thick with 1-1/2 maple edge. Fronts: 3/4 Baltic birch, painted charcoal, routed finger pulls.", 120 + L * k + 160 + (52 * k if face == "S" else 0), 480)
    flip = face in ("W", "N")
    v = View(s, k, 80 + ((L + 3) * k if flip else 0) + (26 * k if face == "S" else 0), 400)   # looking at the west face, north is on the LEFT... we keep +u = right = as the viewer sees it
    # viewer-right axis: S face: +x ; E face: +y ; W face: -y (north on left); N face: -x (east on left)
    def U(a): return -a if flip else a
    base0, base1 = (BASE["x0"], BASE["x1"]) if face in ("S", "N") else (BASE["y0"], BASE["y1"])
    top0, top1 = (TOP["x0"], TOP["x1"]) if face in ("S", "N") else (TOP["y0"], TOP["y1"])
    lo, hi = sorted((U(base0), U(base1)))
    # plinth + base body
    v.rect(lo + TOE_RECESS, hi - TOE_RECESS, 0, PLINTH_H, fill="#111", stroke="none")
    v.rect(lo, hi, PLINTH_H, TOP_UNDER, fill=DARK, stroke="#111", sw=1)
    if face == "N":
        v.rect(U(MOTOR_BAY["x1"]), U(MOTOR_BAY["x0"]), 0, TOP_UNDER, fill="#fee2e2", stroke="#b91c1c", sw=1)
        v.text(U(49), 16, "MOTOR BAY 30 x 15 recess  -  saw motor + 4\" dust hose live here", size=9, fill="#7f1d1d", anchor="middle")
        v.rect(U(MOTOR_BAY["x0"]) - 1.5, U(MOTOR_BAY["x1"]) + 1.5, 30.25, TOP_UNDER, fill=MAPLE, stroke="#7a5c2e")   # beam
        v.text(U(49), 31.6, "outfeed beam 1-1/2 x 3 maple", size=7.5, fill="#4a3a1e", anchor="middle")
    face_fronts(v, face, flip)
    # top slab
    tlo, thi = sorted((U(top0), U(top1)))
    v.rect(tlo, thi, TOP_UNDER, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e", sw=1)
    if face == "N": v.rect(tlo, thi, TOP_HEIGHT - BRIDGE_LIP["t"], TOP_HEIGHT, fill="#c9a86a", stroke="#7a5c2e", sw=0.6)
    # face-specific extras
    if face == "S":
        v.rect(U(LEAF_SLOT["x0"]), U(LEAF_SLOT["x1"]), PLINTH_H, TOP_UNDER, fill="#111", stroke="#333")
        v.rect(U(22), U(32), PLINTH_H, PLINTH_H + 8, fill="#3a3d43", stroke="#111"); v.text(U(27), 7.5, "pedal flap", size=7.5, fill="#c9ccd1", anchor="middle")
        # saw ghost raised
        v.rect(U(22), U(46), TOP_HEIGHT, TOP_HEIGHT + 4, fill="#e9d5ff", stroke="#6d28d9", sw=0.8, extra=GHOST)
        v.rect(U(27), U(41), TOP_HEIGHT + 4, TOP_HEIGHT + MITER_SAW["h_locked"], fill="#e9d5ff", stroke="#6d28d9", sw=0.8, extra=GHOST)
        v.text(U(34), TOP_HEIGHT + 12, "DWS779 raised (ghost)", size=8.5, fill="#4c1d95", anchor="middle")
        for (x0, x1) in ((-DROP_LEAF["len"], 0), (69, 69 + DROP_LEAF["len"])):
            v.rect(U(x0), U(x1), TOP_UNDER, TOP_HEIGHT, fill="#f5f3ff", stroke="#6d28d9", sw=0.8, extra=GHOST)
        v.text(U(-12), TOP_HEIGHT + 3, "drop-leaf up", size=8, fill="#4c1d95", anchor="middle"); v.text(U(81), TOP_HEIGHT + 3, "drop-leaf up", size=8, fill="#4c1d95", anchor="middle")
    if face in ("E", "W"):
        # drop leaf hanging
        v.rect(U(DROP_LEAF["y0"]), U(DROP_LEAF["y1"]), TOP_HEIGHT - 1.5 - DROP_LEAF["len"], TOP_HEIGHT - 1.5, fill="#3b3e44", stroke="#111", sw=0.8)
        v.text(U(16), 20, "drop-leaf (stowed, hangs on piano hinge)", size=7.5, fill="#c9ccd1", anchor="middle")
    if face == "E":
        v.circle(U(78), UTILITY["port4_z"], 2.0, fill="#f97316", stroke="#7c2d12"); v.circle(U(78), UTILITY["port25_z"] + 1, 1.25, fill="#fb923c", stroke="#7c2d12")
        v.rect(U(76.5), U(79.5), UTILITY["inlet_z"], UTILITY["inlet_z"] + 4.5, fill="#facc15", stroke="#713f12")
        v.text(U(78), 25, "utility", size=7.5, fill="#c9ccd1", anchor="middle")
        v.rect(U(66), U(70), 28, 30.5, fill="#dc2626", stroke="#7f1d1d", rx=2); v.text(U(68), 26.5, "router paddle", size=7, fill="#c9ccd1", anchor="middle")
        v.circle(U(62), 31, 1.25, fill="#fff", stroke="#7c2d12")
    if face == "W":
        v.rect(U(FACE_VISE["y0"]), U(FACE_VISE["y1"]), TOP_HEIGHT - 9, TOP_HEIGHT - 0.1, fill="#b5c1d1", stroke="#334155")
        v.circle(U(89), TOP_HEIGHT - 5, 1.1, fill="#64748b", stroke="#1e293b"); v.line(U(89), TOP_HEIGHT - 5, U(89), TOP_HEIGHT - 12, stroke="#1e293b", sw=2.5)
        v.text(U(89), TOP_HEIGHT - 15, "face vise", size=8, fill="#334155", anchor="middle")
        v.rect(U(58), U(50), 30.5, 32.25, fill="#facc15", stroke="#713f12"); v.text(U(54), 28.5, "flush strip + USB", size=7, fill="#c9ccd1", anchor="middle")
    # dims
    v.dim_v(lo - 8, 0, TOP_HEIGHT, "34-3/4\"", size=10)
    v.dim_h(tlo, thi, -8, f"{dim(thi - tlo)}", size=10)
    v.dim_v(hi + 8, TOP_UNDER, TOP_HEIGHT, "1-1/2\"", size=8)
    v.line(lo - 12, 0, hi + 12, 0, stroke="#999", sw=1)
    left = {"S": "WEST", "E": "SOUTH", "W": "NORTH", "N": "EAST"}[face]; right = {"S": "EAST", "E": "NORTH", "W": "SOUTH", "N": "WEST"}[face]
    v.text(lo, -12, f"< {left}", size=9, fill="#666"); v.text(hi, -12, f"{right} >", size=9, fill="#666", anchor="end")
    s.save(os.path.join(OUT, f"2{dict(S=1, E=2, W=3, N=4)[face]}-elevation-{face}.svg"))

# ==================================================================== SECTIONS
def section_A():
    """E-W section at y = 62 through the router plate (looking north)."""
    k = 8.0; s = sheet("SHEET 6  -  SECTION A-A  (east-west at y = 62, through the router lift; looking north)", "Shows the top laminate, downdraft plenum, W1 drawers, service gap with the plenum riser, spine duct under the router cabinet, and the sealed router box.", 120 + 69 * k + 120, 460)
    v = View(s, k, 80, 400)
    # base cut parts
    v.rect(BASE["x0"] + TOE_RECESS, BASE["x1"] - TOE_RECESS, 0, PLINTH_H, fill="#333", stroke="#111")
    # W1 cabinet at y=62: sides are N-S so we see top/bottom + drawers
    c = CABS["W1"]
    v.rect(c["x0"], c["x1"], c["z0"], c["z0"] + PLY, fill=PLYC, stroke="#333"); v.rect(c["x0"], c["x1"], c["z1"] - PLY, c["z1"], fill=PLYC, stroke="#333")
    v.rect(c["x0"], c["x0"] + PLY_QTR, c["z0"], c["z1"], fill="#333", stroke="none")
    for (z0, z1) in ((4, 11.5), (11.5, 19), (19, 26.5)):
        v.rect(c["x0"] + 0.75, c["x0"] + 36.75, z0 + 0.9, z1 - 0.6, fill="#fff7ed", stroke="#92400e", sw=0.6)
        v.rect(c["x0"] - 0.75, c["x0"], z0 + 0.06, z1 - 0.06, fill=DARK, stroke="#111", sw=0.5)
    v.text(19, 14, "W1 drawers, 36\" boxes on full-extension slides", size=8, fill="#7c2d12", anchor="middle")
    # plenum
    p = PLENUM
    v.rect(p["x0"], p["x1"], p["z0"], p["z0"] + PLY, fill=PLYC, stroke="#333"); v.rect(p["x0"], p["x0"] + PLY, p["z0"], p["z1"], fill=PLYC, stroke="#333"); v.rect(p["x1"] - PLY, p["x1"], p["z0"], p["z1"], fill=PLYC, stroke="#333")
    v.rect(p["x0"], p["x1"], p["z1"], TOP_UNDER, fill=PLYC, stroke="#333")   # doubler
    v.text(18, 29.2, "DOWNDRAFT PLENUM  5-1/4\" void, sealed", size=8, fill="#1d4ed8", anchor="middle")
    for i in range(9):
        x = DOG_GRID["x0"] + i * 4; v.rect(x - 0.375, x + 0.375, p["z1"], TOP_HEIGHT, fill="#fff", stroke="#1d4ed8", sw=0.6)
    v.rect(p["x1"] - PLY - 4.5, p["x1"] - PLY, 27.5, 31.5, fill="#ffedd5", stroke=ACC); v.text(37, 25.4, "4\" inlet", size=7, fill=ACC, anchor="middle")
    # service gap + riser
    v.rect(SERVICE_GAP["x0"], SERVICE_GAP["x1"], PLINTH_H, TOP_UNDER, fill="#f8fafc", stroke="#999", sw=0.6, extra=GHOST)
    v.rect(41.5, 45.5, PLINTH_H, 31.5, fill="#ffedd5", stroke=ACC, sw=1); v.text(43.5, 16, "4\"", size=8, fill=ACC, anchor="middle"); v.text(43.5, 13, "riser", size=7, fill=ACC, anchor="middle")
    # E2 router cabinet: raised floor, spine duct under
    c = CABS["E2"]
    v.rect(SPINE["x0"], SPINE["x1"], SPINE["z0"], SPINE["z1"], fill="#ffedd5", stroke=ACC, sw=1); v.text(52.5, 7.2, "SPINE", size=7, fill=ACC, anchor="middle"); v.text(52.5, 4.8, "4\" + 2-1/2\"", size=6.5, fill=ACC, anchor="middle")
    v.rect(c["x0"], c["x1"], 12.0, 12.75, fill=PLYC, stroke="#333"); v.rect(c["x0"], c["x0"] + PLY, PLINTH_H, TOP_UNDER, fill=PLYC, stroke="#333")
    v.rect(c["x1"] - 0.75, c["x1"], 12.75, TOP_UNDER, fill=DARK, stroke="#111")   # door
    v.rect(SPINE["x1"], SPINE["x1"] + PLY, PLINTH_H, 12.0, fill=PLYC, stroke="#333")
    v.rect(c["x1"], c["x1"] + 0.75, PLINTH_H, 12, fill=PLYC, stroke="#333")
    v.text(57, 9.3, "raised floor", size=7, fill="#333", anchor="middle")
    # router + lift
    rb = ROUTER_BOX; rp = ROUTER_PLATE
    v.rect(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, TOP_HEIGHT - rp["thick"], TOP_HEIGHT, fill="#d1d5db", stroke="#374151", sw=1)
    v.rect(rp["cx"] - 3.5, rp["cx"] + 3.5, TOP_HEIGHT - 12, TOP_HEIGHT - rp["thick"] - 2, fill="#facc15", stroke="#713f12")   # DW618 motor
    v.rect(rp["cx"] - 4.5, rp["cx"] + 4.5, TOP_HEIGHT - rp["thick"] - 2.5, TOP_HEIGHT - rp["thick"], fill="#9ca3af", stroke="#374151")
    v.rect(rp["cx"] - 4.6, rp["cx"] - 4.1, TOP_HEIGHT - 12, TOP_HEIGHT - 2, fill="#374151", stroke="none"); v.rect(rp["cx"] + 4.1, rp["cx"] + 4.6, TOP_HEIGHT - 12, TOP_HEIGHT - 2, fill="#374151", stroke="none")
    v.text(rp["cx"], TOP_HEIGHT - 7, "DW618", size=7, fill="#111", anchor="middle"); v.text(rp["cx"], TOP_HEIGHT + 2.2, "Rout-R-Lift II plate, flush", size=7.5, fill="#374151", anchor="middle")
    v.rect(rb["x0"] + 4, rb["x0"] + 4.75, rb["z0"], TOP_UNDER, fill="#333", stroke="none"); v.rect(rb["x1"] - 2, rb["x1"] - 1.25, rb["z0"], TOP_UNDER, fill="#333", stroke="none")
    v.text(57, 17.5, "sealed router box", size=7.5, fill="#7c2d12", anchor="middle"); v.text(57, 15, "4\" to spine + make-up-air slot", size=6.5, fill="#7c2d12", anchor="middle")
    v.rect(rb["x0"] + 4, rb["x1"] - 2, rb["z0"], rb["z0"] + 0.5, fill="#ffedd5", stroke=ACC)
    v.line(52.5, 12.0, 52.5, 12.75, stroke=ACC, sw=6)
    # top slab
    v.rect(0, 69, TOP_UNDER, TOP_UNDER + PLY, fill=MDFC, stroke="#333"); v.rect(0, 69, TOP_UNDER + PLY, TOP_HEIGHT, fill=PLYC, stroke="#333")
    v.rect(-EDGE_BAND, 0, TOP_UNDER, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e"); v.rect(69, 69 + EDGE_BAND, TOP_UNDER, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e")
    v.text(10, TOP_HEIGHT + 2.2, "3/4 Baltic birch over 3/4 MDF, maple edge", size=8, fill="#333", anchor="middle")
    for yy in ROUTER_TRACKS["fence_y"]: pass
    v.rect(ROUTER_TRACKS["combo_x"] - 0.5, ROUTER_TRACKS["combo_x"] + 0.5, TOP_HEIGHT - 0.5, TOP_HEIGHT, fill="#4b5563", stroke="none")
    v.dim_v(-10, 0, TOP_HEIGHT, "34-3/4\"", size=10); v.dim_v(-10, PLENUM["z0"], PLENUM["z1"], "6\"", size=8)
    v.dim_h(0, 69, -6, "69\"", size=10); v.dim_h(SPINE["x0"], SPINE["x1"], -2.5, "5\"", size=8)
    v.line(-14, 0, 84, 0, stroke="#999", sw=1); v.text(-4, -10, "< WEST", size=9, fill="#666"); v.text(73, -10, "EAST >", size=9, fill="#666")
    s.save(os.path.join(OUT, "30-section-A-router.svg"))

def lift_station(v, x_off, raised, label):
    """draws a N-S section of the lift bay at u = y + x_off, lowered or raised"""
    lb = LIFT_BAY; sp = SUB_PLATFORM; ms = MITER_SAW; lt = LIFT_TABLE
    def U(y): return x_off + y
    plat_z = (lt["high"] if raised else lt["low"])
    # bay walls (N side = W1 south side) and top
    v.rect(U(lb["y1"]), U(lb["y1"] + PLY), 4, TOP_UNDER, fill=PLYC, stroke="#333")
    v.rect(U(lb["y0"] - PLY), U(lb["y0"]), 4, TOP_UNDER, fill=DARK, stroke="#111")   # removable front panel
    v.rect(U(0), U(HATCH["y0"]), TOP_UNDER, TOP_HEIGHT, fill=PLYC, stroke="#333"); v.rect(U(HATCH["y1"]), U(96), TOP_UNDER, TOP_HEIGHT, fill=PLYC, stroke="#333")
    v.rect(U(-EDGE_BAND), U(0), TOP_UNDER, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e")
    # ledge
    v.rect(U(HATCH["y0"]), U(HATCH["y0"] + HATCH["ledge"]), TOP_UNDER - 1.0, TOP_UNDER, fill=MAPLE, stroke="#7a5c2e")
    v.rect(U(HATCH["y1"] - HATCH["ledge"]), U(HATCH["y1"]), TOP_UNDER - 1.0, TOP_UNDER, fill=MAPLE, stroke="#7a5c2e")
    # scissor lift (schematic)
    v.rect(U(12), U(34), 0, 2.5, fill=STEEL, stroke="#444"); v.rect(U(9), U(37), plat_z - 1.5, plat_z, fill=STEEL, stroke="#444")
    for (a, b) in ((U(12), U(34)), (U(34), U(12))):
        v.line(a, 2.5, b, plat_z - 1.5, stroke="#444", sw=2)
    v.text(U(23), plat_z / 2 + 1, "scissor lift table", size=7, fill="#333", anchor="middle")
    # sub platform + saw + hood
    v.rect(U(sp["y0"]), U(sp["y1"]), plat_z, plat_z + sp["t"], fill=PLYC, stroke="#333")
    saw0 = plat_z + sp["t"]
    v.rect(U(4), U(4 + ms["d"]), saw0, saw0 + ms["deck"], fill="#e9d5ff", stroke="#6d28d9")           # base/deck
    v.rect(U(14), U(20), saw0 + ms["deck"], saw0 + ms["deck"] + 5, fill="#c4b5fd", stroke="#6d28d9")  # fence
    v.rect(U(8), U(30), saw0 + ms["deck"] + 5, saw0 + ms["h_locked"], fill="#ddd6fe", stroke="#6d28d9")  # head
    v.text(U(19), saw0 + ms["h_locked"] - 4, "DWS779", size=8, fill="#4c1d95", anchor="middle")
    hood = MITER_HOOD
    v.rect(U(hood["y0"]), U(hood["y1"]), saw0, saw0 + hood["h"], fill="#7c3aed", stroke="#4c1d95")
    v.text(U(41), saw0 + hood["h"] + 2, "hood", size=7, fill="#4c1d95", anchor="middle")
    v.line(U(44), saw0 + 3, U(48), 9, stroke=ACC, sw=3, extra="stroke-dasharray='3 2'")
    if raised:
        v.rect(U(HATCH["y0"] + 1), U(HATCH["y0"] + 4), plat_z + sp["t"] - 3, plat_z + sp["t"], fill=MAPLE, stroke="#7a5c2e")  # stop blocks
        v.text(U(23), TOP_HEIGHT + ms["h_locked"] + 4, label, size=9, fill="#111", anchor="middle", weight="bold")
        v.line(U(-4), TOP_HEIGHT, U(50), TOP_HEIGHT, stroke="#6d28d9", sw=0.8, extra=GHOST)
        v.text(U(48), TOP_HEIGHT + 1.2, "deck flush at 34-3/4", size=7, fill="#4c1d95", anchor="end")
    else:
        # leaves in place
        v.rect(U(HATCH["y0"]), U(HATCH["y1"]), TOP_UNDER, TOP_HEIGHT, fill="#f5f3ff", stroke="#6d28d9", sw=1)
        v.line(U((HATCH["y0"] + HATCH["y1"]) / 2), TOP_UNDER, U((HATCH["y0"] + HATCH["y1"]) / 2), TOP_HEIGHT, stroke="#6d28d9")
        v.text(U(23), TOP_HEIGHT + 8, label, size=9, fill="#111", anchor="middle", weight="bold")
        v.text(U(23), TOP_HEIGHT + 2.2, "two lift-off leaves on the ledge + centre bar", size=7.5, fill="#4c1d95", anchor="middle")
    v.dim_v(U(-6), 0, plat_z, dim(plat_z), size=8)

def section_B():
    k = 5.6; s = sheet("SHEET 7  -  SECTION B-B  (north-south at x = 30, through the lift bay, plenum, W2 and laser well; looking east)", "Left: miter saw stowed, hatch leaves in, top fully flat. Right: lift raised until the sub-platform meets the four stop blocks; saw deck flush with the top.", 1400, 520)
    v = View(s, k, 60, 450)
    # full section lowered (left) with W1/W2/well
    lift_station(v, 0, False, "STOWED")
    lift_station(v, 100, True, "RAISED (hood and 4\" flex hose rise with the saw)")
    # W1 + plenum + W2 + well on the left instance only
    for x_off in (0,):
        def U(y): return x_off + y
        c = CABS["W1"]; v.rect(U(c["y0"]), U(c["y1"]), c["z0"], c["z1"], fill="#fff", stroke="#333", sw=0.6)
        v.rect(U(c["y0"]), U(c["y1"]), c["z0"], c["z0"] + PLY, fill=PLYC, stroke="#333"); v.rect(U(c["y0"]), U(c["y1"]), c["z1"] - PLY, c["z1"], fill=PLYC, stroke="#333")
        v.text(U(56), 15, "W1", size=9, fill="#666", anchor="middle")
        p = PLENUM; v.rect(U(p["y0"]), U(p["y1"]), p["z0"], p["z1"], fill="#eff6ff", stroke="#1d4ed8", sw=0.8)
        v.rect(U(p["y0"]), U(p["y1"]), p["z1"], TOP_UNDER, fill=PLYC, stroke="#333")
        for j in range(9):
            y = DOG_GRID["y0"] + j * 4; v.rect(U(y - 0.375), U(y + 0.375), p["z1"], TOP_HEIGHT, fill="#fff", stroke="#1d4ed8", sw=0.5)
        v.text(U(63), 29, "plenum", size=8, fill="#1d4ed8", anchor="middle")
        c = CABS["W2"]; v.rect(U(c["y0"]), U(c["y1"]), c["z0"], c["z1"], fill="#fff", stroke="#333", sw=0.6)
        v.rect(U(c["y0"]), U(c["y1"]), c["z1"] - PLY, c["z1"], fill=PLYC, stroke="#333")
        v.rect(U(67), U(94), 15.5, 18.5, fill="#dbeafe", stroke="#1e40af"); v.text(U(80.5), 12.5, "laser on pull-out tray (stored)", size=7.5, fill="#1e40af", anchor="middle")
        v.rect(U(66), U(80), 24, 26.5, fill=PLYC, stroke="#333")   # spacer
        lw = LASER_WELL
        v.rect(U(lw["y0"] - PLY), U(lw["y0"]), 24, TOP_UNDER, fill=PLYC, stroke="#333"); v.rect(U(lw["y1"]), U(lw["y1"] + PLY), 24, TOP_UNDER, fill=PLYC, stroke="#333")
        v.rect(U(lw["y0"]), U(lw["y1"]), TOP_UNDER, TOP_HEIGHT, fill="#fef3c7", stroke="#92400e", sw=1)
        for d in lw["cleats"]:
            v.rect(U(lw["y0"]), U(lw["y0"] + 0.75), TOP_HEIGHT - d - 0.75, TOP_HEIGHT - d, fill=MAPLE, stroke="#7a5c2e"); v.rect(U(lw["y1"] - 0.75), U(lw["y1"]), TOP_HEIGHT - d - 0.75, TOP_HEIGHT - d, fill=MAPLE, stroke="#7a5c2e")
        v.text(U(85.5), 29, "laser well: insert flush, or floor on cleats at 2 / 4-1/2 / 7", size=7, fill="#78350f", anchor="middle")
        v.rect(U(FACE_VISE["block"]["y0"]), U(95), 24, TOP_UNDER, fill="#fde68a", stroke="#92400e", sw=0.6, extra=GHOST); v.text(U(88.5), 25.5, "vise pad", size=6.5, fill="#92400e", anchor="middle")
        v.rect(U(BASE["y0"] + TOE_RECESS), U(BASE["y1"]), 0, PLINTH_H, fill="#333", stroke="#111")
    v.line(-6, 0, 200, 0, stroke="#999", sw=1); v.text(0, -10, "< SOUTH (miter operator)", size=9, fill="#666"); v.text(96, -10, "NORTH (saw) >", size=9, fill="#666", anchor="end")
    v.dim_h(0, 96, -6, "96\"", size=10)
    s.save(os.path.join(OUT, "31-section-B-lift.svg"))

def section_C():
    k = 7.0; s = sheet("SHEET 8  -  SECTION C-C  (north-south at x = 52, through the spine duct, SE cabinet, router cabinet, duct leg and motor bay; looking east)", "The 4\" main and 2-1/2\" vac trunks run side by side in the spine at floor level. Every drop is a 45-degree wye with a blast gate. The table saw hose exits into the motor bay.", 60 + 130 * k, 520)
    v = View(s, k, 60, 440)
    v.rect(BASE["y0"] + TOE_RECESS, MOTOR_BAY["y0"], 0, PLINTH_H, fill="#333", stroke="#111")
    v.rect(LIFT_BAY["y0"], LIFT_BAY["y1"], 0, TOP_UNDER, fill="#f5f3ff", stroke="#6d28d9", sw=0.6, extra=GHOST); v.text(23, 20, "lift bay (beyond)", size=8, fill="#4c1d95", anchor="middle")
    # spine
    v.rect(SPINE["y0"], SPINE["y1"], SPINE["z0"], SPINE["z1"], fill="#ffedd5", stroke=ACC, sw=1)
    v.rect(SPINE["y0"] + 1, SPINE["y1"] - 1, 4.5, 8.5, fill="#fdba74", stroke=ACC); v.text(40, 6, "4\" main trunk", size=8, fill="#7c2d12", anchor="middle")
    v.rect(SPINE["y0"] + 1, SPINE["y1"] - 1, 9, 11.5, fill="#fed7aa", stroke=ACC); v.text(40, 9.7, "2-1/2\" vac trunk", size=7, fill="#7c2d12", anchor="middle")
    # SE / E2 cabinets
    for key in ("SE", "E2"):
        c = CABS[key]; v.rect(c["y0"], c["y1"], c["z0"], c["z1"], fill="#fff", stroke="#333", sw=0.7)
        v.rect(c["y0"], c["y1"], c["z0"] - 0.75, c["z0"], fill=PLYC, stroke="#333"); v.text((c["y0"] + c["y1"]) / 2, 24, key, size=10, fill="#666", anchor="middle")
    rb = ROUTER_BOX; v.rect(rb["y0"], rb["y1"], rb["z0"], rb["z1"], fill="#fff7ed", stroke="#b45309", sw=0.8, extra=GHOST); v.text(62, 28, "router box", size=7.5, fill="#7c2d12", anchor="middle")
    v.rect(ROUTER_PLATE["cy"] - ROUTER_PLATE["h"] / 2, ROUTER_PLATE["cy"] + ROUTER_PLATE["h"] / 2, TOP_HEIGHT - 0.375, TOP_HEIGHT, fill="#d1d5db", stroke="#374151")
    # drops
    for (name, (x, y, z), size) in DUCT["drops"]:
        if "Router fence" in name: continue
        v.rect(y - size / 2, y + size / 2, 8.5 if size == 4 else 11.5, (z if z > 12 else 12.75) + (0 if "hood" in name or "Miter" in name or "sweep" in name else 0), fill="#fdba74" if size == 4 else "#fed7aa", stroke=ACC, sw=0.8)
        v.rect(y - 1.2, y + 1.2, 12.75, 14.25, fill="#dc2626", stroke="#7f1d1d"); 
        v.text(y, 17, name.split(" (")[0], size=6.5, fill="#7c2d12", anchor="middle")
    # duct leg + utility + bay
    v.rect(DUCT_LEG["y0"], DUCT_LEG["y1"], DUCT_LEG["z0"], DUCT_LEG["z1"], fill="#ffedd5", stroke=ACC, sw=1); v.text(78, 6, "leg", size=7, fill="#7c2d12", anchor="middle")
    v.rect(DUCT_LEG["y0"], DUCT_LEG["y1"], 12, TOP_UNDER, fill="#fefce8", stroke="#713f12", sw=0.6, extra=GHOST); v.text(78, 22, "utility", size=6.5, fill="#713f12", anchor="middle"); v.text(78, 19.5, "column", size=6.5, fill="#713f12", anchor="middle")
    v.rect(MOTOR_BAY["y0"], MOTOR_BAY["y0"] + PLY, PLINTH_H, TOP_UNDER, fill=PLYC, stroke="#333")
    v.rect(MOTOR_BAY["y0"], MOTOR_BAY["y1"], 0, TOP_UNDER, fill="#fee2e2", stroke="#b91c1c", sw=0.6, extra=GHOST)
    v.rect(MOTOR_BAY["y0"] + 3, MOTOR_BAY["y1"] + 2, 12, 24, fill="#e5e7eb", stroke="#444", extra=GHOST); v.text(88, 17, "CNS motor (ghost)", size=7, fill="#444", anchor="middle")
    v.line(80.5, 8, 92, 8, stroke=ACC, sw=4, extra="stroke-dasharray='3 2'"); v.text(88, 4.5, "4\" hose to saw port", size=6.5, fill="#7c2d12", anchor="middle")
    v.rect(28, 68, 30.25, TOP_UNDER, fill="none", stroke="none")
    v.rect(MOTOR_BAY["y0"] - 8, 96, 30.25, TOP_UNDER, fill=MAPLE, stroke="#7a5c2e"); v.text(88, 31.2, "beam", size=7, fill="#4a3a1e", anchor="middle")
    # top
    v.rect(0, 96, TOP_UNDER, TOP_UNDER + PLY, fill=MDFC, stroke="#333"); v.rect(0, 96, TOP_UNDER + PLY, TOP_HEIGHT, fill=PLYC, stroke="#333")
    v.rect(-1.5, 0, TOP_UNDER, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e"); v.rect(96, 99, TOP_HEIGHT - 0.5, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e"); v.text(97.5, TOP_HEIGHT + 1.5, "lip", size=6.5, fill="#4a3a1e", anchor="middle")
    v.rect(96 - OUTFEED_GROOVE["len"], 96, TOP_HEIGHT - OUTFEED_GROOVE["d"], TOP_HEIGHT, fill="#c9c2b2", stroke="#6b5330", sw=0.5)
    # saw ghost
    v.rect(97, 124, TOP_HEIGHT - 1.5, TOP_HEIGHT, fill="#e5e7eb", stroke="#666", extra=GHOST); v.text(110, TOP_HEIGHT + 2, "SawStop table (ghost)", size=8, fill="#444", anchor="middle")
    v.rect(96, 98.5, TOP_HEIGHT - 2.75, TOP_HEIGHT - 1.0, fill="#888", stroke="#444"); 
    v.line(-6, 0, 128, 0, stroke="#999", sw=1); v.text(0, -10, "< SOUTH", size=9, fill="#666"); v.text(124, -10, "NORTH >", size=9, fill="#666", anchor="end")
    v.dim_h(0, 96, -6, "96\"", size=10); v.dim_v(-8, 0, 12, "duct chase 12\"", size=8)
    s.save(os.path.join(OUT, "32-section-C-ducts.svg"))

# ==================================================================== STATION DETAILS
def router_detail():
    k = 12.0; s = sheet("SHEET 9  -  ROUTER STATION DETAIL (plan, east half of the top)", "Plate recess for a JessEm Rout-R-Lift II (9-1/4 x 11-3/4 x 3/8, leveling screws in the corners). Fence tracks are 26\" apart; check your fence's clamp spacing before cutting the dados.", 900, 640)
    v = View(s, k, 60 - 38 * k, 95 + 84 * k)
    v.rect(38, 69, 42, 82, fill=PLYC, stroke="#333")
    rp = ROUTER_PLATE; rt = ROUTER_TRACKS
    for yy in rt["fence_y"]: v.rect(rt["fence_x"][0], rt["fence_x"][1], yy - 0.375, yy + 0.375, fill="#4b5563", stroke="none")
    v.rect(rt["combo_x"] - 0.5, rt["combo_x"] + 0.5, rt["combo_y"][0], rt["combo_y"][1], fill="#4b5563", stroke="none")
    v.rect(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, fill="#e5e7eb", stroke="#111", sw=1.2)
    v.circle(rp["cx"], rp["cy"], 1.75, fill="#fff", stroke="#111"); 
    for (dx, dy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)): v.circle(rp["cx"] + dx * (rp["w"] / 2 - 0.6), rp["cy"] + dy * (rp["h"] / 2 - 0.6), 0.2, fill="#111", stroke="none")
    v.rect(ROUTER_BOX["x0"], ROUTER_BOX["x1"], ROUTER_BOX["y0"], ROUTER_BOX["y1"], fill="none", stroke="#b45309", sw=0.8, extra=GHOST)
    # fence ghost
    v.rect(44, 68, rp["cy"] + 1.5, rp["cy"] + 4.0, fill="#fde68a", stroke="#92400e", sw=0.8, extra=GHOST); v.text(50, rp["cy"] + 5, "your fence (ghost), clamps into both tracks", size=8, fill="#92400e")
    v.circle(ROUTER_FENCE_PORT["x"] + 1.6, ROUTER_FENCE_PORT["y"], 1.25, fill="#fff", stroke="#7c2d12")
    v.label(43, 80.5, "T-track 3/4 x 3/8 dado", size=8, fill="#7c2d12"); v.label(60, 44.2, "combo T-track / miter slot", size=8, fill="#7c2d12")
    v.dim_h(rt["fence_x"][0], rt["fence_x"][1], 84.5, "26\"", size=9); v.dim_v(70.5, rt["fence_y"][0], rt["fence_y"][1], "26\" between fence tracks", size=9)
    v.dim_h(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - 7.5, "9-1/4\"", size=8); v.dim_v(rp["cx"] + 6, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, "11-3/4\"", size=8)
    v.dim_h(rp["cx"], 69, 41.5, "12\" to east edge", size=8); v.dim_h(38, rp["cx"], 41.5, "", size=8)
    v.text(38.5, 83.2, "north (outfeed) is up; operator stands at the east edge (right)", size=9, fill="#555")
    s.save(os.path.join(OUT, "40-router-station.svg"))

def hatch_detail():
    k = 9.0; s = sheet("SHEET 10  -  MITER HATCH AND SUB-PLATFORM (plan) and lift specification", "The sub-platform is a 2x4 torsion frame with a 3/4 BB deck; the saw and the hood bolt to it. Four leveling bolts in its corners land on maple stop blocks so the deck returns to exactly 34-3/4 every time.", 1150, 640)
    v = View(s, k, 60, 540)
    h = HATCH; sp = SUB_PLATFORM; lb = LIFT_BAY
    v.rect(10, 58, 0, 48, fill=PLYC, stroke="#333")
    v.rect(lb["x0"], lb["x1"], lb["y0"], lb["y1"], fill="none", stroke="#6d28d9", sw=0.8, extra=GHOST); v.text(lb["x1"] + 0.5, lb["y1"] - 1.5, "lift bay walls", size=7.5, fill="#4c1d95")
    v.rect(h["x0"], h["x1"], h["y0"], h["y1"], fill="#f5f3ff", stroke="#6d28d9", sw=1.4)
    v.rect(h["x0"] + 1, h["x1"] - 1, h["y0"] + 1, h["y1"] - 1, fill="none", stroke="#7a5c2e", sw=0.8); v.text(h["x0"] + 1.2, h["y1"] - 2.2, "1\" maple ledge, 1\" below top", size=7, fill="#7a5c2e")
    mid = (h["y0"] + h["y1"]) / 2
    v.rect(h["x0"], h["x1"], mid - 1, mid + 1, fill=MAPLE, stroke="#7a5c2e"); v.text(h["x1"] + 0.5, mid - 0.4, "removable centre bar", size=7.5, fill="#7a5c2e")
    v.rect(sp["x0"], sp["x1"], sp["y0"], sp["y1"], fill="none", stroke="#111", sw=1, extra=GHOST); v.text(sp["x0"] + 0.5, sp["y0"] + 0.7, "sub-platform 28 x 41", size=7.5, fill="#111")
    v.rect(22.5, 45.5, 4.5, 4.5 + MITER_SAW["d"], fill="#e9d5ff", stroke="#6d28d9"); v.text(34, 20, "DWS779 footprint 24-1/2 x 32", size=8.5, fill="#4c1d95", anchor="middle")
    v.line(22.5, 16, 45.5, 16, stroke="#4c1d95", sw=2); v.text(34, 17, "fence line", size=7, fill="#4c1d95", anchor="middle")
    v.rect(MITER_HOOD["x0"], MITER_HOOD["x1"], MITER_HOOD["y0"], MITER_HOOD["y1"], fill="#7c3aed", stroke="#4c1d95"); v.text(34, 40.5, "hood 28 x 6 x 14 tall, 4\" port low at the back", size=7.5, fill="#fff", anchor="middle")
    v.rect(20.5, 47.5, 12, 30, fill="none", stroke=STEEL, sw=1.2, extra=GHOST); v.text(34, 31, "lift platform 27-1/2 x 17-3/4 (ghost)", size=7, fill="#444", anchor="middle")
    for (x, y) in ((sp["x0"] + 1, sp["y0"] + 1), (sp["x1"] - 1, sp["y0"] + 1), (sp["x0"] + 1, sp["y1"] - 1), (sp["x1"] - 1, sp["y1"] - 1)):
        v.circle(x, y, 0.4, fill="#111", stroke="none")
    v.text(sp["x1"] + 0.5, sp["y0"] + 0.4, "leveling bolt x4", size=7, fill="#111")
    v.rect(LEAF_SLOT["x0"], LEAF_SLOT["x1"], LEAF_SLOT["y0"], LEAF_SLOT["y1"], fill="#ede9fe", stroke="#6d28d9", sw=0.6); v.text(LEAF_SLOT["x0"] - 0.5, 20, "leaf slot 3-1/2 wide", size=7, fill="#4c1d95", anchor="end")
    v.dim_h(h["x0"], h["x1"], -3, "29\"", size=9); v.dim_v(h["x1"] + 8, h["y0"], h["y1"], "42-1/2\"", size=9)
    v.dim_h(sp["x0"], sp["x1"], -6.5, "28\"", size=8)
    # spec table
    tx, ty = 640, 110
    s.text(tx, ty, "Scissor lift table requirements", 12, weight="bold")
    rows = [("Capacity", ">= 500 lb (load is about 95 lb)"), ("Lowered height", f"<= {dim(TOP_UNDER - MITER_SAW['h_locked'] - SUB_PLATFORM['t'] - 0.5)} so the locked saw clears the top"),
            ("Raised height", f">= {dim(SAW_DECK_Z - SUB_PLATFORM['t'])} (deck at 34-3/4 with a 2\" sub-platform)"), ("Platform", ">= 27 x 17 in."),
            ("Type", "foot-pump hydraulic, stationary; remove wheels/handle"), ("Stop", "4 maple blocks + leveling bolts; UHMW guides"),
            ("Verify", "DWS779 locked height and deck height before buying")]
    for i, (a, b) in enumerate(rows):
        s.text(tx, ty + 22 + i * 18, a, 10, "#333", weight="bold"); s.text(tx + 110, ty + 22 + i * 18, b, 10, "#333")
    s.save(os.path.join(OUT, "41-miter-hatch.svg"))

def dust_plan():
    k = 6.0; s = sheet("SHEET 11  -  DUST COLLECTION ROUTING (plan)", "One 4\" main trunk for the Harbor Freight collector and one 2-1/2\" trunk for the shop vac + cyclone, side by side in the spine. Wyes point toward the ports; blast gate at every drop; cabinets sealed.", 980, 900)
    v = View(s, k, 120, 820)
    v.rect(TOP["x0"], TOP["x1"], TOP["y0"], TOP["y1"], fill="#fff", stroke="#111", sw=1.5)
    for key, c in CABS.items(): v.rect(c["x0"], c["x1"], c["y0"], c["y1"], fill="none", stroke="#d1d5db", sw=0.6)
    v.rect(MOTOR_BAY["x0"], MOTOR_BAY["x1"], MOTOR_BAY["y0"], MOTOR_BAY["y1"], fill="#fee2e2", stroke="#b91c1c", sw=0.6, extra=GHOST)
    v.rect(LIFT_BAY["x0"], LIFT_BAY["x1"], LIFT_BAY["y0"], LIFT_BAY["y1"], fill="#f5f3ff", stroke="#6d28d9", sw=0.6, extra=GHOST)
    v.rect(PLENUM["x0"], PLENUM["x1"], PLENUM["y0"], PLENUM["y1"], fill="#eff6ff", stroke="#1d4ed8", sw=0.6, extra=GHOST)
    v.rect(ROUTER_BOX["x0"], ROUTER_BOX["x1"], ROUTER_BOX["y0"], ROUTER_BOX["y1"], fill="#fff7ed", stroke="#b45309", sw=0.6, extra=GHOST)
    # trunks
    v.line(52.5, 2, 52.5, 78, stroke="#f97316", sw=9); v.line(52.5, 78, 69, 78, stroke="#f97316", sw=9)
    v.line(54.2, 2, 54.2, 79.5, stroke="#fbbf24", sw=5); v.line(54.2, 79.5, 69, 79.5, stroke="#fbbf24", sw=5)
    v.label(60, 74, "4\" main", size=9, fill="#7c2d12"); v.label(60, 82.5, "2-1/2\" vac", size=8, fill="#78350f")
    # drops
    drops = [("floor sweep gate, south toe kick", (52.5, 2), (52.5, -3), 4), ("miter hood: 4\" flex hose rises with the lift", (52.5, 30), (34, 41), 4),
             ("router box: 4\" from box floor", (52.5, 62), (57, 62), 4), ("downdraft plenum: 4\" riser in the service gap", (52.5, 70), (43.5, 70), 4),
             ("table saw: 4\" gate on bay wall, hose to CNS port", (55, 78), (49, 84), 4), ("router fence: 2-1/2\" flip-lid port, east apron", (54.2, 64), (68, 64), 2.5),
             ("miter saw chute: 2-1/2\" flex", (54.2, 26), (34, 20), 2.5)]
    for i, (name, a, b, size) in enumerate(drops):
        col = "#f97316" if size == 4 else "#fbbf24"
        v.line(a[0], a[1], b[0], b[1], stroke=col, sw=5 if size == 4 else 3.5)
        v.rect(a[0] - 1.5, a[0] + 1.5, a[1] - 1.5, a[1] + 1.5, fill="#dc2626", stroke="#7f1d1d", rx=2)
        lx, ly = {0: (46, -7), 1: (20, 44.5), 2: (57, 58.5), 3: (24, 73.5), 4: (30, 90), 5: (84, 68), 6: (20, 16)}[i]
        v.label(lx, ly, name, size=8, fill="#7c2d12", anchor="middle")
    v.label(30, 66.5, "plenum inlet through its east wall", size=7.5, fill="#1d4ed8")
    v.circle(71, 78, 2.2, fill="#f97316", stroke="#7c2d12"); v.circle(71, 79.5 + 3.5, 1.4, fill="#fbbf24", stroke="#78350f")
    v.label(86, 76, "4\" port: HF collector", size=9, fill="#7c2d12"); v.label(86, 85.5, "2-1/2\" port: vac + cyclone", size=9, fill="#78350f")
    v.rect(-3, 71, -8, -6, fill="none", stroke="none")
    # legend / rules
    tx, ty = 560, 640
    s.text(tx, ty, "Rules that make it pull", 12, weight="bold")
    rules = ["Trunk: 4\" thin-wall PVC (S&D) or 4\" spiral, straight, floor level.", "Branches: 45-deg wyes, never tees; 45-deg elbows in pairs instead of a 90.",
             "Blast gate at every drop (red squares). Open ONE 4\" gate at a time on the HF collector.", "Vac trunk: 2-1/2\" PVC with its own gates; the cyclone sits before the vac.",
             "Seal cabinets that duct through them: silicone the plenum, foam tape on doors.", "Router box: a 1\" x 4\" make-up-air slot near the door so it does not starve.",
             "Clean-outs: capped ends at the floor sweep and the utility corner.", "Never route the laser's exhaust into this system (fire risk)."]
    for i, r in enumerate(rules): s.text(tx, ty + 20 + i * 16, "- " + r, 9.5, "#333")
    v.text(0, 99, "north (table saw) is up", size=9, fill="#555")
    s.save(os.path.join(OUT, "50-dust-routing.svg"))

def wiring_plan():
    k = 6.0; s = sheet("SHEET 12  -  ELECTRICAL LAYOUT (plan)", "One 20 A 120 V feed by 12 AWG SJOOW cord to a flush L5-20 inlet in the utility column. Distribution by a metal 15 A surge strip; branch strips inside cabinets; flush strips with USB-A/C on the faces.", 980, 900)
    v = View(s, k, 120, 820)
    v.rect(TOP["x0"], TOP["x1"], TOP["y0"], TOP["y1"], fill="#fff", stroke="#111", sw=1.5)
    for key, c in CABS.items(): v.rect(c["x0"], c["x1"], c["y0"], c["y1"], fill="none", stroke="#d1d5db", sw=0.6); v.text((c["x0"] + c["x1"]) / 2, (c["y0"] + c["y1"]) / 2, key, size=8, fill="#9ca3af", anchor="middle")
    v.rect(SERVICE_GAP["x0"], SERVICE_GAP["x1"], SERVICE_GAP["y0"], SERVICE_GAP["y1"], fill="#f8fafc", stroke="#94a3b8", sw=0.6, extra=GHOST)
    v.rect(LIFT_BAY["x0"], LIFT_BAY["x1"], LIFT_BAY["y0"], LIFT_BAY["y1"], fill="none", stroke="#6d28d9", sw=0.6, extra=GHOST)
    # inlet + main strip
    v.rect(66, 68, 76, 80, fill="#facc15", stroke="#713f12"); v.label(80, 78, "L5-20 inlet, 20 A", size=9, fill="#713f12")
    v.rect(60, 66, 76.5, 79.5, fill="#fef08a", stroke="#713f12"); v.text(56, 82.5, "MAIN STRIP (metal, 15 A, switched)", size=7.5, fill="#713f12", anchor="middle")
    def wire(pts, col="#1d4ed8", sw=2.2):
        for (a, b) in zip(pts, pts[1:]): v.line(a[0], a[1], b[0], b[1], stroke=col, sw=sw)
    # raceway along the spine top (z 12) then branches
    wire([(60, 78), (57.5, 78), (57.5, 4)]); v.label(57.5, 40, "raceway on spine lid", size=7.5, fill="#1d4ed8")
    wire([(57.5, 64), (62, 64)]); v.rect(60.5, 63, 62, 66, fill="#fde68a", stroke="#713f12"); v.label(58, 59.5, "router outlet + paddle switch", size=8, fill="#713f12")
    wire([(57.5, 24), (40, 24)]); v.rect(38, 42, 22, 26, fill="#fde68a", stroke="#713f12"); v.label(28, 24, "miter outlet (cord loop rises with lift) + paddle", size=8, fill="#713f12")
    wire([(57.5, 74), (43.5, 74), (43.5, 56), (5, 56)]); v.rect(1, 4, 54, 58, fill="#fde68a", stroke="#713f12"); v.label(-7, 56, "charging drawer, switched", size=8, fill="#713f12")
    wire([(43.5, 66), (5, 66), (5, 90)]); v.rect(1, 4, 88, 92, fill="#fde68a", stroke="#713f12"); v.label(-7, 90, "laser outlet (W2)", size=8, fill="#713f12")
    wire([(5, 66), (1, 66)]); v.rect(-2, 0, 50, 58, fill="#fef08a", stroke="#713f12"); v.label(-10, 52, "flush strip + USB, west", size=8, fill="#713f12")
    wire([(57.5, 10), (52, 10), (52, 0)]); v.rect(56, 64, -2, 0, fill="#fef08a", stroke="#713f12"); v.label(60, -4.5, "flush strip + USB, south", size=8, fill="#713f12")
    wire([(62, 66), (68, 66), (68, 70)]); v.rect(69, 71, 68, 74, fill="#fef08a", stroke="#713f12"); v.label(80, 71, "flush strip + USB, east", size=8, fill="#713f12")
    wire([(57.5, 78), (57.5, 90), (66, 90)], "#16a34a"); v.rect(66, 68, 88, 92, fill="#bbf7d0", stroke="#166534"); v.label(80, 90, "table saw outlet (north face)", size=8, fill="#166534")
    # LED
    for (x0, x1, y0, y1) in ((-1.5, 0, 1, 95), (69, 70.5, 1, 95), (1, 68, -1.5, 0)):
        v.rect(x0, x1, y0, y1, fill="#a5f3fc", stroke="#0e7490", sw=0.4)
    v.label(34, -9, "LED strip in the top's overhang on W, S, E (12 V driver on the main strip)", size=8, fill="#0e7490")
    tx, ty = 560, 640
    s.text(tx, ty, "Rules", 12, weight="bold")
    rules = ["Everything stays 120 V / 20 A. Never run the router and the miter saw at the same time (each ~15 A).", "Main strip has the red master switch; paddle switches at router and miter are the tool switches.",
             "Cords are strapped to the raceway, never loose in the dust chase; use 12 AWG for the feed, 14 AWG branch strips.", "The miter cord makes a service loop with 30\" of slack for the lift travel.",
             "Charging drawer: switched outlet, 1\" vent slots front and back.", "Metal strips and boxes; screw the strips to plywood, not to the duct."]
    for i, r in enumerate(rules): s.text(tx, ty + 20 + i * 16, "- " + r, 9.5, "#333")
    s.save(os.path.join(OUT, "51-electrical.svg"))

def all():
    os.makedirs(OUT, exist_ok=True)
    plan()
    for f, n in (("S", "SOUTH ELEVATION  (miter station face)"), ("E", "EAST ELEVATION  (router station face)"), ("W", "WEST ELEVATION  (hand-work face)"), ("N", "NORTH ELEVATION  (outfeed / table-saw side)")):
        elevation(n, f)
    section_A(); section_B(); section_C(); router_detail(); hatch_detail(); dust_plan(); wiring_plan()
    print("plans rendered")

if __name__ == "__main__":
    all()
