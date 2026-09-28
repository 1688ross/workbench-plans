"""Nest every sheet-goods part onto 4x8 sheets and draw the cut diagrams."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from parts import build, by_material
from cutlist import Part as CPart, nest_sheets, draw_sheets, nest_boards, draw_boards

OUT = os.path.join(os.path.dirname(__file__), "..", "renders", "cuts")
MAT_NAMES = {"BB34": '3/4" Baltic birch (4x8)', "BB12": '1/2" Baltic birch (4x8)', "BB14": '1/4" Baltic birch (4x8)', "MDF34": '3/4" MDF (4x8)'}

def main():
    os.makedirs(OUT, exist_ok=True)
    P = build(); summary = {}
    for mat, ps in by_material(P).items():
        if mat not in MAT_NAMES: continue
        cparts = []
        for p in ps:
            L, W = max(p.length, p.width), min(p.length, p.width)
            # keep the part's stated orientation when grain matters
            if p.grain == "L": L, W = p.length, p.width
            if L > 96.5 or W > 48.5:
                raise ValueError(f"{p.id} too big for a sheet: {p.length} x {p.width}")
            cparts.append(CPart(p.id, L, W, p.qty, grain=("A" if p.grain == "A" else "L"), thick=p.thick, material=("ply" if "BB" in mat else "mdf")))
        sheets = nest_sheets(cparts)
        n = len(sheets)
        # split into files of 6 sheets max
        for i in range(0, n, 6):
            chunk = sheets[i:i + 6]
            path = os.path.join(OUT, f"{mat}-sheets-{i // 6 + 1}.svg")
            draw_sheets(chunk, f"CUT DIAGRAM  -  {MAT_NAMES[mat]}  -  sheets {i + 1} to {i + len(chunk)} of {n}", path,
                        note=f"{n} sheets of {MAT_NAMES[mat]} in total. 1/8\" kerf allowed. Part IDs match docs/03-cut-list.md. Grey = offcut.")
        summary[mat] = n
    # solid maple: 8/4 x 3" stock, 8 ft lengths for edging/beam; count boards by first-fit
    maple = [p for p in P if p.material == "MAPLE"]
    boards = nest_boards([CPart(p.id, p.length, p.width, p.qty) for p in maple], stock_len=96.0)
    draw_boards(boards, "CUT DIAGRAM  -  hard maple, 8/4 x 3\" x 96\" boards (rip to width after cross-cutting)", os.path.join(OUT, "MAPLE-boards.svg"),
                note=f"{len(boards)} boards of 8/4 hard maple, 3\" wide x 8'. Rip each piece to its listed width; the 1-1/2\" edging comes from the same stock.")
    summary["MAPLE_boards"] = len(boards)
    return summary

if __name__ == "__main__":
    print(main())
