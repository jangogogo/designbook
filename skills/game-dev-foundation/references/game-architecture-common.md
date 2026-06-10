# Game Architecture Common Memory

## Core Principles

- Prefer Godot 4.x C#/.NET for desktop/mobile prototypes unless the project already chooses another engine.
- Build playable, testable, tunable thin slices before expanding content, art, animation, and long-term systems.
- Keep logic separate from presentation.
- Keep data separate from code.
- Let architecture serve iteration speed; do not build heavy frameworks for distant hypotheticals.

## Layering

Use this default flow:

```text
Input / Editor / Debug UI
  -> Command / Intent
  -> Runtime Logic / Systems
  -> Data State
  -> Event / Signal
  -> View / Animation / HUD
```

Common folders:

- `scripts/Logic` or `src/Simulation`: rules, combat, AI, jobs, settlement, config parsing; avoid Godot Node dependencies.
- `scripts/View` or `src/Presentation`: input, rendering, animation, HUD, scene nodes, signal subscription.
- `scripts/Data` or `src/Core`: config models, runtime data, saves, loaders, entity definitions.
- `data/` or `Resources/TableJson/`: source JSON/table config.
- `resources/`: runtime art, UI, audio.
- `docs/design` or `designbooks`: GDD, validation plans, requirement sync, risk lists.

## Logic / View Separation

- Core simulation should run without visual nodes where practical.
- View forwards input into commands, subscribes to events, and plays presentation.
- Logic exposes stable snapshots/events; View does not mutate internal rules directly.
- Animation must not decide rules. Rules resolve first; presentation replays events.

## Data-Driven Design

- Put values and content in JSON, tables, or resources: units, skills, buffs, projectiles, buildings, mechanisms, drops, language, levels, economy.
- Keep formulas in code when useful, but put default values in data.
- Config tools should support create, duplicate, delete, search, validation, reference lookup, and quick preview.
- Preserve design semantics in fields such as `TacticsTag`, `Target`, `condition`, `Actions`, `mechanic_timing`, and `spawn_group`.

## Runtime Editors

Treat runtime editors/debug panels as core production tools.

They should edit:

- units
- skills
- buffs
- projectiles
- buildings
- levels
- mechanisms
- global tuning
- localization/text

They should reveal:

- missing fields
- invalid references
- illegal enum values
- value ranges
- source/target references
- simulation reports or traces

## Command / Event Flow

Input should become a command or intent before mutating state:

```text
Input -> Command/Intent -> Validation -> Job/Action/System -> State/Event -> View
```

Command validation should check target existence, reachability, resource cost, phase legality, and actor state. Return failure reasons for HUD/debug display.

Events should describe gameplay facts such as damage, heal, dodge, death, cast, buff add/remove, pickup, phase change, and battle result.

## Combat

Default combat runtime:

- config data plus runtime state
- HP/CD/Buff/target/position/statistics as runtime state
- centralized win/loss/timeout/result rules
- traceable damage and resource changes

Default skill shape:

```text
condition -> target rule -> action list
```

Common actions:

- Damage
- Heal
- AddBuff
- RemoveBuff
- Move
- SpawnProjectile
- SpawnArea
- Summon
- ResourceChange

## Buffs

Buffs should be reusable infrastructure, not private one-off skill code.

Support:

- duration, permanent buffs, count-limited buffs
- max stacks, refresh, independent instances, exclusive groups
- tags, immunity, dispel
- add/mul/override/final modifiers
- triggers on acquire, remove, tick, hit, damage taken, kill, phase start/end, discard, movement
- source tracking: applier, skill, card, unit, faction
- UI priority: icon, stack count, remaining time, hidden minor buffs

## Projectiles And Hazards

Support configuration of:

- spawn source: unit, node layer, ground point, boss part
- movement: straight, homing, lob, wave, boomerang, orbit, area, radial, beam
- hit rule: single target, pierce, bounce, explosion, persistent area, hit limit
- warning layer and lifetime
- payload: damage, buff, summon, area, resource

Hazard warnings must remain visually above ordinary effects.

## AI And Jobs

AI chooses; systems resolve.

Recommended shape:

```text
World Query -> Scoring / Behavior Tree -> Job / Command
```

Use staggered scans for many units. Use simplified offscreen simulation. Use reservations for work targets.

## Phase State Machines

Use explicit phases for any game flow:

- menu, lobby, level select, battle, result, shop
- battle start, draw, select, fight, discard, end
- formation, snap, live play, play result, next down
- spawn, active, warning, resolve, death/result

Centralize enter/exit events, input registration, save restore points, settlement, and rewards. Avoid direct multi-system jumps from UI buttons.

## Saves

Save player-continuable state:

- flow phase
- level/run/floor
- party/roster/backpack/loadout
- level grid completion/locks
- market/shop/reward pools
- resources, unlocks, codex/book
- random seed or replay context

Do not save transient particles, floating text, or animation queues unless implementing a deliberate battle snapshot system.

## Validation

Prefer:

- headless simulation tests
- fixed seed traces
- combat phase logs
- config validators
- first-minute playtest gates
- evidence logs

Gameplay validation should ask:

- Can the player survive the target duration?
- Can they identify death cause?
- Did they notice warnings?
- Did they make a route, build, or strategy choice?
- Can the loop repeat without manual reset?

## UI / UX

- Prototype UI should serve scanning and debugging.
- HUD should continuously show core state: HP, resources, time, phase, objective, ball carrier, frontline, alarm, danger prompts.
- Long text should not be forced into small buttons.
- Cards/units/buildings should use stable sizes and layered fields.
- Battle presentation must not block the main operation area.
- Distinguish selectable, selected, disabled, cooldown, insufficient resource, non-draggable, non-discardable, and non-selectable states.

## Performance

Prefer:

- object pools
- render only current camera window plus margin
- simplified offscreen simulation
- staggered AI scans
- target locks to reduce over-focus
- avoid every-frame global `Changed` storms
- add path caches, reservations, or spatial indexes only when needed

## Asset Pipeline

- Keep stable folders: `resources/art`, `resources/ui`, `resources/characters`, `resources/icons`, `art/source/generated`.
- Keep generation source, metadata, previews, and style notes.
- Build path resolvers and fallback art before deep UI migration.

