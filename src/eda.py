import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Load cleaned dataset
dataset_path = project_folder / "data" / "cleaned_customer_churn.csv"
data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Shape:", data.shape)

# -------------------------------
# 1. Churn Distribution
# -------------------------------

print("\n========== CHURN DISTRIBUTION ==========")
print(data["Churn"].value_counts())

print("\nChurn Percentage:")
print(data["Churn"].value_counts(normalize=True) * 100)

plt.figure(figsize=(6, 4))
sns.countplot(data=data, x="Churn")
plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")
plt.show()


# -------------------------------
# 2. Churn vs Contract
# -------------------------------

plt.figure(figsize=(8, 5))
sns.countplot(data=data, x="Contract", hue="Churn")
plt.title("Churn by Contract Type")
plt.xlabel("Contract")
plt.ylabel("Number of Customers")
plt.xticks(rotation=15)
plt.show()


# -------------------------------
# 3. Churn vs Tenure
# -------------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(data=data, x="Churn", y="tenure")
plt.title("Churn vs Customer Tenure")
plt.xlabel("Churn")
plt.ylabel("Tenure (Months)")
plt.show()


# -------------------------------
# 4. Churn vs Monthly Charges
# -------------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(data=data, x="Churn", y="MonthlyCharges")
plt.title("Churn vs Monthly Charges")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")
plt.show()


# -------------------------------
# 5. Churn vs Internet Service
# -------------------------------

plt.figure(figsize=(8, 5))
sns.countplot(data=data, x="InternetService", hue="Churn")
plt.title("Churn by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Number of Customers")
plt.show()


print("\nEDA completed successfully!")
