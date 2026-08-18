import os
import random
from PIL import Image, ImageEnhance, ImageOps


# ============================================================
# BUFFALO 5-BREED TRAINING AUGMENTATION
# ============================================================

SOURCE_DIR = r"D:\#SIH 2026\SIH_Buffalo_5Breed\train"

TARGET_PER_BREED = 400

SEED = 42

random.seed(SEED)


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


print("=" * 70)
print("BUFFALO 5-BREED TRAINING AUGMENTATION")
print("=" * 70)


# ============================================================
# AUGMENTATION FUNCTION
# ============================================================

def augment_image(img):

    img = img.convert("RGB")

    # Small rotation
    angle = random.uniform(-7, 7)

    img = img.rotate(
        angle,
        resample=Image.Resampling.BILINEAR,
        expand=False
    )

    # Horizontal flip
    if random.random() < 0.5:

        img = ImageOps.mirror(img)

    # Slight brightness change
    brightness = random.uniform(
        0.90,
        1.10
    )

    img = ImageEnhance.Brightness(
        img
    ).enhance(brightness)

    # Slight contrast change
    contrast = random.uniform(
        0.90,
        1.10
    )

    img = ImageEnhance.Contrast(
        img
    ).enhance(contrast)

    # Slight color change
    color = random.uniform(
        0.92,
        1.08
    )

    img = ImageEnhance.Color(
        img
    ).enhance(color)

    # Slight zoom/crop
    width, height = img.size

    crop_ratio = random.uniform(
        0.92,
        1.0
    )

    crop_w = int(
        width * crop_ratio
    )

    crop_h = int(
        height * crop_ratio
    )

    left = random.randint(
        0,
        width - crop_w
    )

    top = random.randint(
        0,
        height - crop_h
    )

    img = img.crop(
        (
            left,
            top,
            left + crop_w,
            top + crop_h
        )
    )

    img = img.resize(
        (224, 224),
        Image.Resampling.LANCZOS
    )

    return img


# ============================================================
# PROCESS BREEDS
# ============================================================

total_original = 0
total_augmented = 0
total_final = 0


for breed in BREEDS:

    breed_dir = os.path.join(
        SOURCE_DIR,
        breed
    )

    if not os.path.exists(breed_dir):

        print(
            f"\nERROR: Missing folder: {breed_dir}"
        )

        continue


    images = [
        f for f in os.listdir(breed_dir)
        if f.lower().endswith(
            VALID_EXTENSIONS
        )
        and not f.startswith("aug_")
    ]


    original_count = len(images)

    total_original += original_count


    print("\n" + "-" * 70)

    print(
        f"{breed}"
    )

    print(
        f"Original images : {original_count}"
    )


    if original_count >= TARGET_PER_BREED:

        print(
            "Already has target number."
        )

        total_final += original_count

        continue


    needed = (
        TARGET_PER_BREED
        -
        original_count
    )


    print(
        f"Images to create: {needed}"
    )


    created = 0


    for i in range(needed):

        source_filename = random.choice(
            images
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
                "Error:",
                source_filename,
                e
            )


    final_count = (
        original_count
        +
        created
    )


    total_augmented += created
    total_final += final_count


    print(
        f"Created          : {created}"
    )

    print(
        f"Final images     : {final_count}"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")
print("=" * 70)
print("AUGMENTATION COMPLETE")
print("=" * 70)


print(
    f"Original training images : "
    f"{total_original}"
)

print(
    f"Augmented images created : "
    f"{total_augmented}"
)

print(
    f"Final training images    : "
    f"{total_final}"
)


print("\nExpected:")

print(
    "5 breeds × 400 images = 2000 training images"
)


print("\nDataset location:")

print(
    SOURCE_DIR
)


print("\nIMPORTANT:")
print(
    "Validation and test datasets were NOT modified."
)

print(
    "Original source dataset was NOT modified."
)

print(
    "Only the 5-breed training folders were augmented."
)

print("\nDone.")