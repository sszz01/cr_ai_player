import os
import re


def natural_sort_key(s):
    """
    A key for natural sorting. E.g. 'gameplay2' comes before 'gameplay10'.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def rename_frames_sequentially(root_folder):
    """
    Renames all frames in subdirectories of root_folder to be sequentially numbered.
    """
    print(f"Starting frame renaming in '{root_folder}'...")
    global_frame_counter = 0

    try:
        # Get subdirectories and sort them naturally
        subdirs = [d for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]
        subdirs.sort(key=natural_sort_key)
    except FileNotFoundError:
        print(f"Error: The directory '{root_folder}' does not exist.")
        return

    for subdir_name in subdirs:
        subdir_path = os.path.join(root_folder, subdir_name)

        # Get frame files and sort them
        try:
            files = [f for f in os.listdir(subdir_path) if f.lower().endswith('.jpg')]
            files.sort()
        except FileNotFoundError:
            print(f"Could not access directory '{subdir_path}'. Skipping.")
            continue

        print(f"Processing '{subdir_name}'...")

        for filename in files:
            old_filepath = os.path.join(subdir_path, filename)

            # The new filename is based on the global counter
            new_filename = f"frame_{global_frame_counter:05d}.jpg"
            new_filepath = os.path.join(subdir_path, new_filename)

            # Rename the file
            try:
                os.rename(old_filepath, new_filepath)
            except OSError as e:
                print(f"Error renaming '{old_filepath}' to '{new_filepath}': {e}")

            global_frame_counter += 1

    print(f"\nRenaming complete. Total frames processed: {global_frame_counter}.")


if __name__ == "__main__":
    # The main directory containing gameplay folders with extracted frames
    frames_root_directory = os.path.join("extracted_frames", "", "")
    rename_frames_sequentially(frames_root_directory)
