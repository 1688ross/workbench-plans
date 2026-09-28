"""Cut-list nesting and cut-diagram rendering.

Parts are (name, length, width, qty[, grain]) in inches. Sheet goods are
nested onto 48 x 96 sheets with a shelf (row) algorithm that respects grain
direction; solid boards are nested onto stock lengths with a first-fit
decreasing algorithm. Both produce SVG cut diagrams via tools/svg.py.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svg import SVG

KERF = 0.125

class Part:
    def __init__(self, name, length, width, qty=1, grain="L", thick=0.75, material="ply"):
        self.name, self.length, self.width, self.qty = name, float(length), float(width), int(qty)
        self.grain, self.thick, self.material = grain, thick, material   # grain "L": long edge follows sheet length (96")
    def __repr__(self): return f"{self.name} {self.length}x{self.width} x{self.qty}"

# ---------------------------------------------------------------- sheets
def nest_sheets(parts, sheet_l=96.0, sheet_w=48.0, kerf=KERF):
    """Guillotine free-rectangle packing (best short-side fit, split along the
    axis that leaves the larger free rectangle). Grain is respected: 'L' parts
    keep their length along the sheet length, 'W' are rotated, 'A' may rotate.
    Returns a list of sheets; each is a list of (part, x, y, w_along_length,
    h_along_width)."""
    items = []
    for p in parts:
        for _ in range(p.qty):
            items.append(p)
    items.sort(key=lambda p: (-(p.length * p.width), -max(p.length, p.width)))
    sheets = []   # each: {"free": [(x,y,w,h)], "parts": [...]}
    def orientations(p):
        if p.grain == "W": return [(p.width, p.length)]
        if p.grain == "A": return [(p.length, p.width), (p.width, p.length)]
        return [(p.length, p.width)]
    def try_place(sh, p):
        best = None
        for fi, (fx, fy, fw, fh) in enumerate(sh["free"]):
            for (l, w) in orientations(p):
                if l <= fw + 1e-9 and w <= fh + 1e-9:
                    score = min(fw - l, fh - w)
                    if best is None or score < best[0]: best = (score, fi, l, w)
        if best is None: return False
        _, fi, l, w = best
        fx, fy, fw, fh = sh["free"].pop(fi)
        sh["parts"].append((p, fx, fy, l, w))
        # split: remaining right strip and remaining top strip; pick split that keeps the bigger rect whole
        right = (fx + l + kerf, fy, fw - l - kerf, fh)
        top = (fx, fy + w + kerf, fw, fh - w - kerf)
        right_s = (fx + l + kerf, fy, fw - l - kerf, w)          # if we split horizontally first
        top_s = (fx, fy + w + kerf, l, fh - w - kerf)
        if (fw - l) * fh >= fw * (fh - w):   # keep full-height right rect
            cand = [right, top_s]
        else:                                # keep full-width top rect
            cand = [top, right_s]
        for (x, y, ww, hh) in cand:
            if ww > 0.5 and hh > 0.5: sh["free"].append((x, y, ww, hh))
        return True
    for p in items:
        for sh in sheets:
            if try_place(sh, p): break
        else:
            sh = {"free": [(0.0, 0.0, sheet_l, sheet_w)], "parts": []}
            if not try_place(sh, p): raise ValueError(f"part {p} does not fit a {sheet_l}x{sheet_w} sheet")
            sheets.append(sh)
    return [s["parts"] for s in sheets]

def draw_sheets(sheets, title, path, sheet_l=96.0, sheet_w=48.0, per_row=2, note=""):
    k = 4.2; pad = 40; gap = 60
    cols = min(per_row, len(sheets)); rows = (len(sheets) + per_row - 1) // per_row
    W = pad * 2 + cols * (sheet_l * k + gap); H = 90 + rows * (sheet_w * k + gap)
    s = SVG(W, H, "#fafafa")
    s.text(20, 30, title, 16, weight="bold"); s.text(20, 50, note or f"{len(sheets)} sheet(s) of {sheet_l:g} x {sheet_w:g} in.  Kerf {KERF} in allowed between parts.  Grey = offcut.", 11, "#555")
    for i, parts in enumerate(sheets):
        ox = pad + (i % per_row) * (sheet_l * k + gap); oy = 80 + (i // per_row) * (sheet_w * k + gap)
        s.rect(ox, oy, sheet_l * k, sheet_w * k, "#e5e7eb", "#111", 1.5)
        for (p, x, y, l, w) in parts:
            s.rect(ox + x * k, oy + y * k, l * k, w * k, "#dbeafe" if p.material == "ply" else "#fde68a", "#1e3a8a", 0.8)
            cx, cy = ox + (x + l / 2) * k, oy + (y + w / 2) * k
            fs = 10 if l * k > 80 else 8
            s.text(cx, cy - 2, p.name, fs, "#111", "middle")
            s.text(cx, cy + 10, f"{l:g} x {w:g}", fs - 1, "#333", "middle")
        s.text(ox, oy + sheet_w * k + 16, f"Sheet {i + 1}", 12, "#111", weight="bold")
        used = sum(l * w for (_, _, _, l, w) in parts) / (sheet_l * sheet_w)
        s.text(ox + 70, oy + sheet_w * k + 16, f"{used * 100:.0f}% used", 11, "#555")
    s.save(path); return len(sheets)

# ---------------------------------------------------------------- boards
def nest_boards(parts, stock_len=96.0, kerf=KERF):
    """First-fit decreasing along length. Parts are assumed to be ripped to
    width from the same stock width; returns list of boards (lists of parts)."""
    items = sorted([p for p in parts for _ in range(p.qty)], key=lambda p: -p.length)
    boards = []
    for p in items:
        for b in boards:
            if b["rem"] >= p.length:
                b["parts"].append(p); b["rem"] -= p.length + kerf; break
        else:
            boards.append({"rem": stock_len - p.length - kerf, "parts": [p]})
    return [b["parts"] for b in boards]

def draw_boards(boards, title, path, stock_len=96.0, stock_w=None, note=""):
    k = 4.2; pad = 40; rowh = 44
    W = pad * 2 + stock_len * k + 120; H = 90 + len(boards) * rowh
    s = SVG(W, H, "#fafafa")
    s.text(20, 30, title, 16, weight="bold"); s.text(20, 50, note or f"{len(boards)} board(s) at {stock_len:g} in.  Cross-cut in the order shown; kerf allowed.", 11, "#555")
    for i, parts in enumerate(boards):
        oy = 80 + i * rowh; x = 0.0
        s.rect(pad, oy, stock_len * k, 28, "#e5e7eb", "#111", 1.2)
        for p in parts:
            s.rect(pad + x * k, oy, p.length * k, 28, "#fde68a", "#92400e", 0.8)
            s.text(pad + (x + p.length / 2) * k, oy + 12, p.name, 9, "#111", "middle")
            s.text(pad + (x + p.length / 2) * k, oy + 23, f"{p.length:g}\"", 8, "#333", "middle")
            x += p.length + KERF
        s.text(pad + stock_len * k + 8, oy + 18, f"#{i + 1}  ({stock_len - x:.1f}\" left)", 10, "#555")
    s.save(path); return len(boards)

if __name__ == "__main__":   # smoke test
    ps = [Part("side", 30, 27.25, 4), Part("top/bot", 40, 27.25, 4), Part("back", 40, 30, 2, grain="A"), Part("shelf", 39.25, 26, 3), Part("drawer front", 41, 7, 3, grain="A")]
    sh = nest_sheets(ps); out = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tmp_smoke_sheets.svg")
    print("sheets:", draw_sheets(sh, "smoke", out))
    bs = nest_boards([Part("stretcher", 40, 3, 6), Part("leg", 30, 3, 8), Part("rail", 22, 3, 6)])
    print("boards:", draw_boards(bs, "smoke", out.replace("sheets", "boards")))
