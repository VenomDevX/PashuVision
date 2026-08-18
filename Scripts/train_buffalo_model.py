import os
import copy
import numpy as np
import torch
import matplotlib.pyplot as plt

from torch import nn, optim
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms, models
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# BUFFALO BREED CLASSIFIER - IMPROVED VERSION
# ============================================================

print("=" * 70)
print("IMPROVED BUFFALO BREED CLASSIFIER")
print("=" * 70)


# ============================================================
# DEVICE
# ============================================================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("\nDevice:", device)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = r"D:\#SIH 2026\SIH_Livestock_Split"

TRAIN_DIR = os.path.join(BASE_DIR, "train", "buffalo")
VAL_DIR = os.path.join(BASE_DIR, "val", "buffalo")
TEST_DIR = os.path.join(BASE_DIR, "test", "buffalo")

MODEL_PATH = os.path.join(
    BASE_DIR,
    "best_buffalo_breed_model_improved.pth"
)


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((256, 256)),

    transforms.RandomResizedCrop(
        224,
        scale=(0.75, 1.0),
        ratio=(0.85, 1.15)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        15
    ),

    transforms.ColorJitter(
        brightness=0.25,
        contrast=0.25,
        saturation=0.25,
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
    transforms.Resize((224, 224)),

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

print("\nNumber of classes:", num_classes)

print("\nDataset sizes:")
print("Training  :", len(train_dataset))
print("Validation:", len(val_dataset))
print("Testing   :", len(test_dataset))


# ============================================================
# CLASS COUNTS
# ============================================================

class_counts = np.bincount(
    train_dataset.targets
)

print("\nClass counts:")

for i, class_name in enumerate(classes):
    print(
        f"{class_name:<18}: "
        f"{class_counts[i]}"
    )


# ============================================================
# CLASS WEIGHTS
# ============================================================

total_samples = len(train_dataset)

class_weights = total_samples / (
    num_classes * class_counts
)

class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32
).to(device)

print("\nClass weights:")

for i, class_name in enumerate(classes):
    print(
        f"{class_name:<18}: "
        f"{class_weights[i].item():.4f}"
    )


# ============================================================
# WEIGHTED SAMPLER
# ============================================================

sample_weights = [
    1.0 / class_counts[label]
    for label in train_dataset.targets
]

sample_weights = torch.DoubleTensor(
    sample_weights
)

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
    batch_size=32,
    sampler=sampler,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)


# ============================================================
# MODEL
# ============================================================

print("\nLoading EfficientNet-B0...")

weights = models.EfficientNet_B0_Weights.DEFAULT

model = models.efficientnet_b0(
    weights=weights
)

in_features = model.classifier[1].in_features

model.classifier[1] = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(
        in_features,
        num_classes
    )
)

model = model.to(device)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss(
    weight=class_weights,
    label_smoothing=0.1
)


# ============================================================
# STAGE 1
# TRAIN CLASSIFIER HEAD
# ============================================================

print("\n")
print("=" * 70)
print("STAGE 1 - TRAIN CLASSIFIER HEAD")
print("=" * 70)


for param in model.features.parameters():
    param.requires_grad = False

for param in model.classifier.parameters():
    param.requires_grad = True


optimizer = optim.AdamW(
    model.classifier.parameters(),
    lr=0.001,
    weight_decay=1e-4
)


scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=1
)


best_val_acc = 0.0
best_model = copy.deepcopy(model)


for epoch in range(5):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item() *
            images.size(0)
        )

        _, predicted = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

    train_loss = running_loss / total

    train_acc = correct / total


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    model.eval()

    val_loss_total = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            val_loss_total += (
                loss.item() *
                images.size(0)
            )

            _, predicted = torch.max(
                outputs,
                1
            )

            val_total += labels.size(0)

            val_correct += (
                predicted == labels
            ).sum().item()

    val_loss = (
        val_loss_total /
        val_total
    )

    val_acc = (
        val_correct /
        val_total
    )


    scheduler.step(val_acc)


    print(
        f"Epoch {epoch + 1}/5 | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}%"
    )


    if val_acc > best_val_acc:

        best_val_acc = val_acc

        best_model = copy.deepcopy(model)

        torch.save(
            model.state_dict(),
            MODEL_PATH
        )

        print(
            f"Best model saved "
            f"(Val Acc: {val_acc * 100:.2f}%)"
        )


# ============================================================
# STAGE 2
# FINE-TUNING
# ============================================================

print("\n")
print("=" * 70)
print("STAGE 2 - FINE-TUNING")
print("=" * 70)


for param in model.parameters():
    param.requires_grad = True


optimizer = optim.AdamW(
    model.parameters(),
    lr=0.00005,
    weight_decay=1e-4
)


scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)


for epoch in range(12):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )

        optimizer.step()

        running_loss += (
            loss.item() *
            images.size(0)
        )

        _, predicted = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

    train_loss = (
        running_loss /
        total
    )

    train_acc = (
        correct /
        total
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    model.eval()

    val_loss_total = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            val_loss_total += (
                loss.item() *
                images.size(0)
            )

            _, predicted = torch.max(
                outputs,
                1
            )

            val_total += labels.size(0)

            val_correct += (
                predicted == labels
            ).sum().item()

    val_loss = (
        val_loss_total /
        val_total
    )

    val_acc = (
        val_correct /
        val_total
    )


    scheduler.step(val_acc)


    print(
        f"Fine-tune {epoch + 1}/12 | "
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc * 100:.2f}% | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc * 100:.2f}%"
    )


    if val_acc > best_val_acc:

        best_val_acc = val_acc

        best_model = copy.deepcopy(model)

        torch.save(
            model.state_dict(),
            MODEL_PATH
        )

        print(
            f"Best model saved "
            f"(Val Acc: {val_acc * 100:.2f}%)"
        )


# ============================================================
# LOAD BEST MODEL
# ============================================================

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()


# ============================================================
# FINAL TEST
# ============================================================

print("\n")
print("=" * 70)
print("FINAL BUFFALO BREED TEST")
print("=" * 70)


all_predictions = []
all_labels = []


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)

        outputs = model(images)

        _, predicted = torch.max(
            outputs,
            1
        )

        all_predictions.extend(
            predicted.cpu().numpy()
        )

        all_labels.extend(
            labels.numpy()
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

fig, ax = plt.subplots(
    figsize=(12, 10)
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=classes
)

disp.plot(
    ax=ax,
    cmap="viridis",
    xticks_rotation=45,
    values_format="d",
    colorbar=True
)

plt.title(
    "Improved Buffalo Breed Classification"
)

plt.tight_layout()

plt.show()


# ============================================================
# FINAL ACCURACY
# ============================================================

accuracy = (
    np.array(all_predictions)
    ==
    np.array(all_labels)
).mean()


print("\n")
print("=" * 70)
print("FINAL RESULT")
print("=" * 70)

print(
    f"Best Validation Accuracy : "
    f"{best_val_acc * 100:.2f}%"
)

print(
    f"Test Accuracy            : "
    f"{accuracy * 100:.2f}%"
)

print(
    f"Test Images              : "
    f"{len(test_dataset)}"
)

print("\nModel saved at:")

print(MODEL_PATH)

print("\nTraining completed.")