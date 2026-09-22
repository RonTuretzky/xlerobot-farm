# Blender field-guide visuals

Run `Blender --background --factory-startup --python blender/render_handbook.py` from any directory. The script resolves paths from its own location, imports the bundled original STLs, and produces 17 PNGs plus `handbook/downloads/farm-visual-atlas.blend` with 17 named scenes. It does not touch an open Blender session or send printer commands.

Planter and light-paddle meshes are actual imported STL geometry. Electronics, cables, grippers, bottle outlets, plant growth and packing are illustrative. The relay cutaway describes the contact principle, not the exact module internals. These scenes must not be used as manufactured parts, tested robot poses or final wiring pinouts. Use source STLs and the inspected Creality project for printing.

The original complete assembly and exploded square-kit render remain in the guide. The table in that older assembly is explicitly a layout proxy pending the correct editable table files.

Planter mesh adaptations and derived renders: CC BY-SA 4.0; original creators and source links are in `handbook/downloads/MODEL-CREDITS.md`.

The test-first alternative groups the square insert and all six cress components on one bed; it defers the printed cover. The original plate arrangement remains as a historical identification view.

## Software-roadmap scenes

Run `Blender --background --factory-startup --python blender/render_roadmap.py` after the atlas exists. This creates six roadmap illustrations and `handbook/downloads/software-roadmap-scenes.blend` with six named editable scenes. The laptop screens are interface concepts, not an implemented robot-control UI. The roadmap is authored in `handbook/roadmap.py`; its HTML navigation uses `roadmap.js` and `roadmap.css`.
