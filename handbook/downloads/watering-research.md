Current consolidated decisions: [Field guide](../index.html). This is the September 21 evidence review; its cart-status statements are historical.

# XLeRobot plant-care reuse review — September 21, 2026

## Finding

The official 0.3.0 showcase does demonstrate watering plants without an external electric pump. At roughly **00:56–00:59**, the robot tips a small clear plastic bottle over a planted tray. The footage looks like pouring from a bottle, not a demonstrated spray-trigger actuation. The on-screen caption explicitly says **“Teleoped with Switch Joycons”**; the video is sped up 8×. Other sections of this same montage are labelled automated RL, which must not be transferred to the watering segment.

- [Official demo page](https://xlerobot.readthedocs.io/en/latest/demos/index.html)
- [Direct official video at watering segment](https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot030.mp4#t=56,60)
- Evidence frame: `watering-demo.png`, extracted at 59 seconds; `watering-frames.jpg` covers 56–62 seconds.

## What can be reused

| Existing work | Verified scope | Implication for our build |
|---|---|---|
| Official showcase | Teleoperated bottle watering, visually verified | Reuse the simple physical approach, then commission our bottle, pod access and motion. |
| [Official teleoperation examples](https://xlerobot.readthedocs.io/en/latest/software/getting_started/XLeRobot_teleop.html) | Keyboard/gamepad control; repo also includes a two-wheel Joycon example | Useful starting point for a supervised watering motion. A control script is not a plant-care policy. |
| [Official ACT guide](https://xlerobot.readthedocs.io/en/latest/software/getting_started/VLA_ACT.html) | Record demonstrations, train and evaluate a task policy; camera poses matter | Reuse the workflow. Collect our bottle/pod demonstrations after a reliable manual teleop motion. |
| [SmolVLA/ACT community guide](https://xlerobot.readthedocs.io/en/latest/software/getting_started/VLA_smol.html) | Bimanual data recording and task-specific training/inference | An alternative training pipeline; not evidence of a watering checkpoint. |
| [yihao-brain-bot/xlerobot-get-water](https://huggingface.co/datasets/yihao-brain-bot/xlerobot-get-water) | Read actual tasks.parquet: drive to table, grasp drink, put it in robot basket | Drink retrieval, not plant watering. Do not import based on its name. |
| [wangranryan/xlerobot_water](https://huggingface.co/datasets/wangranryan/xlerobot_water) | Read actual tasks.parquet: “把水瓶放到篮子里” (put water bottle in basket) | Bottle transport, not pouring or crop care. |
| [GEST team report](https://devpost.com/software/gest-gesture-enabled-system-for-teleoperation) | Authors report teleoperated water pouring and preliminary data collection | Additional manipulation precedent; not a validated autonomous plant-care system. |

No downloadable plant-watering policy/checkpoint, crop moisture feedback loop or multi-day plant-care evaluation was located in the reviewed sources. This is a bounded search finding, not proof none exists anywhere. No author was contacted.

## Audit scope

- Upstream repository tree at commit `a7ee564294f03484783ed053ab1550bccc3c6c09`; recursive tree reported `truncated: false`.
- Retrieved 77 English documentation and software Python/Markdown files plus README; searched water/plant/spray mentions and training references. Did not execute upstream code.
- Inspected the official 120-second showcase via extracted frames; followed plant segment at one-second intervals.
- Searched public web and Hugging Face XLeRobot model/dataset metadata; model query returned 44 entries and dataset query was capped at 200. Examined task metadata for the two relevant water-named datasets above. Search does not establish exhaustive coverage.

## Updated choice

Use a small bought pouring bottle with a controlled outlet and a printed parking rest. Start with a small fill, manually load the gripper if necessary, and validate grasp, reach, repeatable tiny pours and return-upright. Exact bottle/cap is not selected; no fabricated attachment fit. Spray bottle is a later option only if the actual trigger can be actuated reliably without losing grip.

Remove electric pump, external jug, water hoses/barbs, pump adapter, pump relay role, flyback diode, pump fuse and reservoir float from V0 scope. Water temperature monitoring is also deferred. Keep one relay channel to briefly energize the resistive moisture probe. The 3-relay pack can supply that one channel; do not call all three required. The Amazon cart was not edited in this revision.

The bottle still stores water and needs human refill. There is no automatic refill in V0. Tilting controls water approximately; neither tilt duration nor increased soil wetness proves delivered millilitres. A disabled servo while pouring is not equivalent to closing a valve. Commission an upright recovery when control is available and test power-loss behaviour over containment with only a small bottle fill.

## Movable light measurement

One BH1750 can be held on a removable, upward-facing paddle at canopy height. Set a fixed measurement pose per pod; avoid robot shadows, settle, gather multiple new conversions and report a median/spread. Repeated samples improve repeatability, not calibration accuracy. Do not keep moving until the number happens to look desirable. Log position, orientation, height, timestamp and valid/unstable/saturated status. Test the real moving I2C harness for communication errors before relying on it.

[ROHM's BH1750 datasheet](https://www.mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf) specifies 120 ms typical / 180 ms maximum high-resolution conversion time at default timing and describes approximately human-eye spectral response and ±20% variation. Proposed starting protocol: wait at least one complete conversion after settling, then collect ten distinct conversions over about two seconds (respect configured measurement timing). Reject saturation, stale samples or excessive variation; compare against a trusted lux meter if absolute accuracy matters. Lux does not directly measure PPFD.
