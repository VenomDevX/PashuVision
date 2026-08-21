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
    
    # CRITICAL OOM FIX: Use mmap=True. This memory-maps the file directly from the hard drive 
    # instead of loading the massive file into RAM. This saves hundreds of MBs!
    try:
        checkpoint = torch.load(path, map_location=DEVICE, weights_only=False, mmap=True)
    except TypeError:
        # Fallback for older PyTorch versions
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

# We will stop using global cache for models to prevent Python's malloc arena from holding memory.
# Instead, we load, predict, and instantly destroy.

def predict_with_model(model_path, model_name, image_tensor):
    """Loads a model via mmap, runs prediction, and destroys it completely."""
    model, classes = load_model_smart(model_path, model_name)
    if model is None:
        return None, 0.0
        
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        conf, idx = torch.max(probabilities, dim=1)
        result = classes[idx.item()]
        confidence = conf.item() * 100
        
    # Nuke the model from orbit
    del model
    del classes
    gc.collect()
    
    return result, confidence

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
        # Load Species model, predict, and instantly destroy
        res, conf = predict_with_model(SPECIES_MODEL_PATH, "Species", image_tensor)
        if res:
            species = res
            species_confidence = conf
    
    # 2. Breed classification
    breed = "Unknown"
    breed_confidence = 0.0
    
    if species is None:
        # Fallback if species failed
        c_res, c_conf = predict_with_model(CATTLE_MODEL_PATH, "Cattle", image_tensor)
        b_res, b_conf = predict_with_model(BUFFALO_MODEL_PATH, "Buffalo", image_tensor)
                
        if c_conf > b_conf and c_conf > 0:
            species = "Cattle (Fallback)"
            species_confidence = c_conf
        elif b_conf > 0:
            species = "Buffalo (Fallback)"
            species_confidence = b_conf
    else:
        # Normal routing
        if "buffalo" in species.lower():
            b_res, b_conf = predict_with_model(BUFFALO_MODEL_PATH, "Buffalo", image_tensor)
            if b_res:
                breed = b_res
                breed_confidence = b_conf
        elif "cattle" in species.lower():
            c_res, c_conf = predict_with_model(CATTLE_MODEL_PATH, "Cattle", image_tensor)
            if c_res:
                breed = c_res
                breed_confidence = c_conf
                
    # Final memory cleanup
    gc.collect()
                
    return {
        "species": species or "Unknown",
        "species_confidence": species_confidence,
        "breed": breed,
        "breed_confidence": breed_confidence
    }
