import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

diabetes_model = joblib.load(os.path.join(BASE_DIR, "ml_models", "diabetes.pkl"))
heart_model = joblib.load(os.path.join(BASE_DIR, "ml_models", "heart.pkl"))
kidney_model = joblib.load(os.path.join(BASE_DIR, "ml_models", "kidney.pkl"))