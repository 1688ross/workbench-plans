# workbench-plans

Complete plans for a purpose-built woodworking workbench island: outfeed for a SawStop 10" Contractor Saw with the 36" extension, router lift station, a miter station whose saw flips up out of the base on a two-sided platform, a 3/4" dog-hole clamping station over a downdraft plenum, a laser-engraver well, built-in dust ducting for two collectors, built-in power with USB, and a lot of storage. Footprint 69" x 96", top at 34-3/4".

**Start here:** [`workbench-plans.pdf`](workbench-plans.pdf) is the whole set as one landscape PDF (72 pages). [`index.html`](index.html) is the same set as a web page. Or read the documents in order below.

## Documents

| Document | What it is |
|---|---|
| [`docs/01-design-decisions.md`](docs/01-design-decisions.md) | The concept, what your answers decided, key dimensions, the VERIFY-before-cutting list |
| [`docs/02-materials-and-hardware.md`](docs/02-materials-and-hardware.md) | Every material and hardware item with quantities and a cost estimate (~$4,400 all in) |
| [`docs/03-cut-list.md`](docs/03-cut-list.md) | Every piece of wood, by build step and by material; sheet counts from real nesting |
| [`docs/04-build-guide.md`](docs/04-build-guide.md) | 13 steps in build order, each with parts, tools, procedure, checks and its drawing |
| [`docs/05-dust-collection.md`](docs/05-dust-collection.md) | Two-trunk ducting (4" collector + 2-1/2" vac), drops, gates, rules |
| [`docs/06-electrical.md`](docs/06-electrical.md) | One 20 A feed, strips, outlets, switches, LED |
| [`docs/07-stations.md`](docs/07-stations.md) | How to use each station; storage map |
| [`docs/00-design-brief.md`](docs/00-design-brief.md) | Stage-1 brief (history); [`docs/answers-raw.txt`](docs/answers-raw.txt) are the owner's answers |

## Drawings (`renders/`)

| Files | Content |
|---|---|
| `10-12-final-look-*.svg` | Isometric final look: stowed, in use, and from the router side |
| `20-plan.svg`, `21-24-elevation-*.svg` | Sheet 1 plan; Sheets 2-5 elevations of all four faces |
| `30-32-section-*.svg` | Sections through the router station, the flip bay (stowed, mid-swing, up), and the duct spine |
| `40-router-station.svg`, `41-miter-hatch.svg` | Router station detail; flip-top platform and its safety system |
| `50-dust-routing.svg`, `51-electrical.svg` | Routing plans |
| `cuts/*.svg` | Nested cut diagrams per material (12 sheets 3/4" BB, 2 of 1/2", 2 of 1/4", 2 MDF, maple boards) |
| `601-613-step-*.svg` | One isometric view per build step, new parts highlighted |

## Regenerating

Everything is generated from one geometry file, so a changed dimension propagates to every drawing, the cut list and the sheet count:

```
python3 tools/build_all.py                    # drawings, cut list, index.html
python3 tools/build_pdf.py [--chromium PATH]  # workbench-plans.pdf (needs Playwright + Chromium)
```

`tools/model.py` holds the geometry (inches; x = east, y = north toward the saw, z = up). `tools/parts.py` derives every part. `tools/cutlist.py` nests parts onto sheets. `tools/render_*.py` draw the SVGs; `tools/build_docs.py` writes the cut list; `tools/build_site.py` writes `index.html`. No dependencies beyond Python 3.
