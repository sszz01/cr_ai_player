# Agentic Clash Royale Baseline

This package adds a minimal **agent loop** on top of your detector:

1. Convert YOLO boxes into lightweight detections
2. Estimate tactical pressure by lane
3. Decide an action via a baseline rule planner
4. Execute action through a dry-run controller (print only)

## Files

- `types.py` - shared dataclasses
- `state_estimator.py` - frame -> game state
- `planner.py` - policy logic
- `controller.py` - action executor abstraction
- `smoke_test.py` - tiny deterministic test harness

## Run smoke test

```bash
cd /Users/ovoievodin/PycharmProjects/cr_ai_player
PYTHONPATH=src python -m agent.smoke_test
```

## Next upgrades

- Add tracked unit identities across frames
- Infer ally vs enemy side using arena geometry
- Replace dry-run controller with safe click controller
- Add replay logging for offline policy training


