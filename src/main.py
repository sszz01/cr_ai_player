import cv2
from mss import mss
import numpy as np
import time
from ultralytics import YOLO

def find_game_window(sct):
    offset_x, offset_y = (140, 636)  # offset from the top-left corner of the iphone screen to battle button

    try:
        battle_button_template = cv2.imread("templates/battle_button.png", 0)
    except Exception as e:
        print(f"Error: Could not load template image. Make sure 'templates/battle_button.png' exists.")
        print(e)
        return None

    main_monitor = sct.monitors[1]
    fs_screenshot = sct.grab(main_monitor)
    fs_img = np.array(fs_screenshot)
    fs_gray = cv2.cvtColor(fs_img, cv2.COLOR_BGRA2GRAY)

    res = cv2.matchTemplate(fs_gray, battle_button_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.8:
        print(f"Template found with {max_val:.2f} confidence.")
        top_left_x = max_loc[0] - offset_x
        top_left_y = max_loc[1] - offset_y

        game_window = {
            "top": top_left_y,
            "left": top_left_x,
            "width": 376,
            "height": 830
        }
        return game_window
    else:
        return None

def main():
    t0 = time.time()
    n_frames = 0

    model = YOLO("../runs/detect/train3/weights/last.pt")

    with mss() as sct:
        game_window = find_game_window(sct)
        if not game_window:
            print("Could not find game window. Exiting...")
            return

        while True:
            game_screenshot = sct.grab(game_window)
            game_img = np.array(game_screenshot)
            game_img_bgr = cv2.cvtColor(game_img, cv2.COLOR_BGRA2BGR)

            results = model.predict(game_img_bgr, verbose=False)
            annotated_frame = results[0].plot()

            cv2.imshow("My screen", annotated_frame)

            n_frames += 1
            t1 = time.time()
            elapsed_time = t1 - t0
            if elapsed_time > 1:
                fps = n_frames / elapsed_time
                print(f"FPS: {fps: .2f}")
                n_frames = 0
                t0 = t1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()