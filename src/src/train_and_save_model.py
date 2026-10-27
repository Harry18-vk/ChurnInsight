import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# Project folder
project_folder = Path(__file__).resolve().parent.parent.parent

# Paths
dataset_path = project_folder / "data" / "cleaned_customer_churn.csv"
models_folder = project_folder / "models"

# Create models folder if it doesn't exist
models_folder.mkdir(exist_ok=True)


# Load dataset
data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Shape:", data.shape)


# Encode categorical variables
data_encoded = pd.get_dummies(
    data,
    columns=[
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
    ],
    drop_first=True
)


# Convert target
data_encoded["Churn"] = data_encoded["Churn"].map({
    "Yes": 1,
    "No": 0
})


# Features and target
X = data_encoded.drop("Churn", axis=1)
y = data_encoded["Churn"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Scale features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)


# Train final Logistic Regression model
model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

model.fit(X_train_scaled, y_train)


# Save model and scaler
model_path = models_folder / "churn_model.pkl"
scaler_path = models_folder / "scaler.pkl"

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)


# Save feature names
feature_path = models_folder / "feature_names.pkl"
joblib.dump(X.columns.tolist(), feature_path)


print("\n===================================")
print("MODEL SAVING COMPLETED")
print("===================================")

print("Model saved at:")
print(model_path)

print("\nScaler saved at:")
print(scaler_path)

print("\nFeature names saved at:")
print(feature_path)

print("\nFinal Logistic Regression model is ready!")