"""Stage-1 drawings: plan view, south elevation, isometric concept render."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svg import SVG, Iso
from model import *

OUT = os.path.join(os.path.dirname(__file__), "..", "renders")
MAPLE, MAPLE_EDGE = "#e2c48f", "#c9a86a"
FRONT, FRONT_DK, SIDE = "#2f3136", "#25272b", "#3a3d43"
TOE = "#1a1b1e"; STEEL = "#8d939c"; STEEL_DK = "#6b7078"; CAST = "#a9adb3"
ZONES = {  # plan-view station tints
    "bench":  ("#dbeafe", "#1d4ed8"), "router": ("#fde68a", "#b45309"),
    "outfeed": ("#dcfce7", "#15803d"), "glue": ("#fce7f3", "#be185d"),
    "miter": ("#ede9fe", "#6d28d9"), "clamp": ("#e5e7eb", "#374151")}

# ------------------------------------------------------------------ PLAN
def plan():
    k = 5.0; W, H = 900, 780
    s = SVG(W, H, "#fafafa")
    def X(x): return 80 + (x + 12) * k
    def Y(y): return 80 + (88 - y) * k     # y north up the page
    def R(x0, x1, y0, y1, **kw): s.rect(X(x0), Y(y1), (x1 - x0) * k, (y1 - y0) * k, **kw)
    s.text(20, 34, "PLAN VIEW  -  station layout (looking down, north = up)", 16, weight="bold")
    s.text(20, 54, "Island 96 x 48 in, miter wing 36 x 96 in, top 34 in = SawStop table height.  Scale: 1 in = 5 px", 11, "#555")
    # zones
    R(0, 44, 0, 48, fill=ZONES["bench"][0], stroke="none")
    R(44, 96, 0, 30, fill=ZONES["router"][0], stroke="none")
    R(44, 96, 30, 48, fill=ZONES["outfeed"][0], stroke="none")
    R(WING["x0"], WING["x1"], 0, 48, fill=ZONES["glue"][0], stroke="none")
    R(WING["x0"], WING["x1"], WING["y0"], 0, fill=ZONES["miter"][0], stroke="none")
    # outlines
    R(ISLAND["x0"], ISLAND["x1"], ISLAND["y0"], ISLAND["y1"], stroke="#111", sw=2)
    R(WING["x0"], WING["x1"], WING["y0"], WING["y1"], stroke="#111", sw=2)
    s.line(X(96), Y(0), X(96), Y(48), "#111", 0.6, "stroke-dasharray='4 3'")
    # table saw
    R(SAW["x0"], SAW["x1"], SAW["y0"], SAW["y1"], fill="#d4d7dc", stroke="#333", sw=1.2)
    R(SAW["x0"], SAW["ext_x1"], SAW["y0"], SAW["y1"], fill="#e9ebee", stroke="#333", sw=0.8)
    R(SAW["x0"] - 5, SAW["x1"] + 3, SAW["y1"], SAW["y1"] + 2.5, fill="#777", stroke="none")   # front rail
    R(SAW["x0"] - 5, SAW["x1"] + 3, SAW["y0"] - 1, SAW["y0"] + 1.5, fill="#777", stroke="none")  # rear rail
    bx = SAW["blade_x"]
    s.line(X(bx), Y(SAW["y0"] + 8), X(bx), Y(SAW["y0"] + 19), "#111", 3)
    for dx in (-SAW["slot_offset"], SAW["slot_offset"]):
        s.line(X(bx + dx), Y(SAW["y0"]), X(bx + dx), Y(SAW["y1"]), "#444", 2)
        s.line(X(bx + dx), Y(48), X(bx + dx), Y(48 - OUTFEED_GROOVE_LEN), "#15803d", 2, "stroke-dasharray='5 3'")
    R(44, 46.5, SAW["y0"], SAW["y1"] + 3, fill="#fbbf24", stroke="#333", sw=0.8)   # rip fence (parked)
    s.label(X(58), Y(SAW["y1"] - 4), "SawStop 10\" Contractor Saw + 36\" T-Glide", 11)
    s.label(X(SAW["x0"] + 12), Y(SAW["y0"] + 6), "36\" extension table", 9, "#444")
    s.label(X(bx), Y(SAW["y1"] + 5.5), "OPERATOR feeds south  v", 10, "#15803d")
    s.label(X(bx + 10), Y(SAW["y0"] + 6), "blade", 9, "#444")
    # dog field
    g = DOG_GRID; nx = int((g["x1"] - g["x0"]) / g["pitch"]) + 1; ny = int((g["y1"] - g["y0"]) / g["pitch"]) + 1
    for i in range(nx):
        for j in range(ny):
            s.circle(X(g["x0"] + i * g["pitch"]), Y(g["y0"] + j * g["pitch"]), g["dia"] / 2 * k + 0.6, "#1d4ed8", "none")
    f = FRONT_ROW
    for i in range(int((f["x1"] - f["x0"]) / f["pitch"]) + 1):
        s.circle(X(f["x0"] + i * f["pitch"]), Y(f["y"]), f["dia"] / 2 * k + 0.6, "#1d4ed8", "none")
    # vises
    R(WAGON_VISE["x0"], WAGON_VISE["x1"], WAGON_VISE["y0"], WAGON_VISE["y1"], fill="#94a3b8", stroke="#333")
    R(FACE_VISE["x0"], FACE_VISE["x1"], -2.5, 0, fill="#94a3b8", stroke="#333")
    s.label(X(27), Y(-6), "face vise", 9, "#444"); s.label(X(5), Y(-6), "wagon vise", 9, "#444")
    # router
    rp = ROUTER_PLATE
    R(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, fill="#fff7ed", stroke="#b45309", sw=1.5)
    s.circle(X(rp["cx"]), Y(rp["cy"]), 1.6 * k, "#fde68a", "#b45309")
    t = ROUTER_TTRACK
    for yy in (t["y_front"], t["y_fence"]): s.line(X(t["x0"]), Y(yy), X(t["x1"]), Y(yy), "#b45309", 3)
    for xx in (t["x0"], t["x1"]): s.line(X(xx), Y(t["y_front"]), X(xx), Y(t["y_fence"]), "#b45309", 3)
    s.label(X(66), Y(22), "router lift plate", 9, "#7c2d12"); s.label(X(66), Y(28.5), "fence T-track", 9, "#7c2d12")
    # miter station
    m = MITER_WELL
    R(m["x0"], m["x1"], m["y0"], m["y1"], fill="#f5f3ff", stroke="#6d28d9", sw=1.2, extra="stroke-dasharray='4 2'")
    R(m["x0"] + 2, m["x1"] - 3, m["y0"] + 4, m["y1"] - 4, fill="#c4b5fd", stroke="#4c1d95")
    s.line(X(m["x1"] - 12), Y(m["y0"] + 4), X(m["x1"] - 12), Y(m["y1"] - 4), "#4c1d95", 2)
    s.line(X(m["x0"] + 4), Y((m["y0"] + m["y1"]) / 2), X(m["x1"] - 3), Y((m["y0"] + m["y1"]) / 2), "#4c1d95", 3)
    h = MITER_HOOD
    R(h["x0"], h["x1"], h["y0"], h["y1"], fill="#7c3aed", stroke="#4c1d95")
    s.label(X(110), Y(-46), "12\" miter saw in well, bed flush with top", 9, "#3b0764")
    s.label(X(128), Y(-2), "dust hood", 9, "#fff", bg="#6d28d9")
    R(WING["x0"] + 2, WING["x1"] - 2, WING["y0"] - WING_PULLOUT["len"], WING["y0"], fill="none", stroke="#6d28d9", sw=1, extra="stroke-dasharray='6 3'")
    s.label(X(114), Y(-66), "telescoping extension  (36\" pull-out)", 9, "#3b0764")
    s.label(X(114), Y(30), "north end of wing = 87\" of built-in", 9, "#3b0764")
    s.label(X(114), Y(24), "left-side board support", 9, "#3b0764")
    s.label(X(88), Y(-24), "OPERATOR >", 10, "#6d28d9")
    # utility corner
    s.circle(X(DUST_PORT["x"]), Y(DUST_PORT["y"]), 3 * k, "#f97316", "#7c2d12", 1.5)
    s.label(X(112), Y(53), "6\" dust port + power inlet (utility corner)", 9, "#7c2d12")
    # zone labels
    s.label(X(22), Y(46), "A  WORKBENCH / DOWNDRAFT (dog field)", 10, ZONES["bench"][1])
    s.label(X(70), Y(40), "B  OUTFEED zone (grooves for miter gauge)", 10, ZONES["outfeed"][1])
    s.label(X(70), Y(8.5), "C  ROUTER STATION", 10, ZONES["router"][1])
    s.label(X(114), Y(8), "D  GLUE-UP / ASSEMBLY", 10, ZONES["glue"][1])
    s.label(X(114), Y(-13), "E  MITER STATION", 10, ZONES["miter"][1])
    s.label(X(48), Y(-14), "ALCOVE  (inside of the L, 96 x 48 in of floor)", 11, "#334155")
    # dimensions
    s.dim_h(X(0), X(96), Y(-3) + 30, "96\"", 11); s.dim_h(X(96), X(132), Y(-49) + 12, "36\"", 11)
    s.dim_v(X(-5), Y(48), Y(0), "48\"", 11); s.dim_v(X(137), Y(48), Y(-48), "96\"", 11)
    s.dim_h(X(SAW["x0"]), X(SAW["x1"]), Y(SAW["y1"] + 11), "69-1/8\" saw + extension", 10)
    s.dim_h(X(SAW["x1"]), X(WING["x0"]), Y(SAW["y0"] + 10), "17\" gap", 9)
    # legend
    lx, ly = 20, H - 140
    s.text(lx, ly, "Legend", 12, weight="bold")
    items = [("#1d4ed8", "3/4\" dog holes (4\" grid) - field doubles as downdraft grid"),
             ("#b45309", "T-track around router plate"), ("#15803d", "outfeed grooves aligned to miter slots"),
             ("#6d28d9", "miter saw well, hood and pull-out"), ("#f97316", "single external dust-collector connection")]
    for i, (c, tx) in enumerate(items):
        s.rect(lx, ly + 10 + i * 18, 12, 12, c, "none"); s.text(lx + 18, ly + 20 + i * 18, tx, 11, "#333")
    s.save(os.path.join(OUT, "01-plan-view.svg"))

# ------------------------------------------------------------- ELEVATION
def elevation():
    k = 5.0; W, H = 900, 420
    s = SVG(W, H, "#fafafa")
    def X(x): return 60 + x * k
    def Z(z): return 330 - z * k
    def R(x0, x1, z0, z1, **kw): s.rect(X(x0), Z(z1), (x1 - x0) * k, (z1 - z0) * k, **kw)
    s.text(20, 30, "SOUTH ELEVATION  -  island front (left) and miter wing south end (right)", 16, weight="bold")
    s.text(20, 48, "Modern flat fronts with routed finger pulls, no exposed hardware. Top 2-1/4\" hard maple, 34\" finished height.", 11, "#555")
    # island
    R(3, 93, 0, TOE_KICK, fill=TOE, stroke="none")
    R(0, 96, TOE_KICK, TOP_HEIGHT - TOP_THICK, fill=FRONT, stroke="#111")
    R(-1, 97, TOP_HEIGHT - TOP_THICK, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e")
    # wing south end
    R(99, 129, 0, TOE_KICK, fill=TOE, stroke="none")
    R(96, 132, TOE_KICK, TOP_HEIGHT - TOP_THICK, fill=FRONT, stroke="#111")
    R(95, 133, TOP_HEIGHT - TOP_THICK, TOP_HEIGHT, fill=MAPLE, stroke="#7a5c2e")
    rv = 0.25
    def panel(x0, x1, z0, z1, fill=FRONT_DK, pull="top"):
        R(x0 + rv, x1 - rv, z0 + rv, z1 - rv, fill=fill, stroke="#15161a", sw=0.6)
        if pull == "top": s.line(X(x0 + 2), Z(z1 - 1.2), X(x1 - 2), Z(z1 - 1.2), "#9a9ea6", 1.2)
        if pull == "side": s.line(X(x1 - 1.2), Z(z0 + 2), X(x1 - 1.2), Z(z1 - 2), "#9a9ea6", 1.2)
    # Zone A drawers + plenum panel
    panel(1, 43, 25.75, 31.5, pull=None); panel(1, 43, 18.5, 25.5); panel(1, 43, 11, 18.25); panel(1, 43, 4.25, 10.75)
    # Zone B bit pull-out
    panel(43, 54, 4.25, 31.5, pull="side")
    # Zone C router cabinet
    panel(54, 78, 16, 31.5, pull=None); panel(54, 78, 4.25, 15.75)
    s.rect(X(64), Z(28.5), 4 * k, 2.5 * k, "#dc2626", "#7f1d1d", 1, rx=3)  # paddle switch
    s.line(X(56), Z(30.2), X(60), Z(30.2), "#9a9ea6", 1.2)
    # Zone D drawers
    panel(78, 95, 25, 31.5); panel(78, 95, 17, 24.75); panel(78, 95, 4.25, 16.75)
    # face vise chop
    R(FACE_VISE["x0"], FACE_VISE["x1"], 25.5, TOP_HEIGHT - 0.1, fill="#b5c1d1", stroke="#334155")
    s.circle(X(27), Z(28), 1.1 * k, "#64748b", "#1e293b"); s.line(X(27), Z(28), X(27), Z(21), "#1e293b", 2.5)
    # wing: pull-out extension front + door
    panel(96, 132, 26.5, 31.5, pull=None); s.text(X(100), Z(28.3), "pull-out extension (stowed)", 8.5, "#c8ccd2")
    panel(96, 132, 4.25, 26.25, pull=None)
    # miter saw silhouette above the wing (in the well behind this face)
    s.poly([(X(102), Z(34)), (X(126), Z(34)), (X(126), Z(38)), (X(118), Z(38)), (X(118), Z(50)), (X(108), Z(50)), (X(108), Z(38)), (X(102), Z(38))], "#c4b5fd", "#4c1d95", 1)
    s.rect(X(124), Z(50), 8 * k, 16 * k, "#7c3aed", "#4c1d95")
    s.text(X(101), Z(44), "miter saw (bed flush)", 8.5, "#3b0764")
    # labels
    for x, z, t in [(22, 8, "A  hand-tool drawers"), (10, 28.6, "downdraft plenum"), (48.5, 18, "B"), (66, 24, "C  router lift cabinet"),
                    (66, 10, "fence + accessories"), (86.5, 28.3, "charging drawer"), (86.5, 21, "D  drawers"), (86.5, 10.5, "offcut tilt bin")]:
        s.text(X(x), Z(z), t, 9, "#d5d8dd", "middle")
    s.text(X(48.5), Z(14), "bit", 8, "#d5d8dd", "middle"); s.text(X(48.5), Z(11.5), "pull-", 8, "#d5d8dd", "middle"); s.text(X(48.5), Z(9), "out", 8, "#d5d8dd", "middle")
    s.text(X(114), Z(14), "wing storage", 9, "#d5d8dd", "middle")
    s.dim_h(X(0), X(96), Z(-5) + 22, "96\"", 11); s.dim_h(X(96), X(132), Z(-5) + 22, "36\"", 11)
    s.dim_v(X(-8), Z(34), Z(0), "34\"", 11); s.dim_v(X(140), Z(34), Z(31.75), "2-1/4\"", 9)
    s.line(X(-10), Z(0), X(140), Z(0), "#999", 1)
    s.save(os.path.join(OUT, "02-south-elevation.svg"))

# ------------------------------------------------------------- ISOMETRIC
def isometric():
    W, H = 1180, 760
    s = SVG(W, H, "#f6f5f2")
    iso = Iso(s, 4.1, 300, 585)
    s.text(20, 30, "CONCEPT RENDER  -  L-shaped island seen from the south-west (the working side)", 16, weight="bold")
    s.text(20, 48, "Continuous 2-1/4\" hard maple top over charcoal cabinet bases. Table saw sits against the north (far) edge.", 11, "#555")
    # floor shadow
    iso.face([(-6, -54, 0), (140, -54, 0), (140, 54, 0), (-6, 54, 0)], "#ebe9e4", "none")
    # ---- table saw (far side)
    iso.box(37, 77, 51, 74, 0, 32.5, CAST, STEEL_DK, STEEL_DK)                       # stand / motor housing
    for (x0, y0) in [(11, 51), (11, 71), (31, 51), (31, 71)]: iso.box(x0, x0 + 2, y0, y0 + 2, 0, 32.5, STEEL, STEEL_DK, STEEL_DK)
    iso.box(SAW["x0"], SAW["ext_x1"], SAW["y0"], SAW["y1"], 32.75, TOP_HEIGHT, "#e7e2d8", "#cfc9bd", "#bdb7ab")   # extension table
    iso.box(SAW["ext_x1"], SAW["x1"], SAW["y0"], SAW["y1"], 32.5, TOP_HEIGHT, CAST, STEEL_DK, STEEL_DK)           # cast iron
    iso.box(SAW["x0"] - 5, SAW["x1"] + 3, SAW["y1"], SAW["y1"] + 2.5, 31.0, 33.5, STEEL, STEEL_DK, STEEL_DK)      # front rail
    iso.box(44, 46.5, SAW["y0"], SAW["y1"] + 4, TOP_HEIGHT, TOP_HEIGHT + 3.5, "#fbbf24", "#d97706", "#b45309")   # rip fence
    bx = SAW["blade_x"]
    for dx in (-SAW["slot_offset"], SAW["slot_offset"]): iso.line((bx + dx, SAW["y0"], TOP_HEIGHT), (bx + dx, SAW["y1"], TOP_HEIGHT), "#555", 1.4)
    iso.face([(bx - 0.1, SAW["y0"] + 8, TOP_HEIGHT), (bx + 0.1, SAW["y0"] + 8, TOP_HEIGHT), (bx + 0.1, SAW["y0"] + 18, TOP_HEIGHT + 3), (bx - 0.1, SAW["y0"] + 18, TOP_HEIGHT + 3)], "#111", "#111")
    # ---- wing north part (behind island)
    iso.box(96, 132, 0, 48, 0, TOE_KICK, TOE, TOE, TOE); iso.box(96, 132, 0, 48, TOE_KICK, TOP_HEIGHT - TOP_THICK, FRONT, FRONT, SIDE, faces="ts")
    # ---- island base
    iso.box(3, 96, 3, 48, 0, TOE_KICK, TOE, TOE, TOE)
    iso.box(0, 96, 0, 48, TOE_KICK, TOP_HEIGHT - TOP_THICK, FRONT, FRONT, SIDE)
    # ---- wing south part base
    iso.box(99, 132, -48, 3, 0, TOE_KICK, TOE, TOE, TOE)
    iso.box(96, 132, -48, 0, TOE_KICK, TOP_HEIGHT - TOP_THICK, FRONT, FRONT, SIDE)
    # ---- one continuous L-shaped top
    zt, zb = TOP_HEIGHT, TOP_HEIGHT - TOP_THICK
    L = [(-1, -1), (95, -1), (95, -49), (133, -49), (133, 48), (-1, 48)]
    # edge (thickness) faces that face the viewer: south & west edges
    iso.face([(-1, -1, zb), (95, -1, zb), (95, -1, zt), (-1, -1, zt)], MAPLE_EDGE)
    iso.face([(-1, -1, zb), (-1, 48, zb), (-1, 48, zt), (-1, -1, zt)], "#b8975c")
    iso.face([(95, -49, zb), (95, -1, zb), (95, -1, zt), (95, -49, zt)], "#b8975c")
    iso.face([(95, -49, zb), (133, -49, zb), (133, -49, zt), (95, -49, zt)], MAPLE_EDGE)
    iso.face([(x, y, zt) for x, y in L], MAPLE, "#8a6a35", 1)
    # subtle lamination lines on top (strips run E-W on island, N-S on wing)
    for yy in range(2, 48, 6): iso.line((0, yy, zt), (95, yy, zt), "#d4b37e", 0.5)
    for xx in range(98, 132, 6): iso.line((xx, -48, zt), (xx, 48, zt), "#d4b37e", 0.5)
    # ---- top details
    g = DOG_GRID
    for i in range(int((g["x1"] - g["x0"]) / g["pitch"]) + 1):
        for j in range(int((g["y1"] - g["y0"]) / g["pitch"]) + 1):
            iso.dot_top(g["x0"] + i * g["pitch"], g["y0"] + j * g["pitch"], zt, 0.55, "#3b2a12")
    f = FRONT_ROW
    for i in range(int((f["x1"] - f["x0"]) / f["pitch"]) + 1): iso.dot_top(f["x0"] + i * f["pitch"], f["y"], zt, 0.55, "#3b2a12")
    for dx in (-SAW["slot_offset"], SAW["slot_offset"]): iso.line((bx + dx, 48, zt), (bx + dx, 48 - OUTFEED_GROOVE_LEN, zt), "#6b5330", 1.6)
    rp = ROUTER_PLATE
    iso.rect_top(rp["cx"] - rp["w"] / 2, rp["cx"] + rp["w"] / 2, rp["cy"] - rp["h"] / 2, rp["cy"] + rp["h"] / 2, zt, "#f3ede0", "#6b5330", 1)
    iso.dot_top(rp["cx"], rp["cy"], zt, 1.6, "#c9c2b2")
    t = ROUTER_TTRACK
    for yy in (t["y_front"], t["y_fence"]): iso.line((t["x0"], yy, zt), (t["x1"], yy, zt), "#4b5563", 2.2)
    for xx in (t["x0"], t["x1"]): iso.line((xx, t["y_front"], zt), (xx, t["y_fence"], zt), "#4b5563", 2.2)
    iso.rect_top(WAGON_VISE["x0"], WAGON_VISE["x1"], WAGON_VISE["y0"], WAGON_VISE["y1"], zt, "#9aa5b4", "#334155")
    iso.box(FACE_VISE["x0"], FACE_VISE["x1"], -3, -1, 25.5, zt - 0.1, "#b5c1d1", "#8e9bad", "#7b889a")   # vise chop
    # ---- south face fronts (drawn as slightly lighter panels with reveal lines)
    def front(x0, x1, z0, z1, fill=FRONT_DK):
        iso.face([(x0 + .3, -0.01, z0 + .3), (x1 - .3, -0.01, z0 + .3), (x1 - .3, -0.01, z1 - .3), (x0 + .3, -0.01, z1 - .3)], fill, "#15161a", 0.5)
    for (x0, x1, z0, z1) in [(1, 43, 25.75, 31.5), (1, 43, 18.5, 25.5), (1, 43, 11, 18.25), (1, 43, 4.25, 10.75), (43, 54, 4.25, 31.5),
                             (54, 78, 16, 31.5), (54, 78, 4.25, 15.75), (78, 95, 25, 31.5), (78, 95, 17, 24.75), (78, 95, 4.25, 16.75)]:
        front(x0, x1, z0, z1)
    iso.face([(64, -0.05, 26.5), (68, -0.05, 26.5), (68, -0.05, 29), (64, -0.05, 29)], "#dc2626", "#7f1d1d")
    # west end fronts
    def wfront(y0, y1, z0, z1, fill=SIDE):
        iso.face([(-0.01, y0 + .3, z0 + .3), (-0.01, y1 - .3, z0 + .3), (-0.01, y1 - .3, z1 - .3), (-0.01, y0 + .3, z1 - .3)], "#33363c", "#1d1f23", 0.5)
    wfront(1, 30, 4.25, 25.5); wfront(1, 47, 25.75, 31.5); wfront(31, 47, 12.25, 25.5); wfront(31, 47, 4.25, 12)
    # wing west (alcove) fronts
    def afront(y0, y1, z0, z1):
        iso.face([(95.99, y0 + .3, z0 + .3), (95.99, y1 - .3, z0 + .3), (95.99, y1 - .3, z1 - .3), (95.99, y0 + .3, z1 - .3)], "#33363c", "#1d1f23", 0.5)
    afront(-47, -8, 16, 26.5); afront(-47, -8, 4.25, 15.75); afront(-8, -1, 4.25, 26.5)
    iso.face([(95.99, -40, 27.5), (95.99, -8, 27.5), (95.99, -8, 29.5), (95.99, -40, 29.5)], "#dc2626", "#7f1d1d")  # miter paddle switch strip
    # ---- miter station
    m = MITER_WELL
    iso.rect_top(m["x0"], m["x1"], m["y0"], m["y1"], zt, "#7a6136", "#4a3a1e")          # well opening
    iso.box(99, 123, -35, -13, 30, zt, "#d7d3cc", "#b8b3aa", "#a19c93")                 # saw bed (flush)
    iso.box(112, 114, -35, -13, zt, zt + 4, "#c9c5be", "#a9a49b", "#8f8a82")            # saw fence
    iso.box(101, 117, -27, -21, zt + 4, zt + 16, "#e8e6e1", "#c7c3bc", "#aca7a0")      # head / motor
    iso.box(117, 124, -26, -25, zt + 11, zt + 12, STEEL, STEEL_DK, STEEL_DK); iso.box(117, 124, -23, -22, zt + 11, zt + 12, STEEL, STEEL_DK, STEEL_DK)
    iso.face([(103, -24.2, zt + 3), (115, -24.2, zt + 3), (115, -23.8, zt + 15), (103, -23.8, zt + 15)], "#444", "#222")   # blade
    h = MITER_HOOD
    iso.box(h["x0"], h["x1"], h["y0"], h["y1"], zt, h["z1"], "#5b21b6", "#6d28d9", "#4c1d95")
    iso.face([(h["x0"], h["y0"], zt + 8), (h["x0"], h["y1"], zt + 8), (h["x0"], h["y1"], h["z1"]), (h["x0"], h["y0"], h["z1"])], "#3b0764", "#2e1065")  # hood mouth
    # pull-out extension (shown extended)
    iso.box(99, 129, -84, -48, zt - 1.5, zt, "#e9d9b5", "#c9b98f", "#b3a37c")
    iso.box(112, 116, -83, -50, zt - 4.5, zt - 1.5, STEEL, STEEL_DK, STEEL_DK)
    # ---- callouts
    def call(x, y, z, tx, dx, dy):
        X, Y = iso.p(x, y, z); s.line(X, Y, X + dx, Y + dy, "#333", 0.8); s.circle(X, Y, 2.2, "#333", "none"); s.label(X + dx, Y + dy - 2, tx, 11, "#111", "middle")
    call(20, 24, zt, "A  dog-hole field + downdraft", -60, -150)
    call(66, 15, zt, "C  router lift, T-track", -10, 150)
    call(60, 40, zt, "B  outfeed with miter-slot grooves", 120, -120)
    call(114, 24, zt, "D  glue-up / assembly", 160, -105)
    call(111, -24, zt + 16, "E  miter saw in well", 130, -60)
    call(128, -24, zt + 14, "hood -> 6\" trunk", 120, 30)
    call(114, -70, zt, "36\" pull-out extension", 50, 60)
    call(27, -2, 30, "face vise", -100, 50)
    call(0, 39, 18, "clamp garage (long clamps slide in from this end)", 40, 150)
    call(48, -0.1, 18, "router-bit pull-out", -40, 120)
    call(30, 62, 36, "SawStop CNS + 36\" extension (operator on far side)", 120, -110)
    s.text(20, H - 22, "Not to scale for the saw's stand and motor; bench geometry is dimensionally accurate to the model in tools/model.py.", 10, "#777")
    s.save(os.path.join(OUT, "03-isometric-concept.svg"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    plan(); elevation(); isometric(); print("rendered")
