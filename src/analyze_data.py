import pandas as pd
from pathlib import Path

# Find project folder
project_folder = Path(__file__).resolve().parent.parent
dataset_path = project_folder / "data" / "customer_churn.csv"

# Load dataset
data = pd.read_csv(dataset_path)

print("========== DATASET INFORMATION ==========")
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

print("\n========== COLUMN NAMES ==========")
print(data.columns.tolist())

print("\n========== DATA TYPES ==========")
print(data.dtypes)

print("\n========== MISSING VALUES ==========")
print(data.isnull().sum())

print("\n========== CHURN DISTRIBUTION ==========")
print(data["Churn"].value_counts())

print("\n========== FIRST 5 RECORDS ==========")
print(data.head())
print("\n========== TOTAL CHARGES CHECK ==========")

print("Data type:", data["TotalCharges"].dtype)

print("\nSample TotalCharges values:")
print(data["TotalCharges"].head(20).tolist())

print("\nNumber of blank TotalCharges:")
print((data["TotalCharges"].str.strip() == "").sum())
