import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from catboost import CatBoostClassifier
import joblib

# 1. Project paths
project_folder = Path(__file__).resolve().parent.parent
data_path = project_folder / "data" / "cleaned_customer_churn.csv"
models_folder = project_folder / "models"
models_folder.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("CATBOOST CUSTOMER CHURN MODEL TRAINING")
print("=" * 50)

# 2. Load dataset
data = pd.read_csv(data_path)
print(f"Loaded dataset: {data.shape[0]} rows, {data.shape[1]} columns")

categorical_columns = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod"
]

# Ensure categorical columns are strings
for col in categorical_columns:
    data[col] = data[col].astype(str)

# Convert target
data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0})

# Features matching the one-hot encoded vector expected by the webapp
data_encoded = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

# Align with feature_names.pkl
feature_names_path = models_folder / "feature_names.pkl"
if feature_names_path.exists():
    expected_features = joblib.load(feature_names_path)
    # Ensure all expected columns exist
    for col in expected_features:
        if col not in data_encoded.columns:
            data_encoded[col] = 0.0
    X = data_encoded[expected_features].astype(float)
else:
    X = data_encoded.drop("Churn", axis=1).astype(float)
    expected_features = list(X.columns)
    joblib.dump(expected_features, feature_names_path)

y = data["Churn"]

# Train/Test Split (80/20 Stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")
print(f"Feature count: {X_train.shape[1]}")

# 3. Train CatBoost with balanced class weight & optimal tree depth
train_dir = project_folder / "models" / "catboost_info"
train_dir.mkdir(parents=True, exist_ok=True)

cb_model = CatBoostClassifier(
    iterations=350,
    learning_rate=0.06,
    depth=6,
    l2_leaf_reg=3,
    loss_function="Logloss",
    eval_metric="AUC",
    auto_class_weights="Balanced",
    random_seed=42,
    train_dir=str(train_dir),
    verbose=50
)

cb_model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    use_best_model=True
)

# 4. Evaluation
y_pred = cb_model.predict(X_test)
y_prob = cb_model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print("\n" + "=" * 50)
print("CATBOOST BENCHMARK RESULTS")
print("=" * 50)
print(f"Accuracy  : {acc * 100:.2f}%")
print(f"Precision : {prec * 100:.2f}%")
print(f"Recall    : {rec * 100:.2f}%")
print(f"F1-Score  : {f1:.4f}")
print(f"ROC-AUC   : {auc:.4f}")
print("=" * 50)

# Save metrics
metrics = {
    "model_name": "CatBoost Classifier",
    "accuracy": round(float(acc * 100), 2),
    "precision": round(float(prec * 100), 2),
    "recall": round(float(rec * 100), 2),
    "f1_score": round(float(f1), 4),
    "roc_auc": round(float(auc), 4),
    "features_count": len(expected_features)
}

metrics_path = models_folder / "catboost_metrics.json"
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

# 5. Save Model
model_out = models_folder / "catboost_churn_model.pkl"
joblib.dump(cb_model, model_out)
print(f"\nModel saved to: {model_out}")
print(f"Metrics saved to: {metrics_path}")
