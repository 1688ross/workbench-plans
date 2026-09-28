# Design decisions — stage 2

This records what changed after your answers (transcribed in `answers-raw.txt`) and why. The stage-1 brief is kept as history in `00-design-brief.md`.

## The one big change: no more L

You set a hard rule that the bench be no wider than the saw with its 36" extension (69-1/8"). That rule kills the stage-1 L-shape for a reason that isn't obvious until you draw the outfeed path: an 8' board being ripped travels the full length of the bench at table height. With only 69" of width, a rip between the blade and the fence occupies the middle of the top (x = 11" to 47" from the west edge), and any tool that stands above the top in that path gets hit. A miter saw in a wing beside the outfeed strip is exactly such a tool.

So the miter saw has to *disappear* when it is not in use. The answer is a **hydraulic scissor lift table** on the shop floor inside the base. The DWS779 bolts to a sub-platform on the lift; pump the pedal and it rises through a 29" x 42-1/2" hatch in the south end of the top until its deck is flush at 34-3/4". Release the valve and it sinks below the top; two lift-off leaves close the hatch and the whole 69" x 96" top is flat again. The dust hood rides on the same platform, so its hose stays connected.

This is also the answer to your request for "more tech": a saw that rises out of the bench on demand is the signature feature.

## Concept: four faces, four stations

A 69" x 96" island, 34-3/4" tall, with the table saw docked against the north edge.

| Face | Station | What is there |
|---|---|---|
| North | Outfeed | Flat 20" strip with two 14" grooves aligned to the miter slots; bridge lip over the saw's rear rail; a 30" x 15" recess in the base (the motor bay) for the CNS motor and its 4" dust hose. |
| West | Hand work / clamping station | 9" quick-release face vise at the north end; 81-hole 3/4" dog field on 4" centres over a sealed downdraft plenum; W1 hand-tool drawers incl. a switched charging drawer; W2 holds the laser on a pull-out tray. |
| East | Router station | JessEm Rout-R-Lift II in a 9-1/4 x 11-3/4 plate recess, 12" from the edge; two fence T-tracks 26" apart; combo T-track/miter slot; sealed router box ducted to the spine; 2-1/2" vac port for the fence; vertical bit pull-out; two gasketed doors; paddle switch. |
| South | Miter station | DWS779 on the scissor lift; hatch; drop-leaf wings 24" x 24" on both ends (46" of support each side with the bench); long-item drawers; clamp-rack pull-out; pedal flap. |
| Top, NW | Laser well | 22" x 15" opening with a flush insert. Remove the insert and drop the floor panel onto cleats at 2", 4-1/2" or 7" below the top; rest the Falcon A1 over the opening for rotary work. |

## Your answers, and what each one decided

| Your answer | Decision |
|---|---|
| Shop 12' x 20', bench no wider than the saw, fixed, ceiling 7.5' | 69" x 96" island; ten 1,000 lb levelling feet, no casters. Total floor with the saw and walking room: about 6' x 16'. Raised saw tops out at 56-1/4", well under the ceiling. |
| SawStop CNS, 36" T-Glide, 34-3/4" assembled height | Top at 34-3/4"; levelers give +/- 3/4". Blade lands 47-1/8" from the west edge. **Measure** the rear-rail height and the motor's projection before cutting the bay. |
| DeWalt DWS779 | Sub-platform sized 28 x 41; hatch 29 x 42-1/2. Lift spec: lowered <= 9-1/4", raised >= 28-1/4", 500 lb. **Verify** the saw's locked-down height (design assumes 21-1/2") and deck height (4-1/2"). |
| DW618 + JessEm Rout-R-Lift II (to be bought again) | Plate recess 9-1/4 x 11-3/4 x 3/8 with leveling screws; box 22 x 20 x 20-1/2 clears the lift. Your existing fence: check its clamp spacing against the 26" track spacing before cutting the dados. |
| HF collector (4") *and* shop vac + cyclone (2-1/2") | Two trunks side by side in the spine: 4" main and 2-1/2" vac. Five 4" gates, two 2-1/2" gates. See `05-dust-collection.md`. |
| 120 V, 20 A max, likes the power-strip approach | Single 20 A feed to a flush inlet, metal main strip with master switch, branch strips, flush USB strips on W/S/E faces, paddle switches at router and miter. See `06-electrical.md`. |
| 3/4" dogs, Rockler accessories | 3/4" holes on a 4" grid; 2-1/4" of material at the holes (top + doubler) so dogs and holdfasts grip. |
| "vise" | One 9" quick-release face vise at the NW corner of the west face, jaw liners in maple. A tail/wagon vise was dropped to keep the top uninterrupted. |
| Clamping station + clamp rack | The dog field is the clamping station (dogs, holdfasts, Rockler clamps, dog-hole pipe-clamp cradles); the clamp rack is a 16" x 28" x 20" vertical pull-out at the south-east. |
| Everything flush at saw height | Yes, everywhere, including the miter deck when raised. |
| Top: cheap but ideal; MDF worked OK | **3/4" Baltic birch over 3/4" MDF**, glued, 1-1/2" maple edge, hardwax-oil or wipe-on poly finish; a third 3/4" BB layer (the doubler) under the dog field. About $330 in sheet goods vs $1,000+ for maple, flatter than solid wood, and the birch face drills and wears far better than MDF. |
| Style: different from the Shop Nation bench, more character and tech | The rising saw, the laser well, the downdraft dog field, charcoal fronts with natural birch edges under a maple-edged top, LED strip under the overhang, USB-C at every face. |
| Creality Falcon A1, 15 x 22 drop area | Well at the NW of the top, tray in W2 on 30" slides. **Verify** the laser's footprint (design allows 26 x 23 x 7-1/2). Its exhaust hose goes to a window, never into the dust system. |

## Key dimensions

| Item | Value |
|---|---|
| Top | 69" x 96" x 1-1/2", edges 1-1/2" maple; overhang 1" on E, S, W; flush at N |
| Height | 34-3/4" finished; base 33-1/4" on a 4" plinth recessed 3" |
| Cabinet depth | 40" on the west face (36" drawers), 22" on the east, 45" on the south |
| Hatch | 29" x 42-1/2", two leaves 28-3/4" x 21", 1" maple ledge, removable centre bar |
| Motor bay | 30" x 15" x full height, centred 49" from the west edge |
| Plenum | 40" x 34" x 6", sealed, one 4" inlet on its east wall |
| Laser well | 22" x 15", floor 2" / 4-1/2" / 7" below the top |
| Spine duct | 5" x 8" chase at floor level, 79" long, under the SE and E2 cabinets |
| Router plate | centre 12" from the east edge, 62" from the south edge |
| Drop-leaves | 24" x 24", top-hinged, folding brackets |

## Things you must measure before cutting (the VERIFY list)

1. Table height of the CNS on its mobile base, and the height of the top of the rear rail. Decides the leveler setting and the bridge lip.
2. How far the motor housing projects behind the table at 0 and 45 degrees of tilt. The bay is 15" deep; deepen it if needed.
3. Distance from the blade to each miter slot (design uses 5-1/2"). Sets the outfeed grooves.
4. DWS779: overall height with the head locked down, deck height, and the rails' rearmost point. Sets the lift's lowered/raised limits and the hatch length.
5. Your router fence's clamp spacing. Sets the fence-track spacing (26" in the drawings).
6. The Falcon A1's footprint and height. Sets the tray and the well.
7. The lift table you buy: platform size, lowered and raised heights. Adjust `LIFT_TABLE` in `tools/model.py` and re-run `tools/build_all.py`; every drawing updates.
