import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier


# ============================================================
# PROJECT PATH
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

dataset_path = (
    project_folder
    / "data"
    / "cleaned_customer_churn.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(dataset_path)

print("===================================")
print("XGBOOST CUSTOMER CHURN MODEL")
print("===================================")

print("\nDataset shape:", data.shape)


# ============================================================
# ENCODE CATEGORICAL VARIABLES
# ============================================================

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


data = pd.get_dummies(
    data,
    columns=categorical_columns,
    drop_first=True
)


# ============================================================
# TARGET
# ============================================================

data["Churn"] = data["Churn"].map({
    "Yes": 1,
    "No": 0
})


# ============================================================
# FEATURES + TARGET
# ============================================================

X = data.drop(
    "Churn",
    axis=1
)

y = data["Churn"]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# XGBOOST MODEL
# ============================================================

model = XGBClassifier(
    n_estimators=150,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining XGBoost...")

model.fit(
    X_train,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


# ============================================================
# RESULTS
# ============================================================

print("\n===================================")
print("XGBOOST RESULTS")
print("===================================")

print(
    f"Accuracy : {accuracy * 100:.2f}%"
)

print(
    f"Precision: {precision * 100:.2f}%"
)

print(
    f"Recall   : {recall * 100:.2f}%"
)

print(
    f"F1 Score : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC  : {roc_auc * 100:.2f}%"
)


print("\n===================================")
print("XGBOOST COMPLETED")
print("===================================")