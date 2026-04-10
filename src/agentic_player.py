import argparse
from pathlib import Path
from typing import List

import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

from agent.controller import DryRunController
from agent.planner import RuleBasedPlanner
from agent.state_estimator import StateEstimator
from agent.types import Detection


def find_game_window(sct, template_path: Path):
    offset_x, offset_y = (140, 636)

    battle_button_template = cv2.imread(str(template_path), 0)
    if battle_button_template is None:
        print(f"Error: Could not load template image at {template_path}")
        return None

    main_monitor = sct.monitors[1]
    fs_screenshot = sct.grab(main_monitor)
    fs_img = np.array(fs_screenshot)
    fs_gray = cv2.cvtColor(fs_img, cv2.COLOR_BGRA2GRAY)

    res = cv2.matchTemplate(fs_gray, battle_button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val <= 0.8:
        return None

    top_left_x = max_loc[0] - offset_x
    top_left_y = max_loc[1] - offset_y
    return {
        "top": top_left_y,
        "left": top_left_x,
        "width": 376,
        "height": 830,
    }


def extract_detections(result) -> List[Detection]:
    detections: List[Detection] = []
    names = result.names

    for box in result.boxes:
        cls_id = int(box.cls.item())
        label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else str(cls_id)
        conf = float(box.conf.item())
        x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
        detections.append(Detection(label=label, confidence=conf, bbox=(x1, y1, x2, y2)))

    return detections


def parse_args():
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Run an agentic Clash Royale inference loop.")
    parser.add_argument(
        "--weights",
        default=str(script_dir / "cv" / "runs" / "detect" / "train2" / "weights" / "last.pt"),
        help="Path to YOLO weights file.",
    )
    parser.add_argument(
        "--template",
        default=str(script_dir / "templates" / "battle_button.png"),
        help="Path to battle button template image.",
    )
    parser.add_argument("--show", action="store_true", help="Show annotated inference window.")
    parser.add_argument("--max-frames", type=int, default=0, help="Stop after N frames (0 = infinite).")
    return parser.parse_args()


def main():
    args = parse_args()
    weights_path = Path(args.weights).expanduser().resolve()
    template_path = Path(args.template).expanduser().resolve()

    if not weights_path.is_file():
        raise FileNotFoundError(f"Weights not found: {weights_path}")
    if not template_path.is_file():
        raise FileNotFoundError(f"Template not found: {template_path}")

    model = YOLO(str(weights_path))
    estimator = StateEstimator()
    planner = RuleBasedPlanner()
    controller = DryRunController()

    frame_count = 0
    last_action_text = "action: none"

    with mss() as sct:
        game_window = find_game_window(sct, template_path)
        if not game_window:
            print("Could not find game window. Exiting...")
            return

        while True:
            screenshot = sct.grab(game_window)
            frame = np.array(screenshot)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            result = model.predict(frame_bgr, verbose=False)[0]
            detections = extract_detections(result)
            state = estimator.estimate(detections, arena_width=frame_bgr.shape[1], arena_height=frame_bgr.shape[0])
            action = planner.decide(state)

            if action is not None:
                controller.execute(action)
                last_action_text = f"action: {action.kind} ({action.lane})"

            if args.show:
                annotated = result.plot()
                cv2.putText(
                    annotated,
                    f"pressure={state.pressure_score:.2f} enemies={state.enemy_count} {last_action_text}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.imshow("Agentic Clash Royale", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_count += 1
            if args.max_frames > 0 and frame_count >= args.max_frames:
                break

    if args.show:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

