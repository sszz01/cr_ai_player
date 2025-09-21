import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        videos = os.listdir(video_path)
    except FileNotFoundError:
        print(f"Error: The directory '{video_path}' does not exist.")
        return

    for video_filename in videos:
        full_video_path = os.path.join(video_path, video_filename)
        video_name_without_ext = os.path.splitext(video_filename)[0]
        video_frame_folder = os.path.join(output_folder, video_name_without_ext)
        if not os.path.exists(video_frame_folder):
            os.makedirs(video_frame_folder)
        else:
            print(f"The folder {video_frame_folder} already exists. Skipping...")
            continue

        cap = cv2.VideoCapture(full_video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {full_video_path}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            print(f"Warning: Could not get FPS for {video_filename}. Skipping.")
            cap.release()
            continue

        frame_interval = int(fps / frame_rate)
        if frame_interval == 0:
            frame_interval = 1

        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_filename = os.path.join(video_frame_folder, f"frame_{saved_count:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"Extracted {saved_count} frames from '{video_filename}' to '{video_frame_folder}'")

if __name__ == "__main__":
    vpath = "games_footage"
    out_dir = "extracted_frames"
    extract_frames(vpath, out_dir, frame_rate=1)
