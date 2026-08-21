from PIL import Image
from torchvision import transforms
import shutil
from pathlib import Path

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_upload_file(upload_file, filename: str) -> str:
    """Saves the uploaded file to disk and returns the local path."""
    file_location = UPLOAD_DIR / filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return str(file_location)

def preprocess_image(image_path: str):
    """Loads an image from disk, converts to RGB, and applies PyTorch transforms."""
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((380, 380)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image)
