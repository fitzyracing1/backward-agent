# Backward Agent

"Build AI agents last-to-first. Run them first-to-last." A standard-library Python script builds an agent's layers in reverse (done picture → terminal test → last act → preconditions → gather → intake) and then runs them forward.

## Getting started

```bash
python3 scripts/backward_agent.py --goal "your goal"   # default goal: "build an ai agent backwards"
```

It prints a JSON result and exits with 0 when `ok` is true, otherwise 1.

## Files

| Path | Role |
|---|---|
| `scripts/backward_agent.py` | builder and runner |
| `SKILL.md` | skill description |
| `proof/RESULT.md`, `proof/LAYERS.md`, `proof/LAYERS.json` | recorded run |
| `index.html`, `.github/workflows/pages.yml` | site (https://fitzyracing1.github.io/backward-agent/) |

The repo has no tests and no LICENSE file. CI is only the Pages deploy: a run is **lit** when it succeeds and **dark** otherwise.

Copyright (c) 2026 Joshua Almeida
