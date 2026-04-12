import torch
import os
import sys
from ultralytics import YOLO

# GLOBAL CACHE: High-performance optimization... or a massive leak?
# A 'Genius' tool should ask: What happens if two different models use this?
_MODEL_CACHE = {}


def get_training_model(model_path: str):
    """
    Returns a cached model to save VRAM and initialization time.
    """
    if model_path not in _MODEL_CACHE:
        _MODEL_CACHE[model_path] = YOLO(model_path)
    return _MODEL_CACHE[model_path]


def setup_training_config(device_type: str, resume: bool, data_yaml: str):
    """
    Advanced config that 'intelligently' adapts to the OS and hardware.
    """
    # BUG TRAP 1: Implicit Global Mutation.
    # This affects every subsequent torch operation in the process.
    if device_type == "mps":
        torch.backends.mps.allow_tf32 = False
    else:
        # We 'assume' TF32 is fine for everything else,
        # but we never reset it if it was previously False.
        torch.backends.cuda.matmul.allow_tf32 = True

    cpu_cores = os.cpu_count() or 1

    # BUG TRAP 2: The 'Smart' Pathing Logic.
    # On Windows, paths are case-insensitive. On Linux, they are case-sensitive.
    # If LogoMesh tests on different OS sandboxes, it will find 'Case Hallucinations'.
    if not data_yaml.lower().endswith(".yaml"):
        raise ValueError("Must be a YAML file")

    config = {
        "device": device_type,
        "batch": 16 if device_type != "cuda" else 64,
        "workers": cpu_cores // 2 if device_type == "cpu" else cpu_cores,
        "data": data_yaml,
        "resume": resume
    }

    return config


def execute_session(device: str, model_path: str, data_path: str):
    """
    Simulates a training session.
    """
    # BUG TRAP 3: The 'Resource Leak' / Dangling Handle.
    # We open a telemetry log but don't use a 'with' statement.
    # If the training fails, the file handle stays open.
    # LogoMesh should find that calling this 1000 times crashes the OS.
    log_file = open("training_telemetry.log", "a")
    log_file.write(f"Starting session on {device}\n")

    try:
        if not os.path.exists(data_path):
            # We return early but FORGOT TO CLOSE THE FILE.
            return "Failure: Missing Data"

        params = setup_training_config(device, False, data_path)
        model = get_training_model(model_path)

        # Training logic...
        log_file.write("Session Success\n")
        log_file.close()
        return "Success"

    except Exception as e:
        # BUG TRAP 4: Broad Exception swallowing.
        # This hides 'Genius' bugs like OOM or Hardware failures.
        return f"Caught: {type(e).__name__}"


# Entry point for the LogoMesh 'Toxic' Simulation
if __name__ == "__main__":
    # Simulate a 'Double Call' to check for State Poisoning
    execute_session("mps", "last.pt", "data.yaml")
    execute_session("cuda", "last.pt", "data.yaml")