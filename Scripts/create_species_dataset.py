import os
import shutil
import random

# ============================================================
# SPECIES DATASET GENERATOR
# Consolidates all raw breeds into a binary classification dataset
# (Cattle vs Buffalo) for training the Router Model
# ============================================================

RAW_DIR = r"E:\#SIH 2026\Datasets\Raw"
OUTPUT_DIR = r"E:\#SIH 2026\Datasets\Processed\Species_Dataset"
TARGET_PER_SPECIES = 4000 # Cap it to 4000 images per species so training isn't too slow

random.seed(42)

def generate_species_dataset():
    if os.path.exists(OUTPUT_DIR):
        print(f"Clearing existing dataset at {OUTPUT_DIR}...")
        shutil.rmtree(OUTPUT_DIR)
        
    os.makedirs(os.path.join(OUTPUT_DIR, "train", "Cattle"))
    os.makedirs(os.path.join(OUTPUT_DIR, "train", "Buffalo"))
    
    # Process Cattle
    cattle_raw_dir = os.path.join(RAW_DIR, "Cattle_Data")
    cattle_images = []
    
    for breed in os.listdir(cattle_raw_dir):
        breed_dir = os.path.join(cattle_raw_dir, breed)
        if os.path.isdir(breed_dir):
            for file in os.listdir(breed_dir):
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    cattle_images.append(os.path.join(breed_dir, file))
                    
    print(f"Found {len(cattle_images)} total Cattle images.")
    random.shuffle(cattle_images)
    cattle_selected = cattle_images[:TARGET_PER_SPECIES]
    
    for i, img_path in enumerate(cattle_selected):
        ext = os.path.splitext(img_path)[1]
        new_name = f"cattle_{i:05d}{ext}"
        shutil.copy(img_path, os.path.join(OUTPUT_DIR, "train", "Cattle", new_name))
        
    print(f"Copied {len(cattle_selected)} Cattle images to Species_Dataset/train/Cattle")

    # Process Buffalo
    buffalo_raw_dir = os.path.join(RAW_DIR, "Buffalo_Data")
    buffalo_images = []
    
    for breed in os.listdir(buffalo_raw_dir):
        breed_dir = os.path.join(buffalo_raw_dir, breed)
        if os.path.isdir(breed_dir):
            for file in os.listdir(breed_dir):
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    buffalo_images.append(os.path.join(breed_dir, file))
                    
    print(f"Found {len(buffalo_images)} total Buffalo images.")
    random.shuffle(buffalo_images)
    buffalo_selected = buffalo_images[:TARGET_PER_SPECIES]
    
    for i, img_path in enumerate(buffalo_selected):
        ext = os.path.splitext(img_path)[1]
        new_name = f"buffalo_{i:05d}{ext}"
        shutil.copy(img_path, os.path.join(OUTPUT_DIR, "train", "Buffalo", new_name))
        
    print(f"Copied {len(buffalo_selected)} Buffalo images to Species_Dataset/train/Buffalo")
    print("\nSpecies Dataset generation complete! Ready to train the missing Router model.")

if __name__ == "__main__":
    generate_species_dataset()