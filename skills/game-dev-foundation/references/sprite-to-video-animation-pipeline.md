# Sprite-To-Video-To-Frames Animation Pipeline

Use this workflow when the goal is to turn one approved 2D sprite, several key poses, or a static character illustration into game-ready 2D animation frames.

The preferred path is:

```text
approved 2D sprite
-> model choice checkpoint
-> start/end or multi-keyframe video generation
-> raw frame extraction
-> frame selection
-> background removal / alpha cleanup
-> canvas and pivot normalization
-> identity and silhouette repair
-> gameplay timing
-> PNG frame sequence
-> preview GIF and contact sheet
-> engine import test
-> spritesheet / atlas
```

Do not treat the AI video as the final animation. Treat it as a motion source.

## Helper Script

Use the bundled helper to scaffold and validate the pipeline structure before production:

```powershell
python skills/game-dev-foundation/scripts/sprite_video_pipeline.py init `
  --output C:\tmp\sprite_pipeline_smoke `
  --asset-id test_runner `
  --animation run_right `
  --model Kling `
  --control-mode start-end `
  --background green-screen `
  --size 128x128 `
  --fps 10 `
  --frames 8 `
  --engine Godot

python skills/game-dev-foundation/scripts/sprite_video_pipeline.py validate `
  --task C:\tmp\sprite_pipeline_smoke
```

The script only handles deterministic production structure and validation. It does not call image/video models. Model execution remains a user-confirmed checkpoint.

## Why This Is Preferred

Direct AI spritesheet generation often fails in game production:

- frame cells are uneven
- body identity drifts per frame
- weapons, clothes, and faces mutate
- pivot and feet position jitter
- animation timing follows video rhythm instead of gameplay rhythm
- bad frames are hidden inside the sheet

Video models are better at producing continuous motion. The production trick is to generate a short controlled clip, extract more frames than needed, reject bad frames, repair the survivors, then retime them as game animation.

## Required User Decisions

Before generating video, ask the user to choose:

```text
animation target: character / enemy / VFX / UI / background layer
style: pixel / clean 2D / anime / painterly / low-res prerender / hybrid
view: side / top-down / 3/4 / isometric
model: Kling / Runway / Luma / Pika / Scenario / local ComfyUI or other
control mode: single image / start-end frames / multi-keyframe / reference video
background strategy: transparent if available / green screen / blue screen / flat neutral / black VFX plate
output size: 64 / 128 / 256 / 512
target FPS: 6 / 8 / 10 / 12 / custom
engine: Godot / Unity / GameMaker / other
acceptance screenshot: required scene or camera zoom
```

If the user does not know, default to:

```text
control mode: start-end frames
background strategy: green screen for characters, black plate for additive VFX
target FPS: 8 for small characters, 12 for action/VFX
output: transparent PNG frame sequence first, spritesheet later
```

## Model Choice Matrix

Choose based on control need, not brand preference.

| Option | Best Use | Strength | Main Risk | Choose When |
| --- | --- | --- | --- | --- |
| Kling O1 / current Kling image-to-video | Character actions with start/end frames | Strong start/end frame control and transition generation | May still alter costume or limb details | Need controlled run, attack, jump, hit, death clips |
| Runway Gen-4 / current Runway reference workflow | Character consistency from references | Good reference-based character/object consistency | Can become cinematic unless prompt forbids camera movement | Need identity consistency across variations |
| Luma Ray / Dream Machine | Multi-keyframe motion and smooth clips | Good directed motion and multiple keyframe control | Output may be too cinematic or high-detail | Need several poses held inside one clip |
| Pika | VFX, local motion, stylized deformation | Quick motion/region-style experiments | Character identity less reliable for gameplay sprites | Need slash, burst, aura, UI flourish, meme-like motion |
| Scenario / game-asset platforms | Integrated game-asset workflows | Sprite-oriented interfaces and asset pipeline framing | May hide low-level controls | Need fast iteration and simple exports |
| Local ComfyUI / open workflow | Repeatable controlled experiments | Full pipeline ownership and automation | Setup complexity and model quality variance | Need batch production, privacy, or reproducibility |

Record the chosen model and reason in the asset metadata. If two models are plausible, generate a one-action bakeoff clip from both before bulk work.

## Node 0: Asset Contract

Input:

- project art bible or style reference
- target animation name
- gameplay use
- engine and camera scale

Action:

Write the contract:

```text
asset_id:
animation:
gameplay purpose:
view:
canvas size:
character occupied pixels:
target frame count:
target FPS:
pivot:
collision relation:
hit frame:
loop required:
model candidates:
background strategy:
engine import target:
acceptance scene:
```

Acceptance:

- gameplay purpose is clear
- camera/view is fixed
- frame count and FPS are declared
- pivot and collision relationship are declared
- at least two model candidates are listed or one model is justified

Stop if missing:

- gameplay purpose
- view
- output size
- model/control choice

## Node 1: Approved Static Sprite

Input:

- single sprite or character illustration

Action:

Prepare one approved image:

- full body or full object
- no crop
- fixed costume and weapon
- clean silhouette
- simple readable colors
- transparent or clean flat background
- no baked ground shadow unless required

Acceptance:

- sprite reads at final gameplay zoom
- no random text or symbols
- body proportions are intentional
- export size matches contract or can be safely resized
- user approves this as identity anchor

Stop if:

- source image is only a concept painting
- object is cropped
- camera angle is wrong
- silhouette fails at gameplay zoom

## Node 2: Keyframe Plan

Input:

- approved sprite
- animation contract

Action:

Decide control mode:

```text
single image: fastest, least control
start-end: best default for loops and actions
multi-keyframe: best for complex attacks/death/VFX
reference video: useful for motion style, risky for identity
```

Create key poses when possible:

```text
idle: pose A, pose B, pose A
run: right foot forward, left foot forward
attack: anticipation, contact, recovery
hurt: neutral, impact
death: standing, collapse, final pose
VFX: seed, expansion, peak, dissipate
```

Acceptance:

- start and end poses support the intended motion
- hit/contact frame is identified for attacks
- loop animations have a loop closure plan
- user confirms model/control mode before generation

## Node 3: Video Generation

Input:

- approved sprite
- start/end or multi-keyframes
- chosen model

Prompt rules:

- lock camera
- forbid zoom, pan, orbit, cut, and background story
- describe one action only
- request same character, same outfit, same weapon
- request plain background or transparency if supported
- request game sprite readability

Prompt skeleton:

```text
Use the provided 2D game sprite as the exact character identity.
Generate a short locked-camera [view] animation of [action].
Keep the same outfit, colors, weapon, silhouette, and proportions.
No camera movement, no zoom, no scene cut, no new objects.
Plain [background] background.
Motion should be readable as a small game sprite.
```

Generation settings:

```text
duration: 2-4 seconds
aspect: square or source-compatible
resolution: high enough for cleanup, not final size dependent
motion: low to medium for idle, medium for run/action, high only for VFX
```

Acceptance:

- motion matches one intended action
- camera is locked
- identity remains usable for at least 60 percent of the clip
- no major crop
- no background interaction that blocks removal

Stop if:

- camera moves
- character turns to wrong view
- costume/weapon changes too much
- generated motion cannot be retimed into gameplay

Decision:

- approve clip
- regenerate same model with tighter prompt
- switch model
- add start/end or more keyframes

## Node 4: Raw Frame Extraction

Input:

- approved source video

Action:

Extract frames at a higher rate than final animation needs.

Example:

```powershell
ffmpeg -i input.mp4 -vf "fps=24" raw_%04d.png
```

For short loops, extract at 24 fps and select down to 6-12 game frames. For VFX, extract 12-24 frames depending on readability.

Acceptance:

- raw frames exist as numbered PNGs
- extraction rate is recorded
- no compression issue makes all frames unusable

## Node 5: Frame Selection

Input:

- raw frame sequence

Action:

Select only frames that communicate useful animation phases.

Reject frames with:

- motion blur that hurts sprite readability
- broken hands, limbs, face, weapon, or props
- silhouette collapse
- duplicate action phase
- major scale drift
- wrong contact/hit pose

Target counts:

```text
idle: 4 frames
walk: 6 frames
run: 6-8 frames
attack: 6-10 frames
hurt: 2-4 frames
death: 8-12 frames
VFX: 8-16 frames
```

Acceptance:

- selected frames cover anticipation, action, and recovery when relevant
- frame count matches contract or contract is revised
- rejected frames are not silently kept

## Node 6: Background Removal And Alpha Cleanup

Input:

- selected frames

Action:

Remove or key the background:

```text
character/enemy: green or blue screen -> chroma key -> alpha cleanup
VFX additive: black plate -> additive/import shader path
soft VFX alpha: segmentation/manual mask, avoid destructive keying
UI motion: transparent or flat neutral background
```

Acceptance:

- alpha edge is clean at final scale
- no green/blue fringe remains
- semi-transparent VFX is preserved or explicitly converted to additive
- no holes appear inside character silhouette

Stop if:

- background removal destroys key body parts
- VFX transparency is lost
- alpha edge is too noisy for gameplay scale

## Node 7: Canvas, Scale, And Pivot Normalization

Input:

- cleaned selected frames

Action:

Normalize:

- fixed canvas size
- common scale
- consistent pivot
- feet or origin locked
- consistent visual center
- no auto-trim jitter

Pivot defaults:

```text
grounded character: feet center
flying enemy: body center
projectile: launch origin or visual center
slash VFX: attack origin
explosion VFX: center
UI icon: center
```

Acceptance:

- preview playback has no unintended jitter
- pivot matches engine import plan
- frame bounds do not change runtime position
- canvas matches export contract

## Node 8: Identity And Gameplay Repair

Input:

- normalized frames

Action:

Repair only what matters:

- face/head drift
- weapon shape
- team color
- missing limbs
- silhouette clarity
- hit/contact pose
- edge artifacts

Use manual edits, inpainting, or replacement from neighboring good frames. Prefer deleting a bad frame over preserving it.

Acceptance:

- identity is stable across frames
- action reads at gameplay zoom
- hit frame is visible
- animation does not imply a false hitbox

## Node 9: Gameplay Timing

Input:

- repaired frames

Action:

Retiming should follow gameplay:

```text
idle: slow loop
run: even loop
attack: startup -> active -> recovery
hurt: fast readable impact
death: fast loss of control, slower settle
VFX: warning -> active -> fade
```

For attacks, write:

```text
startup_frames:
active_frames:
recovery_frames:
cancel_allowed:
damage_frame:
```

Acceptance:

- timing supports player feedback
- damage/contact frame is explicit
- loop has no visible pop unless intentional
- animation length matches gameplay state machine

## Node 10: Export Package

Output:

```text
frames/
  {asset}_{action}_{direction}_000.png
  {asset}_{action}_{direction}_001.png
preview.gif
contact_sheet.png
spritesheet.png
metadata.md
import_notes.md
engine_screenshot.png
```

Naming:

```text
character_flagboy_run_right_000.png
enemy_lineman_attack_left_005.png
vfx_tackle_hit_007.png
```

Acceptance:

- PNG frame sequence is the source of truth
- preview GIF exists
- contact sheet exists
- model, prompt, seed if available, source video, extraction FPS, selected frame indices, and edit notes are recorded
- spritesheet/atlas is generated only after frame QA

## Node 11: Engine Test

Godot:

- import frames under `res://assets/...`
- create `AnimatedSprite2D` or equivalent animation resource
- set texture filtering to project standard
- verify pivot/origin in scene
- play at target FPS
- screenshot at real gameplay camera zoom

Unity:

- import as sprites
- set Pixels Per Unit
- create animation clip
- verify pivot in Sprite Editor
- pack Sprite Atlas after single-frame QA
- screenshot in gameplay camera

Acceptance:

- animation plays in engine
- scale is correct
- pivot is stable
- no alpha fringe is visible
- gameplay timing matches state logic
- screenshot shows readability in the intended scene

## Checkpoint Protocol

At each node, report:

```text
Node:
Input:
Decision needed:
Chosen option:
Acceptance result:
Blocked by:
Next action:
```

Ask for user confirmation at these points:

1. model/control mode before video generation
2. source video approval before extraction
3. selected frame set before cleanup
4. repaired preview before engine import
5. engine screenshot before atlas/bulk production

## Local Validation Smoke Test

Before trusting the pipeline skill, run a paper validation:

```text
asset: test_runner
animation: run_right
model options: Kling, Runway, Luma
control mode: start-end
background: green screen
target: 8 frames at 10 fps, 128x128, feet-center pivot
```

Expected outputs:

- asset contract can be filled without ambiguity
- model choice can be justified
- each node has a clear pass/fail gate
- the pipeline never moves from raw video directly to final spritesheet
- engine screenshot is required before bulk production

## Source Notes

- Kling O1 documentation describes start and end frame control for guiding video transitions.
- Runway Gen-4 material emphasizes reference-based character and object consistency.
- Luma Ray material describes multi-keyframe direction inside a clip.
- Scenario describes video generation and frame extraction as a production method for sprite workflows.
- ffmpeg documentation supports extracting numbered image sequences from video.
