"""Assemble index.html: one page that presents the whole plan set (docs + drawings)."""
import os, re, html, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(__file__), "..")

def md_to_html(md):
    out, in_table, in_list, in_code = [], False, None, False
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2).replace("../", "")}">{m.group(1)}</a>', t)
        return t
    for line in md.split("\n"):
        if line.startswith("```"):
            in_code = not in_code; out.append("<pre>" if in_code else "</pre>"); continue
        if in_code: out.append(html.escape(line)); continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells): continue
            if not in_table: out.append("<table>"); in_table = True; out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>"); continue
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>"); continue
        elif in_table: out.append("</table>"); in_table = False
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            if in_list: out.append(f"</{in_list}>"); in_list = None
            lvl = len(m.group(1)) + 1; out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); continue
        m = re.match(r"^\s*(\d+)\.\s+(.*)", line); b = re.match(r"^\s*[-*]\s+(.*)", line)
        if m or b:
            kind = "ol" if m else "ul"
            if in_list != kind:
                if in_list: out.append(f"</{in_list}>")
                out.append(f"<{kind}>"); in_list = kind
            out.append(f"<li>{inline((m or b).group(2 if m else 1))}</li>"); continue
        if in_list and line.strip() == "": out.append(f"</{in_list}>"); in_list = None; continue
        if line.strip() == "---": out.append("<hr>"); continue
        if line.strip(): out.append(f"<p>{inline(line)}</p>")
    if in_table: out.append("</table>")
    if in_list: out.append(f"</{in_list}>")
    return "\n".join(out)

DOCS = [("decisions", "Design decisions", "docs/01-design-decisions.md"), ("materials", "Materials & hardware", "docs/02-materials-and-hardware.md"),
        ("cutlist", "Cut list", "docs/03-cut-list.md"), ("guide", "Build guide", "docs/04-build-guide.md"), ("dust", "Dust collection", "docs/05-dust-collection.md"),
        ("electrical", "Electrical", "docs/06-electrical.md"), ("stations", "Using the stations", "docs/07-stations.md")]
DRAWINGS = [("Final look", ["10-final-look-sw.svg", "11-final-look-in-use.svg", "12-final-look-ne.svg"]),
            ("Dimensioned sheets", ["20-plan.svg", "21-elevation-S.svg", "22-elevation-E.svg", "23-elevation-W.svg", "24-elevation-N.svg", "30-section-A-router.svg", "31-section-B-lift.svg", "32-section-C-ducts.svg", "40-router-station.svg", "41-miter-hatch.svg", "50-dust-routing.svg", "51-electrical.svg"]),
            ("Cut diagrams", ["cuts/BB34-sheets-1.svg", "cuts/BB34-sheets-2.svg", "cuts/BB12-sheets-1.svg", "cuts/BB14-sheets-1.svg", "cuts/MDF34-sheets-1.svg", "cuts/MAPLE-boards.svg"]),
            ("Build steps", [f"6{i:02d}-step-{i:02d}.svg" for i in range(1, 14)])]

CSS = """
/* layout: a drawing-set binder: maple title bar, sticky sheet index, one column of sheets and text */
:root{--bg:#f4f2ec;--ink:#22252a;--muted:#5f6670;--line:#d6d2c8;--acc:#b45309;--card:#fbfaf7;--maple:#dcb87a;--fig:#fdfcf9;
  --display:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--body:"Source Sans 3","Segoe UI",Helvetica,Arial,sans-serif;--mono:"IBM Plex Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#17191c;--ink:#e6e3dc;--muted:#a3a8b0;--line:#2f3338;--acc:#f59e0b;--card:#1e2125;--maple:#a8843f;--fig:#24272b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17191c;--ink:#e6e3dc;--muted:#a3a8b0;--line:#2f3338;--acc:#f59e0b;--card:#1e2125;--maple:#a8843f;--fig:#24272b;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 var(--body)}
header{padding-block:28px 14px;padding-inline:16px;border-bottom:6px solid var(--maple);background:var(--card)}header h1{margin:0 0 4px;font:600 34px/1.1 var(--display);letter-spacing:.01em;text-wrap:balance}header p{margin:0;color:var(--muted);max-width:70ch}
nav{position:sticky;top:env(safe-area-inset-top,0px);background:var(--card);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;gap:6px;flex-wrap:wrap;z-index:2}
h2,h3,h4{font-family:var(--display);text-wrap:balance}h2{font-size:28px;font-weight:600}h3{font-size:21px;font-weight:600;margin:22px 0 6px}h4{font-size:17px;margin:16px 0 4px}
td,th{font-variant-numeric:tabular-nums}code{font-family:var(--mono);font-size:.85em}p{max-width:75ch}li{max-width:75ch}
nav a{color:var(--ink);text-decoration:none;padding:6px 10px;border-radius:6px;border:1px solid var(--line);font-size:14px}nav a:hover{border-color:var(--acc)}
main{max-width:1180px;margin:0 auto;padding:16px}section{margin:24px 0 40px}h2{border-bottom:1px solid var(--line);padding-bottom:6px}
table{border-collapse:collapse;width:100%;font-size:14px;margin:12px 0;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:rgba(180,83,9,.08)}
code{background:rgba(127,127,127,.15);padding:1px 4px;border-radius:4px;font-size:.9em}pre{background:rgba(127,127,127,.12);padding:12px;overflow-x:auto}
.fig{background:var(--fig);border:1px solid var(--line);border-radius:6px;padding:8px;margin:14px 0;min-width:0}figure{margin:0}.fig img{width:100%;height:auto;display:block}.fig figcaption{font-size:13px;color:var(--muted);padding:6px 4px 0}
.grid{display:grid;grid-template-columns:1fr;gap:12px}@media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
.hero{display:grid;gap:12px}main{min-width:0}section{min-width:0}.note{background:rgba(180,83,9,.08);border-left:4px solid var(--acc);padding:10px 14px;border-radius:6px}
a{color:var(--acc)}footer{color:var(--muted);font-size:13px;padding:24px 16px;text-align:center}
"""

FONTS = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono&display=swap'>"

def main(out="index.html", standalone=True):
    head = f"<title>Workbench Plans</title>{FONTS}<style>{CSS}</style>"
    parts = [(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>{head}</head><body>" if standalone else head)]
    parts.append("<header><h1>Workbench Plans</h1><p>A 69&quot; x 96&quot; island at SawStop height: outfeed, router lift, rising miter saw, downdraft clamping station, laser well, built-in ducting and power.</p></header>")
    parts.append("<nav>" + "".join(f"<a href='#{k}'>{t}</a>" for k, t, _ in [("look", "Final look", "")] + DOCS + [("drawings", "Drawings", ""), ("cuts", "Cut diagrams", ""), ("steps", "Step views", "")]) + "</nav><main>")
    parts.append("<section id='look'><h2>Final look</h2><div class='hero'>")
    for f in DRAWINGS[0][1]: parts.append(f"<figure class='fig'><img src='renders/{f}' alt='{f}'><figcaption>{f}</figcaption></figure>")
    parts.append("</div><p class='note'>These are dimensionally accurate line renders generated from the same model as the cut list. Materials are indicated by colour: maple-edged birch top, charcoal fronts, purple = miter station, orange = 4&quot; duct, amber = 2-1/2&quot; vac line, yellow = electrical.</p></section>")
    for key, title, path in DOCS:
        md = open(os.path.join(ROOT, path)).read()
        parts.append(f"<section id='{key}'><h2>{title}</h2>{md_to_html(md)}</section>")
    for key, (title, files) in zip(("drawings", "cuts", "steps"), DRAWINGS[1:]):
        parts.append(f"<section id='{key}'><h2>{title}</h2><div class='grid'>")
        for f in files: parts.append(f"<figure class='fig'><a href='renders/{f}'><img src='renders/{f}' alt='{f}' loading='lazy'></a><figcaption>{f}</figcaption></figure>")
        parts.append("</div></section>")
    parts.append("</main><footer>Generated from tools/model.py. Every dimension on a drawing is the same number in the cut list.</footer>" + ("</body></html>" if standalone else ""))
    open(out if os.path.isabs(out) else os.path.join(ROOT, out), "w").write("\n".join(parts))
    print(out, "written")

if __name__ == "__main__":
    main()
