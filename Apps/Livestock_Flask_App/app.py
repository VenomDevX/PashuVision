
from pathlib import Path

import torch
import torch.nn as nn

from PIL import Image

from flask import Flask, render_template, request

from torchvision import transforms, models


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)

UPLOAD_FOLDER = Path(
    "static/uploads"
)

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = str(
    UPLOAD_FOLDER
)


# ============================================================
# MODEL PATHS
# ============================================================

SPECIES_MODEL_PATH = Path(
    r"E:\#SIH 2026\Models\Livestock_Models\best_species_model.pth"
)

CATTLE_MODEL_PATH = Path(
    r"E:\#SIH 2026\Models\Livestock_Models\best_cattle_breed_model.pth"
)

BUFFALO_MODEL_PATH = Path(
    r"E:\#SIH 2026\Models\Buffalo_Models_B2\best_buffalo_efficientnet_b2.pth"
)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("AI LIVESTOCK BREED IDENTIFICATION SYSTEM")
print("=" * 70)

print("Device:", DEVICE)


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# CHECK MODEL FILES
# ============================================================

for path in [
    SPECIES_MODEL_PATH,
    CATTLE_MODEL_PATH,
    BUFFALO_MODEL_PATH
]:

    if not path.exists():
        if path == SPECIES_MODEL_PATH:
            print(f"\nWARNING: Species model file not found at {path}. Will use confidence-based fallback routing.")
        else:
            raise FileNotFoundError(
                f"Model file not found:\n{path}"
            )


# ============================================================
# LOAD CHECKPOINT
# ============================================================

def load_checkpoint(path):

    return torch.load(
        path,
        map_location=DEVICE
    )


# ============================================================
# CREATE EFFICIENTNET-B0
# ============================================================

def create_b0_model(checkpoint):

    classes = checkpoint["classes"]

    model = models.efficientnet_b0(
        weights=None
    )

    in_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        in_features,
        len(classes)
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)

    model.eval()

    return model, classes


# ============================================================
# CREATE EFFICIENTNET-B2
# ============================================================

def create_b2_model(checkpoint):

    classes = checkpoint["classes"]

    model = models.efficientnet_b2(
        weights=None
    )

    in_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        in_features,
        len(classes)
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)

    model.eval()

    return model, classes


# ============================================================
# LOAD SPECIES MODEL
# ============================================================

print("\nLoading species model...")

if SPECIES_MODEL_PATH.exists():
    species_checkpoint = load_checkpoint(
        SPECIES_MODEL_PATH
    )

    species_model, species_classes = (
        create_b0_model(
            species_checkpoint
        )
    )

    print(
        "Species classes:",
        species_classes
    )
else:
    species_model, species_classes = None, None


# ============================================================
# LOAD CATTLE MODEL
# ============================================================

print("\nLoading cattle breed model...")

cattle_checkpoint = load_checkpoint(
    CATTLE_MODEL_PATH
)

cattle_model, cattle_classes = (
    create_b0_model(
        cattle_checkpoint
    )
)

print(
    "Cattle breeds:",
    cattle_classes
)


# ============================================================
# LOAD BUFFALO MODEL
# ============================================================

print("\nLoading buffalo breed model...")

buffalo_checkpoint = load_checkpoint(
    BUFFALO_MODEL_PATH
)

buffalo_model, buffalo_classes = (
    create_b2_model(
        buffalo_checkpoint
    )
)

print(
    "Buffalo breeds:",
    buffalo_classes
)


print("\nAll models loaded successfully.")


# ============================================================
# PREDICTION
# ============================================================

def predict(image_path, species_hint="auto"):

    image = Image.open(
        image_path
    ).convert("RGB")

    image_tensor = transform(
        image
    )

    image_tensor = image_tensor.unsqueeze(
        0
    )

    image_tensor = image_tensor.to(
        DEVICE
    )


    # ========================================================
    # SPECIES PREDICTION OR MANUAL HINT
    # ========================================================
    
    if species_hint == "cattle":
        species = "Cattle (Manual Selection)"
        species_confidence = 100.0
    elif species_hint == "buffalo":
        species = "Buffalo (Manual Selection)"
        species_confidence = 100.0
    elif species_model is not None:
        with torch.no_grad():
            outputs = species_model(
                image_tensor
            )
            probabilities = torch.softmax(
                outputs,
                dim=1
            )
            species_confidence, species_index = (
                torch.max(
                    probabilities,
                    dim=1
                )
            )

        species = species_classes[
            species_index.item()
        ]
        species_confidence = (
            species_confidence.item()
            * 100
        )
    else:
        species = None
        species_confidence = 0.0

    # ========================================================
    # BREED PREDICTION (AND FALLBACK SPECIES ROUTING)
    # ========================================================

    if species is None:
        # Fallback: run both models and pick highest confidence
        with torch.no_grad():
            c_outputs = cattle_model(image_tensor)
            c_probs = torch.softmax(c_outputs, dim=1)
            c_conf, c_idx = torch.max(c_probs, dim=1)
            
            b_outputs = buffalo_model(image_tensor)
            b_probs = torch.softmax(b_outputs, dim=1)
            b_conf, b_idx = torch.max(b_probs, dim=1)
            
        c_conf = c_conf.item() * 100
        b_conf = b_conf.item() * 100
        
        if c_conf > b_conf:
            species = "Cattle (Fallback)"
            species_confidence = c_conf
            breed = cattle_classes[c_idx.item()]
            breed_confidence = c_conf
        else:
            species = "Buffalo (Fallback)"
            species_confidence = b_conf
            breed = buffalo_classes[b_idx.item()]
            breed_confidence = b_conf
            
    else:
        # Original logic if species model exists
        if "buffalo" in species.lower():
            model = buffalo_model
            classes = buffalo_classes
        elif "cattle" in species.lower():
            model = cattle_model
            classes = cattle_classes
        else:
            raise ValueError(
                f"Unknown species: {species}"
            )

        with torch.no_grad():
            outputs = model(
                image_tensor
            )
            probabilities = torch.softmax(
                outputs,
                dim=1
            )
            breed_confidence, breed_index = (
                torch.max(
                    probabilities,
                    dim=1
                )
            )

        breed = classes[
            breed_index.item()
        ]
        breed_confidence = (
            breed_confidence.item()
            * 100
        )


    return {
        "species": species,
        "species_confidence": species_confidence,
        "breed": breed,
        "breed_confidence": breed_confidence
    }


# ============================================================
# HOME PAGE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    result = None
    image_url = None
    error = None


    if request.method == "POST":

        if "image" not in request.files:
            return render_template(
                "index.html",
                error="No file uploaded"
            )

        file = request.files["image"]
        species_hint = request.form.get("species_hint", "auto")

        if file.filename == "":
            return render_template(
                "index.html",
                error="No file selected"
            )


        try:

            filename = Path(
                file.filename
            ).name

            save_path = (
                UPLOAD_FOLDER /
                filename
            )

            file.save(
                save_path
            )


            result = predict(
                save_path,
                species_hint
            )


            image_url = (
                "/static/uploads/"
                + filename
            )


        except Exception as e:

            error = str(e)


    return render_template(
        "index.html",
        result=result,
        image_url=image_url,
        error=error
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

