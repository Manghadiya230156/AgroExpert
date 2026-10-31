# 🌱 AgroExpert – AI-Powered Smart Agriculture Platform

**An intelligent agriculture platform designed to help farmers make data-driven decisions using Machine Learning, Deep Learning, and real-time agricultural information.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Django-Backend-092E20?logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange" alt="Machine Learning">
  <img src="https://img.shields.io/badge/Deep%20Learning-PyTorch-red?logo=pytorch" alt="PyTorch">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Academic%20Project-success" alt="Project Status">
</p>

---

## 📌 About the Project

**AgroExpert** is an AI-powered smart agriculture web application developed to support farmers through intelligent agricultural recommendations and information.

The platform integrates Machine Learning and Deep Learning techniques with a Django-based web application to provide crop recommendations, fertilizer suggestions, plant disease identification, market price information, and other agricultural services.

The main objective is to make agricultural decision-making more accessible, informative, and data-driven.

## ✨ Key Features

### 🌾 1. Crop Recommendation
- Recommends suitable crops based on agricultural input parameters.
- Uses Machine Learning for crop suitability prediction.
- Helps users make informed crop-selection decisions.

### 🧪 2. Fertilizer Recommendation
- Provides fertilizer recommendations based on input parameters.
- Uses a trained Machine Learning model.
- Helps support better fertilizer selection.

### 🍃 3. Plant Disease Detection
- Identifies plant diseases from uploaded leaf images.
- Uses a MobileNetV3-Small-based Deep Learning model.
- Displays disease-related information, explanations, and prevention guidance.
- Includes a plant disease knowledge module.

### 📊 4. Market Price Insights
- Integrates agricultural market price information through the data.gov.in API.
- Uses AGMARKNET-related market data.
- Supports market price discovery for agricultural commodities.
- Uses database caching to reduce repeated API requests.

### 🌦️ 5. Weather Information
- Provides a dedicated weather information interface within the platform.

### 🌱 6. Soil Testing
- Provides a soil testing request interface.
- Allows users to submit soil-related information.
- Includes administrative request management.

### 🏛️ 7. Government Schemes
- Provides information about agricultural government schemes.
- Helps users discover relevant agricultural support programs.

### 👨‍🌾 8. User and Admin Management
- User registration and login.
- User profile management.
- Administrative dashboard.
- User and soil request management.
- Contact and inquiry management.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Deep Learning | PyTorch, Torchvision |
| Data Processing | Pandas, NumPy |
| Image Processing | Pillow |
| Model Storage | Joblib, PyTorch model files |
| External Data Source | data.gov.in / AGMARKNET |
| Deployment Support | Render |

## 🧠 Machine Learning & Deep Learning

AgroExpert integrates trained models into its Django application to provide intelligent agricultural functionality.

### Crop Recommendation
- Machine Learning-based crop suitability prediction.
- Uses agricultural input parameters.

### Fertilizer Recommendation
- Machine Learning-based fertilizer recommendation.

### Plant Disease Detection
- Architecture: MobileNetV3-Small.
- Framework: PyTorch.
- Input: Plant leaf images.
- Output: Predicted disease class and related guidance.

The trained plant disease model and its associated metadata are maintained in the project repository.

## 🏗️ Project Architecture

```text
AgroExpert/
│
├── agroexpert_backend/
│   ├── agroexpert_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── core/
│   │   ├── migrations/
│   │   ├── ml_model/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── plant_disease.py
│   │   └── plant_disease_knowledge.py
│   │
│   └── manage.py
│
├── ml_models/
│   └── plant_disease/
│       ├── train.py
│       ├── README.md
│       └── requirements-training.txt
│
├── README.md
├── requirements.txt
├── runtime.txt
├── build.sh
├── setup_windows.bat
├── .gitignore
│
├── MARKET_PRICE_SETUP.md
└── MODEL_INTEGRATION_README.md
```

## ⚙️ Installation and Setup

Follow these steps to run AgroExpert locally.

### Prerequisites

- Python 3.10 or compatible version.
- Git.
- pip package manager.

### 1. Clone the Repository

```bash
git clone https://github.com/Manghadiya230156/AgroExpert.git
```

```bash
cd AgroExpert
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set the required environment variables before running the application.

**Windows CMD:**

```cmd
set DATA_GOV_IN_API_KEY=your_data_gov_api_key
set DJANGO_SECRET_KEY=your_django_secret_key
set DJANGO_DEBUG=1
```

For production deployment, configure these values through your hosting provider's environment settings.

Never commit actual API keys, passwords, or production secrets to GitHub.

For Market Price Insights configuration, refer to:

`MARKET_PRICE_SETUP.md`

### 5. Apply Database Migrations

```bash
cd agroexpert_backend
python manage.py migrate
```

### 6. Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to create your administrator account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open your browser:

```text
http://127.0.0.1:8000/
```

## 🔑 Environment Configuration

The application uses environment variables for sensitive configuration.

| Variable | Purpose |
|---|---|
| `DATA_GOV_IN_API_KEY` | Access to data.gov.in market data |
| `DJANGO_SECRET_KEY` | Django application security |
| `DJANGO_DEBUG` | Development or production debug mode |
| `DJANGO_ALLOWED_HOSTS` | Allowed application hostnames |

Do not share or upload your real environment configuration file.

## 📁 Important Project Files

| File | Description |
|---|---|
| `core/views.py` | Application views and business logic |
| `core/models.py` | Database models |
| `core/urls.py` | Application URL routing |
| `core/plant_disease.py` | Plant disease model integration |
| `core/plant_disease_knowledge.py` | Disease information and guidance |
| `core/ml_model/` | Integrated ML model artifacts |
| `ml_models/plant_disease/train.py` | Plant disease model training script |
| `requirements.txt` | Application dependencies |
| `MARKET_PRICE_SETUP.md` | Market price API setup documentation |
| `MODEL_INTEGRATION_README.md` | Model integration documentation |

## 🔒 Security Notes

- Keep API keys and secret credentials in environment variables.
- Do not upload `.env` files.
- Do not expose user database files or private information.
- Use `DEBUG=False` in production.
- Configure production `ALLOWED_HOSTS`.
- Use secure production credentials and HTTPS.

## 🚀 Future Enhancements

Potential improvements for future versions include:

- Enhanced crop yield prediction.
- Advanced weather forecasting integration.
- More comprehensive plant disease coverage.
- Multilingual support for regional farmers.
- Improved agricultural market trend analysis.
- Personalized farming recommendations.
- Mobile-friendly farmer dashboard.

## 🎓 Academic Project

**Project Name:** AgroExpert – AI-Powered Smart Agriculture Platform

**Project Type:** Minor Academic Project

**Domain:** Artificial Intelligence, Machine Learning, Deep Learning, and Web Development

**Institution:** Adani University, Ahmedabad, Gujarat, India

## 👨‍💻 Developer

**Man Ghadiya**

B.Tech – Computer Science and Engineering (AI & ML)  
Adani University, Ahmedabad

- GitHub: [@Manghadiya230156](https://github.com/Manghadiya230156)
- Project Repository: [AgroExpert](https://github.com/Manghadiya230156/AgroExpert)

---

<p align="center">
  <b>🌱 AgroExpert – Empowering Agriculture Through Artificial Intelligence.</b>
</p>
