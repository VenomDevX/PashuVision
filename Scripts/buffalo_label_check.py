from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\#SIH 2026\buffalo")
OUTPUT = Path(r"D:\#SIH 2026\buffalo_label_check.jpg")

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

IMAGES_PER_CLASS = 4
THUMB_WIDTH = 220
THUMB_HEIGHT = 180
LABEL_HEIGHT = 35

classes = [
    folder for folder in ROOT.iterdir()
    if folder.is_dir()
]

classes.sort(key=lambda x: x.name.lower())

rows = len(classes)
cols = IMAGES_PER_CLASS

sheet_width = cols * THUMB_WIDTH
sheet_height = rows * (THUMB_HEIGHT + LABEL_HEIGHT)

sheet = Image.new("RGB", (sheet_width, sheet_height), "white")
draw = ImageDraw.Draw(sheet)

for row, folder in enumerate(classes):

    images = [
        file for file in folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.shuffle(images)
    images = images[:IMAGES_PER_CLASS]

    print(f"{folder.name}: {len(images)} images selected")

    for col, image_path in enumerate(images):

        try:
            img = Image.open(image_path).convert("RGB")
            img.thumbnail((THUMB_WIDTH - 10, THUMB_HEIGHT - 10))

            x = col * THUMB_WIDTH
            y = row * (THUMB_HEIGHT + LABEL_HEIGHT)

            paste_x = x + (THUMB_WIDTH - img.width) // 2
            paste_y = y + (THUMB_HEIGHT - img.height) // 2

            sheet.paste(img, (paste_x, paste_y))

            draw.text(
                (x + 5, y + THUMB_HEIGHT + 5),
                folder.name,
                fill="black"
            )

        except Exception as e:
            print("Error:", image_path, e)

sheet.save(OUTPUT, quality=95)

print("\nContact sheet created:")
print(OUTPUT)