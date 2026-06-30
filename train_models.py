import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# -------------------------
# Create ml_models folder
# -------------------------

os.makedirs("ml_models", exist_ok=True)

# ===========================================================
# DIABETES MODEL
# ===========================================================

print("Training Diabetes Model...")

df = pd.read_csv("datasets/diabetes.csv")

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Diabetes Accuracy :", accuracy_score(y_test, pred))

joblib.dump(model, "ml_models/diabetes.pkl")

# ===========================================================
# HEART MODEL
# ===========================================================

print("Training Heart Disease Model...")

df = pd.read_csv("datasets/heart.csv")

X = df.drop("condition", axis=1)
y = df["condition"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Heart Accuracy :", accuracy_score(y_test, pred))

joblib.dump(model, "ml_models/heart.pkl")

# ===========================================================
# KIDNEY MODEL
# ===========================================================

print("Training Kidney Disease Model...")

df = pd.read_csv("datasets/kidney.csv")

# Remove ID column
df = df.drop("id", axis=1)

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Clean string values
for col in df.columns:

    if df[col].dtype == object:

        df[col] = df[col].astype(str).str.strip()

# Encode all categorical columns
encoders = {}

for col in df.columns:

    if df[col].dtype == object:

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col].astype(str))

        encoders[col] = le

X = df.drop("classification", axis=1)
y = df["classification"]

imputer = SimpleImputer(strategy="most_frequent")

X = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Kidney Accuracy :", accuracy_score(y_test, pred))

joblib.dump(model, "ml_models/kidney.pkl")

print("\n====================================")
print("All Models Trained Successfully")
print("====================================")