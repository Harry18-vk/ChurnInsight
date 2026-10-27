import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

original_path = (
    project_folder
    / "data"
    / "customer_churn.csv"
)

cleaned_path = (
    project_folder
    / "data"
    / "cleaned_customer_churn.csv"
)

mapping_path = (
    project_folder
    / "data"
    / "customer_id_mapping.csv"
)


# ============================================================
# LOAD DATASETS
# ============================================================

original = pd.read_csv(original_path)

cleaned = pd.read_csv(cleaned_path)


print("Original dataset:", original.shape)
print("Cleaned dataset:", cleaned.shape)


# ============================================================
# IDENTIFY VALID ROWS
# ============================================================

# TotalCharges contained blank values in the original dataset.
# These rows were removed during preprocessing.

original["TotalCharges_numeric"] = pd.to_numeric(
    original["TotalCharges"],
    errors="coerce"
)

valid_rows = original[
    original["TotalCharges_numeric"].notna()
].copy()


# ============================================================
# VERIFY ROW COUNT
# ============================================================

if len(valid_rows) != len(cleaned):

    raise ValueError(
        f"Row mismatch!\n"
        f"Valid original rows: {len(valid_rows)}\n"
        f"Cleaned rows: {len(cleaned)}"
    )


# ============================================================
# CREATE CUSTOMER ID MAPPING
# ============================================================

mapping = pd.DataFrame({
    "Customer_ID": valid_rows["customerID"].values
})


# Keep original row number for traceability
mapping["Original_Row"] = (
    valid_rows.index + 2
)


# ============================================================
# SAVE MAPPING
# ============================================================

mapping.to_csv(
    mapping_path,
    index=False
)


# ============================================================
# RESULT
# ============================================================

print("\n===================================")
print("CUSTOMER ID MAPPING CREATED")
print("===================================")

print("Total customer IDs:", len(mapping))

print("\nFirst 10 customer IDs:")

print(
    mapping.head(10).to_string(index=False)
)

print("\nSaved to:")

print(mapping_path)

print("\n===================================")
print("COMPLETED SUCCESSFULLY")
print("===================================")