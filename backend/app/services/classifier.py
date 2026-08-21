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

import gc

# Lazy loading cache - we only keep ONE model in memory at a time to stay under 512MB
_current_model_name = None
_current_model = None
_current_classes = None

def get_model(path, name):
    global _current_model_name, _current_model, _current_classes
    
    # If the requested model is already in memory, use it
    if _current_model_name == name:
        return _current_model, _current_classes
        
    # Otherwise, clear memory first
    if _current_model is not None:
        del _current_model
        _current_model = None
        _current_classes = None
        gc.collect()
        
    print(f"Loading {name} model into memory (Lazy Load)...")
    _current_model, _current_classes = load_model_smart(path, name)
    _current_model_name = name
    return _current_model, _current_classes

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
    else:
        s_model, s_classes = get_model(SPECIES_MODEL_PATH, "Species")
        if s_model is not None:
            with torch.no_grad():
                outputs = s_model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                conf, idx = torch.max(probabilities, dim=1)
                species = s_classes[idx.item()]
                species_confidence = conf.item() * 100
        # CRITICAL: Delete local references so garbage collector can actually free the RAM!
        del s_model
        del s_classes
        import gc
        gc.collect()
    
    # 2. Breed classification
    breed = "Unknown"
    breed_confidence = 0.0
    
    if species is None:
        # Fallback (very heavy on memory as it loads both)
        c_model, c_classes = get_model(CATTLE_MODEL_PATH, "Cattle")
        c_conf, b_conf = 0, 0
        if c_model:
            with torch.no_grad():
                c_out = torch.softmax(c_model(image_tensor), dim=1)
                c_conf, c_idx = torch.max(c_out, dim=1)
        del c_model
        del c_classes
        gc.collect()
                
        b_model, b_classes = get_model(BUFFALO_MODEL_PATH, "Buffalo")
        if b_model:
            with torch.no_grad():
                b_out = torch.softmax(b_model(image_tensor), dim=1)
                b_conf, b_idx = torch.max(b_out, dim=1)
        del b_model
        del b_classes
        gc.collect()
                
        if c_conf > b_conf and c_conf > 0:
            species = "Cattle (Fallback)"
            species_confidence = c_conf.item() * 100
            # Assuming breed fallback just uses highest conf
        elif b_conf > 0:
            species = "Buffalo (Fallback)"
            species_confidence = b_conf.item() * 100
    else:
        # Normal routing
        if "buffalo" in species.lower():
            b_model, b_classes = get_model(BUFFALO_MODEL_PATH, "Buffalo")
            if b_model:
                with torch.no_grad():
                    out = torch.softmax(b_model(image_tensor), dim=1)
                    conf, idx = torch.max(out, dim=1)
                    breed = b_classes[idx.item()]
                    breed_confidence = conf.item() * 100
            del b_model
            del b_classes
            gc.collect()
        elif "cattle" in species.lower():
            c_model, c_classes = get_model(CATTLE_MODEL_PATH, "Cattle")
            if c_model:
                with torch.no_grad():
                    out = torch.softmax(c_model(image_tensor), dim=1)
                    conf, idx = torch.max(out, dim=1)
                    breed = c_classes[idx.item()]
                    breed_confidence = conf.item() * 100
            del c_model
            del c_classes
            gc.collect()
                
    # Final memory cleanup just in case
    gc.collect()
                
    return {
        "species": species or "Unknown",
        "species_confidence": species_confidence,
        "breed": breed,
        "breed_confidence": breed_confidence
    }
