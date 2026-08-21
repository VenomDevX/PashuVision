"""
BREED MODEL RETRAINING SCRIPT
Trains only the Cattle Breed + Buffalo Breed classifiers
with batch_size=8 to fit in RTX 4050 VRAM during Stage 2.
Species Router is already trained (92.87% acc) — skipped.
"""
import torch
import numpy as np
import copy
import os
import time

from torch import nn, optim
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms, models

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# ============================================================
# MODELS TO TRAIN (breed classifiers only)
# ============================================================
MODELS_TO_TRAIN = [
    {
        "name": "Cattle Breed Classifier",
        "dataset_dir": r"E:\#SIH 2026\ai\dataset\Processed\Cropped_Dataset\Cattle_Data",
        "output_path": r"E:\#SIH 2026\ai\models\Livestock_Models\best_cattle_breed_model.pth",
        "stage1_epochs": 5,
        "stage2_epochs": 25,
        "batch_size": 8,       # Reduced from 16 to fit VRAM
        "stage1_lr": 1e-3,
        "stage2_lr": 5e-5,
    },
    {
        "name": "Buffalo Breed Classifier",
        "dataset_dir": r"E:\#SIH 2026\ai\dataset\Processed\Cropped_Dataset\Buffalo_Data",
        "output_path": r"E:\#SIH 2026\ai\models\Livestock_Models\best_buffalo_breed_model.pth",
        "stage1_epochs": 5,
        "stage2_epochs": 25,
        "batch_size": 8,       # Reduced from 16 to fit VRAM
        "stage1_lr": 1e-3,
        "stage2_lr": 5e-5,
    },
]

# ============================================================
# DATA TRANSFORMS
# ============================================================
IMG_SIZE = 380  # EfficientNet-B4 native resolution

train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE + 20, IMG_SIZE + 20)),
    transforms.RandomResizedCrop(IMG_SIZE, scale=(0.7, 1.0), ratio=(0.85, 1.15)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.85, 1.15)),
    transforms.RandomPerspective(distortion_scale=0.2, p=0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    transforms.RandomErasing(p=0.2, scale=(0.02, 0.15)),
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def compute_class_weights(dataset, num_classes):
    targets = [s[1] for s in dataset.samples]
    class_counts = np.bincount(targets, minlength=num_classes).astype(float)
    class_counts = np.maximum(class_counts, 1.0)
    total = len(targets)
    weights = total / (num_classes * class_counts)
    return torch.tensor(weights, dtype=torch.float32).to(DEVICE)


def train_single_model(config):
    name = config["name"]
    dataset_dir = config["dataset_dir"]
    output_path = config["output_path"]
    stage1_epochs = config["stage1_epochs"]
    stage2_epochs = config["stage2_epochs"]
    batch_size = config["batch_size"]
    stage1_lr = config["stage1_lr"]
    stage2_lr = config["stage2_lr"]

    print(f"\n{'=' * 70}")
    print(f"TRAINING: {name}")
    print(f"{'=' * 70}")
    print(f"Dataset: {dataset_dir}")
    print(f"Output:  {output_path}")
    print(f"Batch size: {batch_size}")

    train_dataset = datasets.ImageFolder(dataset_dir, transform=train_transform)
    val_dataset = datasets.ImageFolder(dataset_dir, transform=val_transform)

    class_names = train_dataset.classes
    num_classes = len(class_names)

    # 80/20 split
    total = len(train_dataset)
    indices = list(range(total))
    np.random.seed(42)
    np.random.shuffle(indices)
    split = int(0.8 * total)
    train_indices = indices[:split]
    val_indices = indices[split:]

    train_subset = torch.utils.data.Subset(train_dataset, train_indices)
    val_subset = torch.utils.data.Subset(val_dataset, val_indices)

    # Weighted sampler
    train_targets = [train_dataset.samples[i][1] for i in train_indices]
    class_counts = np.bincount(train_targets, minlength=num_classes).astype(float)
    class_counts = np.maximum(class_counts, 1.0)
    sample_weights = [1.0 / class_counts[t] for t in train_targets]
    sample_weights = torch.DoubleTensor(sample_weights)
    sampler = WeightedRandomSampler(weights=sample_weights, num_samples=len(sample_weights), replacement=True)

    train_loader = DataLoader(train_subset, batch_size=batch_size, sampler=sampler, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)

    print(f"Classes ({num_classes}): {class_names}")
    print(f"Total images: {total}")
    print(f"Train: {len(train_indices)} | Val: {len(val_indices)}")

    print("\nClass distribution (train):")
    for i, cls in enumerate(class_names):
        print(f"  {cls:<20s}: {int(class_counts[i])}")

    # ---- Model: EfficientNet-B4 ----
    model = models.efficientnet_b4(weights=models.EfficientNet_B4_Weights.DEFAULT)
    num_ftrs = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(num_ftrs, num_classes),
    )
    model = model.to(DEVICE)

    class_weights = compute_class_weights(train_dataset, num_classes)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)
    scaler = torch.amp.GradScaler("cuda")

    best_acc = 0.0
    best_model_state = None

    # ========== STAGE 1: HEAD ONLY ==========
    print(f"\n--- STAGE 1: Training classifier head ({stage1_epochs} epochs, lr={stage1_lr}) ---")
    for param in model.features.parameters():
        param.requires_grad = False
    for param in model.classifier.parameters():
        param.requires_grad = True

    optimizer = optim.AdamW(model.classifier.parameters(), lr=stage1_lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=1)

    for epoch in range(stage1_epochs):
        start = time.time()
        model.train()
        running_loss, running_corrects, total_train = 0.0, 0, 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            with torch.amp.autocast(device_type="cuda"):
                outputs = model(inputs)
                loss = criterion(outputs, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_train += inputs.size(0)

        epoch_loss = running_loss / total_train
        epoch_acc = running_corrects.double() / total_train

        model.eval()
        val_corrects, val_total = 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                with torch.amp.autocast(device_type="cuda"):
                    outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)
                val_total += inputs.size(0)

        val_acc = val_corrects.double() / val_total
        elapsed = time.time() - start
        scheduler.step(val_acc)

        print(f"  S1 Epoch {epoch+1}/{stage1_epochs} | Loss: {epoch_loss:.4f} | "
              f"Train: {epoch_acc:.4f} | Val: {val_acc:.4f} | Time: {elapsed:.1f}s",
              flush=True)

        if val_acc > best_acc:
            best_acc = val_acc
            best_model_state = copy.deepcopy(model.state_dict())
            print(f"  *** NEW BEST: {best_acc:.4f} -- Saved! ***", flush=True)

    # ========== STAGE 2: FULL FINE-TUNING ==========
    print(f"\n--- STAGE 2: Full fine-tuning ({stage2_epochs} epochs, lr={stage2_lr}) ---", flush=True)
    for param in model.parameters():
        param.requires_grad = True

    optimizer = optim.AdamW(model.parameters(), lr=stage2_lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=stage2_epochs, eta_min=1e-7)

    patience = 7
    no_improve = 0

    for epoch in range(stage2_epochs):
        start = time.time()
        model.train()
        running_loss, running_corrects, total_train = 0.0, 0, 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            with torch.amp.autocast(device_type="cuda"):
                outputs = model(inputs)
                loss = criterion(outputs, labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_train += inputs.size(0)

        epoch_loss = running_loss / total_train
        epoch_acc = running_corrects.double() / total_train

        model.eval()
        val_corrects, val_total = 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                with torch.amp.autocast(device_type="cuda"):
                    outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)
                val_total += inputs.size(0)

        val_acc = val_corrects.double() / val_total
        elapsed = time.time() - start
        scheduler.step()

        print(f"  S2 Epoch {epoch+1}/{stage2_epochs} | Loss: {epoch_loss:.4f} | "
              f"Train: {epoch_acc:.4f} | Val: {val_acc:.4f} | Time: {elapsed:.1f}s",
              flush=True)

        if val_acc > best_acc:
            best_acc = val_acc
            best_model_state = copy.deepcopy(model.state_dict())
            no_improve = 0
            print(f"  *** NEW BEST: {best_acc:.4f} -- Saved! ***", flush=True)
        else:
            no_improve += 1
            if no_improve >= patience:
                print(f"  Early stopping after {patience} epochs without improvement.")
                break

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torch.save({"model_state_dict": best_model_state, "classes": class_names}, output_path)
    print(f"\nFinished {name}. Best Val Accuracy: {best_acc:.4f}")
    print(f"Model saved to: {output_path}")

    # Free GPU memory before next model
    del model, optimizer, scaler, criterion
    torch.cuda.empty_cache()

    return best_acc


if __name__ == "__main__":
    print("=" * 70)
    print("BREED MODEL RETRAINING (batch_size=8 for RTX 4050)")
    print("=" * 70)

    results = {}
    for config in MODELS_TO_TRAIN:
        acc = train_single_model(config)
        results[config["name"]] = acc

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE -- SUMMARY")
    print("=" * 70)
    for name, acc in results.items():
        print(f"  {name}: {acc:.4f} ({acc*100:.1f}%)")
    print("\nRestart the backend API to use the new models!")
