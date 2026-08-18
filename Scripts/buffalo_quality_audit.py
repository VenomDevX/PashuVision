from pathlib import Path
from PIL import Image

ROOT = Path(r"D:\#SIH 2026\buffalo")

extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

MIN_WIDTH = 128
MIN_HEIGHT = 128

total = 0
good = 0
small = 0
errors = 0

print("=" * 70)
print("BUFFALO DATASET QUALITY AUDIT")
print("=" * 70)

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue

    class_total = 0
    class_good = 0
    class_small = 0

    for file in folder.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in extensions:
            continue

        total += 1
        class_total += 1

        try:
            with Image.open(file) as img:
                width, height = img.size

            if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                good += 1
                class_good += 1
            else:
                small += 1
                class_small += 1

        except Exception:
            errors += 1

    print(
        f"{folder.name:<20} "
        f"Total: {class_total:>4} | "
        f"Good: {class_good:>4} | "
        f"Small: {class_small:>4}"
    )

print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

print(f"Total images       : {total}")
print(f"Usable >=128x128   : {good}")
print(f"Very small images  : {small}")
print(f"Read errors        : {errors}")

print("\nNo files were deleted or modified.")