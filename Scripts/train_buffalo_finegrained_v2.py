
from pathlib import Path
import copy

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from torchvision.models import EfficientNet_B2_Weights

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score
)

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

DATASET = Path(
    r"D:\#SIH 2026\SIH_Buffalo_5Breed"
)

MODEL_DIR = Path(
    r"D:\#SIH 2026\SIH_Buffalo_Models_B2"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH = (
    MODEL_DIR /
    "best_buffalo_finegrained_v2.pth"
)

BATCH_SIZE = 16

EPOCHS_HEAD = 5
EPOCHS_FINE = 15

LR_HEAD = 0.0003
LR_FINE = 0.00002

IMAGE_SIZE = 260

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)


print("=" * 70)
print("BUFFALO 5-BREED FINE-GRAINED CLASSIFIER V2")
print("=" * 70)

print("Device:", DEVICE)


# ============================================================
# TRANSFORMS
#
# No ColorJitter.
# Buffalo breeds are visually similar and mostly dark.
# We want to preserve natural appearance.
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        7
    ),

    transforms.RandomResizedCrop(
        IMAGE_SIZE,
        scale=(0.90, 1.0),
        ratio=(0.90, 1.10)
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
# CLASS COUNTS
# ============================================================

class_counts = [
    0
    for _ in train_dataset.classes
]


for _, label in train_dataset.samples:

    class_counts[label] += 1


print("\nClass counts:")

for name, count in zip(
    train_dataset.classes,
    class_counts
):

    print(
        f"{name:<15}: {count}"
    )


# ============================================================
# CLASS WEIGHTS
# ============================================================

total_samples = sum(
    class_counts
)

num_classes = len(
    class_counts
)

class_weights = [
    total_samples /
    (num_classes * count)
    for count in class_counts
]


class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32,
    device=DEVICE
)


print("\nClass weights:")

for name, weight in zip(
    train_dataset.classes,
    class_weights
):

    print(
        f"{name:<15}: "
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

print(
    "\nLoading pretrained EfficientNet-B2..."
)

weights = EfficientNet_B2_Weights.DEFAULT

model = models.efficientnet_b2(
    weights=weights
)


# Freeze feature extractor initially

for parameter in model.features.parameters():

    parameter.requires_grad = False


# Replace classifier

in_features = (
    model.classifier[1].in_features
)


model.classifier[1] = nn.Linear(
    in_features,
    num_classes
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
# VALIDATION FUNCTION
# ============================================================

def evaluate():

    model.eval()

    running_loss = 0.0

    all_predictions = []
    all_labels = []

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
                * images.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_labels.extend(
                labels.cpu().numpy()
            )


    loss = (
        running_loss /
        len(val_dataset)
    )


    accuracy = sum(
        p == y
        for p, y in zip(
            all_predictions,
            all_labels
        )
    ) / len(all_labels)


    macro_f1 = f1_score(
        all_labels,
        all_predictions,
        average="macro"
    )


    return (
        loss,
        accuracy,
        macro_f1
    )


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_one_epoch(
    optimizer
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
            * images.size(0)
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
# HISTORY
# ============================================================

train_losses = []
val_losses = []

train_accuracies = []
val_accuracies = []

val_f1_scores = []


best_f1 = 0.0

best_model_weights = copy.deepcopy(
    model.state_dict()
)


# ============================================================
# STAGE 1
# ============================================================

print("\n" + "=" * 70)
print("STAGE 1 - TRAIN CLASSIFIER HEAD")
print("=" * 70)


optimizer = torch.optim.AdamW(
    model.classifier.parameters(),
    lr=LR_HEAD,
    weight_decay=1e-4
)


for epoch in range(
    EPOCHS_HEAD
):

    train_loss, train_acc = (
        train_one_epoch(
            optimizer
        )
    )


    val_loss, val_acc, val_f1 = (
        evaluate()
    )


    train_losses.append(
        train_loss
    )

    val_losses.append(
        val_loss
    )

    train_accuracies.append(
        train_acc
    )

    val_accuracies.append(
        val_acc
    )

    val_f1_scores.append(
        val_f1
    )


    print(
        f"Epoch {epoch + 1}/{EPOCHS_HEAD} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}% | "
        f"Val Macro F1: {val_f1 * 100:.2f}%"
    )


    if val_f1 > best_f1:

        best_f1 = val_f1

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
                    "efficientnet_b2"
            },
            MODEL_PATH
        )


        print(
            f"Best model saved "
            f"(Macro F1: "
            f"{best_f1 * 100:.2f}%)"
        )


# ============================================================
# STAGE 2
# FINE-TUNE LAST PART OF EFFICIENTNET
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2 - FINE-TUNING")
print("=" * 70)


# Unfreeze last 4 feature blocks

for parameter in model.features[-4:].parameters():

    parameter.requires_grad = True


optimizer = torch.optim.AdamW(
    filter(
        lambda p:
        p.requires_grad,
        model.parameters()
    ),
    lr=LR_FINE,
    weight_decay=1e-4
)


for epoch in range(
    EPOCHS_FINE
):

    train_loss, train_acc = (
        train_one_epoch(
            optimizer
        )
    )


    val_loss, val_acc, val_f1 = (
        evaluate()
    )


    train_losses.append(
        train_loss
    )

    val_losses.append(
        val_loss
    )

    train_accuracies.append(
        train_acc
    )

    val_accuracies.append(
        val_acc
    )

    val_f1_scores.append(
        val_f1
    )


    print(
        f"Fine-tune "
        f"{epoch + 1}/{EPOCHS_FINE} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}% | "
        f"Val Macro F1: {val_f1 * 100:.2f}%"
    )


    if val_f1 > best_f1:

        best_f1 = val_f1

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
                    "efficientnet_b2"
            },
            MODEL_PATH
        )


        print(
            f"Best model saved "
            f"(Macro F1: "
            f"{best_f1 * 100:.2f}%)"
        )


# ============================================================
# RESTORE BEST MODEL
# ============================================================

model.load_state_dict(
    best_model_weights
)


# ============================================================
# FINAL TEST
# ============================================================

print("\n" + "=" * 70)
print("FINAL BUFFALO V2 TEST")
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

test_accuracy = sum(
    p == y
    for p, y in zip(
        all_predictions,
        all_labels
    )
) / len(all_labels)


test_macro_f1 = f1_score(
    all_labels,
    all_predictions,
    average="macro"
)


print(
    f"\nTest Accuracy : "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Test Macro F1 : "
    f"{test_macro_f1 * 100:.2f}%"
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
        target_names=
            train_dataset.classes,
        digits=4
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions
)


disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=
        train_dataset.classes
)


disp.plot(
    values_format="d",
    xticks_rotation=45
)


plt.title(
    "Buffalo 5-Breed Classification V2"
)


plt.tight_layout()


plt.savefig(
    MODEL_DIR /
    "buffalo_v2_confusion_matrix.png",
    dpi=300
)


plt.show()


# ============================================================
# ACCURACY GRAPH
# ============================================================

epochs_range = range(
    1,
    len(train_losses) + 1
)


plt.figure()


plt.plot(
    epochs_range,
    train_accuracies,
    label="Training Accuracy"
)


plt.plot(
    epochs_range,
    val_accuracies,
    label="Validation Accuracy"
)


plt.xlabel(
    "Epoch"
)


plt.ylabel(
    "Accuracy"
)


plt.title(
    "Buffalo V2 Training vs Validation Accuracy"
)


plt.legend()


plt.grid()


plt.tight_layout()


plt.savefig(
    MODEL_DIR /
    "buffalo_v2_accuracy.png",
    dpi=300
)


plt.show()


# ============================================================
# LOSS GRAPH
# ============================================================

plt.figure()


plt.plot(
    epochs_range,
    train_losses,
    label="Training Loss"
)


plt.plot(
    epochs_range,
    val_losses,
    label="Validation Loss"
)


plt.xlabel(
    "Epoch"
)


plt.ylabel(
    "Loss"
)


plt.title(
    "Buffalo V2 Training vs Validation Loss"
)


plt.legend()


plt.grid()


plt.tight_layout()


plt.savefig(
    MODEL_DIR /
    "buffalo_v2_loss.png",
    dpi=300
)


plt.show()


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n" + "=" * 70)

print(
    f"BEST VALIDATION MACRO F1: "
    f"{best_f1 * 100:.2f}%"
)

print(
    f"FINAL TEST ACCURACY: "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"FINAL TEST MACRO F1: "
    f"{test_macro_f1 * 100:.2f}%"
)

print(
    "\nModel saved at:"
)

print(
    MODEL_PATH
)

print(
    "\nBuffalo V2 training complete."
)

print("=" * 70)

