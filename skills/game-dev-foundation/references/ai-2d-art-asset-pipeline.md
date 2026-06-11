# AI 2D Game Art Asset Pipeline

This is the default full-AI 2D asset workflow for game projects. It assumes AI tools are used for concept, generation, cleanup, variation, animation assistance, and QA support, but the final acceptance test is always in-engine readability.

## Core Principle

AI output is not the asset. AI output is raw visual material.

A game asset becomes usable only after it has:

- a gameplay role
- a stable size and camera-scale contract
- transparent or layered exports where needed
- animation/frame consistency where needed
- engine import settings
- collision, anchor, pivot, and sorting assumptions
- in-engine screenshots proving readability

## Folder Contract

Use this structure per project or asset pack:

```text
art/
  bible/
    style_bible.md
    palette.png
    scale_sheet.png
    references/
  source_ai/
    prompts/
    raw_generations/
    selected/
  work/
    cleanup/
    layered/
    animation/
    upscale/
  export/
    characters/
    enemies/
    props/
    projectiles/
    pickups/
    tiles/
    vfx/
    ui/
    backgrounds/
  engine/
    import_notes.md
    contact_sheets/
    previews/
```

Rules:

- `source_ai` keeps raw generations and prompt metadata.
- `work` keeps editable cleanup files and frame work.
- `export` contains only game-ready PNG/WebP/atlas files.
- `engine` contains import settings, preview screenshots, and acceptance notes.
- Never overwrite raw AI output. Select, copy, then edit.

## Asset Contract Template

Every asset family should have a short contract before generation:

```text
Asset family:
Gameplay role:
Camera/view:
World scale:
Export size:
Pixel density:
Background:
Silhouette rule:
Palette:
Lighting/shadow:
Animation list:
Frame count per animation:
Pivot:
Collision shape:
Sorting layer/z index:
Engine import settings:
Forbidden details:
Acceptance screenshot:
```

Example:

```text
Asset family: flag football player
Gameplay role: controllable runner
Camera/view: top-down 3/4
World scale: 128x128 PNG, body reads at 48-64 px in-game
Export size: 128x128 transparent frame sequence
Pixel density: clean pixel/illustrative hybrid, no microtexture
Background: transparent
Silhouette rule: flag belt and ball arm readable at gameplay zoom
Palette: team color primary, white pants, dark outline
Lighting/shadow: consistent soft top-left light, no baked ground shadow
Animation list: idle, run_right, run_left, catch, dive, flag_pull
Frame count per animation: idle 4, run 6, action 6-8
Pivot: feet center
Collision shape: capsule around torso/legs, not full sprite bounds
Sorting layer/z index: actor
Engine import settings: no mipmaps for pixel art, filter nearest or project standard
Forbidden details: random jersey numbers, extra limbs, unreadable flags
Acceptance screenshot: 4 actors on field at default camera zoom
```

## Pipeline

### 1. Visual Bible

Create a small visual bible before bulk generation:

- target camera view
- scale sheet with one player, one enemy, one pickup, one projectile, one tile
- palette and contrast rules
- line weight and outline rules
- animation exaggeration rules
- UI icon readability rules
- banned artifacts: extra fingers, random symbols, baked backgrounds, inconsistent shadows, semi-transparent edge noise

Do not generate a full content set before the bible has passed an in-engine screenshot test.

### 2. Generate Source Images

Generate many rough candidates, but select aggressively.

For 2D game assets, prompt for:

- exact camera angle
- isolated asset
- transparent background if supported
- full body or full object, uncropped
- simple readable silhouette
- consistent material and outline language
- no text unless creating UI text intentionally
- no baked drop shadow unless the engine never supplies shadows

For character/enemy sets, generate or derive a canonical pose first. Use the selected image as reference for variants and animation frames.

For backgrounds, generate in layers when possible:

- far background
- midground
- gameplay plane
- foreground occluders
- sky/weather overlay

### 3. Cleanup And Normalize

All selected images pass through cleanup:

- remove background
- remove edge halos
- correct alpha fringing
- simplify noisy details
- normalize canvas size
- normalize pivot
- enforce palette and contrast
- remove unwanted text/symbols
- check silhouette at gameplay zoom

Use AI cleanup/inpainting for defects, then use deterministic image tools for canvas, crop, trim, scaling, naming, and atlas packing.

### 4. Animation Workflow

Use frame sequences as the source of truth.

Preferred order:

1. Choose canonical design.
2. Define animation list and frame counts.
3. Generate rough motion or key poses.
4. Fix identity drift frame by frame.
5. Normalize canvas and pivot.
6. Export transparent PNG frames.
7. Build preview GIF/contact sheet.
8. Import into engine and test at gameplay zoom.
9. Pack atlas only after frame QA passes.

Minimum acceptance for a 2D character animation:

- same body proportions across frames
- stable head/torso identity
- no limb count errors
- no random costume changes
- no canvas jitter unless intentionally animated
- readable primary action at actual camera zoom
- loop feels acceptable at target FPS

### 5. Tiles And Terrain

Tiles need stricter constraints than illustrations.

Requirements:

- fixed tile size
- edge continuity
- readable collision boundary
- separated decorative overlays
- variants per terrain type
- contact sheet showing tiling seams
- in-engine camera screenshot

For AI-generated terrain, avoid relying on a single large generated image as the gameplay layer. Prefer tileable pieces and overlays that the level system can compose.

### 6. UI Icons And Portraits

UI assets must be tested at final screen size, not artboard size.

Requirements:

- 1 icon reads at small size
- no illegible AI text
- consistent stroke and fill language
- rarity/state variants defined by data, not random recolors
- disabled/hover/selected states planned
- exported at expected sizes, usually 1x/2x/4x or project standard

For portraits, keep expression variants separate from gameplay icons. Portrait polish should not delay core gameplay readability.

### 7. VFX

VFX should communicate gameplay, not just look expensive.

Contract fields:

- warning frame
- active frame
- recovery/fade frame
- damage/hit timing
- color meaning
- team/enemy ownership
- opacity limit
- collision shape relationship

Acceptance:

- hazard boundary is visible before damage
- effect does not hide player/enemy silhouettes
- effect reads on common backgrounds
- effect does not imply wrong hitbox size

### 8. Import Into Engine

Godot defaults:

- place exports under `res://assets/...`
- use consistent folder naming per asset family
- set texture filtering per art style
- disable mipmaps for crisp pixel art unless the project needs zoomed minification
- set pivots consistently in `Sprite2D`, `AnimatedSprite2D`, or animation resources
- keep collision in scenes/resources, not baked into art
- create a contact-test scene with all new assets at gameplay camera zoom

Unity defaults:

- import as Sprite or Multiple Sprite for sheets
- set Pixels Per Unit consistently per category
- use Sprite Editor for slicing and pivot
- pack with Sprite Atlas after sprite QA
- separate visual prefab from gameplay data where possible

## Naming Contract

Use predictable names:

```text
{family}_{asset}_{action}_{direction}_{frame}.png
```

Examples:

```text
character_flagboy_idle_down_000.png
character_flagboy_run_right_003.png
enemy_lineman_charge_left_005.png
projectile_arrow_fly_right_002.png
vfx_tackle_hit_004.png
ui_icon_skill_sprint.png
tile_grass_edge_north_00.png
```

Rules:

- lowercase
- ASCII
- no spaces
- zero-padded frame numbers
- direction only when relevant
- suffix variants intentionally: `_team_red`, `_rare`, `_damaged`, `_night`

## Metadata Contract

Each asset family should keep metadata:

```text
tool:
model:
date:
prompt:
negative_prompt:
seed:
reference_images:
license_notes:
edited_by:
source_path:
export_path:
engine_preview:
acceptance_status:
```

The goal is repeatability and legal/production traceability, not bureaucracy.

## QA Checklist

Before accepting an asset:

- gameplay role is clear
- silhouette reads at camera zoom
- canvas size is correct
- pivot is correct
- alpha edge is clean
- naming follows contract
- metadata exists
- import settings are documented
- collision assumptions are documented
- animation has no unwanted jitter
- contact sheet exists for sets
- in-engine screenshot exists
- asset does not introduce style drift

## Production Rule

Bulk production starts only after one vertical slice passes:

- one playable character
- one enemy or interactable target
- one projectile or action VFX
- one pickup or reward
- one UI icon
- one terrain/background sample
- one in-engine screenshot showing all of them together

This prevents generating a large inconsistent asset library that later fails inside the actual game.
