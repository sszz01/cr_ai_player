import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from roboflow import Roboflow

DEFAULT_GENERATE_SETTINGS = {
    "preprocessing": {
        "auto-orient": True,
        "resize": {"width": 640, "height": 640, "format": "Stretch to"},
    },
    "augmentation": {},
}


def parse_version_number(version_obj):
    version_id = str(version_obj.get("id", ""))
    try:
        return int(version_id.rstrip("/").split("/")[-1])
    except (ValueError, IndexError):
        return None


def get_version_map(project):
    version_info = project.get_version_information()
    version_map = {}
    for version_obj in version_info:
        number = parse_version_number(version_obj)
        if number is not None:
            version_map[number] = version_obj
    return version_map


def resolve_target_version(project, requested_version, create_new):
    version_map = get_version_map(project)

    if create_new:
        new_version = project.generate_version(DEFAULT_GENERATE_SETTINGS)
        print(f"Generated new dataset version: {new_version}")
        return new_version, get_version_map(project).get(new_version, {})

    if requested_version is None:
        if not version_map:
            raise RuntimeError("No dataset versions exist yet. Use --create-version first.")
        requested_version = max(version_map)

    if requested_version not in version_map:
        available = ", ".join(str(v) for v in sorted(version_map)) or "none"
        raise RuntimeError(f"Version {requested_version} does not exist. Available versions: {available}")

    return requested_version, version_map[requested_version]


def parse_args():
    script_dir = Path(__file__).resolve().parent
    default_model_dir = script_dir / "runs" / "detect" / "train2"

    parser = argparse.ArgumentParser(description="Upload local YOLO weights to a Roboflow dataset version.")
    parser.add_argument("--project", default=os.getenv("ROBOFLOW_PROJECT", "clashroyalechardetector-u5yux"))
    parser.add_argument("--version", type=int, default=None, help="Dataset version to upload to.")
    parser.add_argument(
        "--create-version",
        action="store_true",
        help="Create a fresh dataset version before uploading weights.",
    )
    parser.add_argument("--model-type", default="yolo11s", help="Roboflow model type identifier.")
    parser.add_argument(
        "--model-dir",
        default=str(default_model_dir),
        help="Directory containing exported model files.",
    )
    parser.add_argument(
        "--weights-file",
        default="weights/best.pt",
        help="Relative path to weights file inside --model-dir.",
    )
    parser.add_argument(
        "--allow-trained-version",
        action="store_true",
        help="Attempt upload even when selected version already has a Roboflow-trained model.",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise ValueError("ROBOFLOW_API_KEY is missing. Add it to your .env file.")

    model_dir = Path(args.model_dir).expanduser().resolve()
    weights_path = model_dir / args.weights_file
    if not model_dir.is_dir():
        raise FileNotFoundError(f"Model directory does not exist: {model_dir}")
    if not weights_path.is_file():
        raise FileNotFoundError(f"Weights file does not exist: {weights_path}")

    rf = Roboflow(api_key=api_key)
    project = rf.workspace().project(args.project)

    version_number, version_obj = resolve_target_version(project, args.version, args.create_version)

    if "model" in version_obj and not args.allow_trained_version:
        raise RuntimeError(
            f"Version {version_number} already has a Roboflow model. "
            "Use --create-version to generate a new one or --allow-trained-version to try anyway."
        )

    version = project.version(version_number)
    print(
        f"Uploading '{args.weights_file}' from '{model_dir}' "
        f"to project '{args.project}', version {version_number}..."
    )
    version.deploy(args.model_type, str(model_dir), filename=args.weights_file)


if __name__ == "__main__":
    main()
