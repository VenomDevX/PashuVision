import os
import random
from PIL import Image, ImageEnhance


# ============================================================
# BUFFALO 5-BREED DATASET V2
# TRAINING AUGMENTATION ONLY
# ============================================================

BASE_DIR = r"D:\#SIH 2026\SIH_Buffalo_5Breed_v2"

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "train"
)

TARGET_PER_BREED = 300

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

SEED = 42

random.seed(SEED)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("BUFFALO 5-BREED V2 - TRAINING AUGMENTATION")
print("=" * 70)

print("\nDataset:")
print(BASE_DIR)

print("\nTarget per breed:", TARGET_PER_BREED)


# ============================================================
# AUGMENTATION FUNCTION
# ============================================================

def augment_image(img):

    img = img.convert("RGB")

    # --------------------------------------------------------
    # SMALL ROTATION
    # --------------------------------------------------------

    angle = random.uniform(
        -7,
        7
    )

    img = img.rotate(
        angle,
        resample=Image.Resampling.BILINEAR,
        expand=False
    )


    # --------------------------------------------------------
    # HORIZONTAL FLIP
    # --------------------------------------------------------

    if random.random() < 0.5:

        img = img.transpose(
            Image.Transpose.FLIP_LEFT_RIGHT
        )


    # --------------------------------------------------------
    # BRIGHTNESS
    # --------------------------------------------------------

    brightness = random.uniform(
        0.90,
        1.10
    )

    img = ImageEnhance.Brightness(
        img
    ).enhance(
        brightness
    )


    # --------------------------------------------------------
    # CONTRAST
    # --------------------------------------------------------

    contrast = random.uniform(
        0.90,
        1.10
    )

    img = ImageEnhance.Contrast(
        img
    ).enhance(
        contrast
    )


    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    color = random.uniform(
        0.92,
        1.08
    )

    img = ImageEnhance.Color(
        img
    ).enhance(
        color
    )


    # --------------------------------------------------------
    # SMALL TRANSLATION / CROP
    # --------------------------------------------------------

    width, height = img.size

    crop_ratio = random.uniform(
        0.94,
        1.0
    )

    crop_width = int(
        width * crop_ratio
    )

    crop_height = int(
        height * crop_ratio
    )


    if (
        crop_width > 0
        and crop_height > 0
        and crop_width <= width
        and crop_height <= height
    ):

        left = random.randint(
            0,
            width - crop_width
        )

        top = random.randint(
            0,
            height - crop_height
        )

        img = img.crop(
            (
                left,
                top,
                left + crop_width,
                top + crop_height
            )
        )


    # --------------------------------------------------------
    # RESIZE
    # --------------------------------------------------------

    img = img.resize(
        (224, 224),
        Image.Resampling.LANCZOS
    )


    return img


# ============================================================
# PROCESS BREEDS
# ============================================================

total_original = 0
total_created = 0
total_final = 0


for breed in BREEDS:

    breed_dir = os.path.join(
        TRAIN_DIR,
        breed
    )


    if not os.path.exists(
        breed_dir
    ):

        print(
            f"\nERROR: Folder not found:"
            f"\n{breed_dir}"
        )

        continue


    # --------------------------------------------------------
    # ONLY ORIGINAL IMAGES
    # --------------------------------------------------------

    original_images = []

    for filename in os.listdir(
        breed_dir
    ):

        if filename.lower().endswith(
            VALID_EXTENSIONS
        ):

            # Do not use previously generated images
            if not filename.startswith(
                "aug_"
            ):

                original_images.append(
                    filename
                )


    original_images.sort()


    original_count = len(
        original_images
    )


    total_original += original_count


    print("\n" + "-" * 70)

    print(
        f"{breed}"
    )

    print(
        f"Original training images : "
        f"{original_count}"
    )


    # --------------------------------------------------------
    # CHECK TARGET
    # --------------------------------------------------------

    if original_count >= TARGET_PER_BREED:

        print(
            "Target already reached."
        )

        total_final += original_count

        continue


    needed = (
        TARGET_PER_BREED
        -
        original_count
    )


    print(
        f"Augmented images needed   : "
        f"{needed}"
    )


    created = 0


    # --------------------------------------------------------
    # CREATE AUGMENTED IMAGES
    # --------------------------------------------------------

    for i in range(
        needed
    ):

        source_filename = random.choice(
            original_images
        )


        source_path = os.path.join(
            breed_dir,
            source_filename
        )


        try:

            with Image.open(
                source_path
            ) as img:

                augmented = augment_image(
                    img
                )


            output_filename = (
                f"aug_{breed}_"
                f"{i:04d}.jpg"
            )


            output_path = os.path.join(
                breed_dir,
                output_filename
            )


            augmented.save(
                output_path,
                "JPEG",
                quality=95
            )


            created += 1


        except Exception as e:

            print(
                f"Error processing "
                f"{source_filename}: {e}"
            )


    final_count = (
        original_count
        +
        created
    )


    total_created += created
    total_final += final_count


    print(
        f"Created                  : "
        f"{created}"
    )

    print(
        f"Final training images    : "
        f"{final_count}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("AUGMENTATION COMPLETE")
print("=" * 70)


print(
    f"\nOriginal training images : "
    f"{total_original}"
)

print(
    f"Augmented images created : "
    f"{total_created}"
)

print(
    f"Final training images    : "
    f"{total_final}"
)


print("\nExpected:")

print(
    "5 breeds × 300 = 1500 training images"
)


# ============================================================
# VERIFY FINAL COUNTS
# ============================================================

print("\n")
print("=" * 70)
print("FINAL PER-BREED COUNTS")
print("=" * 70)


for breed in BREEDS:

    breed_dir = os.path.join(
        TRAIN_DIR,
        breed
    )


    count = 0

    for filename in os.listdir(
        breed_dir
    ):

        if filename.lower().endswith(
            VALID_EXTENSIONS
        ):

            count += 1


    print(
        f"{breed:<15}: "
        f"{count}"
    )


# ============================================================
# IMPORTANT
# ============================================================

print("\n")
print("=" * 70)
print("IMPORTANT")
print("=" * 70)

print(
    "Only TRAIN folders were modified."
)

print(
    "Validation set was NOT modified."
)

print(
    "Test set was NOT modified."
)

print(
    "Original source dataset was NOT modified."
)

print(
    "\nDataset:"
)

print(
    BASE_DIR
)

print("\nDone.")
