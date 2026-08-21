import os
import shutil
import hashlib
import random
from PIL import Image


# ============================================================
# BUFFALO 5-BREED DATASET V2
# ============================================================

SOURCE_DIR = r"D:\#SIH 2026\archive\buffalo"

OUTPUT_DIR = r"D:\#SIH 2026\SIH_Buffalo_5Breed_v2"


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


TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

random.seed(SEED)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("BUFFALO 5-BREED DATASET V2")
print("=" * 70)

print("\nSource:")
print(SOURCE_DIR)

print("\nOutput:")
print(OUTPUT_DIR)


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

for split in ["train", "val", "test"]:

    for breed in BREEDS:

        os.makedirs(
            os.path.join(
                OUTPUT_DIR,
                split,
                breed
            ),
            exist_ok=True
        )


# ============================================================
# SHA-256 FUNCTION
# ============================================================

def file_hash(path):

    sha = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            data = f.read(1024 * 1024)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


# ============================================================
# IMAGE VALIDATION
# ============================================================

def valid_image(path):

    try:

        with Image.open(path) as img:

            img.verify()

        return True

    except Exception:

        return False


# ============================================================
# PROCESS
# ============================================================

grand_total = 0
grand_duplicates = 0
grand_invalid = 0
grand_train = 0
grand_val = 0
grand_test = 0


print("\n")
print("=" * 70)
print("PROCESSING BREEDS")
print("=" * 70)


for breed in BREEDS:

    source_breed_dir = os.path.join(
        SOURCE_DIR,
        breed
    )


    if not os.path.exists(
        source_breed_dir
    ):

        print(
            f"\nERROR: Folder not found: "
            f"{source_breed_dir}"
        )

        continue


    files = []

    for filename in os.listdir(
        source_breed_dir
    ):

        path = os.path.join(
            source_breed_dir,
            filename
        )

        if (
            os.path.isfile(path)
            and filename.lower().endswith(
                VALID_EXTENSIONS
            )
        ):

            files.append(path)


    files.sort()


    print("\n" + "-" * 70)

    print(
        f"{breed}"
    )

    print(
        f"Images found : {len(files)}"
    )


    # --------------------------------------------------------
    # VALIDATE + REMOVE EXACT DUPLICATES
    # --------------------------------------------------------

    unique_files = []

    hashes = set()

    invalid = 0
    duplicates = 0


    for path in files:

        if not valid_image(path):

            invalid += 1

            continue


        try:

            h = file_hash(path)

        except Exception:

            invalid += 1

            continue


        if h in hashes:

            duplicates += 1

            continue


        hashes.add(h)

        unique_files.append(path)


    print(
        f"Invalid images : {invalid}"
    )

    print(
        f"Exact duplicates: {duplicates}"
    )

    print(
        f"Usable unique images: "
        f"{len(unique_files)}"
    )


    grand_duplicates += duplicates
    grand_invalid += invalid


    # --------------------------------------------------------
    # SHUFFLE
    # --------------------------------------------------------

    random.shuffle(
        unique_files
    )


    total = len(unique_files)


    # --------------------------------------------------------
    # SPLIT
    # --------------------------------------------------------

    train_end = int(
        total * TRAIN_RATIO
    )

    val_end = train_end + int(
        total * VAL_RATIO
    )


    train_files = unique_files[
        :train_end
    ]

    val_files = unique_files[
        train_end:val_end
    ]

    test_files = unique_files[
        val_end:
    ]


    print(
        f"Train : {len(train_files)}"
    )

    print(
        f"Val   : {len(val_files)}"
    )

    print(
        f"Test  : {len(test_files)}"
    )


    # --------------------------------------------------------
    # COPY FILES
    # --------------------------------------------------------

    splits = {
        "train": train_files,
        "val": val_files,
        "test": test_files
    }


    for split_name, split_files in splits.items():

        destination_dir = os.path.join(
            OUTPUT_DIR,
            split_name,
            breed
        )


        for index, source_path in enumerate(
            split_files
        ):

            extension = os.path.splitext(
                source_path
            )[1].lower()


            destination_name = (
                f"{breed}_{index:05d}"
                f"{extension}"
            )


            destination_path = os.path.join(
                destination_dir,
                destination_name
            )


            shutil.copy2(
                source_path,
                destination_path
            )


    grand_total += total

    grand_train += len(train_files)
    grand_val += len(val_files)
    grand_test += len(test_files)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)


print(
    f"\nTotal usable unique images : "
    f"{grand_total}"
)

print(
    f"Exact duplicates removed  : "
    f"{grand_duplicates}"
)

print(
    f"Invalid images skipped    : "
    f"{grand_invalid}"
)


print("\nFINAL SPLIT")

print(
    f"Training   : "
    f"{grand_train}"
)

print(
    f"Validation : "
    f"{grand_val}"
)

print(
    f"Testing    : "
    f"{grand_test}"
)

print(
    f"TOTAL      : "
    f"{grand_train + grand_val + grand_test}"
)


# ============================================================
# PER-BREED FINAL COUNTS
# ============================================================

print("\n")
print("=" * 70)
print("PER-BREED FINAL COUNTS")
print("=" * 70)


for breed in BREEDS:

    train_count = len(
        os.listdir(
            os.path.join(
                OUTPUT_DIR,
                "train",
                breed
            )
        )
    )

    val_count = len(
        os.listdir(
            os.path.join(
                OUTPUT_DIR,
                "val",
                breed
            )
        )
    )

    test_count = len(
        os.listdir(
            os.path.join(
                OUTPUT_DIR,
                "test",
                breed
            )
        )
    )


    print(
        f"{breed:<15} "
        f"Train={train_count:<4} "
        f"Val={val_count:<4} "
        f"Test={test_count:<4} "
        f"Total={train_count + val_count + test_count}"
    )


# ============================================================
# FINISHED
# ============================================================

print("\n")
print("=" * 70)
print("DATASET CREATION COMPLETED")
print("=" * 70)

print("\nDataset created at:")
print(OUTPUT_DIR)

print("\nOriginal dataset was NOT modified.")

print("\nIMPORTANT:")
print("- No augmentation was performed.")
print("- Validation images are untouched.")
print("- Test images are untouched.")
print("- Only exact duplicate images were removed.")