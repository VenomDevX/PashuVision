# Dataset Guide

## Raw Data
Images are collected from Kaggle, field submissions, and web scraping. They are stored in `ai/dataset/Raw`.

## Preprocessing
1. **YOLO Cropper (`ai/scripts/crop_backgrounds_yolo.py`)**: Uses YOLOv8n to identify the animal, crop out the background context (farms, trees, people), and pad the bounding box by 10%.
2. **Augmentation (`ai/scripts/augment_dataset.py`)**: Imbalanced classes are heavily augmented (brightness, blur, flip) until every class has exactly 350 images.

## Structure
- `Processed/Cropped_Dataset/Cattle_Data`
- `Processed/Cropped_Dataset/Buffalo_Data`
- `Processed/Species_Dataset`
