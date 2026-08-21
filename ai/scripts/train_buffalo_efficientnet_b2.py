
from pathlib import Path
import copy

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from torchvision.models import EfficientNet_B2_Weights

import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET = Path(
    r"D:\#SIH 2026\SIH_Buffalo_5Breed_Clean"
)

MODEL_DIR = Path(
    r"D:\#SIH 2026\SIH_Buffalo_Models_B2"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


BATCH_SIZE = 8

EPOCHS_STAGE1 = 5
EPOCHS_STAGE2 = 10

LR_STAGE1 = 0.0003
LR_STAGE2 = 0.00003

IMAGE_SIZE = 260


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print("=" * 70)
print("BUFFALO 5-BREED CLASSIFIER - EFFICIENTNET-B2")
print("=" * 70)

print("Device:", DEVICE)


# ============================================================
# TRANSFORMS
# NO AUGMENTATION
# ============================================================

train_transform = transforms.Compose([

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
# DATASETS
# ============================================================

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


print("\nClasses:")
print(train_dataset.classes)


print("\nDataset sizes:")

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
# CHECK DATASET
# ============================================================

if train_dataset.classes != val_dataset.classes:

    raise ValueError(
        "Training and validation classes do not match."
    )


if train_dataset.classes != test_dataset.classes:

    raise ValueError(
        "Training and test classes do not match."
    )


# ============================================================
# CLASS COUNTS
# ============================================================

class_counts = [
    0
    for _ in train_dataset.classes
]


for _, label in train_dataset.samples:

    class_counts[label] += 1


print("\nClass counts:")

for class_name, count in zip(
    train_dataset.classes,
    class_counts
):

    print(
        f"{class_name:<15}: {count}"
    )


# ============================================================
# CLASS WEIGHTS
# ============================================================

total_samples = sum(
    class_counts
)


class_weights = [
    total_samples /
    (
        len(class_counts)
        *
        count
    )

    for count in class_counts
]


class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32
).to(DEVICE)


print("\nClass weights:")

for class_name, weight in zip(
    train_dataset.classes,
    class_weights
):

    print(
        f"{class_name:<15}: "
        f"{weight.item():.4f}"
    )


# ============================================================
# DATALOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ============================================================
# MODEL
# ============================================================

print("\nLoading EfficientNet-B2...")

weights = EfficientNet_B2_Weights.DEFAULT

model = models.efficientnet_b2(
    weights=weights
)


# ============================================================
# FREEZE FEATURES
# ============================================================

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
    len(train_dataset.classes)
)


model = model.to(
    DEVICE
)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss(
    weight=class_weights
)


# ============================================================
# BEST MODEL
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

    total = 0


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
                predictions == labels
            ).sum().item()


            total += labels.size(0)


    return (
        running_loss / total,
        correct / total
    )


# ============================================================
# STAGE 1
# ============================================================

print(
    "\n"
    +
    "=" * 70
)

print(
    "STAGE 1 - TRAIN CLASSIFIER HEAD"
)

print(
    "=" * 70
)


optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=LR_STAGE1
)


for epoch in range(
    EPOCHS_STAGE1
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0


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
            predictions == labels
        ).sum().item()


        total += labels.size(0)


    train_loss = (
        running_loss / total
    )


    train_accuracy = (
        correct / total
    )


    val_loss, val_accuracy = validate()


    print(
        f"Epoch {epoch + 1}/"
        f"{EPOCHS_STAGE1} | "
        f"Train Loss: "
        f"{train_loss:.4f} | "
        f"Train Acc: "
        f"{train_accuracy * 100:.2f}% | "
        f"Val Loss: "
        f"{val_loss:.4f} | "
        f"Val Acc: "
        f"{val_accuracy * 100:.2f}%"
    )


    if val_accuracy > best_accuracy:

        best_accuracy = val_accuracy

        best_model_weights = copy.deepcopy(
            model.state_dict()
        )


        torch.save(
            {
                "model_state_dict":
                    model.state_dict(),

                "classes":
                    train_dataset.classes,

                "image_size":
                    IMAGE_SIZE,

                "model":
                    "EfficientNet-B2"
            },

            MODEL_DIR /
            "best_buffalo_efficientnet_b2.pth"
        )


        print(
            f"Best model saved: "
            f"{best_accuracy * 100:.2f}%"
        )


# ============================================================
# STAGE 2
# FINE-TUNING
# ============================================================

print(
    "\n"
    +
    "=" * 70
)

print(
    "STAGE 2 - FINE-TUNING"
)

print(
    "=" * 70
)


# Unfreeze last three feature blocks

for parameter in model.features[-3:].parameters():

    parameter.requires_grad = True


optimizer = torch.optim.Adam(

    filter(
        lambda p: p.requires_grad,
        model.parameters()
    ),

    lr=LR_STAGE2
)


for epoch in range(
    EPOCHS_STAGE2
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0


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
            predictions == labels
        ).sum().item()


        total += labels.size(0)


    train_loss = (
        running_loss / total
    )


    train_accuracy = (
        correct / total
    )


    val_loss, val_accuracy = validate()


    print(
        f"Fine-tune "
        f"{epoch + 1}/"
        f"{EPOCHS_STAGE2} | "
        f"Train Loss: "
        f"{train_loss:.4f} | "
        f"Train Acc: "
        f"{train_accuracy * 100:.2f}% | "
        f"Val Loss: "
        f"{val_loss:.4f} | "
        f"Val Acc: "
        f"{val_accuracy * 100:.2f}%"
    )


    if val_accuracy > best_accuracy:

        best_accuracy = val_accuracy

        best_model_weights = copy.deepcopy(
            model.state_dict()
        )


        torch.save(
            {
                "model_state_dict":
                    model.state_dict(),

                "classes":
                    train_dataset.classes,

                "image_size":
                    IMAGE_SIZE,

                "model":
                    "EfficientNet-B2"
            },

            MODEL_DIR /
            "best_buffalo_efficientnet_b2.pth"
        )


        print(
            f"Best model saved: "
            f"{best_accuracy * 100:.2f}%"
        )


# ============================================================
# LOAD BEST MODEL
# ============================================================

model.load_state_dict(
    best_model_weights
)


# ============================================================
# FINAL TEST
# ============================================================

print(
    "\n"
    +
    "=" * 70
)

print(
    "FINAL BUFFALO 5-BREED TEST"
)

print(
    "=" * 70
)


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
# CLASSIFICATION REPORT
# ============================================================

print(
    "\nClassification Report:\n"
)


print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=train_dataset.classes,
        digits=4,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions
)


print(
    "\nConfusion Matrix:\n"
)

print(cm)


disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=train_dataset.classes
)


disp.plot(
    values_format="d",
    xticks_rotation=45
)


plt.title(
    "Buffalo 5-Breed Classification - EfficientNet-B2"
)


plt.tight_layout()


plt.savefig(
    MODEL_DIR /
    "buffalo_efficientnet_b2_confusion_matrix.png",
    dpi=300
)


plt.show()


# ============================================================
# FINAL TEST ACCURACY
# ============================================================

test_accuracy = (
    torch.tensor(all_predictions)
    ==
    torch.tensor(all_labels)
).float().mean().item()


print(
    "\n"
    +
    "=" * 70
)

print(
    f"BEST VALIDATION ACCURACY: "
    f"{best_accuracy * 100:.2f}%"
)

print(
    f"TEST ACCURACY: "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"TEST IMAGES: "
    f"{len(test_dataset)}"
)


print(
    "\nModel saved at:"
)

print(
    MODEL_DIR /
    "best_buffalo_efficientnet_b2.pth"
)


print(
    "\nEfficientNet-B2 buffalo training complete."
)

print(
    "=" * 70
)
