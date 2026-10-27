import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Get the main project folder
project_folder = Path(__file__).resolve().parent.parent.parent

# Load cleaned dataset
dataset_path = project_folder / "data" / "cleaned_customer_churn.csv"
data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Original shape:", data.shape)

# Convert categorical columns into numerical columns
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

# Convert Churn into numerical values
data_encoded["Churn"] = data_encoded["Churn"].map({
    "Yes": 1,
    "No": 0
})

print("\nEncoding completed!")
print("Encoded shape:", data_encoded.shape)

# Separate features and target
X = data_encoded.drop("Churn", axis=1)
y = data_encoded["Churn"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\n========== TRAIN TEST SPLIT ==========")
print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)
print("Training target:", y_train.shape)
print("Testing target:", y_test.shape)

print("\nML preprocessing completed successfully!")