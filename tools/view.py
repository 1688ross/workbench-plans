"""2D orthographic view helper on top of svg.py: model inches -> pixels."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from svg import SVG

class View:
    """u = horizontal model axis (right), v = vertical model axis (up)."""
    def __init__(self, svg, scale, ox, oy):
        self.s, self.k, self.ox, self.oy = svg, scale, ox, oy
    def X(self, u): return self.ox + u * self.k
    def Y(self, v): return self.oy - v * self.k
    def rect(self, u0, u1, v0, v1, **kw):
        self.s.rect(self.X(min(u0, u1)), self.Y(max(v0, v1)), abs(u1 - u0) * self.k, abs(v1 - v0) * self.k, **kw)
    def line(self, u0, v0, u1, v1, **kw): self.s.line(self.X(u0), self.Y(v0), self.X(u1), self.Y(v1), **kw)
    def circle(self, u, v, r, **kw): self.s.circle(self.X(u), self.Y(v), r * self.k, **kw)
    def text(self, u, v, t, **kw): self.s.text(self.X(u), self.Y(v), t, **kw)
    def label(self, u, v, t, **kw): self.s.label(self.X(u), self.Y(v), t, **kw)
    def poly(self, pts, **kw): self.s.poly([(self.X(u), self.Y(v)) for u, v in pts], **kw)
    def dim_h(self, u0, u1, v, txt, **kw): self.s.dim_h(self.X(u0), self.X(u1), self.Y(v), txt, **kw)
    def dim_v(self, u, v0, v1, txt, **kw): self.s.dim_v(self.X(u), self.Y(v1), self.Y(v0), txt, **kw)
    def hatch(self, u0, u1, v0, v1, step=0.6, color="#999"):
        """diagonal section hatching inside a rect"""
        x0, x1 = self.X(min(u0, u1)), self.X(max(u0, u1)); y0, y1 = self.Y(max(v0, v1)), self.Y(min(v0, v1))
        w, h = x1 - x0, y1 - y0; st = step * self.k; d = 0
        self.s.add(f"<clipPath id='c{abs(hash((x0,y0,x1,y1)))}'><rect x='{x0:.1f}' y='{y0:.1f}' width='{w:.1f}' height='{h:.1f}'/></clipPath>")
        self.s.add(f"<g clip-path='url(#c{abs(hash((x0,y0,x1,y1)))})' stroke='{color}' stroke-width='0.6'>")
        while d < w + h:
            self.s.add(f"<line x1='{x0 + d:.1f}' y1='{y0:.1f}' x2='{x0 + d - h:.1f}' y2='{y1:.1f}'/>"); d += st
        self.s.add("</g>")
    def dashed(self, u0, u1, v0, v1, color="#666", sw=0.8):
        self.rect(u0, u1, v0, v1, fill="none", stroke=color, sw=sw, extra="stroke-dasharray='5 3'")

def sheet(title, sub, W, H):
    s = SVG(W, H, "#fbfbfa")
    s.text(20, 30, title, 16, weight="bold"); s.text(20, 50, sub, 11, "#555")
    s.text(W - 20, H - 12, "workbench-plans  |  generated from tools/model.py  |  inches", 9, "#999", "end")
    return s
