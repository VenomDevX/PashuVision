import os
from ultralytics import YOLO
from PIL import Image

# ============================================================
# YOLOv8 LIVESTOCK CROPPER
# Uses Object Detection to crop the animal and remove background bias
# ============================================================

DATASET_ROOT = r"E:\#SIH 2026\ai\dataset\Raw" # Adjust to target directory
OUTPUT_ROOT = r"E:\#SIH 2026\ai\dataset\Processed\Cropped_Dataset"

# Load the pretrained YOLOv8 nano model (fastest)
model = YOLO('yolov8n.pt')

# COCO classes for Cow is 16. (Buffalo usually falls under cow, elephant, or bear in generic COCO,
# but 'cow' is the safest bet for livestock. For a production system, train a custom YOLO model).
TARGET_CLASS = 16 

def process_image(img_path, output_path):
    results = model.predict(img_path, conf=0.25, classes=[TARGET_CLASS], verbose=False)
    
    if len(results) == 0 or len(results[0].boxes) == 0:
        # If YOLO fails to find an animal, just copy the original to avoid losing data
        img = Image.open(img_path).convert("RGB")
        img = img.resize((380, 380), Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=95)
        return False
        
    # Get the bounding box with the highest confidence
    boxes = results[0].boxes
    best_box = boxes[0] # Usually sorted by confidence
    
    # Coordinates: x1, y1, x2, y2
    x1, y1, x2, y2 = best_box.xyxy[0].tolist()
    
    # Add a small 10% padding so we don't cut off ears/horns
    padding = 0.10
    w = x2 - x1
    h = y2 - y1
    x1 = max(0, x1 - (w * padding))
    y1 = max(0, y1 - (h * padding))
    x2 = min(results[0].orig_shape[1], x2 + (w * padding))
    y2 = min(results[0].orig_shape[0], y2 + (h * padding))
    
    # Crop and save — convert to RGB to handle RGBA PNGs
    try:
        img = Image.open(img_path).convert("RGB")
        cropped = img.crop((x1, y1, x2, y2))
        cropped = cropped.resize((380, 380), Image.Resampling.LANCZOS)
        cropped.save(output_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Error cropping {img_path}: {e}")
        return False

def batch_crop(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Count total files first for progress tracking
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_files.append((root, file))

    total = len(all_files)
    detected = 0
    fallback = 0

    for i, (root, file) in enumerate(all_files):
        source_path = os.path.join(root, file)

        # Create mirroring directory structure in dest
        rel_path = os.path.relpath(root, source_dir)
        target_dir = os.path.join(dest_dir, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_path = os.path.join(target_dir, file)
        found = process_image(source_path, target_path)
        if found:
            detected += 1
        else:
            fallback += 1

        if (i + 1) % 500 == 0 or (i + 1) == total:
            print(f"  Progress: {i+1}/{total} | Detected: {detected} | Fallback: {fallback}")

if __name__ == "__main__":
    print("=" * 60)
    print("STARTING YOLOv8 BACKGROUND REMOVAL CROPPER")
    print("=" * 60)
    print(f"Source: {DATASET_ROOT}")
    print(f"Output: {OUTPUT_ROOT}")
    print("This will take a significant amount of time without a GPU...")
    batch_crop(DATASET_ROOT, OUTPUT_ROOT)
    print("\nCropping Complete!")
