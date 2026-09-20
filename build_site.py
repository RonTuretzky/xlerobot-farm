#!/usr/bin/env python3
"""Build a standalone GitHub Pages site into dist/ using Python 3."""
from pathlib import Path
import runpy
import shutil
HERE = Path(__file__).resolve().parent
runpy.run_path(str(HERE / "build_xlerobot_deck.py"), run_name="__main__")
out = HERE / "dist"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ("xlerobot-deck.html", "sensor-shopping.html", "sensor-bom.json", ".nojekyll"):
    shutil.copy2(HERE / name, out / name)
shutil.copy2(HERE / "xlerobot-deck.html", out / "index.html")
shutil.copytree(HERE / "assets", out / "assets")
print(f"Built {out}")
