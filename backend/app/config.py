import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
AI_MODELS_DIR = BASE_DIR / "ai" / "models" / "Livestock_Models"

SPECIES_MODEL_PATH = AI_MODELS_DIR / "best_species_model.pth"
CATTLE_MODEL_PATH = AI_MODELS_DIR / "best_cattle_breed_model.pth"
BUFFALO_MODEL_PATH = AI_MODELS_DIR / "best_buffalo_breed_model.pth"
