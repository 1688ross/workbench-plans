"""Regenerate everything: drawings, cut diagrams, cut-list doc, site page."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import render_plans, render_iso, build_docs, build_site
render_plans.all(); render_iso.hero_views(); render_iso.step_views(); build_docs.main(); build_site.main()
