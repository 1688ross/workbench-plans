"""Single source of truth for the workbench geometry (inches).

Coordinate system: x = east (across the saw's width), y = north (toward the
table saw), z = up. Origin: south-west corner of the TOP at floor level.

Stage 2 concept: a 69" x 96" island, same width as the SawStop with its 36"
extension. Four faces, four stations:
  north  - outfeed for the table saw (motor bay recessed into the base)
  west   - hand-work face: front vise, 3/4" dog field over a downdraft plenum
  east   - router station (JessEm Rout-R-Lift II, DW618)
  south  - miter station: DWS779 on a flip-top platform that rotates through
           a hatch (saw up / flush box up); drop-leaf wings on both sides
plus a laser well (Creality Falcon A1) in the north-west of the top, a
clamp-rack pull-out, and a vertical router-bit pull-out.
Stage 2b: the miter saw sits on a two-sided FLIP-TOP platform instead of a
scissor lift (owner's request).
"""
from fractions import Fraction

# ---------------------------------------------------------------- datum
TOP_HEIGHT = 34.75          # SawStop CNS assembled table height (spec). Levelers give +-3/4".
TOP_THICK = 1.5             # 3/4" Baltic birch over 3/4" MDF
TOP_UNDER = TOP_HEIGHT - TOP_THICK          # 33.25
PLINTH_H = 4.0              # levelling feet + toe kick zone (z 0..4)
TOE_RECESS = 3.0
CARCASS_Z0 = PLINTH_H        # cabinets sit on the plinth at z = 4
PLY = 0.75; PLY_HALF = 0.5; PLY_QTR = 0.25

# ---------------------------------------------------------------- top
TOP = dict(x0=0.0, x1=69.0, y0=0.0, y1=96.0)     # 69 x 96 (1/8" under the saw's 69-1/8")
EDGE_BAND = 1.5             # hard maple edging on E, S, W edges (1.5 x 1.5)
BASE = dict(x0=1.0, x1=68.0, y0=1.0, y1=95.0)   # base outline: 1" overhang all round

# ---------------------------------------------------------------- table saw (SawStop CNS + 36" T-Glide)
SAW = dict(x0=0.0, x1=69.125, y0=97.0, y1=124.0,     # table 27" deep; 1" over the rear rail
           ext_x1=23.75,                            # laminate extension on the WEST (operator's right)
           blade_x=69.125 - 22.0,                   # 47.125: 22" from the east edge of the cast iron
           slot_offset=5.5,                         # miter-slot centre from blade  (MEASURE)
           motor_protrusion=15.0)                   # rear motor housing behind the table (MEASURE)
OUTFEED_GROOVE = dict(len=14.0, w=0.75, d=0.375)   # grooves in top aligned to miter slots, from north edge
MOTOR_BAY = dict(x0=34.0, x1=64.0, y0=80.0, y1=95.0)   # recess in the base for the CNS motor + dust port
BRIDGE_LIP = dict(w=3.0, t=0.5)                    # hardwood lip over the rear rail (MEASURE rail height)

# ---------------------------------------------------------------- west face: hand-work station
DOG_GRID = dict(x0=4.0, x1=36.0, y0=46.0, y1=78.0, pitch=4.0, dia=0.75)   # 9 x 9 = 81 holes
PLENUM = dict(x0=1.0, x1=41.0, y0=46.0, y1=80.0, z0=26.5, z1=32.5)        # sealed downdraft/holdfast void
DOUBLER = dict(x0=1.0, x1=41.0, y0=46.0, y1=80.0)                         # 3/4" BB under the top = plenum lid
FACE_VISE = dict(y0=84.0, y1=94.0, jaw=9.0, block=dict(x0=1.0, x1=13.0, y0=82.0, y1=95.0, z0=24.0))
LASER_WELL = dict(x0=12.0, x1=34.0, y0=78.0, y1=93.0, depth_max=8.5, cleats=(2.0, 4.5, 7.0))  # 22 x 15 opening
LASER = dict(w=26.0, d=23.0, h=7.5)   # Creality Falcon A1 10W envelope (VERIFY)

# ---------------------------------------------------------------- east face: router station
ROUTER_PLATE = dict(cx=57.0, cy=62.0, w=9.25, h=11.75, thick=0.375)   # JessEm Rout-R-Lift II plate, long axis N-S
ROUTER_TRACKS = dict(fence_y=(49.0, 75.0), fence_x=(42.0, 68.0),       # two E-W T-tracks the fence clamps into
                     combo_x=64.5, combo_y=(46.0, 78.0))               # N-S combo T-track/miter slot near the operator
ROUTER_BOX = dict(x0=46.0, x1=68.0, y0=52.0, y1=72.0, z0=12.75, z1=TOP_UNDER)   # sealed dust box around the router
ROUTER_FENCE_PORT = dict(x=68.0, y=62.0, z=31.0, dia=2.5)             # flip-lid vac port in the east apron

# ---------------------------------------------------------------- south face: miter station on a FLIP-TOP
# A two-sided platform pivots on an E-W axle inside the lift bay. Saw on one face, a hollow
# "flush box" on the other. Both stand the same 4-1/2" (the saw's deck height) off the core,
# so whichever side is up, the working surface is flush with the top at 34-3/4".
MITER_SAW = dict(model="DeWalt DWS779", w=24.5, d=32.0, base_d=22.0, h_locked=21.5, deck=4.5, weight=56)   # VERIFY h_locked/deck/base_d
LIFT_BAY = dict(x0=18.0, x1=50.0, y0=1.0, y1=46.0)                     # open floor; doors on the south face
FLIP = dict(axle_y=22.0,                                               # E-W axle, N-S position
            axle_z=TOP_HEIGHT - 4.5 - 1.0,                             # 29.25: 5-1/2" below the top surface
            core_len=24.0, core_w=28.0, core_t=2.0,                    # N-S x E-W x thick (two 3/4 BB skins on a 1/2 BB rib frame)
            box_h=4.5, box_w=26.0,                                     # flush box on the underside; 1" narrower than the core each side for the rest blocks
            rod=1.0, bearings=2, plungers=2, toggle_clamps=2, rest_blocks=4, counterweight_lb=70, seat_switch=True,
            swing_radius=((24.0 / 2) ** 2 + (21.5 + 1.0) ** 2) ** 0.5)  # 25.5: saw's top corners
HATCH = dict(x0=19.5, x1=48.5, y0=FLIP["axle_y"] - 12.25, y1=FLIP["axle_y"] + 12.25, chamfer=0.5)   # 29 x 24-1/2; 45-deg chamfer under the N/S edges
MITER_HOOD = dict(x0=20.0, x1=48.0, y0=FLIP["axle_y"] + 6.0, y1=FLIP["axle_y"] + 12.0, h=14.0)      # on the core's north end; quick-connect hose
DROP_LEAF = dict(y0=4.0, y1=28.0, len=24.0)                            # 24 x 24 leaves on E and W faces, south end
SAW_DECK_Z = TOP_HEIGHT - MITER_SAW["deck"]                            # 30.25: core's upper face when the saw is up
BAY_DOORS = dict(x0=18.0, x1=50.0, z0=4.0, z1=TOP_UNDER)               # two 16" doors; open them before flipping

# ---------------------------------------------------------------- base cabinets  (x0,x1,y0,y1,z0,z1, opens toward)
CABS = {
    "SW":  dict(x0=1.0,  x1=18.0, y0=1.0,  y1=46.0, z0=4.0,   z1=TOP_UNDER, face="S", label="Long-item drawers"),
    "SE":  dict(x0=50.0, x1=68.0, y0=1.0,  y1=46.0, z0=12.75, z1=TOP_UNDER, face="S", label="Clamp rack + bit pull-out"),
    "W1":  dict(x0=1.0,  x1=41.0, y0=46.0, y1=66.0, z0=4.0,   z1=26.5,      face="W", label="Hand-tool drawers"),
    "W2":  dict(x0=1.0,  x1=34.0, y0=66.0, y1=95.0, z0=4.0,   z1=24.0,      face="W", label="Laser tray + drawer"),
    "E2":  dict(x0=46.0, x1=68.0, y0=46.0, y1=76.0, z0=12.75, z1=TOP_UNDER, face="E", label="Router cabinet"),
}
SPINE = dict(x0=50.0, x1=55.0, y0=1.0, y1=80.0, z0=4.0, z1=12.0)       # main duct chase under SE/E2
DUCT_LEG = dict(x0=50.0, x1=68.0, y0=76.0, y1=80.0, z0=4.0, z1=12.0)   # E-W leg to the utility ports
SERVICE_GAP = dict(x0=41.0, x1=46.0, y0=46.0, y1=80.0)                 # riser + wiring gap between W and E cabinets
UTILITY = dict(face="E", y0=76.0, y1=80.0, port4_z=6.0, port25_z=10.0, inlet_z=18.0)

# ---------------------------------------------------------------- dust ducting
DUCT = dict(main=4.0, vac=2.5,
            drops=[  # name, gate location (x,y,z), size
                ("Floor sweep (south toe kick)",        (52.5, 1.0,  8.0), 4.0),
                ("Miter hood (quick-connect flex)",      (50.0, 30.0, 8.0), 4.0),
                ("Router box",                          (52.5, 62.0, 12.75), 4.0),
                ("Downdraft plenum riser",              (43.5, 70.0, 12.0), 4.0),
                ("Table saw (hose into motor bay)",     (49.0, 80.0, 8.0), 4.0),
                ("Router fence (vac)",                  (68.0, 62.0, 31.0), 2.5),
                ("Miter saw chute (vac, flex)",         (50.0, 26.0, 11.0), 2.5),
            ])

# ---------------------------------------------------------------- drawers / openings (front layout per face)
# each: face, x/y range along the face, z0, z1, kind
FRONTS = [
    # south face
    ("S", 1.0, 18.0, 4.0, 13.5, "drawer", "SW-D3 long drawer (bottom)"),
    ("S", 1.0, 18.0, 13.5, 23.25, "drawer", "SW-D2 long drawer"),
    ("S", 1.0, 18.0, 23.25, TOP_UNDER, "drawer", "SW-D1 long drawer (top)"),
    ("S", 18.0, 34.0, 4.0, TOP_UNDER, "door", "flip-bay door L"),
    ("S", 34.0, 50.0, 4.0, TOP_UNDER, "door", "flip-bay door R + paddle switch"),
    ("S", 50.0, 68.0, 12.75, TOP_UNDER, "pullout", "clamp rack pull-out"),
    # east face
    ("E", 30.0, 46.0, 12.75, TOP_UNDER, "pullout", "router-bit pull-out"),
    ("E", 46.0, 61.0, 12.75, TOP_UNDER, "door", "router cabinet door L (gasketed)"),
    ("E", 61.0, 76.0, 12.75, TOP_UNDER, "door", "router cabinet door R (gasketed) + paddle switch"),
    # west face
    ("W", 46.0, 66.0, 4.0, 11.5, "drawer", "W1-D3"),
    ("W", 46.0, 66.0, 11.5, 19.0, "drawer", "W1-D2"),
    ("W", 46.0, 66.0, 19.0, 26.5, "drawer", "W1-D1 charging drawer"),
    ("W", 66.0, 95.0, 4.0, 15.0, "drawer", "W2-D2"),
    ("W", 66.0, 95.0, 15.0, 24.0, "pullout", "laser tray"),
]

# ---------------------------------------------------------------- helpers
def frac(v, den=16):
    """1.5 -> 1-1/2, 0.375 -> 3/8, 24 -> 24"""
    f = Fraction(v).limit_denominator(den)
    whole, rem = divmod(f.numerator, f.denominator)
    if rem == 0: return f"{whole}"
    if whole == 0: return f"{rem}/{f.denominator}"
    return f"{whole}-{rem}/{f.denominator}"

def dim(v): return frac(v) + '"'
