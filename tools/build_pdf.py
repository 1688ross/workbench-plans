"""Build workbench-plans.pdf: the whole plan set, landscape US Letter, drawings one per page.

Needs Playwright (python) and a Chromium executable. Run:
    python3 tools/build_pdf.py [--chromium /path/to/chrome]
"""
import os, sys, datetime, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from build_site import md_to_html, DOCS, DRAWINGS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CSS = """
@page { size: Letter landscape; margin: 0.55in 0.6in 0.6in 0.6in; }
:root{--ink:#22252a;--muted:#5f6670;--line:#cfcbc2;--acc:#b45309;--maple:#dcb87a}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);font:10.5pt/1.45 "Source Sans 3","Segoe UI",Helvetica,Arial,sans-serif;background:#fff}
h1,h2,h3,h4{font-family:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;font-weight:600;line-height:1.15}
h1{font-size:30pt;margin:0 0 6pt}h2{font-size:20pt;margin:0 0 10pt;padding-bottom:5pt;border-bottom:2.5pt solid var(--maple)}
h3{font-size:14pt;margin:14pt 0 4pt}h4{font-size:11.5pt;margin:10pt 0 3pt}
p,li{max-width:none}p{margin:0 0 6pt}ul,ol{margin:0 0 6pt 18pt;padding:0}li{margin:0 0 2pt}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:6pt 0 10pt;break-inside:auto}tr{break-inside:avoid}
th,td{border:0.6pt solid var(--line);padding:3pt 5pt;text-align:left;vertical-align:top}th{background:#f3eadb}
code{font-family:"IBM Plex Mono",Menlo,Consolas,monospace;font-size:8.5pt;background:#f1efe9;padding:0 2pt;border-radius:2pt}
pre{font-family:"IBM Plex Mono",Menlo,Consolas,monospace;font-size:8.5pt;background:#f1efe9;padding:6pt;border-radius:3pt}
hr{border:0;border-top:0.6pt solid var(--line);margin:10pt 0}
.cover{height:7.3in;display:flex;flex-direction:column;justify-content:flex-end;border-bottom:8pt solid var(--maple);padding-bottom:18pt;break-after:page}
.cover .kicker{font:600 11pt "Barlow Semi Condensed",Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--acc)}
.cover p{font-size:13pt;color:var(--muted);max-width:60ch}.cover .meta{font-size:10pt;color:var(--muted);margin-top:12pt}
.toc{break-after:page}.toc ol{columns:2;column-gap:30pt;font-size:11pt}.toc li{margin:0 0 4pt}
.two{columns:2;column-gap:28pt}.two h3{break-after:avoid}.two table{break-inside:avoid-page}
section.doc{break-before:page}
figure.sheet{break-before:page;margin:0;display:flex;flex-direction:column;height:7.25in}
figure.sheet img{display:block;max-width:100%;max-height:6.75in;width:auto;height:auto;margin:0 auto;border:0.5pt solid var(--line)}
figure.sheet figcaption{font-size:9pt;color:var(--muted);margin-top:4pt;text-align:center}
.secthead{break-before:page;height:7.25in;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.secthead h2{border:0;font-size:34pt}.secthead p{font-size:13pt;color:var(--muted);max-width:60ch}
.hero-pair{display:grid;grid-template-columns:1fr;gap:8pt}
.note{border-left:3pt solid var(--acc);background:#faf4ea;padding:6pt 10pt;margin:6pt 0}
"""

def html():
    today = datetime.date.today().strftime("%B %d, %Y")
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Workbench Plans</title>"
             "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono&display=swap'>"
             f"<style>{CSS}</style></head><body>"]
    parts.append(f"<div class='cover'><div class='kicker'>Plan set</div><h1>Workbench Plans</h1>"
                 "<p>A 69&quot; x 96&quot; island at SawStop height: outfeed, router lift station, flip-top miter saw, downdraft clamping station, laser well, built-in ducting and power.</p>"
                 f"<div class='meta'>Owner: 1688ross &middot; Generated {today} from tools/model.py &middot; All dimensions in inches &middot; github.com/1688ross/workbench-plans</div></div>")
    toc = ["Final look (3 views)"] + [t for _, t, _ in DOCS] + ["Dimensioned sheets 1 to 12", "Cut diagrams", "Build step views 1 to 13"]
    parts.append("<div class='toc'><h2>Contents</h2><ol>" + "".join(f"<li>{t}</li>" for t in toc) + "</ol>"
                 "<div class='note'>Measure before you cut: the seven items on the VERIFY list in Design decisions. Every number in this set comes from one model file, so a changed measurement regenerates every drawing and the cut list together.</div></div>")
    for f in DRAWINGS[0][1]:
        parts.append(f"<figure class='sheet'><img src='renders/{f}'><figcaption>{f}</figcaption></figure>")
    for key, title, path in DOCS:
        md = open(os.path.join(ROOT, path)).read()
        body = md_to_html(md)
        wide = key in ("cutlist",)   # tables: single column
        parts.append(f"<section class='doc'><h2>{title}</h2><div class='{'' if wide else 'two'}'>{body}</div></section>")
    for (title, files), blurb in zip(DRAWINGS[1:], ("Plan, four elevations, three sections, station details, dust and electrical routing. Sheet numbers match the build guide.",
                                                     "Nested 4x8 layouts with 1/8\" kerf. Part IDs match the cut list. Grey is offcut.",
                                                     "One isometric view per build step; the step's new parts are in colour, earlier work is grey.")):
        parts.append(f"<div class='secthead'><h2>{title}</h2><p>{blurb}</p></div>")
        for f in files:
            parts.append(f"<figure class='sheet'><img src='renders/{f}'><figcaption>{f}</figcaption></figure>")
    parts.append("</body></html>")
    out = os.path.join(ROOT, "print.html")
    open(out, "w").write("\n".join(parts)); return out

async def render(chromium, out_pdf):
    from playwright.async_api import async_playwright
    page_html = html()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=chromium) if chromium else await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + page_html, wait_until="networkidle")
        await pg.emulate_media(media="print")
        await pg.pdf(path=out_pdf, format="Letter", landscape=True, print_background=True, prefer_css_page_size=True,
                     display_header_footer=True, header_template="<span></span>",
                     footer_template="<div style='width:100%;font-size:7.5pt;color:#888;padding:0 0.6in;display:flex;justify-content:space-between;font-family:Arial'><span>Workbench Plans</span><span class='pageNumber'></span></div>")
        await b.close()
    os.remove(page_html)

if __name__ == "__main__":
    chromium = None
    if "--chromium" in sys.argv: chromium = sys.argv[sys.argv.index("--chromium") + 1]
    out = os.path.join(ROOT, "workbench-plans.pdf")
    asyncio.run(render(chromium, out))
    print("wrote", out, round(os.path.getsize(out) / 1e6, 1), "MB")
