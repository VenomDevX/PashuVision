import torch
import torch.nn as nn
from torchvision import models
from app.config import SPECIES_MODEL_PATH, CATTLE_MODEL_PATH, BUFFALO_MODEL_PATH
from app.services.image_service import preprocess_image
import os

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def create_b4_model(checkpoint):
    classes = checkpoint["classes"]
    model = models.efficientnet_b4(weights=None)
    num_ftrs = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(num_ftrs, len(classes))
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(DEVICE)
    model.eval()
    return model, classes

def create_b0_model(checkpoint):
    classes = checkpoint["classes"]
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, len(classes))
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(DEVICE)
    model.eval()
    return model, classes

def load_model_smart(path, name):
    if not os.path.exists(path):
        print(f"Warning: {name} model not found at {path}")
        return None, []
    
    # Use weights_only=True for security (PyTorch 2.0+)
    try:
        checkpoint = torch.load(path, map_location=DEVICE, weights_only=False)
    except TypeError:
        checkpoint = torch.load(path, map_location=DEVICE)
        
    try:
        return create_b4_model(checkpoint)
    except Exception:
        try:
            return create_b0_model(checkpoint)
        except Exception as e:
            print(f"Failed to load {name} model: {e}")
            return None, []

# Load models into memory
print("Loading AI Models into memory...")
species_model, species_classes = load_model_smart(SPECIES_MODEL_PATH, "Species")
cattle_model, cattle_classes = load_model_smart(CATTLE_MODEL_PATH, "Cattle")
buffalo_model, buffalo_classes = load_model_smart(BUFFALO_MODEL_PATH, "Buffalo")

def predict_image(image_path: str, species_hint: str = "auto") -> dict:
    image_tensor = preprocess_image(image_path).unsqueeze(0).to(DEVICE)
    
    species = None
    species_confidence = 0.0
    
    # 1. Species routing
    if species_hint == "cattle":
        species = "Cattle"
        species_confidence = 100.0
    elif species_hint == "buffalo":
        species = "Buffalo"
        species_confidence = 100.0
    elif species_model is not None:
        with torch.no_grad():
            outputs = species_model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            conf, idx = torch.max(probabilities, dim=1)
            species = species_classes[idx.item()]
            species_confidence = conf.item() * 100
    
    # 2. Breed classification
    breed = "Unknown"
    breed_confidence = 0.0
    
    if species is None:
        # Fallback if species model is missing
        c_conf, b_conf = 0, 0
        if cattle_model:
            with torch.no_grad():
                c_out = torch.softmax(cattle_model(image_tensor), dim=1)
                c_conf, c_idx = torch.max(c_out, dim=1)
        if buffalo_model:
            with torch.no_grad():
                b_out = torch.softmax(buffalo_model(image_tensor), dim=1)
                b_conf, b_idx = torch.max(b_out, dim=1)
                
        if c_conf > b_conf and cattle_model:
            species = "Cattle (Fallback)"
            species_confidence = c_conf.item() * 100
            breed = cattle_classes[c_idx.item()]
            breed_confidence = species_confidence
        elif buffalo_model:
            species = "Buffalo (Fallback)"
            species_confidence = b_conf.item() * 100
            breed = buffalo_classes[b_idx.item()]
            breed_confidence = species_confidence
    else:
        # Normal routing
        if "buffalo" in species.lower() and buffalo_model:
            with torch.no_grad():
                out = torch.softmax(buffalo_model(image_tensor), dim=1)
                conf, idx = torch.max(out, dim=1)
                breed = buffalo_classes[idx.item()]
                breed_confidence = conf.item() * 100
        elif "cattle" in species.lower() and cattle_model:
            with torch.no_grad():
                out = torch.softmax(cattle_model(image_tensor), dim=1)
                conf, idx = torch.max(out, dim=1)
                breed = cattle_classes[idx.item()]
                breed_confidence = conf.item() * 100
                
    return {
        "species": species or "Unknown",
        "species_confidence": species_confidence,
        "breed": breed,
        "breed_confidence": breed_confidence
    }
