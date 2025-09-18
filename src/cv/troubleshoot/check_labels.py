import glob
import os

nc = 156  # must match your data.yaml

for split in ["train", "valid"]:
    path = f"../datasets/char_detection_dataset/{split}/labels"
    for file in glob.glob(os.path.join(path, "*.txt")):
        with open(file) as f:
            lines = f.readlines()
            if len(lines) > 50:  # arbitrarily large
                print(f"{f} has {len(lines)} labels")
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    print("Wrong format:", file, line)
                    continue
                else:
                    cls, x, y, w, h = parts
                    cls = int(cls)
                    x, y, w, h = map(float, [x, y, w, h])
                    vals = list(map(float, [x, y, w, h]))
                    # catch zero or negative widths/heights
                    if any(v < 0 or v > 1 for v in vals) or float(w) <= 0 or float(h) <= 0:
                        print("⚠️ Invalid box:", file, vals)
                    if cls < 0 or cls >= nc:
                        print("Class index out of range:", file, cls)
                    if w <= 0 or h <= 0:
                        print("Box with zero or negative size:", file, w, h)
                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        print("Box coords out of bounds:", file, x, y, w, h)
