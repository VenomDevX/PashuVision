from pathlib import Path
import hashlib
from collections import defaultdict

ROOT = Path(r"D:\#SIH 2026")

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"
}


def file_hash(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(1024 * 1024)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


# Find cattle dataset
cattle_folder = ROOT / "cattle"

# Find IICBD automatically
iicbd_folder = None

for folder in ROOT.iterdir():
    if folder.is_dir() and "Annotated Multiview" in folder.name:
        iicbd_folder = folder
        break

if not cattle_folder.exists():
    print("Cattle folder not found.")
    exit()

if iicbd_folder is None:
    print("IICBD folder not found.")
    exit()


print("=" * 70)
print("DUPLICATE IMAGE CHECK")
print("=" * 70)

print("\nCattle dataset:")
print(cattle_folder)

print("\nIICBD dataset:")
print(iicbd_folder)


# ---------------------------------------------------------
# Collect cattle images
# ---------------------------------------------------------

cattle_images = [
    p for p in cattle_folder.rglob("*")
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
]

print(f"\nCattle images: {len(cattle_images)}")


# ---------------------------------------------------------
# Collect IICBD images
# ---------------------------------------------------------

iicbd_images = [
    p for p in iicbd_folder.rglob("*")
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
]

print(f"IICBD images: {len(iicbd_images)}")


# ---------------------------------------------------------
# Hash cattle images
# ---------------------------------------------------------

print("\nHashing cattle images...")

cattle_hashes = defaultdict(list)

for i, image in enumerate(cattle_images, 1):

    try:
        h = file_hash(image)
        cattle_hashes[h].append(image)

    except Exception as e:
        print("Error:", image, e)

    if i % 500 == 0:
        print(f"Processed {i}/{len(cattle_images)}")


# ---------------------------------------------------------
# Check IICBD against cattle
# ---------------------------------------------------------

print("\nChecking IICBD against cattle...")

duplicate_pairs = []

for i, image in enumerate(iicbd_images, 1):

    try:
        h = file_hash(image)

        if h in cattle_hashes:

            for cattle_image in cattle_hashes[h]:

                duplicate_pairs.append(
                    (cattle_image, image)
                )

    except Exception as e:
        print("Error:", image, e)

    if i % 500 == 0:
        print(f"Processed {i}/{len(iicbd_images)}")


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(f"\nCattle images checked : {len(cattle_images)}")
print(f"IICBD images checked  : {len(iicbd_images)}")
print(f"Exact duplicate pairs : {len(duplicate_pairs)}")


if duplicate_pairs:

    print("\nDUPLICATES FOUND:")
    print("-" * 70)

    for cattle_image, iicbd_image in duplicate_pairs[:50]:

        print("\nCattle:")
        print(cattle_image)

        print("IICBD:")
        print(iicbd_image)

    if len(duplicate_pairs) > 50:
        print(
            f"\nOnly first 50 shown. "
            f"Total duplicate pairs: {len(duplicate_pairs)}"
        )

else:

    print("\nNo exact duplicate images found.")


print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("No files were modified.")
print("=" * 70)