# AgroExpert 🌱

AI-powered agriculture expert system built using Django, HTML, CSS, JavaScript, and Machine Learning.

## Features

- Crop Recommendation
- Fertilizer Suggestion
- Yield Prediction
- Weather Information
- Soil Test Requests
- Admin Dashboard
- User Authentication

## Technologies Used

- Django
- Python
- HTML5
- CSS3
- JavaScript
- Machine Learning

## Project Structure

```bash
AgroExpert/
│
├── agroexpert_backend/
├── ml_models/
├── static/
├── templates/
└── manage.py
```

## Installation

```bash
git clone https://github.com/Manghadiya230156/AgroExpert.git
cd AgroExpert
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
python manage.py runserver
```

## Future Improvements

- Live Weather API
- Better UI/UX
- Mobile Responsive Design
- Cloud Deployment
- AI Chatbot Support

## Contributors

- Man Ghadiya
- Hemal Parmar



## New: Plant Disease Detection (7th-semester minor-project extension)

A new authenticated `/plant-disease/` page lets users upload a crop-leaf photo and receive a MobileNetV3-Small class prediction with explanation and general prevention guidance. The trained model is not included because the public dataset is large; see `ml_models/plant_disease/README.md` to download PlantVillage and train it. Until training produces `plant_disease_model.pth` and `plant_disease_classes.json`, the page intentionally shows a setup message instead of a fake prediction.
