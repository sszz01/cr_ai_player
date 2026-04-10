from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2


@dataclass(frozen=True)
class GameState:
    enemy_count: int
    pressure_score: float
    left_lane_threat: float
    right_lane_threat: float


@dataclass(frozen=True)
class AgentAction:
    kind: str
    lane: str
    reason: str

