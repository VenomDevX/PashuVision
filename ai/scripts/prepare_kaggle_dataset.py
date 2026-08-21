import os
import shutil
from pathlib import Path
import zipfile

def clean_and_zip_dataset(dataset_dir: str, output_filename: str):
    print(f"Cleaning and preparing dataset in {dataset_dir}...")
    
    # 1. Remove hidden/system files that clutter datasets
    junk_files = ['.DS_Store', 'Thumbs.db', 'desktop.ini']
    cleaned_count = 0
    
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file in junk_files or file.startswith("._"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    cleaned_count += 1
                except Exception as e:
                    print(f"Warning: Could not remove {file_path}: {e}")
                    
    print(f"Cleaned {cleaned_count} junk files.")
    
    # 2. Create the zip file
    print(f"Zipping dataset to {output_filename} (This may take a minute)...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Create relative path for zip structure
                arcname = os.path.relpath(file_path, dataset_dir)
                zipf.write(file_path, arcname)
                
    print(f"Done! Your dataset is ready for Kaggle: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    # Ensure this points to your actual dataset folder
    target_dataset_dir = os.path.join(os.path.dirname(__file__), "..", "dataset")
    output_zip = os.path.join(os.path.dirname(__file__), "..", "kaggle_dataset.zip")
    
    if os.path.exists(target_dataset_dir):
        clean_and_zip_dataset(target_dataset_dir, output_zip)
    else:
        print(f"Error: Could not find dataset folder at {target_dataset_dir}")
