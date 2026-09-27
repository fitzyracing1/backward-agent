---
name: backward-agent
description: Build and run AI agents from the end state backward. Start with the finished artifact and success test, then the last act that produces it, then preconditions, then gather, then intake. Use when the user says build an agent backwards, reverse-chain an agent, outcome-first agent, backward design agent, or wants a working agent constructed last-to-first.
metadata:
  type: workflow
  version: "1.0"
---

# Backward Agent

Construct agents last-to-first. Execute them first-to-last. Never invent tools or memory before the success test exists.

## Build order (mandatory)

Write these layers in this exact order. Do not skip. Do not start with prompts or tool lists.

1. **Done picture** — one sentence of the world after success. Name the concrete artifact path.
2. **Terminal test** — a predicate that returns true only when the artifact is good enough. Prefer a file that exists plus a short check (nonempty, JSON parses, command exit 0).
3. **Last act** — the single write, run, or call that would make the test pass if preconditions were already true.
4. **Preconditions** — the smallest facts that last act needs. Each fact must be observable.
5. **Gather** — cheapest observations or tool calls that produce those facts.
6. **Intake** — how a raw user line becomes a done-picture. Default if the line is short.

Only after 1–6 exist, write the run loop and any skill wrapper.

## Run order

```
intake -> done picture -> gather -> check preconditions -> last act -> terminal test
if test fails, treat the failure as a new done-picture one layer back and repeat once
stop after one recurse unless the user asked to keep going
```

## Defaults that remove delay

- Artifact root is `/home/workdir/artifacts/backward-agent/`
- Stack is plain Python 3, no new frameworks
- One agent, one goal, one artifact
- Success bar is "usable file exists and test passes", not elegance
- If the user names no domain, the agent writes a `RESULT.md` that records the goal, layers, and proof of the test

## Implementation

Run the bundled loop:

```bash
python3 /home/workdir/.grok/skills/backward-agent/scripts/backward_agent.py --goal "GOAL TEXT"
```

Or from the artifacts copy after a ship.

When this skill is active, do the work in the sandbox. Write the layers to `artifacts/backward-agent/LAYERS.md`, run the agent, and leave the resulting artifact on disk.

## Anti-patterns

- Starting with a system prompt
- Listing tools before the terminal test
- Multi-agent swarms on the first pass
- Asking which architecture they prefer
- Building a framework instead of finishing one goal
---
