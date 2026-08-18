import os
import random
from PIL import Image, ImageEnhance
import math

# ============================================================
# UNIVERSAL LIVESTOCK AUGMENTATION SCRIPT
# Balances all breeds to exactly 350 images
# ============================================================

RAW_DIR = r"E:\#SIH 2026\Datasets\Raw"
TARGET_PER_BREED = 350
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
SEED = 42

random.seed(SEED)

def augment_image(img):
    img = img.convert("RGB")
    
    # Random Rotation
    angle = random.uniform(-15, 15)
    img = img.rotate(angle, resample=Image.Resampling.BILINEAR, expand=False)
    
    # Horizontal Flip
    if random.random() < 0.5:
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
    # Brightness
    brightness = random.uniform(0.85, 1.15)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    
    # Contrast
    contrast = random.uniform(0.85, 1.15)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    
    # Color
    color = random.uniform(0.9, 1.1)
    img = ImageEnhance.Color(img).enhance(color)
    
    # Small Translation / Crop (Zooming in slightly to vary scale)
    width, height = img.size
    crop_ratio = random.uniform(0.85, 1.0)
    crop_width = int(width * crop_ratio)
    crop_height = int(height * crop_ratio)
    
    if crop_width > 0 and crop_height > 0 and crop_width <= width and crop_height <= height:
        left = random.randint(0, width - crop_width)
        top = random.randint(0, height - crop_height)
        img = img.crop((left, top, left + crop_width, top + crop_height))
        
    # Resize to standard classification size
    img = img.resize((224, 224), Image.Resampling.LANCZOS)
    return img

def process_species_folder(species_dir):
    if not os.path.exists(species_dir):
        print(f"Directory not found: {species_dir}")
        return

    breeds = [d for d in os.listdir(species_dir) if os.path.isdir(os.path.join(species_dir, d))]
    
    for breed in breeds:
        breed_dir = os.path.join(species_dir, breed)
        
        # Get original images
        original_images = [
            f for f in os.listdir(breed_dir) 
            if f.lower().endswith(VALID_EXTENSIONS) and not f.startswith("aug_")
        ]
        
        original_count = len(original_images)
        print(f"\nProcessing {breed}: {original_count} original images")
        
        if original_count >= TARGET_PER_BREED:
            print(f"Target already reached. No augmentation needed.")
            continue
            
        needed = TARGET_PER_BREED - original_count
        print(f"Needs {needed} augmented images to reach target.")
        
        created = 0
        for i in range(needed):
            source_filename = random.choice(original_images)
            source_path = os.path.join(breed_dir, source_filename)
            
            try:
                with Image.open(source_path) as img:
                    augmented = augment_image(img)
                    
                output_filename = f"aug_{breed}_{i:04d}.jpg"
                output_path = os.path.join(breed_dir, output_filename)
                
                augmented.save(output_path, "JPEG", quality=95)
                created += 1
            except Exception as e:
                print(f"Error processing {source_filename}: {e}")
                
        print(f"Generated {created} images. Final count: {original_count + created}")

if __name__ == "__main__":
    print("=" * 60)
    print("BALANCING CATTLE DATASET")
    print("=" * 60)
    process_species_folder(os.path.join(RAW_DIR, "Cattle_Data"))
    
    print("\n" + "=" * 60)
    print("BALANCING BUFFALO DATASET")
    print("=" * 60)
    process_species_folder(os.path.join(RAW_DIR, "Buffalo_Data"))
    
    print("\nData balancing complete! All classes should now have exactly 350 images.")
