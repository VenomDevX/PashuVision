import os
import gdown

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")

MODELS = {
    "best_species_model.pth": "1lcZ1qgGw0NNMFhDpBqOWkyUPpZReHWrT",
    "best_cattle_breed_model.pth": "1P9UYOOYOnpcrItFPs9QMzVxDiF8NsFWo",
    "best_buffalo_breed_model.pth": "10dN2LJu1663IOcj3OkGDkNNeF_jVEm9Z",
}

def download_models():
    """Download model files from Google Drive if they don't exist locally."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    for filename, file_id in MODELS.items():
        filepath = os.path.join(MODEL_DIR, filename)
        if os.path.exists(filepath):
            print(f"✓ {filename} already exists, skipping download.")
            continue
        
        print(f"⬇ Downloading {filename} from Google Drive...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, filepath, quiet=False)
        print(f"✓ {filename} downloaded successfully!")

if __name__ == "__main__":
    download_models()
