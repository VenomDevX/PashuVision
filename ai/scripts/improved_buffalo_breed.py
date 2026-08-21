import os
import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, WeightedRandomSampler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score


# ============================================================
# PATHS
# ============================================================

BASE_DIR = r"D:\#SIH 2026\SIH_Livestock_Split"

TRAIN_DIR = os.path.join(BASE_DIR, "train", "buffalo")
VAL_DIR   = os.path.join(BASE_DIR, "val", "buffalo")
TEST_DIR  = os.path.join(BASE_DIR, "test", "buffalo")

MODEL_PATH = r"D:\#SIH 2026\SIH_Livestock_Project\best_buffalo_breed_improved.pth"


# ============================================================
# SETTINGS
# ============================================================

BATCH_SIZE = 16
NUM_WORKERS = 0

HEAD_EPOCHS = 3
FINETUNE_EPOCHS = 15

IMG_SIZE = 224

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("IMPROVED BUFFALO BREED CLASSIFIER")
print("=" * 60)

print("Device:", DEVICE)


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),

    transforms.RandomHorizontalFlip(p=0.5),

    transforms.RandomRotation(15),

    transforms.RandomResizedCrop(
        IMG_SIZE,
        scale=(0.75, 1.0)
    ),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.05
    ),

    transforms.RandomAffine(
        degrees=0,
        translate=(0.08, 0.08),
        scale=(0.9, 1.1)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


test_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# DATASETS
# ============================================================

train_dataset = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    VAL_DIR,
    transform=test_transform
)

test_dataset = datasets.ImageFolder(
    TEST_DIR,
    transform=test_transform
)


classes = train_dataset.classes
num_classes = len(classes)

print("\nClasses:")
print(classes)

print("\nDataset sizes:")
print("Training  :", len(train_dataset))
print("Validation:", len(val_dataset))
print("Testing   :", len(test_dataset))


# ============================================================
# CLASS COUNTS
# ============================================================

targets = np.array(train_dataset.targets)

class_counts = np.bincount(
    targets,
    minlength=num_classes
)

print("\nTraining class counts:")

for i, cls in enumerate(classes):
    print(f"{cls:15s}: {class_counts[i]}")


# ============================================================
# WEIGHTED SAMPLER
# ============================================================

class_weights = 1.0 / class_counts

sample_weights = class_weights[targets]

sample_weights = torch.DoubleTensor(sample_weights)

sampler = WeightedRandomSampler(
    weights=sample_weights,
    num_samples=len(sample_weights),
    replacement=True
)


# ============================================================
# DATALOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    sampler=sampler,
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


# ============================================================
# MODEL
# ============================================================

print("\nLoading EfficientNet-B0...")

weights = models.EfficientNet_B0_Weights.DEFAULT

model = models.efficientnet_b0(
    weights=weights
)


# Replace classifier
in_features = model.classifier[1].in_features

model.classifier[1] = nn.Linear(
    in_features,
    num_classes
)

model = model.to(DEVICE)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss(
    label_smoothing=0.1
)


# ============================================================
# VALIDATION FUNCTION
# ============================================================

def evaluate(model, loader):

    model.eval()

    total_loss = 0
    predictions = []
    actual = []

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            total_loss += loss.item() * images.size(0)

            preds = torch.argmax(
                outputs,
                dim=1
            )

            predictions.extend(
                preds.cpu().numpy()
            )

            actual.extend(
                labels.cpu().numpy()
            )

    avg_loss = total_loss / len(loader.dataset)

    accuracy = accuracy_score(
        actual,
        predictions
    )

    macro_f1 = f1_score(
        actual,
        predictions,
        average="macro"
    )

    return avg_loss, accuracy, macro_f1


# ============================================================
# STAGE 1
# TRAIN CLASSIFIER HEAD
# ============================================================

print("\n" + "=" * 60)
print("STAGE 1 - TRAIN CLASSIFIER HEAD")
print("=" * 60)


for param in model.features.parameters():
    param.requires_grad = False


optimizer = optim.AdamW(
    model.classifier.parameters(),
    lr=0.001,
    weight_decay=1e-4
)


best_f1 = 0
best_model = copy.deepcopy(model.state_dict())


for epoch in range(HEAD_EPOCHS):

    model.train()

    running_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item() * images.size(0)

        preds = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            preds == labels
        ).sum().item()

        total += labels.size(0)

    train_loss = running_loss / total

    train_acc = correct / total

    val_loss, val_acc, val_f1 = evaluate(
        model,
        val_loader
    )

    print(
        f"Epoch {epoch + 1}/{HEAD_EPOCHS} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}% | "
        f"Val Macro F1: {val_f1 * 100:.2f}%"
    )

    if val_f1 > best_f1:

        best_f1 = val_f1

        best_model = copy.deepcopy(
            model.state_dict()
        )

        print(
            f"Best model saved "
            f"(Macro F1: {val_f1 * 100:.2f}%)"
        )


# ============================================================
# STAGE 2
# FINE-TUNING
# ============================================================

print("\n" + "=" * 60)
print("STAGE 2 - FINE-TUNING")
print("=" * 60)


# Unfreeze the whole model
for param in model.features.parameters():
    param.requires_grad = True


optimizer = optim.AdamW(
    model.parameters(),
    lr=0.0001,
    weight_decay=1e-4
)


scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=FINETUNE_EPOCHS
)


for epoch in range(FINETUNE_EPOCHS):

    model.train()

    running_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item() * images.size(0)

        preds = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            preds == labels
        ).sum().item()

        total += labels.size(0)

    scheduler.step()

    train_loss = running_loss / total

    train_acc = correct / total

    val_loss, val_acc, val_f1 = evaluate(
        model,
        val_loader
    )

    print(
        f"Fine-tune {epoch + 1}/{FINETUNE_EPOCHS} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}% | "
        f"Val Macro F1: {val_f1 * 100:.2f}%"
    )

    if val_f1 > best_f1:

        best_f1 = val_f1

        best_model = copy.deepcopy(
            model.state_dict()
        )

        torch.save(
            best_model,
            MODEL_PATH
        )

        print(
            f"Best model saved "
            f"(Macro F1: {val_f1 * 100:.2f}%)"
        )


# ============================================================
# LOAD BEST MODEL
# ============================================================

model.load_state_dict(best_model)

torch.save(
    model.state_dict(),
    MODEL_PATH
)


# ============================================================
# FINAL TEST
# ============================================================

print("\n" + "=" * 60)
print("FINAL IMPROVED BUFFALO BREED TEST")
print("=" * 60)


model.eval()

all_predictions = []
all_labels = []


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(DEVICE)

        outputs = model(images)

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


test_accuracy = accuracy_score(
    all_labels,
    all_predictions
)

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

print("\nClassification Report:\n")

print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=classes,
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

print("\nConfusion Matrix:\n")

print(cm)


# ============================================================
# CONFUSION MATRIX PLOT
# ============================================================

plt.figure(figsize=(11, 9))

plt.imshow(cm)

plt.title(
    "Improved Buffalo Breed Classification"
)

plt.colorbar()

plt.xticks(
    range(num_classes),
    classes,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(num_classes),
    classes
)

plt.xlabel("Predicted label")
plt.ylabel("True label")


for i in range(num_classes):

    for j in range(num_classes):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )


plt.tight_layout()

plt.show()


print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"Best Validation Macro F1: "
    f"{best_f1 * 100:.2f}%"
)

print(
    f"Final Test Accuracy: "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Final Test Macro F1: "
    f"{test_macro_f1 * 100:.2f}%"
)

print("\nModel saved at:")
print(MODEL_PATH)