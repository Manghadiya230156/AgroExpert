# AgroExpert Plant Disease Detection — model training

This folder trains a model from public PlantVillage-style images and the Django app serves the saved checkpoint. The dataset is not bundled in this repository/ZIP because it is large and has separate dataset terms.

## Dataset

Use the PlantVillage dataset, which contains about 54,000 leaf images across 38 crop/disease/healthy classes. Reference: [TensorFlow Datasets PlantVillage catalog](https://www.tensorflow.org/datasets/catalog/plant_village) and [Mendeley Data source](https://data.mendeley.com/datasets/tywbtsjrjv/1).

For a straightforward folder layout, download the **non-augmented/original** images and arrange them like:

```text
ml_models/plant_disease/data/PlantVillage/
  Apple___Apple_scab/
    image1.jpg
  Apple___Black_rot/
    image2.jpg
  Apple___healthy/
    image3.jpg
  ...
```

Each class must be a separate folder. Do not put `train`, `valid`, or `test` folders inside the root unless each split contains the same class folders; this script creates its own stratified 75/10/15 split. Avoid datasets where augmented copies of the same original image have already been placed in different folders/splits; that can inflate reported test performance.

## Train (recommended: Google Colab GPU)

1. Upload or mount the dataset in Colab and set `--data` to the dataset root.
2. Install dependencies:

```bash
pip install -r ml_models/plant_disease/requirements-training.txt
```

3. Run from the `ml_models/plant_disease` directory:

```bash
python train.py --data data/PlantVillage --epochs 12 --batch-size 32
```

The script fine-tunes ImageNet-pretrained MobileNetV3-Small, prints train/validation metrics, evaluates once on a held-out test set, and saves these files to `agroexpert_backend/core/ml_model/`:

- `plant_disease_model.pth`
- `plant_disease_classes.json`
- `plant_disease_metrics.json`

If you run without internet and have no cached ImageNet weights, add `--no-pretrained`; expect training to be slower/less accurate. Do not claim a specific accuracy until your own test run reports it.

## Integrate with Django

Install PyTorch, torchvision, and Pillow in the environment running Django:

```bash
pip install torch torchvision Pillow
```

Then run the usual Django server. The new route is `/plant-disease/` and requires a logged-in user. It accepts JPG/PNG uploads up to 8 MB, predicts a class, and displays an explanation and general prevention guidance. The app will display a setup message if the checkpoint is not present.

## Important limitations

PlantVillage mostly contains leaf images photographed in controlled conditions. Real field images have different lighting, backgrounds, camera quality, and disease stages, so performance can be lower in practice. A confidence score is not a calibrated probability. Use the page as an educational screening aid, not as a definitive diagnosis or pesticide prescription. Validate with field images before making claims about real-world performance.

## Dataset citation

Hughes, D. P., & Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics through machine learning and crowdsourcing.* arXiv:1511.08060.
