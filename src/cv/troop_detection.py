import torch
import os
from ultralytics import YOLO

torch.backends.mps.allow_tf32 = False

# some default params
params = dict(
    data="datasets/char_detection_dataset/data.yaml",
    epochs=100,
    imgsz=640,
    optimizer="AdamW",
    val=True,
    half=False,
    plots=False,
    lr0=0.001,
    auto_augment=None,
    mosaic=0.0,
    seed=42
)

def set_params():
    print("Which device are you training on?\n1. CPU\n2. GPU\n3. MPS (Apple Silicon Macs only)\n")
    while True:
        choice = input("Select a number: ")
        if choice == "1":
            params["device"] = "cpu"
            params["batch"] = 8
            params["imgsz"] = 640
            params["cache"] = False
            params["workers"] = os.cpu_count() // 2 #use half of the available cores
            break
        elif choice == "2":
            if torch.cuda.is_available():
                # optimizations for CUDA GPU (RTX 3090)
                params["device"] = "cuda"
                params["batch"] = 64
                params["imgsz"] = 1024
                params["cache"] = True
                params["workers"] = os.cpu_count() #use all available cores
                break
            else:
                print("CUDA is not available on your device. Please choose another device.")
        elif choice == "3":
            if torch.backends.mps.is_available() and torch.backends.mps.is_built():
                # optimizations for MPS (Apple Silicon)
                torch.mps.empty_cache()
                params["device"] = "mps"
                params["batch"] = 8
                params["imgsz"] = 640
                params["cache"] = False
                # params["workers"] = 0
                params["patience"] = 50  # add early stopping
                break
            else:
                print("MPS is not available on your device. Please choose another device.")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    while True:
        resume = input("resume training from a previous checkpoint? (y/n): ")
        if resume.lower().strip() == "y":
            params["resume"] = True
            break
        elif resume.lower().strip() == "n":
            params["resume"] = False
            break
        else:
            print("Invalid choice. Please enter y or n.")

set_params()

if not os.path.exists(params["data"]):
    print(f"Error: Data file not found at {params['data']}")
else:
    try:
        model = YOLO("../../runs/detect/train3/weights/last.pt")
        results = model.train(**params)
    except Exception as e:
        print(f"An error occurred during training: {e}")