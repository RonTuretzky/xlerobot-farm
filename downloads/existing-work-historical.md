# Historical research — September 18, 2026

Background references, not the current BOM or implementation status. See the [current handbook](../index.html).

# Existing work, adjacent projects, and lessons learned

Companion to `v0-hardware-spec.md` and `v0-findings-deck.html`. Survey date: 2026-09-18.
Three parallel literature/forum sweeps (open farm robots · low-cost manipulators/mobile/USV ·
adjacent fields and failures), ~225 primary fetches. Prices USD, current unless noted.
**Budget focus: what you can actually build for $500–1,000.**

---

## 0. Executive summary — what this changes

1. **Nobody has shipped a sub-$1k robot that reliably manipulates growing plants.** The closest
   working things are (a) a $1,276 HardwareX gantry that *weighs* pots on a rail, (b) FarmBot
   ($6k, and its cheap Express line is on hold), (c) the LeRobot SO-101 ecosystem ($100–500
   arms, no force sensing). Our arm-on-rail V0 is not exotic — but the field says the arm is the
   *least* important part.
2. **The interface wins, not the robot.** Every survivor (FarmBot's magnetic tool mount, Jubilee's
   kinematic couplings, Opentrons' per-run fiducial check, 95%+ transplanters that grip a rigid
   plug) succeeds by making the target self-locating so a low-precision actuator only needs ±3–5 mm.
   Our cone-base pod + lip + AprilTag is the right instinct; upgrade it to a 3-point kinematic seat.
3. **Water chemistry and water delivery are the unattended-operation killers**, not software:
   pH probes drift in weeks when left immersed, tubing fails in 3–6 months, mineral scale is
   Gardyn's "#1 killer", Bowery died of one pathogen in a shared reservoir, NASA Veggie failed
   grow-outs on watering alone. **Passive Kratky pods with isolated reservoirs and a robot that
   dips-rinses-restores one probe** is exactly the counter-design — this is our real advantage.
4. **Skip imitation learning for V0.** Field data: 100–340 teleop demos yield 60–90% on
   in-distribution pick-and-place, ~0% generalisation, no recovery on insertion. A scripted,
   fiducial-referenced routine will beat that. Buy one arm, not a leader/follower pair (saves ~$150).
5. **STS3215 servos overheat with no firmware cutoff** (71 °C at 110 min, misbehaviour, no
   shutdown). Copy Nori Bot's 59/60 °C two-tier cutoff + stall detection from day one; duty-cycle
   the arm (dips take seconds).
6. **"Move the module to the tool" beats "move a robot to the module"** at this budget: MACARONS
   ($145/unit tray rail), AutoStore-style grids, Fifth Season's regret ("bots we didn't need yet"),
   Iron Ox's mobile-robot+arm farm closing. Option B stays, but a **tray/tile rail** is the cheaper
   Stage-3 step and should precede the cart.
7. **The boat + arm cannot be done for $1k.** A DIY ArduRover catamaran alone is $800–1,000, has
   no docking mode, and even the $4.4k BlueBoat suffers 50–200 m WiFi and runaway RTLs. Realistic
   Option C at this budget: a **fixed arm on the raft**, boat only as transporter.
8. **Communities survive on a JLCPCB-orderable board + forum + vendors allowed to profit**
   (AgOpenGPS, OWL, Mycodo). Acorn, hydromisc, OpenAg and Open Source Ecology's ag tools died
   without that loop. Publish the tile controller as an orderable PCB.

---

## 1. Landscape

### 1a. Open / low-cost farm and garden robots

| Project | Price | Open? | Status | What it teaches |
|---|---|---|---|---|
| **FarmBot Genesis / XL** | $5,995 / $7,995; Express **on hold** | HW CC-BY-NC-SA, SW MIT (active) | Active since 2016 | Bed levelness *is* the product; belts creep after ~20 cm and drift ~5 mm with temperature; no reliable tool pickup without endstops/encoders; wobble grows super-linearly with size; colour-threshold weed vision breaks in shadow; owners: "you have to enjoy tinkering" |
| **MIT OpenAg PFC** | ~$3k BOM | open, archived | **Defunct 2020** (scandal) | Never grew anything consistently; staged demos; over-engineered. The community **$300 MVP** (PVC box, Pi, cron scripts) "works reliably" — ship the boring thing first |
| **Acorn** (Twisted Fields) | never sold | Apache-2.0 | Dormant (last push 2024-07, forum dead) | Elegant solar/supercap rover with no users → gone in 3 yrs |
| **WEEDINATOR** | DIY | open | Active 2017–26 | Took 9 years; succeeded only after *buying* a hydrostatic tractor and building just the end-effector + vision |
| **OpenWeedLocator (OWL)** | ~$250–450/unit | MIT, peer-reviewed | Very active | One tight task, excess-green heuristic before ML, printable enclosure, forum. Fails green-on-green / variable light — our LED bed removes that |
| **AgOpenGPS** | £600–700 DIY vs $5–10k commercial | Apache-2.0, 942★ | Very active | Why it won: 10× cost cut on one high-value job, JLCPCB-orderable reference PCB, Discourse forum, ecosystem vendors profiting |
| **farm-ng Amiga** | $12,990 | open SDK, closed iron | Active | Out of budget; "open API, closed hardware" model |
| **Open Source Ecology** | $2–20k/machine | open | Ag tools dormant since 2023 | 50-machine scope, no per-machine user base, "little documentation of failures" |
| **Iron Ox** | VC-scale | closed | Closed (2022–25) | Mobile robot + arm moving hydroponic modules — our Option B, at $103M — did not survive as a farm |

### 1b. Grow controllers, probes, dosing (the "instrument" stage)

| Item | Price | Status | Lesson |
|---|---|---|---|
| **Mycodo** | free (Pi) | Active v8.17, 3.3k★ | The survivor of 2016-era Pi controllers: one maintainer, plugins, forum. Pi+SD+InfluxDB is a single point of failure for dosing |
| **HAGR** (Home Assistant grow) | ESP32 + Atlas | Active 2026 | Dosing as a **state machine**: pre-fill → refill → sequential dose → mix delay → **post-dose pH/EC verify**; sensor watchdogs; fail-safe closes CO₂ if sensor dies |
| **DFRobot industrial pH/EC/temp** | $65 + $199 + $7.50 ≈ **$272** | current | "Lab-grade probes drift within weeks if left submerged — the most common and expensive DIY mistake"; recal every 30–45 days |
| **Atlas EZO pH / EC kits** | $195–423 / $260–384 | current | ±0.002 pH; holds calibration for months; community calls it "overpriced" for hobby |
| Home Assistant pH/TDS thread | — | — | PTFE-junction probes for immersion; **replace probes yearly at 24/7**; isolate or **stagger pH and EC reads** (EC excitation corrupts pH); run dosing on the ESP so it survives Wi-Fi outages |
| **hydromisc** | ~$90 board | Dormant 2022 | Good PCB, no maintainer → dead. Steal: **pump-current monitoring** as a cheap failure detector |
| **GreenPiThumb** | ~$100 | Blog postmortem | Cheap soil sensors useless ("82% for days"); ended with "water if dry OR 7 days elapsed"; 2–3 month plan took >1 year; test hardware in isolation |
| **OpenSprinkler** | $135–203 | Real product | Narrow scope + open firmware + sold hardware = the one that became a business |
| Peristaltic tubing | — | — | Wear part: replace **every 3–6 months on schedule**; nutrient crystallisation blocks lines |
| **Gardyn / Rise / AeroGarden** | $349–1,499 | consumer | Gardyn: plant-ID 68%, pump failures, **mineral scale #1 killer**. Rise ships **no pH/EC** because "notoriously unreliable". AeroGarden closed then relaunched — proprietary pods = platform risk |

### 1c. Arms, gantries and robots that actually touch plants

| Item | Price | Result | Lesson |
|---|---|---|---|
| **HardwareX pot gantry** (U. Hawaii 2021) | **$1,276** | belt X-axis, actuators lift pots onto 5 kg load cells, gravimetric watering, mass error +0.3/−0.1% | Nearly our geometry. **Weigh the pod for water level** instead of probing; magnets + Hall sensors for row indexing; one bad calibration poisons a column |
| **UPM dual-arm seeder** (IEEE Access 2025) | ABB YuMi (~$50k) | **75 s per rockwool cube** | Cycle time is perception + re-seating, even with a cobot → mechanical registration over vision |
| Hydroponic transplanters (lit.) | research | 67% on loose early plugs → **90–99% on rigid plugs/net cups** | **Give the robot a handle, not a plant** |
| **Duckbot** (Jubilee + OT-2 pipette) | ~$2k | 10-day duckweed assay, 1 min imaging per plate | Tool-changer over a fixed bed is the proven "many end-effectors, one motion system"; water-column height made syringe transfer fragile |
| **MACARONS** tray transport | **$145/grow unit**, ~$1.5k system | moves 12.5 kg trays at 100 mm/s between stations | "Move the tray to the tool" is the cheap expansion primitive |
| Hackaday lettuce seeder | DIY | 150 seeds / 3–4 min | Vacuum seeding works only with pelleted/large seeds and non-porous nozzles |
| V1E forum: **SO-101 on a LowRider XY gantry** (Dec 2025) | DIY | in progress | Exactly our architecture, one hobbyist, no results yet — worth following |

### 1d. Low-cost manipulators (measured, not marketed)

| Arm | Price | Key numbers | Verdict for us |
|---|---|---|---|
| **SO-101** (LeRobot) | $100 parts / $220–278 kit / ~$500 assembled | ~500 mm reach, ~500 g practical, backlash **0.87°** (spec 0.5°), repeatability ±0.3 mm at 10 cm; overload trips ~2 kg and drops to 20%; **71 °C at 110 min with no auto shutdown**; no force sensing | V0 arm. Needs thermal cutoff, duty cycle, compliant TPU on the tool for current-based contact sensing |
| **Koch v1.1** | $250–300 | Dynamixel XL430/330 with current-based position control | Only if you want servo-native gripper force |
| **Thor** | <€350 | 6-DoF steppers, 750 g, stiffer, no thermal issue | Open-loop, no LeRobot; better *rail-mounted* rigidity if you script everything |
| **AR4 MK5** | ~$2k built | 629 mm, 1.9 kg, **0.2 mm repeatability** | The benchmark for what $2k buys; over budget |
| myCobot 280 / Mirobot | $900–1,760 | 250 g / 150 g payload, closed firmware | Too weak, not open |
| **Nori Bot A3** (arXiv 2605.16537) | $1,688 | 19-DoF bimanual, graded Feetech servos, telescoping column; **59/60 °C two-tier cutoff + 15-sample stall detector**; TPU finger makes current a clean force signal | Copy the protection architecture, not the robot |
| Imitation learning (ML6, Correll) | 2× SO-100 + 3 cams | 100 eps → 60%; 340 eps → 90% in-distribution, **0% out**; VLA on peg insertion: no re-centering, no recovery | Script V0; reserve IL for unstructured V1 tasks |

### 1e. Mobile bases and boats

| Platform | Price | Reality |
|---|---|---|
| **LeKiwi** | **$482** incl. arm | Omni wheels slip and can be displaced with zero encoder motion; odometry "too noisy"; fix was a $100 LiDAR + slam_toolbox. Wrong wheels for wet/gravel floors |
| **XLeRobot** | **~$660** (+$79 Pi); Dec-2025 differential base is cheaper and more accurate | 288 Wh → 10–12 h; workspace 0.5–1.25 m high; no lift, no >1 kg, **no autonomous docking/charging**, no field-reliability data |
| Mobile ALOHA / TidyBot++ | $20–32k / <$30k | Cost = arms + industrial casters; leader arms double the arm bill |
| **BlueBoat** | **$4,400** | Open firmware; forum: WiFi 50–200 m real, GPS needs 1–2 min warm-up, runaway RTLs, compass errors, "mission not aligning" unresolved Sept 2025 |
| **DIY ArduRover catamaran** | **$800–1,000** | No docking mode in ArduRover (loiter + external guidance); RTK loiter drift ~45 cm is "expected"; F9P needed (dual, moving-baseline for heading); solar is supplementary, not primary; ESC braking/reverse must be reprogrammed for boats |
| Salmon-pen cleaning robots (Remora, Ultra AQ, SINTEF) | commercial | **Docked, self-charging, continuous** prevention beat free-navigating cleaners; in-water vision fails in turbidity; tethers entangle |
| AprilTag docking (lit.) | — | sub-cm to ±20 mm; Nav2 uses 2 cm threshold, 3 retries, 0.15 m/s; needs LiDAR/depth fusion when tags occlude |

### 1f. Adjacent: replication, autonomous growing, and the graveyard

| Item | Lesson |
|---|---|
| **RepRap** (48% → 73% self-printed by count) | Minimising vitamins made "a less robust machine that was fiddly to calibrate"; printed racks wobble; no agreed fabricated-fraction metric. What people actually copied: cheap snap-fit brackets |
| **Dollo 3D** | Part count and fastener count mattered more than "% printed" |
| **Freitas / NASA 1980** | 90–96% closure attainable; the last few % cost orders of magnitude; hardest vitamins = electronics, bearings, precision instruments. Set ~90% and import the rest deliberately |
| **Wageningen Autonomous Greenhouse Challenge** (4 editions) | Winners used cheap inputs (crop temperature, spacing, screen timing); every team harvested a week late; teams throttled their own AI out of distrust; "not a single grower does this completely autonomously" |
| **NASA Veggie / APH** | Pillows designed passive but "typically watered manually"; grow-outs failed on watering; **biofilm is the chronic maintenance problem** |
| **Growing Beyond Earth** | 10,000 students screened ~200 crops in one standard cheap habitat — standardise the pod, vary the crop |
| **Bowery** ($700M) | One pathogen through a shared recirculating system; labour still 25–33% "despite automation" |
| **AppHarvest, Plenty, Fifth Season, Iron Ox** | What resisted automation: transplanting, harvest, packing, cleaning, pest response — anything tactile. Fifth Season: "we spent too much on bots we didn't need yet" |
| **GreenWave** | Permits and nursery seed are solved in the US; bottleneck is post-harvest |
| **Running Tide** (closed 2024), **Parabel/Lemnature** (bankrupt 2023) | Open-ocean and duckweed biology are easy; processing economics killed both |
| **Microgreens** | 10–14 oz/tray, ~10-day cycle, 30–35 cycles/yr; Microwth hobby farm: 25% flow imbalance from one shared pump, pump noise corrupting the MCU, LEDs at 44 °C |

---

## 2. Ranked lessons for our program

1. **Design the interface, not the robot.** 3-point kinematic seats + chamfers + magnets on pods and tiles; require ≤5 mm arm accuracy, never sub-mm. (FarmBot UTM, Jubilee, OT-2, transplanter data.)
2. **Make pH/EC an intermittent, verified act, not a 24/7 immersion.** Dip → read → rinse → store in KCl → periodic 2-point recal; post-dose verify (HAGR); time-based fallback (GreenPiThumb). This is the one thing the robot does that no $500 consumer device can.
3. **Isolate water per pod; schedule wear parts.** No shared reservoir (Bowery), tubing every 3–6 months, rinse/replace pods instead of scrubbing, weigh pods for level.
4. **Thermal + stall protection on hobby servos from day one**, and duty-cycle the arm. Compliant TPU on the probe holder turns servo current into a "seated" signal.
5. **Script V0; buy one arm, not a teleop pair.** IL needs 100–340 demos for 60–90% in-distribution and generalises to nothing.
6. **Move the module to the tool before adding a mobile robot.** A tray/tile rail (MACARONS) is the Stage-3 step; the cart is Stage 3b.
7. **Fixed cameras under fixed LEDs, colour reference in frame, projected leaf area vs time** — the only cheap phenotype that every group converged on. Skip depth until it pays.
8. **Track closure as three numbers** (count, mass, $) and pin SKUs with substitutes; log every human override and every failure (OSE's biggest critique).
9. **Buy the platform, print only tooling** (WEEDINATOR, AgOpenGPS, OWL); aluminium not wood/PLA for structure; endstops/encoders on every axis.
10. **Publish the tile controller as a JLCPCB-orderable board and let vendors sell it** — that, plus a forum, is what kept AgOpenGPS/OWL/Mycodo alive and killed Acorn/hydromisc/OpenAg.

---

## 3. The $500–1,000 options menu

Prices are current single-unit retail. Each row is a complete, buildable thing.

### 3a. Grow + sense layer (no arm)

| # | Build | What you get | ≈ Cost | Gaps |
|---|---|---|---|---|
| G1 | **MVP rack** — 12 printed Kratky pods, 100 W LED bar, ESP32 + DS18B20 + float switch, Mycodo or Home Assistant | The OpenAg-MVP lesson applied: boring, reproducible, grows radish/duckweed | **$250–400** | No pH/EC; manual dosing |
| G2 | **HAGR-lite** — G1 + DFRobot industrial pH ($65) + EC ($199) + signal isolator, 2 peristaltic pumps, ESPHome state-machine dosing with post-dose verify | Closed-loop chemistry on a bulk reservoir | **$450–650** | Probes immersed → recal every 30–45 d, replace yearly; tubing every 3–6 mo |
| G3 | **Weigh rail** (HardwareX pattern) — 2020 rail + NEMA17 belt axis + endstop, HX711 5 kg load cells under 12 pods, solenoid top-up | Water consumption + biomass per pod per day, gravimetric top-up | **$400–700** | Weight ≠ chemistry; per-column calibration drift |
| G4 | **Pod camera** — Pi Camera 3 / ESP32-CAM under fixed LEDs, excess-green canopy area per pod, colour card in frame | The phenotype that actually works cheaply | **$80–150** | Gross problems only |

### 3b. Robot layer

| # | Build | What you get | ≈ Cost | Biggest gap |
|---|---|---|---|---|
| R1 | **SO-101 follower only (12 V) + Pi 5 + wrist cam + PSU** | 6-DoF, 500 mm, ~500 g, current/temp telemetry, LeRobot native | **≈ $400** | No force sensing; 0.87° backlash; overheats on continuous duty |
| R2 | **R1 + 600 mm MGN12 belt axis** (NEMA17 + TMC2209 + endstop) or the printed SO-ARM100 Track-Axis | Fixed arm serving a 2–3 m pod row | **$550–600** | Rail repeatability undocumented for the printed version; add homing + fiducials |
| R3 | **R1 + rotating pod carousel** (stepper ring, pods come to the arm) | Fewest moving DoF; cheapest coverage | **≈ $480** | Ring diameter limits pod count (~12–16) |
| R4 | **Thor stepper arm** | 6-DoF, 750 g, stiff, no thermal issue | **≈ $400** | Open-loop, no LeRobot, own firmware |
| R5 | **LeKiwi** (12 V) with SO-101 | Holonomic base + arm + Pi + cams | **$482** | Omni wheels slip; no lift; no docking |
| R6 | **XLeRobot basic, differential base** | 2× SO-101, IKEA cart, 288 Wh (10 h), Bluetooth teleop | **≈ $660** (+$79 Pi) | Fixed 0.5–1.25 m workspace; no docking/charging; no field data |
| R7 | **DIY ArduRover catamaran** — PVC/foam pontoons, 2 thrusters + ESCs, Pixhawk-class FC, single F9P RTK, 4G or LoRa, 20–30 Ah LiFePO4, 50 W solar | Waypoint/loiter, ~4 h, ~0.5 m hold | **$800–1,000** | No docking mode; no arm on board at this price; comms/GPS failsafes are on you |

### 3c. Recommended complete builds under $1,000

| Name | Composition | ≈ Total | What it proves |
|---|---|---|---|
| **"Dip station"** (recommended V0) | G1 rack ($300) + R1 arm ($400) + probe head: DFRobot pH/EC/temp ($272) mounted on the arm with a KCl/DI/buffer dock, TPU compliant holder | **≈ $970** | The core thesis: one probe set, dipped and self-calibrated, serving 12 isolated pods. Stages 0–2 on a table. |
| **"Weigh & watch"** (cheapest instrumented farm) | G1 ($300) + G3 weigh rail ($450) + G4 camera ($120) | **≈ $870** | Closed-loop water + growth curves with *zero* arms; the HardwareX result at 2026 prices. Best if you want data before robotics. |
| **"Carousel"** (cheapest robot coverage) | G1 ($300) + R3 arm+carousel ($480) + DFRobot pH only ($65) + DS18B20 | **≈ $850** | Arm never moves its base; pods rotate to it. Simplest kinematics, highest repeatability per dollar. |
| **"Tile rail"** (Stage-3 primitive) | MACARONS-style 2020 rail + belt + NEMA17 moving a 12-pod tile between a light station, a dip station and a swap station; ESP32 | **≈ $400–600** | "Move the module to the tool" — the expansion step that should precede any mobile robot |
| **"Cart"** (only if mobility is the question) | R6 XLeRobot ($740) + G4 ($120) + AprilTags | **≈ $860** | Whether a $700 mobile dual-arm can seat a tile at all. Expect docking to be the whole project. |

Not achievable under $1,000: boat + arm; mobile robot + reliable docking/charging; any tactile task (harvest, packing, cleaning); sub-mm insertion.

---

## 4. Deltas to the V0 deck / spec

| Deck item | Change | Why |
|---|---|---|
| Tier A BOM: leader + follower arms ($250) | **Follower only ($120–200)**; script V0 | IL data (60–90% in-dist, 0% out); saves $100–150 |
| Pod base: keyed cone | **3-point kinematic seat + cone + magnet** | Jubilee/FarmBot: registration beats sensing |
| Water level: VL53L0X ToF on probe head | Keep, **add weigh dock as primary** | HardwareX: gravimetric is the robust signal |
| Servo protection | **Add 59/60 °C two-tier cutoff + 15-sample stall detector; 5-min rest per 20 min** | STS3215 has no firmware thermal cutoff |
| Probe head | **TPU-compliant mount; stagger pH/EC reads; PTFE-junction probes; annual probe budget** | HA thread, DFRobot guide |
| Stage 3 | **Insert "tile rail" before the cart** | MACARONS, Fifth Season, Iron Ox |
| Option B | Prefer **XLeRobot differential base**; treat docking/charging as unsolved research | LeKiwi slip; no docking anywhere |
| Option C | **Fixed arm on raft + boat as transporter; docked self-charging cleaner pattern**; dual-F9P heading; 4G failsafe | Boat+arm > $1k; BlueBoat forum; Remora |
| Crops | Keep radish + duckweed; **add a colour card to every pod photo** | Phenotyping literature |
| Metrics (roadmap slide 09) | **Fabricated fraction by count / mass / $; human-minutes per replication; override log** | RepRap, Freitas, OSE, AGC |
| Community | **Tile controller as JLCPCB-orderable PCB + forum** | AgOpenGPS pattern |

---

## 5. Sources

### Farm / garden robots and controllers
- https://farm.bot/collections/farmbot-kits · https://farm.bot/pages/express · https://farm.bot/products/farmbot-genesis-v1-8 · https://farm.bot/blogs/news/its-time-for-farmbot-express-and-genesis-max
- https://forum.farmbot.org/t/reviews-of-farmbot/8171 · https://forum.farmbot.org/t/the-newbs-guide-to-farmbots-limiting-factors-and-strengths/71 · https://forum.farmbot.org/t/farmbot-express-xl-doesnt-seem-to-be-a-ready-product/6233 · https://forum.farmbot.org/t/problems-with-x-axis-belts/4534
- https://software.farm.bot/v15/app/photos/weed-detection.html · https://software.farm.bot/v15/app/photos/camera-calibration.html · https://github.com/FarmBot/Farmbot-Web-App
- https://hackaday.com/2020/05/21/open-agriculture-initiative-shuttered-amid-scandal/ · https://spectrum.ieee.org/mit-media-lab-food-computer-project-shut-down · https://spectrum.ieee.org/mit-media-lab-scientist-used-syrian-refugees-to-tout-food-computers · https://github.com/futureag/mvp · https://github.com/WebbPeter/OpenAg-MVP-II
- https://github.com/Twisted-Fields/acorn-precision-farming-rover · https://twistedfields.readthedocs.io/en/latest/overview.html
- https://hackaday.io/project/204846-weedinator-2026-agricultural-robot · https://hackaday.com/2026/06/19/come-with-me-if-you-want-to-weed-autonomous-weedinator-robot-back-for-2026/
- https://github.com/geezacoleman/OpenWeedLocator · https://docs.openweedlocator.org/en/latest/ · https://www.nature.com/articles/s41598-021-03858-9
- https://store.farm-ng.com/products/la-maquina-amiga · https://github.com/farm-ng/farm-ng-amiga
- https://github.com/AgOpenGPS-Official/AgOpenGPS · https://www.fwi.co.uk/machinery/technology/how-to-build-your-own-tractor-autosteer-system-for-700 · https://discourse.agopengps.com/t/all-in-one-pcb/10444
- https://wiki.opensourceecology.org/wiki/Microtractor · https://en.wikipedia.org/wiki/Open_Source_Ecology · https://www.opensourceecology.org/gvcs/ · https://blog.p2pfoundation.net/a-makerhacker-communitys-critique-of-open-source-ecology/ · https://www.technologyreview.com/2025/10/16/1125146/civilization-start-kit-open-source-essential-machines/
- https://github.com/kizniche/Mycodo · https://github.com/JakeTheRabbit/HAGR · https://community.home-assistant.io/t/ph-tds-in-automation/414862 · https://www.dfrobot.com/blog-21377.html · https://atlas-scientific.com/kits/ezo-complete-ph-kit/ · https://atlas-scientific.com/kits/ezo-complete-ec-kit/ · https://github.com/hydromisc/hydromisc · https://mudpi.app/docs/release-notes · https://opensprinkler.com/product/opensprinkler/ · https://mtlynch.io/greenpithumb/
- https://hackaday.io/project/12517-hydrobot/details · https://hackaday.io/project/2964-hydropwnics · https://hackaday.io/project/172146-automated-hydroponic-farm-controller · https://hackaday.io/project/18961-arduino-based-automated-hydroponic-lettuce-seeder · https://hackaday.io/project/168342-microwth-automated-microgreen-farm
- https://www.blue-white.com/article/understanding-wear-factors-for-peristaltic-pump-tubes-and-other-components/ · https://www.jihpump.net/technical-support/blogs/why-peristaltic-pump-tubing-fails-and-how-to-fix-it · https://atlas-scientific.com/blog/peristaltic-pump-advantages-and-disadvantages/
- https://mistculture.com/gardyn-review-2025/ · https://risegardens.com/pages/faqs · https://www.sproutflat.com/posts/rise-gardens-gen-3-review-what-buyers-should-know-before-purchasing/ · https://shershegrows.com/aerogardens-back-2025-relaunch/ · https://littletechgirl.com/2024/10/02/aerogarden-is-going-out-of-business/

### Plant-handling robots and phenotyping
- https://oa.upm.es/96851/1/10366542.pdf · https://ieeexplore.ieee.org/abstract/document/10884759 · https://pmc.ncbi.nlm.nih.gov/articles/PMC9041226/ · https://forum.v1e.com/t/vertical-xy-gantry-for-automatic-robot-arm-harvester/52426
- https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2025.1605107/full · https://www.intechopen.com/chapters/70662 · https://arxiv.org/pdf/2505.16547
- https://www.researchgate.net/publication/339792088_Development_of_transplanting_manipulator_for_hydroponic_leafy_vegetables · https://www.nature.com/articles/s41598-023-28760-4 · https://doi.org/10.3390/agriengineering6010040
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10805289/ (Duckbot) · https://arxiv.org/abs/2210.04975 (MACARONS) · https://www.sciencedirect.com/science/article/pii/S2468067222000645 (Sidekick) · https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0275688
- https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.15129 (PhenoBox) · https://onlinelibrary.wiley.com/doi/full/10.1111/tpj.16587 (SPIRO) · https://plantmethods.biomedcentral.com/articles/10.1186/s13007-017-0248-5 (PYM) · https://www.mdpi.com/2077-0472/13/10/1874 · https://bsapubs.onlinelibrary.wiley.com/doi/full/10.1002/aps3.1031

### Manipulators, mobile, USV
- https://huggingface.co/docs/lerobot/so101 · https://huggingface.co/docs/lerobot/en/lekiwi · https://huggingface.co/docs/lerobot/en/koch · https://github.com/huggingface/lerobot/issues/1243 · https://github.com/alpibrusl/lex-robot/issues/3
- https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/ · https://www.roboticscenter.ai/hardware/so-101 · https://www.roboticscenter.ai/learn/robot-arms/openarm-vs-so101 · https://www.seeedstudio.com/SO-ARM101-Low-Cost-AI-Arm-Kit-p-6426.html · https://thinkrobotics.com/blogs/product-reviews-buying-guides/thinkrobotics-lerobot-so-101-6-axis-robotic-arm-review-ai-ready-open-source-and-built-for-learning
- https://www.ml6.eu/en/blog/ai-robotics-a-field-report-on-imitation-learning-with-lerobot · https://medium.com/correll-lab/when-fine-tuning-hurts-failure-modes-of-visuomotor-imitation-learning-on-a-low-cost-robot-5f5013df7c95 · https://arxiv.org/pdf/2605.12247
- https://github.com/SIGRobotics-UIUC/LeKiwi · https://foxglove.dev/blog/upgrading-the-lekiwi-into-a-lidar-equipped-explorer · https://kamathrobotics.com/sensor-fusion-on-lekiwi
- https://github.com/Vector-Wangel/XLeRobot · https://xlerobot.readthedocs.io/ · https://shop.wowrobo.com/products/xlerobot-dual-arm-mobile-household-robot-kit · https://github.com/timqian/bambot · https://github.com/phospho-app/lecabot
- https://github.com/avenhaus/SO-ARM100-Track-Axis · https://github.com/kunxiang/Linear-Rail-System
- https://arxiv.org/abs/2605.16537 (Nori Bot) · https://arxiv.org/abs/2412.10447 (TidyBot++) · https://arxiv.org/pdf/2401.02117 (Mobile ALOHA) · https://arxiv.org/abs/2110.00736 (Pupper) · https://www.petoi.com/pages/research-spotlight
- https://github.com/enactic/OpenArm · https://github.com/AngelLM/Thor · https://github.com/BCN3D/BCN3D-Moveo · https://github.com/peng-zhihui/Dummy-Robot · https://anninrobotics.com/product-page/ar4-mk5-robot-combo-kit/ · https://anninrobotics.com/forum/questions/total-cost-of-ar4-arm/ · https://shop.elephantrobotics.com/collections/mycobot-280 · https://www.wlkata.com/ · https://www.robotshop.com/products/feetech-74v-19kg-serial-bus-servo-w-current-feedback
- https://www.filastruder.com/products/jubilee-motion-platform-kit · https://science-jubilee.readthedocs.io/en/latest/getting_started/new_user_guide.html · https://github.com/machineagency/science-jubilee · https://jubilee3d.com/index.php?title=Locating_Tools · https://dl.acm.org/doi/10.1145/3313831.3376425
- https://en.wikipedia.org/wiki/Opentrons · https://opentrons.com/robots/ot-2 · https://github.com/Opentrons/ot2 · https://docs.opentrons.com/ot-2/calibration/robot-calibration/ · https://support.opentrons.com/s/article/SmoothieError-Homing-fail · https://labautomation.io/t/opentrons-ot-2-pipette-tip-pickup-problem-cant-pick-up-second-column-from-tiprack/3275
- https://www.sciencedirect.com/science/article/pii/S2405896322010989 · https://automaticaddison.com/autonomous-docking-with-apriltags-using-nav2-ros-2-jazzy/ · https://www.researchgate.net/publication/393571825_Multi-Sensor_Fusion_for_Autonomous_Mobile_Robot_Docking_Integrating_LiDAR_YOLO-Based_AprilTag_Detection_and_Depth-Aided_Localization
- https://bluerobotics.com/store/boat/blueboat/blueboat/ · https://discuss.bluerobotics.com/t/blueboats-in-the-wild/15151 · https://discuss.bluerobotics.com/t/travel-not-aligning-well-with-mission/20535/18 · https://discuss.bluerobotics.com/t/blueboat-issues-prearm-check-mag-field-xy-diff-176-100/22466 · https://discuss.bluerobotics.com/t/gps-issues-with-blueboat/16134
- https://ardupilot.org/rover/docs/boat-configuration.html · https://discuss.ardupilot.org/t/how-to-make-loiter-more-accurate-with-rtk/13059 · https://ardupilot.org/copter/docs/common-gps-for-yaw.html · https://hackaday.io/project/166552-small-autonomous-survey-vessel · https://hackaday.io/project/167480-creating-an-autonomous-dinghy-with-ardurover · https://pmc.ncbi.nlm.nih.gov/articles/PMC10181514/ · https://www.sciencedirect.com/science/article/pii/S2468067219300367 · https://www.hardware-x.com/article/S2468-0672(25)00012-4/fulltext · https://www.researchgate.net/publication/353813259_Vision-based_positioning_system_for_auto-docking_of_unmanned_surface_vehicles_USVs · https://osab.xyz/ · https://hackaday.io/project/180505-deepplankter-autonomous-drone-boat · https://hackaday.io/project/1677-solarsurfer

### Replication, autonomous growing, failures, aquatic
- https://reprap.org/wiki/Development_Pathway · https://hackaday.com/2015/09/12/the-most-self-replicating-reprap-yet/ · https://hackaday.com/2016/03/02/getting-it-right-by-getting-it-wrong-reprap-and-the-evolution-of-3d-printing/ · https://3dprint.com/139445/dollo-kickstarter-3d-printer/ · https://pswscience.org/meeting/entropy-and-self-replicating-robots/ · http://www.rfreitas.com/Astro/GrowingLunarFactory1981.htm
- https://www.wur.nl/en/research/plant/autonomous-greenhouse-challenge · https://www.hortidaily.com/article/9441502/focus-on-crop-temperature-brings-victory-to-koala-in-autonomous-greenhouse-challenge/ · https://www.hortidaily.com/article/9696098/all-or-nothing-strategy-pays-of-in-autonomous-greenhouse-challenge/
- https://www.nasa.gov/wp-content/uploads/2019/04/veggie_fact_sheet_508.pdf · https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2021.733944/full · https://science.nasa.gov/sciact-team/growing-beyond-earth/ · https://www.nasa.gov/news-release/nasa-selects-winners-announces-final-phase-of-space-food-challenge/
- https://foodlore.blog/why-vertical-farms-go-bankrupt/ · https://news.crunchbase.com/agtech-foodtech/vertical-farming-venture-capital-plenty-appharvest/ · https://pitchbook.com/news/articles/bowery-farming-collapse-leaf-eating-pathogen-failed-acquisition · https://www.agnavigator.com/Article/2024/11/05/What-does-Bowery-s-closure-tell-us-about-the-future-of-vertical-farming/ · https://www.fertilizerdaily.com/20251114-bowery-farmings-70m-georgia-vertical-farm-heads-to-liquidation-as-startups-collapse-triggers-nationwide-sell-offs/ · https://agfundernews.com/plenty-has-an-opportunity-to-succeed-say-some-vertical-farming-experts-what-happens-next · https://www.lpm.org/investigate/2023-11-16/a-celebrated-startup-promised-kentuckians-green-jobs-it-gave-them-a-grueling-hell-on-earth · https://agfundernews.com/fifth-seasons-former-vp-on-why-it-failed-and-how-vertical-farming-must-change · https://www.verticalfarmdaily.com/article/9537965/lessons-from-vertical-farming-bankruptcies-layoffs-and-closures-in-2023/ · https://techcrunch.com/2022/11/03/iron-ox-lays-off-50-amounting-to-nearly-half-its-staff/ · https://agfundernews.com/another-blow-for-indoor-farm-robotics-as-iron-ox-lays-off-nearly-half-its-staff
- https://www.greenwave.org/our-model · https://www.greenwave.org/report · https://thefishsite.com/articles/report-north-american-kelp-farming-poised-for-growth · https://heatmap.news/politics/running-tide-carbon-shut-down · https://www.latitudemedia.com/news/running-tides-final-year/ · https://agfundernews.com/lemna-duckweed-processor-lemnature-aquafarms-files-for-bankruptcy-asset-sale-set-for-dec-12
- https://businessnorway.com/solutions/aqua-robotics-safer-and-healthier-fish-farms-with-autonomous-net-cleaning · https://aquanor.no/en/2025/08/13/continuous-net-cleaning-with-a-wireless-self-operating-robot/ · https://www.sintef.no/en/projects/2019/netclean-247/ · https://ar5iv.labs.arxiv.org/html/2404.12995 · https://ponicslife.com/how-to-build-a-big-floating-raft-hydroponics-system-lessons-learned/
- https://www.fytechsystems.com/how-to-build-a-microgreens-vertical-farm-complete-commercial-guide/ · https://ageyetech.com/news/automation-playbook-robotics-indoor-farms

Caveats: AgriCruiser did not surface in searches this pass; Acorn's and OpenAg's forums are offline; a few paywalled pages (PitchBook, one MDPI paper, one HardwareX USV paper, Post-Gazette Fifth Season) were read via abstracts/secondary coverage.
