import os
import hashlib
from pathlib import Path

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def remove_duplicates(dataset_dir):
    print(f"Scanning for duplicates in {dataset_dir}...")
    hashes = set()
    duplicates_removed = 0
    
    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                filepath = Path(root) / file
                file_hash = get_file_hash(filepath)
                if file_hash in hashes:
                    os.remove(filepath)
                    duplicates_removed += 1
                else:
                    hashes.add(file_hash)
                    
    print(f"Removed {duplicates_removed} duplicate images.")

if __name__ == "__main__":
    remove_duplicates(r"E:\#SIH 2026\ai\dataset\Raw")
