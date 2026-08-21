
from pathlib import Path

import torch
import torch.nn as nn

from PIL import Image

from torchvision import transforms, models


# ============================================================
# CONFIGURATION
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
print("INTEGRATED LIVESTOCK SPECIES + BREED PREDICTOR")
print("=" * 70)

print("Device:", DEVICE)


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# CHECK MODEL FILES
# ============================================================

for model_path in [
    SPECIES_MODEL_PATH,
    CATTLE_MODEL_PATH,
    BUFFALO_MODEL_PATH
]:

    if not model_path.exists():
        if model_path == SPECIES_MODEL_PATH:
            print(f"\nWARNING: Species model file not found at {model_path}. Will use confidence-based fallback routing.")
        else:
            raise FileNotFoundError(
                f"\nModel file not found:\n{model_path}"
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
# CREATE EFFICIENTNET-B0 MODEL
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
# CREATE EFFICIENTNET-B2 MODEL
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
# LOAD CATTLE BREED MODEL
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
# LOAD BUFFALO BREED MODEL
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


print("\nAll three models loaded successfully.")


# ============================================================
# PREDICT SPECIES
# ============================================================

def predict_species(image_tensor):
    if species_model is None:
        return None, 0.0

    with torch.no_grad():

        outputs = species_model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, index = torch.max(
            probabilities,
            dim=1
        )

    species = species_classes[
        index.item()
    ]

    confidence = (
        confidence.item() * 100
    )

    return species, confidence


# ============================================================
# PREDICT CATTLE BREED
# ============================================================

def predict_cattle_breed(image_tensor):

    with torch.no_grad():

        outputs = cattle_model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, index = torch.max(
            probabilities,
            dim=1
        )

    breed = cattle_classes[
        index.item()
    ]

    confidence = (
        confidence.item() * 100
    )

    return breed, confidence


# ============================================================
# PREDICT BUFFALO BREED
# ============================================================

def predict_buffalo_breed(image_tensor):

    with torch.no_grad():

        outputs = buffalo_model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, index = torch.max(
            probabilities,
            dim=1
        )

    breed = buffalo_classes[
        index.item()
    ]

    confidence = (
        confidence.item() * 100
    )

    return breed, confidence


# ============================================================
# COMPLETE PREDICTION
# ============================================================

def predict(image_path):

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        print(
            "\nERROR: Image not found."
        )

        print(
            image_path
        )

        return


    # --------------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------------

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as e:

        print(
            "\nERROR: Could not open image."
        )

        print(e)

        return


    # --------------------------------------------------------
    # TRANSFORM IMAGE
    # --------------------------------------------------------

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
    # STEP 1 & 2 — SPECIES AND BREED
    # ========================================================

    species, species_confidence = (
        predict_species(
            image_tensor
        )
    )

    if species is None:
        # Fallback: test both and pick highest confidence
        c_breed, c_conf = predict_cattle_breed(image_tensor)
        b_breed, b_conf = predict_buffalo_breed(image_tensor)
        
        if c_conf > b_conf:
            species = "Cattle (Fallback)"
            species_confidence = c_conf
            breed = c_breed
            breed_confidence = c_conf
        else:
            species = "Buffalo (Fallback)"
            species_confidence = b_conf
            breed = b_breed
            breed_confidence = b_conf
    else:
        species_lower = species.lower()

        if "buffalo" in species_lower:

            breed, breed_confidence = (
                predict_buffalo_breed(
                    image_tensor
                )
            )

        elif "cattle" in species_lower:

            breed, breed_confidence = (
                predict_cattle_breed(
                    image_tensor
                )
            )

        else:

            print(
                "\nERROR: Unknown species returned:"
            )

            print(species)

            return


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n")

    print("=" * 70)

    print("FINAL LIVESTOCK PREDICTION")

    print("=" * 70)

    print(
        f"Image       : {image_path.name}"
    )

    print(
        f"Species     : {species}"
    )

    print(
        f"Species Conf: {species_confidence:.2f}%"
    )

    print(
        f"Breed       : {breed}"
    )

    print(
        f"Breed Conf  : {breed_confidence:.2f}%"
    )

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\nEnter the path of an animal image.")

    image_path = input(
        "\nImage path: "
    ).strip().strip('"')

    predict(
        image_path
    )

