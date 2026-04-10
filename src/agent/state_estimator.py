from typing import Iterable

from .types import Detection, GameState


class StateEstimator:
    """Builds a compact tactical state from per-frame detections."""

    def estimate(self, detections: Iterable[Detection], arena_width: int, arena_height: int) -> GameState:
        left_lane_threat = 0.0
        right_lane_threat = 0.0
        enemy_count = 0

        for det in detections:
            x1, y1, x2, y2 = det.bbox
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            # Units lower on the screen are treated as more urgent threats.
            urgency = max(0.0, min(1.0, cy / max(1.0, float(arena_height))))
            threat = max(0.05, det.confidence) * (0.4 + urgency)

            if cx < arena_width / 2.0:
                left_lane_threat += threat
            else:
                right_lane_threat += threat

            enemy_count += 1

        pressure_score = left_lane_threat + right_lane_threat

        return GameState(
            enemy_count=enemy_count,
            pressure_score=pressure_score,
            left_lane_threat=left_lane_threat,
            right_lane_threat=right_lane_threat,
        )

