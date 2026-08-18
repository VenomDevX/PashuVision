from pathlib import Path

ROOT = Path(r"D:\#SIH 2026\SIH_Livestock_Dataset")

for species in ["cattle", "buffalo"]:

    print("\n" + "=" * 60)
    print(species.upper())
    print("=" * 60)

    total = 0

    for folder in sorted((ROOT / species).iterdir()):

        if not folder.is_dir():
            continue

        count = sum(
            1 for f in folder.rglob("*")
            if f.is_file()
        )

        print(f"{folder.name:<20} {count:>5}")

        total += count

    print("-" * 60)
    print(f"{'TOTAL':<20} {total:>5}")