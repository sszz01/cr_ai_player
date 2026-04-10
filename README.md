# cr_ai_player

Computer vision and agent-loop experiments for Clash Royale.

## New agentic runner

- `src/agentic_player.py` - live detection + state estimation + rule planner + dry-run action controller
- `src/agent/` - modular planning components

## Quick start

```bash
cd /Users/ovoievodin/PycharmProjects/cr_ai_player
source .venv/bin/activate
PYTHONPATH=src python -m agent.smoke_test
```

```bash
cd /Users/ovoievodin/PycharmProjects/cr_ai_player
source .venv/bin/activate
PYTHONPATH=src python src/agentic_player.py --show --max-frames 300
```

