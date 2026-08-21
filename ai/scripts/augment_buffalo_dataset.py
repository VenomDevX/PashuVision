import os
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

SOURCE = r"D:\#SIH 2026\SIH_Livestock_Split\train"
OUTPUT = r"D:\#SIH 2026\SIH_Buffalo_Augmented\train"

BUFFALO_CLASSES = [
    "Banni",
    "Bargur",
    "Chhattisgarhi",
    "Chilika",
    "Gojri",
    "Jaffarabadi",
    "Kalahandi",
    "Luit",
    "Marathwada",
    "Mehsana",
    "Murrah"
]

TARGET_IMAGES = 300

augment = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(20),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    )
])

os.makedirs(OUTPUT, exist_ok=True)

for breed in BUFFALO_CLASSES:

    source_dir = os.path.join(SOURCE, "buffalo", breed)
    output_dir = os.path.join(OUTPUT, breed)

    os.makedirs(output_dir, exist_ok=True)

    images = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
    ]

    print("\n" + breed)
    print("Original images:", len(images))

    for i, filename in enumerate(images):

        src = os.path.join(source_dir, filename)

        try:
            img = Image.open(src).convert("RGB")

            save_path = os.path.join(
                output_dir,
                f"original_{i}.jpg"
            )

            img.save(save_path, quality=95)

        except:
            continue

    current = len(images)
    needed = max(0, TARGET_IMAGES - current)

    print("Augmented images needed:", needed)

    for i in tqdm(range(needed)):

        filename = images[i % len(images)]
        src = os.path.join(source_dir, filename)

        try:
            img = Image.open(src).convert("RGB")

            aug_img = augment(img)

            save_path = os.path.join(
                output_dir,
                f"augmented_{i}.jpg"
            )

            aug_img.save(save_path, quality=95)

        except:
            pass


print("\n" + "=" * 50)
print("BUFFALO DATASET AUGMENTATION COMPLETE")
print("=" * 50)

total = 0

for breed in BUFFALO_CLASSES:

    folder = os.path.join(OUTPUT, breed)

    count = len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
    ])

    print(f"{breed:15} : {count}")

    total += count

print("-" * 50)
print(f"TOTAL TRAINING IMAGES : {total}")
print("=" * 50)