import time
from typing import Optional

from .types import AgentAction, GameState


class RuleBasedPlanner:
    """Simple baseline planner with cooldown to avoid action spam."""

    def __init__(self, action_cooldown_s: float = 1.2) -> None:
        self.action_cooldown_s = action_cooldown_s
        self._last_action_ts = 0.0

    def decide(self, state: GameState) -> Optional[AgentAction]:
        now = time.time()
        if now - self._last_action_ts < self.action_cooldown_s:
            return None

        lane = "left" if state.left_lane_threat >= state.right_lane_threat else "right"

        if state.pressure_score >= 3.0:
            action = AgentAction(
                kind="defend",
                lane=lane,
                reason=f"high pressure ({state.pressure_score:.2f})",
            )
        elif state.pressure_score >= 1.2:
            action = AgentAction(
                kind="kite",
                lane=lane,
                reason=f"medium pressure ({state.pressure_score:.2f})",
            )
        elif state.enemy_count == 0:
            action = AgentAction(
                kind="cycle",
                lane="center",
                reason="no visible enemy units",
            )
        else:
            return None

        self._last_action_ts = now
        return action

