import os
from dotenv import load_dotenv
load_dotenv()
from roboflow import Roboflow

api_key = os.getenv("ROBOFLOW_API_KEY")
if api_key is None:
    raise ValueError("ROBOFLOW_API_KEY environment variable not set. Please set it in your .env file.")

rf = Roboflow(api_key=api_key)
project = rf.workspace().project("clashroyalechardetector-u5yux")

#can specify weights_filename, default is "weights/best.pt"
version = project.version(4)

#example1 - directory path is "training1/model1.pt" for yolov8 model
version.deploy("yolo11s", "runs/detect/train2")
