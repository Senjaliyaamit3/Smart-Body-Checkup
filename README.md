# Smart Body Checkup

A Django web app that predicts the risk of **Diabetes**, **Heart Disease**, and **Kidney Disease** using machine learning models trained on clinical datasets. Users can register, log in, run a checkup by entering their health parameters, view their prediction history on a dashboard, and download a PDF report of each result.

## Features

- User registration, login, and authentication
- ML-based risk prediction for three diseases (Diabetes, Heart Disease, Kidney Disease)
- Patient dashboard showing prediction count, report count, positive results, and recent checkup history
- Downloadable PDF reports for each prediction (via ReportLab)
- Email notifications on checkup form submission

## Tech Stack

- **Backend:** Django (Python)
- **ML:** scikit-learn models (serialized with joblib) trained on `datasets/diabetes.csv`, `datasets/heart.csv`, `datasets/kidney.csv`
- **PDF generation:** ReportLab
- **Database:** SQLite (development)
- **Frontend:** Django templates, HTML/CSS/JS

## Project Structure

```
BodyCheckupML/
├── bodycheckup/        # Project settings, URLs, WSGI/ASGI
├── prediction/         # Prediction app: ML inference, PDF reports
├── users/              # Auth app: register, login, profile/dashboard
├── datasets/           # Training CSVs
├── ml_models/          # Trained .pkl models
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── train_models.py     # Script to retrain/export the ML models
└── manage.py
```

## Setup (Local Development)

1. Clone the repository
   ```bash
   git clone https://github.com/Senjaliyaamit3/Smart-Body-Checkup.git
   cd Smart-Body-Checkup
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   pip install -r requirements.txt
   ```

3. Create a `.env` file (or set environment variables) for secrets:
   ```
   SECRET_KEY=your-secret-key
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-app-password
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Run the development server
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/`

## Retraining the Models

The `.pkl` models in `ml_models/` were generated from the CSVs in `datasets/`. To retrain:
```bash
python train_models.py
```

## Deployment

Deployed on [Render](https://render.com) using:
- `build.sh` for build/migrate steps
- `gunicorn` as the WSGI server
- `whitenoise` for static file serving

## License

This project is for educational purposes.
