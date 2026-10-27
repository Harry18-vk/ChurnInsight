import pandas as pd
from pathlib import Path

# Find the project folder automatically
project_folder = Path(__file__).resolve().parent.parent

# Location of the dataset
dataset_path = project_folder / "data" / "customer_churn.csv"

print("Looking for dataset at:")
print(dataset_path)
print()

# Check whether the file exists
if not dataset_path.exists():
    print("ERROR: Dataset file was not found.")
    print("Please check that customer_churn.csv is inside the data folder.")
else:
    data = pd.read_csv(dataset_path)

    print("Dataset loaded successfully!")
    print()

    print("Number of rows:", data.shape[0])
    print("Number of columns:", data.shape[1])
    print()

    print("Columns:")
    print(data.columns.tolist())
    print()

    print("First 5 customers:")
    print(data.head())