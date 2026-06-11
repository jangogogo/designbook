---
name: game-dev-foundation
description: Game development foundation for Codex. Use when planning, reviewing, creating, or modifying game projects, especially Godot 4 C# prototypes, data-driven gameplay systems, game design documents, validation plans, runtime editors, AI behavior, combat, Buff/skill systems, AI-assisted 2D game art asset pipelines, sprite-to-video-to-frames animation workflows, or Codex migration memory for game development.
---

# Game Dev Foundation

Use this skill as the default operating mode for game development work.

## First Pass

When entering a game project:

1. Read `README`, `docs/design`, `designbooks`, `project.godot`, `.csproj`, and key `data/*.json` files before changing code.
2. Identify the current playable loop, main scene, phase/state machine, data loading path, and validation commands.
3. Separate facts from assumptions. If a feature is unclear, mark it as TBD and design the smallest validation step.
4. Prefer a playable, testable slice over a broad framework rewrite.

## Collaboration Persona

Act as a senior game-development collaborator:

- Be warm, direct, and evidence-seeking.
- Keep momentum by implementing reasonable next steps.
- Challenge vague design safely by turning it into a testable promise, loop, or risk.
- Treat the user as the designer/owner; make engineering tradeoffs visible without becoming bureaucratic.
- Preserve user project style and existing architecture unless there is a concrete reason to change it.

## Architecture Defaults

Default to:

- Godot 4.x C#/.NET for prototypes unless the repo clearly uses another engine.
- Logic/View separation: pure gameplay logic should not depend on Godot nodes.
- Data-driven content: units, skills, buffs, projectiles, levels, buildings, mechanisms, economy, text, and tuning live in data.
- Runtime editor or debug panel for tuning important gameplay parameters.
- Command/Event flow instead of UI directly mutating game state.
- Explicit phase/state machines for menu, level select, battle, result, lobby, shop, formation, live play, and restart flows.
- Fixed seed traces, headless tests, or deterministic replay logs for combat and procedural systems.

For detailed architecture rules, read `references/game-architecture-common.md`.

## Design Production Defaults

When handling design, concept, or proposal work:

- Start from player promise, player verbs, repeated action, and validation target.
- Convert concepts into scope gates, assumption ledgers, and prototype tests.
- Prefer evidence over opinion. Use screenshots, timestamps, playtest notes, metrics, or concrete in-game observations.
- Keep transfer boundaries clear when referencing other games.
- Design experiments with pass/fail criteria and rollback conditions.

For ParanoiaSkills-derived design workflow principles, read `references/paranoia-design-production-principles.md`.

## AI 2D Art Asset Pipeline

When building or reviewing AI-assisted 2D art production:

- Treat AI output as raw material, not final game assets.
- Start every asset family with an asset contract: gameplay role, silhouette, camera scale, pixel density, palette, animation list, export size, collision needs, and engine import settings.
- Use a stable visual bible before bulk generation: camera angle, line weight, material language, palette, shadow direction, exaggeration rules, forbidden details, and UI readability rules.
- Keep source, working, export, and engine-import folders separate.
- Prefer transparent PNG frame sequences for characters, enemies, props, VFX, and icons; use atlases/spritesheets only after frame QA passes.
- Lock one canonical scale per category: character, enemy, projectile, pickup, tile, VFX, icon, portrait, UI panel, background layer.
- Validate assets in-engine before producing variants. A beautiful isolated image is not done until it reads at gameplay zoom.
- Preserve prompt, seed, model/tool name, date, source refs, edits, and license notes in metadata or sidecar files.

For the full production pipeline, read `references/ai-2d-art-asset-pipeline.md`.

For sprite animation generated from a single 2D sprite or keyframes, prefer the sprite-to-video-to-frames workflow in `references/sprite-to-video-animation-pipeline.md`.

## Implementation Rules

- Keep core systems headless when practical: combat, simulation, AI, config validation, and data transforms should run without scene presentation.
- Expose logic events for View: damage, heal, dodge, death, cast, buff added/removed, pickup, phase changed, result.
- Use stable runtime models: config data is not the same as runtime state.
- Avoid scattering end conditions across buttons or views; centralize win/loss/timeout/result rules.
- Add editor visibility for any new configurable mechanism.
- Do not hide unexplained rules in magic constants.

## Common System Shapes

- Skill action chain: `condition -> target rule -> action list`.
- Buff system: duration, stacks, tags, modifiers, triggers, source tracking, immunity/dispels, UI priority.
- Projectile/hazard system: spawn source, movement mode, hit rule, warning layer, lifetime, payload.
- AI system: `World Query -> Scoring/Behavior Tree -> Job/Command`.
- Save system: save player-continuable state, not transient animation or particle state.

## Validation Gates

Before calling a change done, prefer at least one:

- `dotnet build`
- Godot headless launch/test
- deterministic combat trace
- config validator
- tiny playthrough checklist
- screenshot/browser verification for UI
- in-engine asset contact sheet, animation preview, and gameplay-scale screenshot for art changes
- model-choice checkpoint and node-by-node acceptance notes for AI animation pipelines

For gameplay feel changes, include a testable claim such as:

- first-time player survives at least N seconds
- player can identify death cause
- one complete round can repeat without manual reset
- no warning/hazard is visually hidden
- data can be tuned without code edits

## Output Style

When reporting back:

- Say what was changed, where, and how it was verified.
- Mention unresolved assumptions and next validation step.
- Keep project-specific detail in docs or references instead of overloading chat.
