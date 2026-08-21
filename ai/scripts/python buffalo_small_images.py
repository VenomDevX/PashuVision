from pathlib import Path
from PIL import Image

ROOT = Path(r"D:\#SIH 2026\buffalo")

extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

MIN_WIDTH = 128
MIN_HEIGHT = 128

print("=" * 70)
print("SMALL IMAGE ANALYSIS BY BREED")
print("=" * 70)

total_small = 0

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue

    small_images = []

    for file in folder.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in extensions:
            continue

        try:
            with Image.open(file) as img:
                width, height = img.size

            if width < MIN_WIDTH or height < MIN_HEIGHT:
                small_images.append((file.name, width, height))
                total_small += 1

        except:
            pass

    if small_images:
        print(f"\n{folder.name}: {len(small_images)} small images")

        for name, width, height in small_images[:10]:
            print(f"   {name} -> {width} x {height}")

        if len(small_images) > 10:
            print(f"   ... and {len(small_images) - 10} more")

print("\n" + "=" * 70)
print(f"TOTAL SMALL IMAGES: {total_small}")
print("=" * 70)