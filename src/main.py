import cv2
from mss import mss
import numpy as np
import time

def main():
    t0 = time.time()
    n_frames = 0

    with mss() as sct:
        monitor = sct.monitors[1]

        while True:
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            cv2.imshow("My screen", img)

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