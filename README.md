# workbench-plans

Plans for a purpose-built woodworking workbench island: outfeed for a SawStop
10" Contractor Saw with the 36" extension, router lift station, miter station,
dog-hole workbench, built-in dust ducting and electrical, and a lot of storage.

## Index

### Stage 1 — design brief (current)

| Document | Purpose |
|---|---|
| [`docs/00-design-brief.md`](docs/00-design-brief.md) | Concept, station layout, key dimensions, dust and electrical strategy, storage map, suggestions, open questions |
| [`renders/01-plan-view.svg`](renders/01-plan-view.svg) | Plan view with zones and the table saw in place |
| [`renders/02-south-elevation.svg`](renders/02-south-elevation.svg) | South elevation (working face) |
| [`renders/03-isometric-concept.svg`](renders/03-isometric-concept.svg) | Isometric concept render |

### Stage 2 — full plan set (after the brief is signed off)

Materials list, cut lists and cut diagrams, step-by-step guide with visuals,
tool list per section, and a single-page presentation of the whole set.

## Tools

All drawings are generated from one geometry model so dimensions stay
consistent:

```
python3 tools/render_brief.py   # regenerates renders/*.svg from tools/model.py
```

`tools/model.py` holds every dimension in inches (x = east, y = north toward
the table saw, z = up). `tools/svg.py` is a small SVG writer with an
isometric projector.
