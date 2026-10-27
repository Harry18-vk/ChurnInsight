import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. PROJECT PATH
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

dataset_path = (
    project_folder
    / "data"
    / "cleaned_customer_churn.csv"
)

models_folder = project_folder / "models"
models_folder.mkdir(exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Shape:", data.shape)


# ============================================================
# 3. KEEP CUSTOMER IDs
# ============================================================

# Customer IDs are useful for showing which customers may churn.
# They are NOT used as a machine-learning feature.

# The cleaned dataset no longer contains customerID,
# so we will use row numbers as customer identifiers.
# Load real customer IDs
mapping_path = (
    project_folder
    / "data"
    / "customer_id_mapping.csv"
)

customer_mapping = pd.read_csv(
    mapping_path
)

customer_ids = customer_mapping[
    "Customer_ID"
].tolist()

# ============================================================
# 4. ENCODE CATEGORICAL VARIABLES
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

data_encoded = pd.get_dummies(
    data,
    columns=categorical_columns,
    drop_first=True
)


# ============================================================
# 5. TARGET
# ============================================================

data_encoded["Churn"] = data_encoded["Churn"].map({
    "Yes": 1,
    "No": 0
})


# ============================================================
# 6. FEATURES + TARGET
# ============================================================

X = data_encoded.drop("Churn", axis=1)
y = data_encoded["Churn"]


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 8. TRAIN FINAL RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ============================================================
# 9. SAVE MODEL
# ============================================================

model_path = models_folder / "best_churn_model.pkl"

joblib.dump(
    model,
    model_path
)


# ============================================================
# 10. SAVE FEATURE NAMES
# ============================================================

feature_path = models_folder / "feature_names.pkl"

joblib.dump(
    X.columns.tolist(),
    feature_path
)


# ============================================================
# 11. CREATE PREDICTIONS FOR ALL CUSTOMERS
# ============================================================

all_probabilities = model.predict_proba(X)[:, 1]

all_predictions = model.predict(X)


# ============================================================
# 12. CREATE CUSTOMER RISK TABLE
# ============================================================

results = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Churn_Probability": all_probabilities,
    "Prediction": all_predictions
})


# Convert prediction to readable text
results["Prediction"] = results["Prediction"].map({
    1: "Yes",
    0: "No"
})


# Risk category
def risk_level(probability):

    if probability >= 0.70:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    else:
        return "Low"


results["Risk_Level"] = results[
    "Churn_Probability"
].apply(risk_level)


# Convert probability to percentage
results["Churn_Probability"] = (
    results["Churn_Probability"] * 100
).round(2)


# Sort highest-risk customers first
results = results.sort_values(
    by="Churn_Probability",
    ascending=False
)


# ============================================================
# 13. SAVE CUSTOMER PREDICTIONS
# ============================================================

predictions_path = (
    project_folder
    / "data"
    / "customer_churn_predictions.csv"
)

results.to_csv(
    predictions_path,
    index=False
)


# ============================================================
# 14. DISPLAY SUMMARY
# ============================================================

print("\n===================================")
print("FINAL MODEL SAVED")
print("===================================")

print("Model:")
print(model_path)

print("\nFeature names:")
print(feature_path)

print("\nCustomer predictions:")
print(predictions_path)

print("\n===================================")
print("CUSTOMER RISK SUMMARY")
print("===================================")

print(
    "Total customers:",
    len(results)
)

print(
    "High-risk customers:",
    (results["Risk_Level"] == "High").sum()
)

print(
    "Medium-risk customers:",
    (results["Risk_Level"] == "Medium").sum()
)

print(
    "Low-risk customers:",
    (results["Risk_Level"] == "Low").sum()
)

print("\nTop 10 customers most likely to churn:")

print(
    results.head(10).to_string(index=False)
)

print("\n===================================")
print("COMPLETED SUCCESSFULLY")
print("===================================")