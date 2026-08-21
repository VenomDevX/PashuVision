import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

# ============================================================
# ADVANCED EFFICIENTNET-B4 TRAINING SCRIPT
# Supports Mixed Precision (AMP), Cosine Annealing, and Early Stopping
# ============================================================

# Configuration (Change dataset path to either Species_Dataset or Breed datasets)
DATASET_DIR = r"E:\#SIH 2026\Datasets\Processed\Species_Dataset" 
OUTPUT_MODEL = r"E:\#SIH 2026\Models\Livestock_Models\best_species_model_v2.pth"

BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 1e-4

def train_model():
    # 1. Device Configuration
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 2. Advanced Data Augmentation & Normalization
    train_transform = transforms.Compose([
        transforms.Resize((380, 380)), # EfficientNet-B4 expects 380x380
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((380, 380)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Load dataset (assuming an 80/20 train/val split structure)
    train_dir = os.path.join(DATASET_DIR, 'train')
    val_dir = os.path.join(DATASET_DIR, 'val')
    
    if not os.path.exists(val_dir):
        # Fallback: Just use train dir for demonstration if val doesn't exist
        print("Warning: No 'val' folder found. Using 'train' for both for demonstration.")
        val_dir = train_dir
        
    train_data = datasets.ImageFolder(train_dir, transform=train_transform)
    val_data = datasets.ImageFolder(val_dir, transform=val_transform)
    
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)
    
    class_names = train_data.classes
    print(f"Classes found ({len(class_names)}): {class_names}")

    # 3. Model Architecture (EfficientNet-B4)
    model = models.efficientnet_b4(weights=models.EfficientNet_B4_Weights.DEFAULT)
    
    # Freeze lower layers
    for param in model.parameters():
        param.requires_grad = False
        
    # Unfreeze top layers for fine-tuning
    for param in model.features[-2:].parameters():
        param.requires_grad = True
        
    # Replace classifier head
    num_ftrs = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(num_ftrs, len(class_names))
    )
    
    model = model.to(device)
    
    # 4. Optimization strategy
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
    scaler = torch.amp.GradScaler('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 5. Training Loop
    best_acc = 0.0
    
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        print("-" * 10)
        
        # Train
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            # Mixed Precision
            with torch.amp.autocast(device_type='cuda' if torch.cuda.is_available() else 'cpu'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
        epoch_loss = running_loss / len(train_data)
        epoch_acc = running_corrects.double() / len(train_data)
        
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                
        epoch_val_loss = val_loss / len(val_data)
        epoch_val_acc = val_corrects.double() / len(val_data)
        
        print(f"Val Loss: {epoch_val_loss:.4f} Acc: {epoch_val_acc:.4f}")
        
        scheduler.step()
        
        # Save best model
        if epoch_val_acc > best_acc:
            best_acc = epoch_val_acc
            print(f"*** Saving new best model with Acc: {best_acc:.4f} ***")
            os.makedirs(os.path.dirname(OUTPUT_MODEL), exist_ok=True)
            torch.save({
                'model_state_dict': model.state_dict(),
                'class_names': class_names
            }, OUTPUT_MODEL)
            
    print(f"\nTraining Complete. Best Validation Accuracy: {best_acc:.4f}")

if __name__ == "__main__":
    train_model()
