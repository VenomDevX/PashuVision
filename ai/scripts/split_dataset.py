from pathlib import Path
import shutil
import random

ROOT = Path(r"D:\#SIH 2026\SIH_Livestock_Dataset")
OUTPUT = Path(r"D:\#SIH 2026\SIH_Livestock_Split")

random.seed(42)

EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

SPECIES = ["cattle", "buffalo"]

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15


if OUTPUT.exists():
    print("Output folder already exists.")
    print("Delete or rename it before running again.")
    exit()


total_train = 0
total_val = 0
total_test = 0


for species in SPECIES:

    source_species = ROOT / species

    for breed_folder in sorted(source_species.iterdir()):

        if not breed_folder.is_dir():
            continue

        images = [
            f for f in breed_folder.rglob("*")
            if f.is_file()
            and f.suffix.lower() in EXTENSIONS
        ]

        if len(images) == 0:
            continue

        random.shuffle(images)

        n = len(images)

        train_end = int(n * TRAIN_RATIO)
        val_end = train_end + int(n * VAL_RATIO)

        train_images = images[:train_end]
        val_images = images[train_end:val_end]
        test_images = images[val_end:]

        print(
            f"{species:<8} "
            f"{breed_folder.name:<20} "
            f"Total={n:<5} "
            f"Train={len(train_images):<5} "
            f"Val={len(val_images):<5} "
            f"Test={len(test_images)}"
        )

        for split_name, split_images in [
            ("train", train_images),
            ("val", val_images),
            ("test", test_images)
        ]:

            destination = (
                OUTPUT
                / split_name
                / species
                / breed_folder.name
            )

            destination.mkdir(
                parents=True,
                exist_ok=True
            )

            for index, image in enumerate(split_images):

                new_name = (
                    f"{species}_{breed_folder.name}_"
                    f"{index:05d}{image.suffix.lower()}"
                )

                shutil.copy2(
                    image,
                    destination / new_name
                )

        total_train += len(train_images)
        total_val += len(val_images)
        total_test += len(test_images)


print("\n" + "=" * 70)
print("FINAL SPLIT")
print("=" * 70)

print(f"Training   : {total_train}")
print(f"Validation : {total_val}")
print(f"Testing    : {total_test}")
print(f"Total      : {total_train + total_val + total_test}")

print("\nDataset created at:")
print(OUTPUT)

print("\nOriginal dataset was NOT modified.")