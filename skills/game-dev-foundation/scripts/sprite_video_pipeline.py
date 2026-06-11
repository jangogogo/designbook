#!/usr/bin/env python3
"""Scaffold and validate sprite-to-video-to-frames animation tasks."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import textwrap


NODES = [
    ("00_contract", "Asset Contract"),
    ("01_static_sprite", "Approved Static Sprite"),
    ("02_keyframes", "Keyframe Plan"),
    ("03_video_generation", "Video Generation"),
    ("04_raw_frames", "Raw Frame Extraction"),
    ("05_frame_selection", "Frame Selection"),
    ("06_alpha_cleanup", "Background Removal And Alpha Cleanup"),
    ("07_normalize", "Canvas Scale And Pivot Normalization"),
    ("08_repair", "Identity And Gameplay Repair"),
    ("09_timing", "Gameplay Timing"),
    ("10_export", "Export Package"),
    ("11_engine_test", "Engine Test"),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")


def init_task(args: argparse.Namespace) -> int:
    root = Path(args.output).resolve()
    if root.exists() and any(root.iterdir()) and not args.force:
        print(f"Refusing to overwrite non-empty directory: {root}", file=sys.stderr)
        print("Use --force to add missing scaffold files.", file=sys.stderr)
        return 2

    root.mkdir(parents=True, exist_ok=True)
    for dirname, title in NODES:
        (root / dirname).mkdir(parents=True, exist_ok=True)
        readme = root / dirname / "README.md"
        if not readme.exists() or args.force:
            write_text(readme, f"# {title}\n\nStatus: pending\n")

    write_text(
        root / "metadata.md",
        f"""
        # Sprite Animation Task Metadata

        asset_id: {args.asset_id}
        animation: {args.animation}
        model: {args.model}
        control_mode: {args.control_mode}
        background_strategy: {args.background}
        canvas_size: {args.size}
        target_fps: {args.fps}
        target_frame_count: {args.frames}
        engine: {args.engine}
        status: scaffolded

        ## Source Tracking

        source_sprite:
        start_frame:
        end_frame:
        source_video:
        extraction_fps:
        selected_frame_indices:
        prompt:
        negative_prompt:
        seed:
        license_notes:
        """,
    )

    write_text(
        root / "00_contract" / "asset_contract.md",
        f"""
        # Asset Contract

        asset_id: {args.asset_id}
        animation: {args.animation}
        gameplay purpose:
        view:
        canvas size: {args.size}
        character occupied pixels:
        target frame count: {args.frames}
        target FPS: {args.fps}
        pivot:
        collision relation:
        hit frame:
        loop required:
        model candidates: Kling, Runway, Luma
        chosen model: {args.model}
        control mode: {args.control_mode}
        background strategy: {args.background}
        engine import target: {args.engine}
        acceptance scene:

        ## Acceptance

        - [ ] gameplay purpose is clear
        - [ ] camera/view is fixed
        - [ ] frame count and FPS are declared
        - [ ] pivot and collision relationship are declared
        - [ ] model/control choice is approved by user
        """,
    )

    write_text(
        root / "03_video_generation" / "prompt.md",
        f"""
        # Video Generation Prompt

        Model: {args.model}
        Control mode: {args.control_mode}
        Background: {args.background}

        ```text
        Use the provided 2D game sprite as the exact character identity.
        Generate a short locked-camera animation of {args.animation}.
        Keep the same outfit, colors, weapon, silhouette, and proportions.
        No camera movement, no zoom, no scene cut, no new objects.
        Plain {args.background} background.
        Motion should be readable as a small game sprite.
        ```

        ## Acceptance

        - [ ] motion matches one intended action
        - [ ] camera is locked
        - [ ] identity remains usable for most of the clip
        - [ ] no major crop
        - [ ] background can be removed or keyed
        """,
    )

    write_text(
        root / "checkpoints.md",
        """
        # Checkpoints

        Use this report format at every node:

        ```text
        Node:
        Input:
        Decision needed:
        Chosen option:
        Acceptance result:
        Blocked by:
        Next action:
        ```

        Required user confirmations:

        - [ ] model/control mode before video generation
        - [ ] source video approval before extraction
        - [ ] selected frame set before cleanup
        - [ ] repaired preview before engine import
        - [ ] engine screenshot before atlas/bulk production
        """,
    )

    print(f"Created sprite animation task: {root}")
    return 0


def validate_task(args: argparse.Namespace) -> int:
    root = Path(args.task).resolve()
    required = [
        root / "metadata.md",
        root / "checkpoints.md",
        root / "00_contract" / "asset_contract.md",
        root / "03_video_generation" / "prompt.md",
    ]
    required.extend(root / dirname / "README.md" for dirname, _ in NODES)

    missing = [path for path in required if not path.exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    metadata = (root / "metadata.md").read_text(encoding="utf-8")
    checkpoints = (root / "checkpoints.md").read_text(encoding="utf-8")
    needed_terms = [
        "model:",
        "control_mode:",
        "background_strategy:",
        "target_fps:",
        "target_frame_count:",
    ]
    missing_terms = [term for term in needed_terms if term not in metadata]
    if "source video approval before extraction" not in checkpoints:
        missing_terms.append("source video approval checkpoint")

    if missing_terms:
        print("Missing required metadata/checkpoint terms:")
        for term in missing_terms:
            print(f"- {term}")
        return 1

    print(f"Validated sprite animation task scaffold: {root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold or validate a sprite-to-video-to-frames animation task."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a new animation task scaffold.")
    init.add_argument("--output", required=True, help="Task output directory.")
    init.add_argument("--asset-id", required=True, help="Asset id, e.g. flagboy.")
    init.add_argument("--animation", required=True, help="Animation name, e.g. run_right.")
    init.add_argument("--model", default="Kling", help="Chosen model.")
    init.add_argument("--control-mode", default="start-end", help="single-image/start-end/multi-keyframe/reference-video.")
    init.add_argument("--background", default="green-screen", help="Background strategy.")
    init.add_argument("--size", default="128x128", help="Final canvas size.")
    init.add_argument("--fps", default="10", help="Target animation FPS.")
    init.add_argument("--frames", default="8", help="Target final frame count.")
    init.add_argument("--engine", default="Godot", help="Target engine.")
    init.add_argument("--force", action="store_true", help="Overwrite scaffold files.")
    init.set_defaults(func=init_task)

    validate = sub.add_parser("validate", help="Validate an animation task scaffold.")
    validate.add_argument("--task", required=True, help="Task directory.")
    validate.set_defaults(func=validate_task)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
