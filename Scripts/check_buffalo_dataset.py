import os
import hashlib
from collections import Counter

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# ============================================================
# BUFFALO DATASET QUALITY CHECK
# ============================================================

print("=" * 70)
print("BUFFALO BREED DATASET QUALITY CHECK")
print("=" * 70)


# ============================================================
# PATHS
# ============================================================

TRAIN_DIR = r"D:\#SIH 2026\SIH_Buffalo_Augmented\train"

VAL_DIR = r"D:\#SIH 2026\SIH_Livestock_Split\val\buffalo"

TEST_DIR = r"D:\#SIH 2026\SIH_Livestock_Split\test\buffalo"


CLASSES = [
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


VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# BASIC DATASET STATISTICS
# ============================================================

def get_images(folder):

    if not os.path.exists(folder):
        return []

    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]


print("\n")
print("=" * 70)
print("1. IMAGE COUNTS")
print("=" * 70)


for split_name, base_dir in [
    ("TRAIN", TRAIN_DIR),
    ("VALIDATION", VAL_DIR),
    ("TEST", TEST_DIR)
]:

    print("\n" + split_name)

    total = 0

    for breed in CLASSES:

        folder = os.path.join(
            base_dir,
            breed
        )

        images = get_images(folder)

        count = len(images)

        total += count

        print(
            f"{breed:<18} : {count}"
        )

    print("-" * 40)
    print(
        f"TOTAL {split_name:<11}: {total}"
    )


# ============================================================
# IMAGE SIZE CHECK
# ============================================================

print("\n")
print("=" * 70)
print("2. IMAGE SIZE ANALYSIS")
print("=" * 70)


widths = []
heights = []

small_images = []
read_errors = []

all_train_images = []


for breed in CLASSES:

    folder = os.path.join(
        TRAIN_DIR,
        breed
    )

    images = get_images(folder)

    all_train_images.extend(images)

    for path in images:

        try:

            with Image.open(path) as img:

                width, height = img.size

                widths.append(width)
                heights.append(height)

                if width < 128 or height < 128:

                    small_images.append(
                        (path, width, height)
                    )

        except Exception as e:

            read_errors.append(
                (path, str(e))
            )


if widths:

    print(
        f"\nTotal training images checked : "
        f"{len(widths)}"
    )

    print(
        f"Minimum width                 : "
        f"{min(widths)}"
    )

    print(
        f"Maximum width                 : "
        f"{max(widths)}"
    )

    print(
        f"Average width                 : "
        f"{np.mean(widths):.2f}"
    )

    print(
        f"Minimum height                : "
        f"{min(heights)}"
    )

    print(
        f"Maximum height                : "
        f"{max(heights)}"
    )

    print(
        f"Average height                : "
        f"{np.mean(heights):.2f}"
    )

    print(
        f"Images smaller than 128x128  : "
        f"{len(small_images)}"
    )

    print(
        f"Read errors                  : "
        f"{len(read_errors)}"
    )


# ============================================================
# DUPLICATE CHECK
# ============================================================

print("\n")
print("=" * 70)
print("3. EXACT DUPLICATE CHECK")
print("=" * 70)


hashes = {}

duplicate_files = []

for path in all_train_images:

    try:

        with open(path, "rb") as f:

            file_hash = hashlib.md5(
                f.read()
            ).hexdigest()

        if file_hash in hashes:

            duplicate_files.append(
                (
                    path,
                    hashes[file_hash]
                )
            )

        else:

            hashes[file_hash] = path

    except:

        pass


print(
    "Training images checked :",
    len(all_train_images)
)

print(
    "Unique file hashes      :",
    len(hashes)
)

print(
    "Exact duplicates        :",
    len(duplicate_files)
)


if duplicate_files:

    print("\nFirst 20 duplicates:")

    for duplicate, original in duplicate_files[:20]:

        print(
            "\nDuplicate:",
            duplicate
        )

        print(
            "Original :",
            original
        )


# ============================================================
# IMAGE SAMPLE GRID
# ============================================================

print("\n")
print("=" * 70)
print("4. CREATING BREED SAMPLE GRID")
print("=" * 70)


fig, axes = plt.subplots(
    11,
    5,
    figsize=(15, 30)
)


for row, breed in enumerate(CLASSES):

    folder = os.path.join(
        TRAIN_DIR,
        breed
    )

    images = get_images(folder)

    if len(images) == 0:

        for col in range(5):

            axes[row, col].axis("off")

        continue


    # Pick up to 5 evenly distributed images

    if len(images) >= 5:

        indices = np.linspace(
            0,
            len(images) - 1,
            5,
            dtype=int
        )

        selected = [
            images[i]
            for i in indices
        ]

    else:

        selected = images


    for col in range(5):

        ax = axes[row, col]

        ax.axis("off")


        if col >= len(selected):

            continue


        path = selected[col]


        try:

            img = Image.open(path).convert(
                "RGB"
            )

            ax.imshow(img)

            if col == 0:

                ax.set_ylabel(
                    breed,
                    fontsize=11
                )

        except:

            ax.text(
                0.5,
                0.5,
                "ERROR",
                ha="center",
                va="center"
            )


plt.suptitle(
    "Buffalo Breed Training Dataset - Sample Images",
    fontsize=18
)

plt.tight_layout()

sample_grid_path = os.path.join(
    os.path.dirname(TRAIN_DIR),
    "buffalo_breed_sample_grid.png"
)

plt.savefig(
    sample_grid_path,
    dpi=150,
    bbox_inches="tight"
)

print(
    "\nSample grid saved at:"
)

print(sample_grid_path)

plt.show()


# ============================================================
# CLASS DISTRIBUTION GRAPH
# ============================================================

print("\n")
print("=" * 70)
print("5. CREATING CLASS DISTRIBUTION GRAPH")
print("=" * 70)


counts = []

for breed in CLASSES:

    folder = os.path.join(
        TRAIN_DIR,
        breed
    )

    counts.append(
        len(get_images(folder))
    )


plt.figure(
    figsize=(12, 6)
)

plt.bar(
    CLASSES,
    counts
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.ylabel(
    "Number of Training Images"
)

plt.xlabel(
    "Buffalo Breed"
)

plt.title(
    "Buffalo Breed Training Dataset Distribution"
)

plt.tight_layout()


distribution_path = os.path.join(
    os.path.dirname(TRAIN_DIR),
    "buffalo_breed_distribution.png"
)

plt.savefig(
    distribution_path,
    dpi=150,
    bbox_inches="tight"
)

print(
    "Distribution graph saved at:"
)

print(distribution_path)

plt.show()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("FINAL DATASET QUALITY SUMMARY")
print("=" * 70)


print(
    f"Training images       : "
    f"{len(all_train_images)}"
)

print(
    f"Small images          : "
    f"{len(small_images)}"
)

print(
    f"Read errors           : "
    f"{len(read_errors)}"
)

print(
    f"Exact duplicates      : "
    f"{len(duplicate_files)}"
)


print("\nBreed distribution:")

for breed, count in zip(
    CLASSES,
    counts
):

    print(
        f"{breed:<18} : {count}"
    )


print("\nDataset check completed.")