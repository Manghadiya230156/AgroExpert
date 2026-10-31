# AgroExpert plant disease model integration

The trained MobileNetV3-Small model and class labels have been placed in:
`agroexpert_backend/core/ml_model/`

Files:
- `plant_disease_model.pth`
- `plant_disease_classes.json`
- `plant_disease_metadata.json`

## Run locally (Windows)
1. Create/activate your existing virtual environment.
2. From the folder containing `requirements.txt`, install dependencies: `pip install -r requirements.txt`.
3. In `agroexpert_backend`, run `python manage.py check`.
4. Run `python manage.py runserver` and sign in.
5. Open `/plant-disease/`, upload a clear leaf photo, and click Analyze Leaf.

The classifier was evaluated on a sampled PlantVillage test set: accuracy 91.54%, macro F1 91.59%, weighted F1 91.59% (3,900 test images across 39 classes). These metrics do not guarantee similar performance on real farm photographs. Model confidence is a score, not a calibrated probability.
