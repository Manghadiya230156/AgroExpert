"""Train a MobileNetV3-Small classifier on PlantVillage-style ImageFolder data.

Expected input: data/PlantVillage/<class_name>/*.(jpg|jpeg|png)
For best evaluation, use the original non-augmented PlantVillage images, not a
pre-augmented mirror with transformed copies split across train/test.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader, Subset
from torchvision import datasets, models, transforms
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

IMAGE_SIZE = 224
SEED = 42

class TransformSubset(Dataset):
    def __init__(self, base, indices, transform):
        self.base, self.indices, self.transform = base, indices, transform
    def __len__(self): return len(self.indices)
    def __getitem__(self, i):
        image, label = self.base[self.indices[i]]
        return self.transform(image), label

def stratified_indices(targets, seed=SEED):
    rng = random.Random(seed)
    by_class = {}
    for i, label in enumerate(targets): by_class.setdefault(int(label), []).append(i)
    train, val, test = [], [], []
    for indices in by_class.values():
        rng.shuffle(indices)
        n = len(indices)
        n_test = max(1, round(n * 0.15))
        n_val = max(1, round(n * 0.10))
        if n_test + n_val >= n: n_test, n_val = 1, 1
        test.extend(indices[:n_test])
        val.extend(indices[n_test:n_test+n_val])
        train.extend(indices[n_test+n_val:])
    rng.shuffle(train); rng.shuffle(val); rng.shuffle(test)
    return train, val, test

def run_epoch(model, loader, criterion, optimizer, device):
    train = optimizer is not None
    model.train(train)
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        if train: optimizer.zero_grad(set_to_none=True)
        with torch.set_grad_enabled(train):
            logits = model(images)
            loss = criterion(logits, labels)
            if train: loss.backward(); optimizer.step()
        total_loss += loss.item() * labels.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        total += labels.size(0)
    return total_loss / max(total, 1), correct / max(total, 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data/PlantVillage', help='ImageFolder root containing one subfolder per class')
    parser.add_argument('--output', default='../../agroexpert_backend/core/ml_model', help='Output model directory')
    parser.add_argument('--epochs', type=int, default=12)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--no-pretrained', action='store_true', help='Do not download pretrained ImageNet weights')
    args = parser.parse_args()
    torch.manual_seed(SEED); np.random.seed(SEED); random.seed(SEED)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(SEED)
    data_path = Path(args.data).resolve()
    if not data_path.exists(): raise SystemExit(f'Dataset directory not found: {data_path}')

    base = datasets.ImageFolder(str(data_path))
    if len(base.classes) < 2: raise SystemExit('Expected at least two class subfolders.')
    print(f'Images: {len(base)} | Classes: {len(base.classes)}')
    train_idx, val_idx, test_idx = stratified_indices(base.targets)
    train_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(), transforms.RandomRotation(12),
        transforms.ColorJitter(brightness=0.12, contrast=0.12, saturation=0.10),
        transforms.ToTensor(),
        transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225)),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)), transforms.ToTensor(),
        transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225)),
    ])
    train_ds = TransformSubset(base, train_idx, train_tf)
    val_ds = TransformSubset(base, val_idx, eval_tf)
    test_ds = TransformSubset(base, test_idx, eval_tf)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device:', device)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.workers, pin_memory=device.type=='cuda')
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.workers)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.workers)

    weights = None if args.no_pretrained else models.MobileNet_V3_Small_Weights.DEFAULT
    model = models.mobilenet_v3_small(weights=weights)
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, len(base.classes))
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)
    best_val, best_state = -1, None
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = run_epoch(model, train_loader, criterion, optimizer, device)
        va_loss, va_acc = run_epoch(model, val_loader, criterion, None, device)
        scheduler.step(va_acc)
        print(f'Epoch {epoch:02d}/{args.epochs} | train loss {tr_loss:.4f} acc {tr_acc:.4f} | val loss {va_loss:.4f} acc {va_acc:.4f}')
        if va_acc > best_val:
            best_val = va_acc
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    all_y, all_pred = [], []
    with torch.inference_mode():
        for images, labels in test_loader:
            pred = model(images.to(device)).argmax(1).cpu().tolist()
            all_pred.extend(pred); all_y.extend(labels.tolist())
    print('\nHeld-out test accuracy:', round(accuracy_score(all_y, all_pred), 4))
    print(classification_report(all_y, all_pred, labels=list(range(len(base.classes))), target_names=base.classes, zero_division=0))
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    torch.save({'model_state_dict': model.state_dict(), 'image_size': IMAGE_SIZE, 'architecture': 'mobilenet_v3_small', 'test_accuracy': float(accuracy_score(all_y, all_pred)), 'seed': SEED}, out/'plant_disease_model.pth')
    (out/'plant_disease_classes.json').write_text(json.dumps(base.classes, indent=2), encoding='utf-8')
    (out/'plant_disease_metrics.json').write_text(json.dumps({'test_accuracy': float(accuracy_score(all_y, all_pred)), 'class_names': base.classes, 'confusion_matrix': confusion_matrix(all_y, all_pred).tolist()}, indent=2), encoding='utf-8')
    print('Saved model and labels to:', out)

if __name__ == '__main__': main()
