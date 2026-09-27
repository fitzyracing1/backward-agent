#!/usr/bin/env python3
"""Backward Agent — construct last-to-first, execute first-to-last.

Presumed need: user asked to build an AI agent backwards.
Evidence: single-line request with no domain, so default goal is a proven RESULT.md.
"""

from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/home/workdir/artifacts/backward-agent")
ROOT.mkdir(parents=True, exist_ok=True)


@dataclass
class Layers:
    done_picture: str
    artifact_path: str
    terminal_test: str
    last_act: str
    preconditions: list[str]
    gather: list[str]
    intake: str
    built_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def default_layers(goal: str) -> Layers:
    artifact = ROOT / "RESULT.md"
    return Layers(
        done_picture=(
            f"A readable RESULT.md exists at {artifact} proving the goal "
            f"{goal!r} was reverse-built and the terminal test passed."
        ),
        artifact_path=str(artifact),
        terminal_test=(
            "file exists AND size > 80 bytes AND contains headings "
            "DONE PICTURE, LAST ACT, TERMINAL TEST, PROOF"
        ),
        last_act="write RESULT.md from gathered facts plus layer record",
        preconditions=[
            "goal text is nonempty",
            "layers object is complete",
            "output directory exists and is writable",
        ],
        gather=[
            "read --goal argument",
            "confirm ROOT.mkdir succeeded",
            "stamp UTC time",
        ],
        intake="raw line -> one-sentence goal; if empty use 'prove backward construction'",
    )


def gather(goal: str, layers: Layers) -> dict:
    facts = {
        "goal": goal.strip() or "prove backward construction",
        "root_exists": ROOT.exists(),
        "root_writable": True,
        "now": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "layers_complete": all(
            [
                layers.done_picture,
                layers.artifact_path,
                layers.terminal_test,
                layers.last_act,
                layers.preconditions,
                layers.gather,
                layers.intake,
            ]
        ),
    }
    try:
        probe = ROOT / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
    except OSError:
        facts["root_writable"] = False
    return facts


def preconditions_ok(facts: dict) -> tuple[bool, list[str]]:
    missing = []
    if not facts["goal"]:
        missing.append("goal text is nonempty")
    if not facts["layers_complete"]:
        missing.append("layers object is complete")
    if not facts["root_exists"] or not facts["root_writable"]:
        missing.append("output directory exists and is writable")
    return (len(missing) == 0, missing)


def last_act(facts: dict, layers: Layers) -> Path:
    path = Path(layers.artifact_path)
    body = textwrap.dedent(
        f"""\
        # Backward Agent Result

        Built last-to-first. Ran first-to-last.

        ## DONE PICTURE
        {layers.done_picture}

        ## INTAKE
        {layers.intake}

        ## GOAL
        {facts["goal"]}

        ## GATHER
        {json.dumps(facts, indent=2)}

        ## PRECONDITIONS
        {chr(10).join("- " + p for p in layers.preconditions)}

        ## LAST ACT
        {layers.last_act}

        ## TERMINAL TEST
        {layers.terminal_test}

        ## PROOF
        - written_at: {facts["now"]}
        - path: {path}
        - method: backward layers 1-6 then one run loop
        """
    )
    path.write_text(body, encoding="utf-8")
    (ROOT / "LAYERS.json").write_text(
        json.dumps(asdict(layers), indent=2), encoding="utf-8"
    )
    (ROOT / "LAYERS.md").write_text(
        textwrap.dedent(
            f"""\
            # Layers (written in build order)

            1. Done picture — {layers.done_picture}
            2. Terminal test — {layers.terminal_test}
            3. Last act — {layers.last_act}
            4. Preconditions
            {chr(10).join("   - " + p for p in layers.preconditions)}
            5. Gather
            {chr(10).join("   - " + g for g in layers.gather)}
            6. Intake — {layers.intake}

            Artifact: `{layers.artifact_path}`
            Built at: {layers.built_at}
            """
        ),
        encoding="utf-8",
    )
    return path


def terminal_test(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "file missing"
    text = path.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) <= 80:
        return False, "file too small"
    needed = ("DONE PICTURE", "LAST ACT", "TERMINAL TEST", "PROOF")
    missing = [h for h in needed if h not in text]
    if missing:
        return False, "missing headings: " + ", ".join(missing)
    return True, "pass"


def run(goal: str) -> dict:
    layers = default_layers(goal)
    facts = gather(goal, layers)
    ok, missing = preconditions_ok(facts)
    if not ok:
        return {
            "ok": False,
            "stage": "preconditions",
            "missing": missing,
            "facts": facts,
        }
    path = last_act(facts, layers)
    passed, why = terminal_test(path)
    return {
        "ok": passed,
        "stage": "terminal_test",
        "why": why,
        "artifact": str(path),
        "layers": str(ROOT / "LAYERS.md"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Backward-built AI agent")
    parser.add_argument(
        "--goal",
        default="build an ai agent backwards",
        help="raw intake line",
    )
    args = parser.parse_args()
    result = run(args.goal)
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
