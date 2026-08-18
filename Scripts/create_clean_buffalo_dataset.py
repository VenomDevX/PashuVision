from pathlib import Path
import shutil


# ============================================================
# CREATE CLEAN BUFFALO 5-BREED DATASET
# NO AUGMENTED IMAGES
# ============================================================

SOURCE = Path(
    r"D:\#SIH 2026\SIH_Buffalo_5Breed_v2"
)

DESTINATION = Path(
    r"D:\#SIH 2026\SIH_Buffalo_5Breed_Clean"
)


BREEDS = [
    "Jaffarabadi",
    "Murrah",
    "Gojri",
    "Marathwada",
    "Chilika"
]


VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("CREATING CLEAN BUFFALO 5-BREED DATASET")
print("=" * 70)

print("\nSource:")
print(SOURCE)

print("\nDestination:")
print(DESTINATION)


# ============================================================
# CREATE DESTINATION
# ============================================================

if DESTINATION.exists():

    print(
        "\nDestination already exists."
    )

    print(
        "Removing old clean dataset..."
    )

    shutil.rmtree(
        DESTINATION
    )


DESTINATION.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SPLITS
# ============================================================

splits = [
    "train",
    "val",
    "test"
]


total_copied = 0


# ============================================================
# COPY ORIGINAL IMAGES
# ============================================================

for split in splits:

    print("\n")
    print("-" * 70)

    print(
        f"{split.upper()} SET"
    )

    print("-" * 70)


    split_total = 0


    for breed in BREEDS:

        source_dir = (
            SOURCE
            /
            split
            /
            breed
        )


        destination_dir = (
            DESTINATION
            /
            split
            /
            breed
        )


        destination_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        if not source_dir.exists():

            print(
                f"{breed:<15}: "
                f"SOURCE NOT FOUND"
            )

            continue


        copied = 0


        for image_path in source_dir.iterdir():

            if not image_path.is_file():
                continue


            if image_path.suffix.lower() not in VALID_EXTENSIONS:
                continue


            # ------------------------------------------------
            # IMPORTANT:
            # Ignore all generated augmented images
            # ------------------------------------------------

            if image_path.name.lower().startswith(
                "aug_"
            ):
                continue


            destination_path = (
                destination_dir
                /
                image_path.name
            )


            shutil.copy2(
                image_path,
                destination_path
            )


            copied += 1


        split_total += copied
        total_copied += copied


        print(
            f"{breed:<15}: "
            f"{copied}"
        )


    print(
        f"\nTOTAL {split.upper():<10}: "
        f"{split_total}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("CLEAN DATASET CREATED")
print("=" * 70)


print(
    "\nTotal images copied:",
    total_copied
)


print(
    "\nExpected:"
)

print(
    "Training   : 779"
)

print(
    "Validation : 164"
)

print(
    "Testing    : 172"
)

print(
    "TOTAL      : 1115"
)


print("\nDataset location:")

print(
    DESTINATION
)


print("\n")
print("=" * 70)
print("IMPORTANT")
print("=" * 70)

print(
    "No augmentation was performed."
)

print(
    "All aug_*.jpg files were excluded."
)

print(
    "Validation images were not modified."
)

print(
    "Test images were not modified."
)

print(
    "Original source dataset was not modified."
)

print(
    "\nClean dataset creation completed."
)