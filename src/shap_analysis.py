import pandas as pd
import joblib
import shap

from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

dataset_path = (
    project_folder
    / "data"
    / "cleaned_customer_churn.csv"
)

model_path = (
    project_folder
    / "models"
    / "best_churn_model.pkl"
)

feature_path = (
    project_folder
    / "models"
    / "feature_names.pkl"
)


# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


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

data_encoded = pd.get_dummies(
    data,
    columns=categorical_columns,
    drop_first=True
)


# ============================================================
# TARGET
# ============================================================

data_encoded["Churn"] = data_encoded["Churn"].map({
    "Yes": 1,
    "No": 0
})


# ============================================================
# FEATURES
# ============================================================

X = data_encoded.drop(
    "Churn",
    axis=1
)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(model_path)

feature_names = joblib.load(
    feature_path
)


# Make sure feature order is identical
X = X.reindex(
    columns=feature_names,
    fill_value=0
)


print("\nModel loaded successfully!")
print("Number of features:", len(feature_names))


# ============================================================
# SHAP EXPLAINER
# ============================================================

print("\nCreating SHAP explainer...")

explainer = shap.TreeExplainer(model)

print("SHAP explainer created successfully!")


# ============================================================
# CALCULATE SHAP VALUES
# ============================================================

print("\nCalculating SHAP values...")

# Use a sample for faster analysis
sample_size = min(1000, len(X))

X_sample = X.iloc[:sample_size]

shap_values = explainer.shap_values(
    X_sample
)

print("SHAP values calculated successfully!")


# ============================================================
# HANDLE SHAP OUTPUT
# ============================================================

# ============================================================
# HANDLE SHAP OUTPUT SHAPE
# ============================================================

if isinstance(shap_values, list):

    # Older SHAP versions
    shap_values_for_churn = shap_values[1]

else:

    shap_values_for_churn = shap_values


# Newer SHAP versions may return:
# (samples, features, classes)

if len(shap_values_for_churn.shape) == 3:

    # Select class 1 = Churn
    shap_values_for_churn = shap_values_for_churn[:, :, 1]


print(
    "SHAP value shape:",
    shap_values_for_churn.shape
)



# ============================================================
# GLOBAL FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "Feature": feature_names,
    "Mean_ABS_SHAP": (
        abs(shap_values_for_churn)
        .mean(axis=0)
    )
})


importance = importance.sort_values(
    by="Mean_ABS_SHAP",
    ascending=False
)


print("\n===================================")
print("TOP FEATURES AFFECTING CHURN")
print("===================================")

print(
    importance.head(15).to_string(
        index=False
    )
)


# ============================================================
# SAVE FEATURE IMPORTANCE
# ============================================================

importance_path = (
    project_folder
    / "data"
    / "shap_feature_importance.csv"
)

importance.to_csv(
    importance_path,
    index=False
)


# ============================================================
# INDIVIDUAL CUSTOMER EXPLANATION
# ============================================================

customer_index = 0

customer_data = X.iloc[
    customer_index
    :customer_index + 1
]

customer_shap = shap_values_for_churn[
    customer_index
]


customer_explanation = pd.DataFrame({
    "Feature": feature_names,
    "Feature_Value": customer_data.iloc[0].values,
    "SHAP_Value": customer_shap
})


# Sort by absolute impact
customer_explanation["Absolute_Impact"] = (
    customer_explanation["SHAP_Value"].abs()
)


customer_explanation = customer_explanation.sort_values(
    by="Absolute_Impact",
    ascending=False
)


print("\n===================================")
print("INDIVIDUAL CUSTOMER EXPLANATION")
print("===================================")

print(
    customer_explanation
    .head(10)
    .to_string(index=False)
)


# ============================================================
# SAVE INDIVIDUAL EXPLANATION
# ============================================================

individual_path = (
    project_folder
    / "data"
    / "customer_shap_explanation.csv"
)

customer_explanation.to_csv(
    individual_path,
    index=False
)


# ============================================================
# SHAP SUMMARY PLOT
# ============================================================

print("\nGenerating SHAP summary plot...")

shap.summary_plot(
    shap_values_for_churn,
    X_sample,
    feature_names=feature_names,
    show=True
)


print("\n===================================")
print("SHAP ANALYSIS COMPLETED")
print("===================================")

print(
    "Global explanation saved to:"
)

print(importance_path)

print(
    "\nIndividual explanation saved to:"
)

print(individual_path)