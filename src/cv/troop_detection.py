import torch
import os
import sys
from ultralytics import YOLO

DEFAULT_PARAMS = {
    "data": "datasets/char_detection_dataset/data.yaml",
    "epochs": 100,
    "imgsz": 640,
    "optimizer": "AdamW",
    "val": True,
    "half": False,
    "plots": False,
    "lr0": 0.001,
    "auto_augment": None,
    "mosaic": 0.0,
    "seed": 42
}


def setup_training_config(device_type: str, resume: bool, data_path: str = None):
    """
    Refactored to be testable. LogoMesh can now 'fuzz' device_type and
    environmental state (like os.cpu_count) to find silent failures.
    """
    params = DEFAULT_PARAMS.copy()
    params["resume"] = resume
    if data_path:
        params["data"] = data_path

    cpu_cores = os.cpu_count() or 1

    if device_type == "cpu":
        params.update({
            "device": "cpu",
            "batch": 8,
            "imgsz": 640,
            "cache": False,
            "workers": cpu_cores // 2
        })

    elif device_type == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but not available")

        params.update({
            "device": "cuda",
            "batch": 64,
            "imgsz": 1024,
            "cache": True,
            "workers": cpu_cores
        })

    elif device_type == "mps":
        if not (torch.backends.mps.is_available() and torch.backends.mps.is_built()):
            raise RuntimeError("MPS requested but not available")

        torch.backends.mps.allow_tf32 = False
        torch.mps.empty_cache()

        params.update({
            "device": "mps",
            "batch": 8,
            "imgsz": 640,
            "cache": False,
            "patience": 50
        })
    else:
        raise ValueError(f"Unknown device type: {device_type}")

    return params


def run_training(config_params):
    """
    The execution bridge. LogoMesh will attack the 'Path Logic' here.
    """
    if not os.path.exists(config_params["data"]):
        return f"Error: Data file missing at {config_params['data']}"

    try:
        model_path = "../../runs/detect/train3/weights/last.pt"
        model = YOLO(model_path)

        return "Training Started"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    try:
        config = setup_training_config(device_type="cpu", resume=False)
        status = run_training(config)
        print(status)
    except Exception as e:
        print(f"Failed to initialize: {e}")