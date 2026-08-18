from pathlib import Path
import shutil

ROOT = Path(r"D:\#SIH 2026")
OUTPUT = ROOT / "SIH_Livestock_Dataset"

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"
}

CATTLE_BREEDS = {
    "bargur",
    "gir",
    "hallikar",
    "ongole",
    "tharparkar"
}

BUFFALO_BREEDS = {
    "banni",
    "bargur",
    "bhadawari",
    "chhattisgarhi",
    "chilika",
    "gojri",
    "jaffarabadi",
    "kalahandi",
    "luit",
    "marathwada",
    "mehsana",
    "murrah"
}

MIN_WIDTH = 128
MIN_HEIGHT = 128


def find_folder(name):
    matches = []

    for folder in ROOT.rglob("*"):
        if folder.is_dir() and folder.name.lower() == name.lower():
            matches.append(folder)

    return matches


def get_images(folder):
    return [
        file for file in folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def copy_images(source_folder, destination_folder, prefix):
    destination_folder.mkdir(parents=True, exist_ok=True)

    count = 0
    skipped = 0

    for image in get_images(source_folder):

        try:
            from PIL import Image

            with Image.open(image) as img:
                width, height = img.size

            if width < MIN_WIDTH or height < MIN_HEIGHT:
                skipped += 1
                continue

            extension = image.suffix.lower()

            new_name = f"{prefix}_{count + 1:05d}{extension}"

            destination = destination_folder / new_name

            shutil.copy2(image, destination)

            count += 1

        except Exception as e:
            print("Skipped:", image)
            print("Reason:", e)

    return count, skipped


print("=" * 70)
print("BUILDING FINAL SIH LIVESTOCK DATASET")
print("=" * 70)

print("\nOutput:")
print(OUTPUT)

if OUTPUT.exists():
    print("\nWARNING:")
    print("Output folder already exists.")
    print("Delete/rename it before running again if you want a fresh dataset.")
    exit()


# ---------------------------------------------------------
# Locate cattle and buffalo datasets
# ---------------------------------------------------------

cattle_root = ROOT / "cattle"
buffalo_root = ROOT / "buffalo"

if not cattle_root.exists():
    print("\nERROR: cattle folder not found.")
    exit()

if not buffalo_root.exists():
    print("\nERROR: buffalo folder not found.")
    exit()


# ---------------------------------------------------------
# Locate IICBD
# ---------------------------------------------------------

iicbd_root = None

for folder in ROOT.iterdir():

    if folder.is_dir() and "Annotated Multiview" in folder.name:
        iicbd_root = folder
        break

if iicbd_root is None:
    print("\nERROR: IICBD folder not found.")
    exit()


print("\nCattle dataset :", cattle_root)
print("Buffalo dataset:", buffalo_root)
print("IICBD          :", iicbd_root)


# ---------------------------------------------------------
# Create output folders
# ---------------------------------------------------------

for breed in CATTLE_BREEDS:
    (OUTPUT / "cattle" / breed.title()).mkdir(
        parents=True,
        exist_ok=True
    )

for breed in BUFFALO_BREEDS:
    (OUTPUT / "buffalo" / breed.title()).mkdir(
        parents=True,
        exist_ok=True
    )


# ---------------------------------------------------------
# Process cattle dataset
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("PROCESSING CATTLE DATASET")
print("=" * 70)

cattle_total = 0
cattle_skipped = 0

for breed in CATTLE_BREEDS:

    matches = find_folder(breed)

    # Only use folders located under cattle dataset
    matches = [
        folder for folder in matches
        if cattle_root in folder.parents
    ]

    if not matches:
        print(f"\nWARNING: {breed} not found in cattle dataset.")
        continue

    source = matches[0]
    destination = OUTPUT / "cattle" / breed.title()

    count, skipped = copy_images(
        source,
        destination,
        "cattle"
    )

    cattle_total += count
    cattle_skipped += skipped

    print(
        f"{breed.title():<15} "
        f"Copied: {count:>5} | "
        f"Skipped: {skipped:>4}"
    )


# ---------------------------------------------------------
# Process IICBD
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("PROCESSING IICBD")
print("=" * 70)

iicbd_total = 0
iicbd_skipped = 0

for breed in CATTLE_BREEDS:

    matches = find_folder(breed)

    matches = [
        folder for folder in matches
        if iicbd_root in folder.parents
    ]

    if not matches:
        print(f"\nWARNING: {breed} not found in IICBD.")
        continue

    source = matches[0]
    destination = OUTPUT / "cattle" / breed.title()

    count, skipped = copy_images(
        source,
        destination,
        "iicbd"
    )

    iicbd_total += count
    iicbd_skipped += skipped

    print(
        f"{breed.title():<15} "
        f"Copied: {count:>5} | "
        f"Skipped: {skipped:>4}"
    )


# ---------------------------------------------------------
# Process buffalo dataset
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("PROCESSING BUFFALO DATASET")
print("=" * 70)

buffalo_total = 0
buffalo_skipped = 0

for breed in BUFFALO_BREEDS:

    source = buffalo_root / breed

    if not source.exists():

        # Case-insensitive search
        candidates = [
            folder for folder in buffalo_root.iterdir()
            if folder.is_dir()
            and folder.name.lower() == breed.lower()
        ]

        if candidates:
            source = candidates[0]

    if not source.exists():
        print(f"\nWARNING: {breed} not found.")
        continue

    destination = OUTPUT / "buffalo" / breed.title()

    count, skipped = copy_images(
        source,
        destination,
        "buffalo"
    )

    buffalo_total += count
    buffalo_skipped += skipped

    print(
        f"{breed.title():<15} "
        f"Copied: {count:>5} | "
        f"Skipped: {skipped:>4}"
    )


# ---------------------------------------------------------
# Final summary
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)

print(f"\nCattle from original dataset : {cattle_total}")
print(f"Cattle from IICBD            : {iicbd_total}")
print(f"Buffalo                      : {buffalo_total}")

print(f"\nTotal cattle images          : {cattle_total + iicbd_total}")
print(f"Total buffalo images         : {buffalo_total}")
print(
    f"TOTAL FINAL IMAGES           : "
    f"{cattle_total + iicbd_total + buffalo_total}"
)

print(f"\nSmall images skipped         : "
      f"{cattle_skipped + iicbd_skipped + buffalo_skipped}")

print("\nDataset created at:")
print(OUTPUT)

print("\nOriginal datasets were NOT modified.")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)