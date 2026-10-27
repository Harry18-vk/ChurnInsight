import pandas as pd
from pathlib import Path

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Dataset path
dataset_path = project_folder / "data" / "customer_churn.csv"

# Load dataset
data = pd.read_csv(dataset_path)

print("Original shape:", data.shape)

# Remove unnecessary customer ID
data = data.drop(columns=["customerID"])

# Convert TotalCharges from text to numeric
data["TotalCharges"] = pd.to_numeric(
    data["TotalCharges"],
    errors="coerce"
)

# Check missing values created during conversion
print("\nMissing values after converting TotalCharges:")
print(data.isnull().sum())

# Remove rows where TotalCharges is missing
data = data.dropna(subset=["TotalCharges"])

print("\nShape after cleaning:", data.shape)

# Save cleaned dataset
cleaned_path = project_folder / "data" / "cleaned_customer_churn.csv"

data.to_csv(cleaned_path, index=False)

print("\nCleaned dataset saved successfully!")
print(cleaned_path)