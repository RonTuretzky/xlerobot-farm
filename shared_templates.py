"""Shared deck styling, navigation and gallery markup."""
from pathlib import Path
from html import escape
import re
HERE = Path(__file__).parent
style = (HERE / "base-style.inc.html").read_text()
extra = (HERE / "deck-figures.css.html").read_text()
script = (HERE / "navigation.inc.html").read_text()
def gal(items, cols, aspect="4/3"):
    figs = ""
    for filename, caption in items:
        alt = escape(re.sub(r"<[^>]+>", "", caption), quote=True)
        cls = "pix" if filename.endswith("apriltag.png") else ""
        figs += f'<figure><img src="assets/{filename}" class="{cls}" style="aspect-ratio:{aspect}" alt="{alt}"><figcaption>{caption}</figcaption></figure>'
    return f'<div class="gallery" style="grid-template-columns:repeat({cols},1fr)">{figs}</div>'
CREDIT = '<p class="credit">Images: TheRobotStudio, SIGRobotics-UIUC, Vector-Wangel and AprilRobotics. <a href="assets/CREDITS.md">Sources and licenses</a>.</p>'
