from agent.planner import RuleBasedPlanner
from agent.types import GameState


def run_smoke_test() -> None:
    planner = RuleBasedPlanner(action_cooldown_s=0.0)

    cases = [
        GameState(enemy_count=0, pressure_score=0.0, left_lane_threat=0.0, right_lane_threat=0.0),
        GameState(enemy_count=2, pressure_score=1.5, left_lane_threat=1.1, right_lane_threat=0.4),
        GameState(enemy_count=4, pressure_score=3.4, left_lane_threat=0.9, right_lane_threat=2.5),
    ]

    for idx, state in enumerate(cases, start=1):
        action = planner.decide(state)
        print(f"case_{idx}: {action}")


if __name__ == "__main__":
    run_smoke_test()

