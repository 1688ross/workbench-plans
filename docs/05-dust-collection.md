# Dust collection

*Drawings: Sheet 8 (`renders/32-section-C-ducts.svg`), Sheet 11 (`renders/50-dust-routing.svg`), step view `605-step-05.svg`.*

## Two systems, one chase

You have a Harbor Freight collector with 4" ducting on this side of the shop and a DeWalt shop vac behind a cyclone separator. They do different jobs and want different pipe:

| | HF collector | Shop vac + cyclone |
|---|---|---|
| Moves | high volume, low pressure (~600-800 CFM claimed, 350-450 real through 4") | low volume, high pressure (~100-150 CFM through 2-1/2") |
| Good at | hoods, chips, the table saw, the router box, the floor sweep, the downdraft field | small ports right at the cut: router fence, miter saw chute |
| Pipe | 4" | 2-1/2" |

So the bench carries **both trunks side by side** in the 5" x 8" spine chase at floor level: the 4" main below, the 2-1/2" vac trunk above it. Each has its own port on the east face at the utility column (4" at 6" above the floor, 2-1/2" at 10"), so you connect each machine to its own trunk and never need a reducer.

## Drops

| # | Drop | Trunk | Gate location | Notes |
|---|---|---|---|---|
| 1 | Floor sweep | 4" | south toe kick, behind a flap | sweep the shop floor straight into it |
| 2 | Miter hood | 4" | flip-bay east wall | 4' of 4" flex with a quick-connect cuff; plug it onto the hood after each flip |
| 3 | Router box | 4" | router-box floor | box is sealed; 1" x 4" make-up-air slot on the north partition |
| 4 | Downdraft plenum | 4" | service gap (reach through the W-BAND1 clean-out) | 81 holes x 0.44 sq in = 36 sq in of open area; at 350 CFM that is ~1,400 fpm through the holes, plenty for sanding |
| 5 | Table saw | 4" | motor-bay south wall | 4' of 4" flex to the CNS's own port |
| 6 | Router fence | 2-1/2" | behind the flip-lid port in the east edge band | your fence's hose plugs into the face of the bench |
| 7 | Miter saw chute | 2-1/2" | flip-bay east wall | 3' of 2-1/2" flex to the DWS779's port, connected after the flip |

## Rules that make it pull

1. **One 4" gate open at a time** on the HF collector. It cannot feed two hoods at once through 4" pipe.
2. **Wyes, not tees.** Every branch enters the trunk through a 45-degree wye pointing toward the port.
3. **No 90s.** Two 45s with a short straight between them where the run must turn (the leg at the north end).
4. **Straight and short.** The spine is 79" of straight pipe. The longest drop (miter hood) is 6' of flex; everything else is under 3'.
5. **Seal the boxes.** Silicone every plenum joint; foam-tape the router doors; the router box has one deliberate air inlet and nothing else.
6. **Clean-outs.** The floor-sweep gate doubles as the south clean-out; the utility-column flanges are the north clean-out.
7. **Static.** Ground the 4" run with a bare copper wire inside if you use PVC and get shocks; not strictly needed on a run this short.

## The miter hood

A 28" wide x 6" deep x 14" tall box on the flip core behind the saw, open toward the blade, with a floor sloped to a 4" port low at the back. Height 14" puts its top about 9-1/2" above the bench top when the saw is up. It flips with the saw; the hose has a quick-connect cuff that you push on after the platform is locked. Add a strip of 1/8" brush or rubber flap across the top edge if you want to catch the high spray from a slider.

## Optional automation

An iVac-style tool sensor on the router and miter outlets can start the collector and open a motorised gate. The wiring is on the main strip; the gates replace the manual ones at drops 2 and 3. Do this later if the manual routine bothers you.
