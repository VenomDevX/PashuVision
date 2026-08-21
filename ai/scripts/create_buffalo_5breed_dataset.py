import os
import random
import shutil
from PIL import Image


# ============================================================
# 5-BREED BUFFALO DATASET CREATOR
# ============================================================

print("=" * 70)
print("BUFFALO 5-BREED DATASET CREATOR")
print("=" * 70)


# ============================================================
# PATHS
# ============================================================

SOURCE_DIR = r"D:\#SIH 2026\SIH_Livestock_Dataset\buffalo"

OUTPUT_DIR = r"D:\#SIH 2026\SIH_Buffalo_5Breed"


# ============================================================
# SELECTED BREEDS
# ============================================================

BREEDS = [
    "Jaffarabadi",
    "Murrah",
    "Gojri",
    "Marathwada",
    "Chilika"
]


# ============================================================
# SETTINGS
# ============================================================

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

random.seed(SEED)


VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# CHECK SOURCE
# ============================================================

if not os.path.exists(SOURCE_DIR):

    print("\nERROR: Source directory not found:")
    print(SOURCE_DIR)
    raise SystemExit


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

for split in ["train", "val", "test"]:

    for breed in BREEDS:

        folder = os.path.join(
            OUTPUT_DIR,
            split,
            breed
        )

        os.makedirs(
            folder,
            exist_ok=True
        )


# ============================================================
# GET VALID IMAGES
# ============================================================

def get_images(folder):

    images = []

    if not os.path.exists(folder):
        return images

    for filename in os.listdir(folder):

        if filename.lower().endswith(
            VALID_EXTENSIONS
        ):

            images.append(
                os.path.join(
                    folder,
                    filename
                )
            )

    return images


# ============================================================
# PROCESS EACH BREED
# ============================================================

print("\nSelected breeds:")

for breed in BREEDS:
    print("-", breed)


print("\n")
print("=" * 70)
print("CREATING TRAIN / VALIDATION / TEST SPLIT")
print("=" * 70)


total_train = 0
total_val = 0
total_test = 0


for breed in BREEDS:

    source_breed_dir = os.path.join(
        SOURCE_DIR,
        breed
    )

    images = get_images(
        source_breed_dir
    )


    print("\n")
    print(breed)

    print(
        "Original images:",
        len(images)
    )


    if len(images) == 0:

        print(
            "WARNING: No images found!"
        )

        continue


    # --------------------------------------------------------
    # SHUFFLE
    # --------------------------------------------------------

    random.shuffle(images)


    # --------------------------------------------------------
    # SPLIT ORIGINAL IMAGES
    # --------------------------------------------------------

    total = len(images)

    train_count = int(
        total * TRAIN_RATIO
    )

    val_count = int(
        total * VAL_RATIO
    )

    train_images = images[
        :train_count
    ]

    val_images = images[
        train_count:
        train_count + val_count
    ]

    test_images = images[
        train_count + val_count:
    ]


    # --------------------------------------------------------
    # COPY FUNCTION
    # --------------------------------------------------------

    def copy_images(
        image_list,
        split
    ):

        copied = 0

        destination = os.path.join(
            OUTPUT_DIR,
            split,
            breed
        )


        for index, source_path in enumerate(
            image_list
        ):

            try:

                # Verify image can be opened

                with Image.open(
                    source_path
                ) as img:

                    img.verify()


                extension = os.path.splitext(
                    source_path
                )[1].lower()


                new_name = (
                    f"{breed}_"
                    f"{split}_"
                    f"{index:05d}"
                    f"{extension}"
                )


                destination_path = os.path.join(
                    destination,
                    new_name
                )


                shutil.copy2(
                    source_path,
                    destination_path
                )


                copied += 1


            except Exception as e:

                print(
                    "Skipped:",
                    source_path
                )

                print(
                    "Reason:",
                    e
                )


        return copied


    # --------------------------------------------------------
    # COPY DATA
    # --------------------------------------------------------

    train_copied = copy_images(
        train_images,
        "train"
    )

    val_copied = copy_images(
        val_images,
        "val"
    )

    test_copied = copy_images(
        test_images,
        "test"
    )


    total_train += train_copied
    total_val += val_copied
    total_test += test_copied


    print(
        f"Train : {train_copied}"
    )

    print(
        f"Val   : {val_copied}"
    )

    print(
        f"Test  : {test_copied}"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")
print("=" * 70)
print("FINAL 5-BREED DATASET")
print("=" * 70)


print(
    f"Training   : {total_train}"
)

print(
    f"Validation : {total_val}"
)

print(
    f"Testing    : {total_test}"
)

print(
    f"TOTAL      : "
    f"{total_train + total_val + total_test}"
)


print("\n")
print("Selected breeds:")

for breed in BREEDS:

    print(
        f"- {breed}"
    )


print("\nDataset created at:")

print(
    OUTPUT_DIR
)


print("\nOriginal dataset was NOT modified.")

print("\nIMPORTANT:")
print(
    "Only the original images were split."
)

print(
    "No augmentation was performed yet."
)

print(
    "Validation and test images are kept untouched."
)


print("\nDataset creation completed.")