"""Single source of truth for the workbench geometry (inches).

Coordinate system: x = east (along the island), y = north (toward the
table saw), z = up. Origin is the island's south-west bottom corner.
"""

# ---- Global datum -----------------------------------------------------
TOP_HEIGHT = 34.0          # SawStop 10" Contractor Saw table height (nominal)
TOP_THICK = 2.25           # laminated hard maple slab
TOE_KICK = 4.0             # levelling-foot / toe-kick zone
TOE_RECESS = 3.0           # toe kick set back from the door plane

# ---- Island (main bench + outfeed) -----------------------------------
ISLAND = dict(x0=0.0, x1=96.0, y0=0.0, y1=48.0)
SOUTH_CAB_DEPTH = 28.0     # cabinets opening to the south face
SERVICE_CHASE = (28.0, 31.0)   # y-range: wiring chase behind cabinets
NORTH_STRIP = (31.0, 48.0)     # y-range: duct trunk + clamp garage
DUCT_CHASE_Z = (4.0, 12.0)     # 6" main trunk lives here
PLENUM = dict(x0=0.0, x1=44.0, y0=0.0, y1=48.0, z0=25.75, z1=31.75)  # downdraft / holdfast void

# Dog-hole field (3/4" on 4" centres - see open question on 20 mm)
DOG_GRID = dict(x0=4.0, x1=40.0, y0=4.0, y1=44.0, pitch=4.0, dia=0.75)
FRONT_ROW = dict(x0=48.0, x1=92.0, y=3.0, pitch=8.0, dia=0.75)

# Vises
WAGON_VISE = dict(x0=1.0, x1=9.0, y0=1.5, y1=6.5)          # inset/wagon vise, west end of front dog row
FACE_VISE = dict(x0=22.0, x1=32.0, jaw=9.0)                # quick-release front vise on south face

# ---- Router station --------------------------------------------------
ROUTER_PLATE = dict(cx=66.0, cy=15.0, w=11.75, h=9.25)     # standard lift plate, long axis E-W
ROUTER_TTRACK = dict(x0=46.0, x1=86.0, y_front=4.0, y_fence=26.0)  # rectangle of T-track
ROUTER_CAB = dict(x0=54.0, x1=78.0)                        # sealed router cabinet, south face

# ---- Table saw (SawStop CNS + 36" T-Glide) ---------------------------
# Operator stands north of the saw feeding south into the island.
# Seen from the operator, the fence/extension is on the right = WEST.
SAW = dict(x0=10.0, x1=79.0,      # 69-1/8" overall table width (25" ext + 12 + 20 + 12 cast)
           y0=49.0, y1=76.0,      # 27" deep; 1" rear-rail gap to outfeed edge
           blade_x=57.0,          # 22" from the east (left) cast-iron edge
           slot_offset=5.5,       # miter slot centre from blade - MEASURE on your saw
           ext_x1=35.0)           # west end of laminate extension table
OUTFEED_GROOVE_LEN = 20.0         # grooves in outfeed top aligned with miter slots

# ---- Miter wing (the short leg of the L) -----------------------------
WING = dict(x0=96.0, x1=132.0, y0=-48.0, y1=48.0)          # 36" deep x 96" long, N-S
MITER_WELL = dict(x0=97.0, x1=124.0, y0=-39.0, y1=-9.0)    # saw sits on plate at bed-flush height
MITER_HOOD = dict(x0=124.0, x1=132.0, y0=-41.0, y1=-7.0, z1=50.0)
WING_PULLOUT = dict(len=36.0)                                # telescoping south extension

# ---- Utility corner ---------------------------------------------------
DUST_PORT = dict(x=92.0, y=48.0, z=8.0, dia=6.0)           # 6" main trunk exits north face, NE corner
POWER_INLET = dict(x=88.0, y=48.0, z=20.0)                 # twist-lock inlet(s), north face, NE corner
