from pathlib import Path
import copy

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from torchvision.models import EfficientNet_B0_Weights

import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ============================================================
# CONFIGURATION
# ============================================================

# YOUR ACTUAL DATASET LOCATION
DATASET = Path(
    r"D:\Shrey\SIH\sih2026_ml\#SIH 2026 - Copy\#SIH 2026 - Copy\SIH_Buffalo_5Breed_v2"
)

# YOUR ACTUAL MODEL OUTPUT LOCATION
MODEL_DIR = Path(
    r"D:\Shrey\SIH\sih2026_ml\#SIH 2026 - Copy\#SIH 2026 - Copy\SIH_Buffalo_Models"
)

# Create model directory if it doesn't exist
MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# TRAINING SETTINGS
# ============================================================

# Intel Iris Xe + CPU
# Start with 8 to keep RAM usage reasonable
BATCH_SIZE = 8

# Number of epochs
EPOCHS_STAGE1 = 5
EPOCHS_STAGE2 = 5

# Learning rates
LR_STAGE1 = 3e-4
LR_STAGE2 = 3e-5

# EfficientNet-B0 standard image size
IMAGE_SIZE = 224

# Stop if validation accuracy doesn't improve
EARLY_STOPPING_PATIENCE = 3

# CPU-friendly
NUM_WORKERS = 0


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print()
print("=" * 70)
print("BUFFALO 5-BREED CLASSIFIER")
print("=" * 70)

print("PyTorch version :", torch.__version__)

try:
    import torchvision
    print("TorchVision     :", torchvision.__version__)
except Exception:
    print("TorchVision     : Could not determine version")

print("Device          :", DEVICE)

if DEVICE.type == "cuda":
    print(
        "GPU             :",
        torch.cuda.get_device_name(0)
    )
else:
    print("GPU             : None")
    print("Running on CPU  : Yes")

print("=" * 70)


# ============================================================
# CHECK DATASET
# ============================================================

print()
print("Checking dataset...")

if not DATASET.exists():

    raise FileNotFoundError(
        f"""
Dataset folder was not found.

Expected location:
{DATASET}
"""
    )


# Check train/val/test folders
required_folders = [
    "train",
    "val",
    "test"
]

for folder in required_folders:

    folder_path = DATASET / folder

    if not folder_path.exists():

        raise FileNotFoundError(
            f"""
Missing dataset folder:

{folder_path}

Expected structure:

SIH_Buffalo_5Breed_v2
├── train
├── val
└── test
"""
        )


print("Dataset found:")
print(DATASET)


# ============================================================
# DATASET STRUCTURE
# ============================================================

print()
print("Checking dataset structure...")

for folder in required_folders:

    folder_path = DATASET / folder

    subfolders = [
        item.name
        for item in folder_path.iterdir()
        if item.is_dir()
    ]

    print(
        f"{folder:<10}: {len(subfolders)} classes"
    )


# ============================================================
# TRANSFORMS
# ============================================================

print()
print("Creating image transformations...")


# Training augmentation
train_transform = transforms.Compose([

    transforms.RandomResizedCrop(
        IMAGE_SIZE,
        scale=(0.80, 1.0)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        10
    ),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),

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


# Validation and testing
val_test_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

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
# LOAD DATASETS
# ============================================================

print()
print("Loading datasets...")


train_dataset = datasets.ImageFolder(
    DATASET / "train",
    transform=train_transform
)


val_dataset = datasets.ImageFolder(
    DATASET / "val",
    transform=val_test_transform
)


test_dataset = datasets.ImageFolder(
    DATASET / "test",
    transform=val_test_transform
)


# ============================================================
# DATASET INFORMATION
# ============================================================

print()
print("=" * 70)
print("DATASET INFORMATION")
print("=" * 70)


print()
print("Classes:")

for index, class_name in enumerate(
    train_dataset.classes
):

    print(
        f"{index}: {class_name}"
    )


print()
print("Dataset sizes:")

print(
    "Training   :",
    len(train_dataset)
)

print(
    "Validation :",
    len(val_dataset)
)

print(
    "Testing    :",
    len(test_dataset)
)


# ============================================================
# CHECK CLASS CONSISTENCY
# ============================================================

if train_dataset.classes != val_dataset.classes:

    raise ValueError(
        """
Train and validation classes do not match.

Train:
{}

Validation:
{}
""".format(
            train_dataset.classes,
            val_dataset.classes
        )
    )


if train_dataset.classes != test_dataset.classes:

    raise ValueError(
        """
Train and test classes do not match.

Train:
{}

Test:
{}
""".format(
            train_dataset.classes,
            test_dataset.classes
        )
    )


NUM_CLASSES = len(
    train_dataset.classes
)


print()
print(
    "Number of classes:",
    NUM_CLASSES
)


# ============================================================
# CLASS COUNTS
# ============================================================

print()
print("=" * 70)
print("CLASS DISTRIBUTION")
print("=" * 70)


class_counts = [
    0
] * NUM_CLASSES


for _, label in train_dataset.samples:

    class_counts[label] += 1


for class_name, count in zip(
    train_dataset.classes,
    class_counts
):

    print(
        f"{class_name:<25} : {count}"
    )


# ============================================================
# CLASS WEIGHTS
# ============================================================

# Helps if some buffalo breeds have fewer images
total_samples = sum(
    class_counts
)


class_weights = []


for count in class_counts:

    if count > 0:

        weight = (
            total_samples /
            (
                NUM_CLASSES *
                count
            )
        )

    else:

        weight = 0.0

    class_weights.append(
        weight
    )


class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32
).to(DEVICE)


print()
print("Class weights:")


for class_name, weight in zip(
    train_dataset.classes,
    class_weights
):

    print(
        f"{class_name:<25} : "
        f"{weight.item():.4f}"
    )


# ============================================================
# DATALOADERS
# ============================================================

print()
print("Creating DataLoaders...")


train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS
)


val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


print("Batch size:", BATCH_SIZE)
print("Workers   :", NUM_WORKERS)


# ============================================================
# LOAD EFFICIENTNET-B0
# ============================================================

print()
print("=" * 70)
print("LOADING EFFICIENTNET-B0")
print("=" * 70)


try:

    weights = EfficientNet_B0_Weights.DEFAULT

    model = models.efficientnet_b0(
        weights=weights
    )

except Exception as error:

    print()
    print("ERROR while loading EfficientNet-B0:")
    print(error)

    print()
    print(
        "This may indicate a Torch/TorchVision "
        "version compatibility problem."
    )

    raise


# ============================================================
# FREEZE FEATURE EXTRACTOR
# ============================================================

print()
print("Freezing EfficientNet feature extractor...")


for parameter in model.features.parameters():

    parameter.requires_grad = False


# ============================================================
# REPLACE CLASSIFIER
# ============================================================

in_features = (
    model.classifier[1].in_features
)


model.classifier[1] = nn.Linear(
    in_features,
    NUM_CLASSES
)


# Move model to CPU/GPU
model = model.to(
    DEVICE
)


print(
    "Classifier output:",
    NUM_CLASSES
)


# ============================================================
# LOSS FUNCTION
# ============================================================

criterion = nn.CrossEntropyLoss(
    weight=class_weights
)


# ============================================================
# BEST MODEL TRACKING
# ============================================================

best_accuracy = 0.0

best_model_weights = copy.deepcopy(
    model.state_dict()
)


# ============================================================
# VALIDATION FUNCTION
# ============================================================

def validate():

    model.eval()

    running_loss = 0.0

    correct = 0

    total_samples = 0


    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )


            outputs = model(
                images
            )


            loss = criterion(
                outputs,
                labels
            )


            running_loss += (
                loss.item()
                *
                images.size(0)
            )


            predictions = torch.argmax(
                outputs,
                dim=1
            )


            correct += (
                (predictions == labels)
                .sum()
                .item()
            )


            total_samples += (
                labels.size(0)
            )


    if total_samples == 0:

        return 0.0, 0.0


    val_loss = (
        running_loss /
        total_samples
    )


    val_accuracy = (
        correct /
        total_samples
    )


    return (
        val_loss,
        val_accuracy
    )


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_stage(
    stage_name,
    epochs,
    optimizer,
    scheduler=None
):

    global best_accuracy
    global best_model_weights


    print()
    print("=" * 70)
    print(stage_name)
    print("=" * 70)


    patience_counter = 0


    for epoch in range(
        epochs
    ):

        model.train()


        running_loss = 0.0

        correct = 0

        total_samples = 0


        print()
        print(
            f"Starting epoch "
            f"{epoch + 1}/{epochs}..."
        )


        # ====================================================
        # TRAINING LOOP
        # ====================================================

        for images, labels in train_loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )


            optimizer.zero_grad()


            outputs = model(
                images
            )


            loss = criterion(
                outputs,
                labels
            )


            loss.backward()


            optimizer.step()


            running_loss += (
                loss.item()
                *
                images.size(0)
            )


            predictions = torch.argmax(
                outputs,
                dim=1
            )


            correct += (
                (predictions == labels)
                .sum()
                .item()
            )


            total_samples += (
                labels.size(0)
            )


        # ====================================================
        # TRAIN METRICS
        # ====================================================

        if total_samples > 0:

            train_loss = (
                running_loss /
                total_samples
            )

            train_accuracy = (
                correct /
                total_samples
            )

        else:

            train_loss = 0.0
            train_accuracy = 0.0


        # ====================================================
        # VALIDATION
        # ====================================================

        val_loss, val_accuracy = (
            validate()
        )


        # ====================================================
        # LEARNING RATE SCHEDULER
        # ====================================================

        if scheduler is not None:

            scheduler.step(
                val_loss
            )


        current_lr = (
            optimizer.param_groups[0]["lr"]
        )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        print()

        print(
            f"Epoch {epoch + 1}/{epochs}"
        )

        print(
            f"Train Loss : "
            f"{train_loss:.4f}"
        )

        print(
            f"Train Acc  : "
            f"{train_accuracy * 100:.2f}%"
        )

        print(
            f"Val Loss   : "
            f"{val_loss:.4f}"
        )

        print(
            f"Val Acc    : "
            f"{val_accuracy * 100:.2f}%"
        )

        print(
            f"Learning Rate : "
            f"{current_lr:.8f}"
        )


        # ====================================================
        # SAVE BEST MODEL
        # ====================================================

        if val_accuracy > best_accuracy:

            best_accuracy = (
                val_accuracy
            )


            best_model_weights = (
                copy.deepcopy(
                    model.state_dict()
                )
            )


            model_path = (
                MODEL_DIR /
                "best_buffalo_5breed_model.pth"
            )


            torch.save(
                {
                    "model_state_dict":
                        model.state_dict(),

                    "classes":
                        train_dataset.classes,

                    "num_classes":
                        NUM_CLASSES,

                    "image_size":
                        IMAGE_SIZE,

                    "best_val_accuracy":
                        best_accuracy
                },
                model_path
            )


            print()
            print(
                "✓ NEW BEST MODEL!"
            )

            print(
                f"✓ Validation Accuracy: "
                f"{best_accuracy * 100:.2f}%"
            )

            print(
                f"✓ Saved to:\n"
                f"{model_path}"
            )


            patience_counter = 0


        else:

            patience_counter += 1


            print(
                f"No improvement "
                f"({patience_counter}/"
                f"{EARLY_STOPPING_PATIENCE})"
            )


        # ====================================================
        # EARLY STOPPING
        # ====================================================

        if (
            patience_counter
            >= EARLY_STOPPING_PATIENCE
        ):

            print()
            print(
                "Early stopping triggered."
            )

            break


# ============================================================
# STAGE 1
# ============================================================

print()
print("=" * 70)
print("STAGE 1")
print("=" * 70)

print(
    "Training only the classifier head..."
)


optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=LR_STAGE1
)


scheduler = (
    torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=1
    )
)


train_stage(
    "STAGE 1 — CLASSIFIER TRAINING",
    EPOCHS_STAGE1,
    optimizer,
    scheduler
)


# ============================================================
# RESTORE BEST STAGE 1 MODEL
# ============================================================

model.load_state_dict(
    best_model_weights
)


# ============================================================
# STAGE 2 — FINE TUNING
# ============================================================

print()
print("=" * 70)
print("STAGE 2")
print("=" * 70)

print(
    "Unfreezing the last 3 EfficientNet blocks..."
)


# Unfreeze last three feature blocks
for parameter in model.features[-3:].parameters():

    parameter.requires_grad = True


# ============================================================
# FINE-TUNING OPTIMIZER
# ============================================================

optimizer = torch.optim.Adam(
    filter(
        lambda parameter:
            parameter.requires_grad,
        model.parameters()
    ),
    lr=LR_STAGE2
)


scheduler = (
    torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=1
    )
)


train_stage(
    "STAGE 2 — FINE-TUNING",
    EPOCHS_STAGE2,
    optimizer,
    scheduler
)


# ============================================================
# LOAD BEST MODEL
# ============================================================

print()
print("Loading best model...")

model.load_state_dict(
    best_model_weights
)


# ============================================================
# FINAL TEST
# ============================================================

print()
print("=" * 70)
print("FINAL BUFFALO BREED TEST")
print("=" * 70)


model.eval()


all_predictions = []

all_labels = []


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(
            DEVICE
        )


        outputs = model(
            images
        )


        predictions = torch.argmax(
            outputs,
            dim=1
        )


        all_predictions.extend(
            predictions.cpu().numpy()
        )


        all_labels.extend(
            labels.numpy()
        )


# ============================================================
# TEST ACCURACY
# ============================================================

if len(all_labels) > 0:

    test_correct = sum(
        prediction == label
        for prediction, label
        in zip(
            all_predictions,
            all_labels
        )
    )


    test_accuracy = (
        test_correct /
        len(all_labels)
    )

else:

    test_accuracy = 0.0


print()
print(
    f"Test Accuracy: "
    f"{test_accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print()
print("=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)


print()


print(
    classification_report(
        all_labels,
        all_predictions,
        labels=list(
            range(NUM_CLASSES)
        ),
        target_names=
            train_dataset.classes,
        digits=4,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print()
print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)


cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(
        range(NUM_CLASSES)
    )
)


print()
print(cm)


# ============================================================
# SAVE CONFUSION MATRIX
# ============================================================

print()
print(
    "Creating confusion matrix image..."
)


disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=
        train_dataset.classes
)


fig, ax = plt.subplots(
    figsize=(9, 7)
)


disp.plot(
    ax=ax,
    values_format="d",
    xticks_rotation=45,
    cmap="Blues"
)


plt.title(
    "Buffalo 5-Breed Classification"
)


plt.tight_layout()


confusion_path = (
    MODEL_DIR /
    "buffalo_5breed_confusion_matrix.png"
)


plt.savefig(
    confusion_path,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# SAVE FINAL MODEL
# ============================================================

final_model_path = (
    MODEL_DIR /
    "buffalo_5breed_final_model.pth"
)


torch.save(
    {
        "model_state_dict":
            model.state_dict(),

        "classes":
            train_dataset.classes,

        "num_classes":
            NUM_CLASSES,

        "image_size":
            IMAGE_SIZE,

        "test_accuracy":
            test_accuracy,

        "best_validation_accuracy":
            best_accuracy
    },
    final_model_path
)


# ============================================================
# FINAL RESULTS
# ============================================================

print()
print()
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)


print()
print(
    f"Best Validation Accuracy : "
    f"{best_accuracy * 100:.2f}%"
)


print(
    f"Final Test Accuracy      : "
    f"{test_accuracy * 100:.2f}%"
)


print()
print("Best model:")
print(
    MODEL_DIR /
    "best_buffalo_5breed_model.pth"
)


print()
print("Final model:")
print(
    final_model_path
)


print()
print("Confusion matrix:")
print(
    confusion_path
)


print()
print("=" * 70)
print("Buffalo 5-Breed Training Finished!")
print("=" * 70)