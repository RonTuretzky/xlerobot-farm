# XLeRobot autonomous farm

A 28-slide roadmap for a small autonomous farm, with an itemized sensor shopping checklist and Amazon links.

- [Open the deck](https://ronturetzky.github.io/xlerobot-farm/)
- [Open the sensor checklist](https://ronturetzky.github.io/xlerobot-farm/sensor-shopping.html)

The roadmap uses September 19–29 for software preparation and starts physical work September 30. It assumes a likely Bambu A1, and uses labels, symbols and patterns alongside color.

## Build and preview

Python 3 is the only build dependency:

```sh
python3 build_site.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. Use arrow keys to navigate. Slide 7 links to the full measurement-parts checklist.

Edit `build_xlerobot_deck.py` for slides, `sensor-bom.json` for parts/prices/links, and `build_sensor_shopping.py` for the checklist. Shared layout and interactions are in the HTML includes and `shared_templates.py`.

## Publishing

`main` contains source; `gh-pages` contains only built files. GitHub Pages publishes from the root of `gh-pages` in branch mode. To update an existing clone:

```sh
python3 build_site.py
git fetch origin gh-pages
git worktree add ../xlerobot-farm-pages gh-pages
rsync -a --delete --exclude=.git dist/ ../xlerobot-farm-pages/
git -C ../xlerobot-farm-pages add -A
git -C ../xlerobot-farm-pages commit -m "Update farm site"
git -C ../xlerobot-farm-pages push origin gh-pages
git worktree remove ../xlerobot-farm-pages
```

Commit source changes on `main` as well. Commit signing follows your Git configuration.

## Data and comments

Prices are a September 20, 2026 research snapshot in USD, before tax/shipping; check listings before ordering. The checklist distinguishes core and optional hardware. No purchases are performed by this site.

Slide comments are saved only in the current browser's local storage. They are not shared or uploaded. Use the copy/export controls to share feedback; comments on a localhost copy do not automatically transfer to the public site.

Image attribution is in [assets/CREDITS.md](assets/CREDITS.md). This repository contains the deck and its checklist; private attachments and unrelated research are excluded.
