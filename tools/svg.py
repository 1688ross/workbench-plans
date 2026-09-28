"""Tiny SVG builder + isometric projection helpers (no dependencies)."""
import math

FONT = "font-family='Inter, Helvetica, Arial, sans-serif'"

class SVG:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h = w, h
        self.parts = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}>",
                      f"<rect width='{w}' height='{h}' fill='{bg}'/>"]
    def add(self, s): self.parts.append(s)
    def rect(self, x, y, w, h, fill="none", stroke="#222", sw=1, rx=0, extra=""):
        self.add(f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' {extra}/>")
    def poly(self, pts, fill="none", stroke="#222", sw=1, extra=""):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f"<polygon points='{p}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' stroke-linejoin='round' {extra}/>")
    def line(self, x1, y1, x2, y2, stroke="#222", sw=1, extra=""):
        self.add(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{stroke}' stroke-width='{sw}' {extra}/>")
    def circle(self, cx, cy, r, fill="none", stroke="#222", sw=1, extra=""):
        self.add(f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.2f}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' {extra}/>")
    def ellipse(self, cx, cy, rx, ry, fill="none", stroke="#222", sw=1, extra=""):
        self.add(f"<ellipse cx='{cx:.1f}' cy='{cy:.1f}' rx='{rx:.2f}' ry='{ry:.2f}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' {extra}/>")
    def text(self, x, y, s, size=12, fill="#222", anchor="start", weight="normal", extra=""):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
        self.add(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' fill='{fill}' text-anchor='{anchor}' font-weight='{weight}' {extra}>{s}</text>")
    def label(self, x, y, s, size=11, fill="#111", anchor="middle", bg="#ffffffcc"):
        w = len(s) * size * 0.58 + 8
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        self.rect(x0, y - size, w, size + 6, fill=bg, stroke="none", rx=3)
        self.text(x, y, s, size, fill, anchor)
    def dim_h(self, x1, x2, y, txt, size=10, color="#555"):
        self.line(x1, y, x2, y, color, 0.8); self.line(x1, y - 4, x1, y + 4, color, 0.8); self.line(x2, y - 4, x2, y + 4, color, 0.8)
        self.label((x1 + x2) / 2, y - 3, txt, size, color)
    def dim_v(self, x, y1, y2, txt, size=10, color="#555"):
        self.line(x, y1, x, y2, color, 0.8); self.line(x - 4, y1, x + 4, y1, color, 0.8); self.line(x - 4, y2, x + 4, y2, color, 0.8)
        self.add(f"<text x='{x - 4:.1f}' y='{(y1 + y2) / 2:.1f}' font-size='{size}' fill='{color}' text-anchor='middle' transform='rotate(-90 {x - 4:.1f} {(y1 + y2) / 2:.1f})'>{txt}</text>")
    def save(self, path):
        self.parts.append("</svg>")
        with open(path, "w") as f: f.write("\n".join(self.parts))

# ---- Isometric projection (viewer at the south-west, looking down 30 deg) ---
COS30, SIN30 = math.cos(math.radians(30)), 0.5

class Iso:
    def __init__(self, svg, scale, ox, oy):
        self.s, self.k, self.ox, self.oy = svg, scale, ox, oy
    def p(self, x, y, z):
        X = (x - y) * COS30 * self.k + self.ox
        Y = -((x + y) * SIN30 + z) * self.k + self.oy
        return (X, Y)
    def face(self, pts3, fill, stroke="#333", sw=0.8):
        self.s.poly([self.p(*q) for q in pts3], fill, stroke, sw)
    def box(self, x0, x1, y0, y1, z0, z1, top, south, west, stroke="#333", sw=0.8, faces="tsw"):
        if "t" in faces: self.face([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke, sw)
        if "s" in faces: self.face([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], south, stroke, sw)
        if "w" in faces: self.face([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], west, stroke, sw)
    def line(self, a, b, stroke="#333", sw=0.8, extra=""):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b); self.s.line(x1, y1, x2, y2, stroke, sw, extra)
    def rect_top(self, x0, x1, y0, y1, z, fill="none", stroke="#333", sw=0.8):
        self.face([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], fill, stroke, sw)
    def dot_top(self, x, y, z, r, fill="#333"):
        cx, cy = self.p(x, y, z)
        self.s.ellipse(cx, cy, r * self.k * 1.0, r * self.k * 0.58, fill, "none")
    def text_at(self, x, y, z, s, size=11, fill="#111", anchor="middle"):
        X, Y = self.p(x, y, z); self.s.label(X, Y, s, size, fill, anchor)
