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

predictions_path = (
    project_folder
    / "data"
    / "customer_churn_predictions.csv"
)

output_path = (
    project_folder
    / "data"
    / "customer_retention_recommendations.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

original = pd.read_csv(original_path)

predictions = pd.read_csv(predictions_path)


print("Original customer data:", original.shape)

print(
    "Prediction data:",
    predictions.shape
)


# ============================================================
# CREATE CUSTOMER INFORMATION
# ============================================================

# The preprocessing removed rows with invalid TotalCharges.
# Keep only the same valid rows used by the model.

original["TotalCharges_numeric"] = pd.to_numeric(
    original["TotalCharges"],
    errors="coerce"
)

original = original[
    original["TotalCharges_numeric"].notna()
].copy()


# ============================================================
# VERIFY ROW COUNT
# ============================================================

if len(original) != len(predictions):

    raise ValueError(
        f"Customer count mismatch!\n"
        f"Original valid customers: {len(original)}\n"
        f"Predictions: {len(predictions)}"
    )


# ============================================================
# USE REAL CUSTOMER IDs
# ============================================================

customer_info = original[
    [
        "customerID",
        "tenure",
        "MonthlyCharges",
        "Contract",
        "InternetService",
        "OnlineSecurity",
        "TechSupport",
        "PaymentMethod",
        "PaperlessBilling",
        "OnlineBackup",
        "DeviceProtection"
    ]
].copy()


customer_info = customer_info.rename(
    columns={
        "customerID": "Customer_ID"
    }
)


# ============================================================
# COMBINE WITH PREDICTIONS
# ============================================================

results = customer_info.copy()

results["Churn_Probability"] = (
    predictions["Churn_Probability"].values
)

results["Prediction"] = (
    predictions["Prediction"].values
)

results["Risk_Level"] = (
    predictions["Risk_Level"].values
)


# ============================================================
# RETENTION RECOMMENDATION FUNCTION
# ============================================================

def generate_recommendation(row):

    recommendations = []


    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    if row["Risk_Level"] == "High":

        # Contract
        if row["Contract"] == "Month-to-month":

            recommendations.append(
                "Offer a discount or incentive "
                "for upgrading to a long-term contract."
            )


        # Monthly charges
        if row["MonthlyCharges"] >= 80:

            recommendations.append(
                "Provide a personalized pricing "
                "or loyalty discount."
            )


        # Tenure
        if row["tenure"] <= 12:

            recommendations.append(
                "Provide an early-tenure loyalty "
                "benefit to encourage retention."
            )


        # Internet service
        if row["InternetService"] == "Fiber optic":

            recommendations.append(
                "Review fiber service pricing and "
                "offer a suitable service package."
            )


        # Security
        if row["OnlineSecurity"] == "No":

            recommendations.append(
                "Offer an Online Security package "
                "or bundled service."
            )


        # Technical support
        if row["TechSupport"] == "No":

            recommendations.append(
                "Offer technical support assistance "
                "or a support bundle."
            )


        # Payment method
        if row["PaymentMethod"] == "Electronic check":

            recommendations.append(
                "Encourage automatic payment enrollment "
                "with a suitable incentive."
            )


        # Backup / device protection
        if row["OnlineBackup"] == "No":

            recommendations.append(
                "Offer an Online Backup service bundle."
            )


        if row["DeviceProtection"] == "No":

            recommendations.append(
                "Offer a device protection package."
            )


    # --------------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------------

    elif row["Risk_Level"] == "Medium":

        recommendations.append(
            "Send a personalized engagement offer "
            "and monitor customer activity."
        )

        if row["Contract"] == "Month-to-month":

            recommendations.append(
                "Promote benefits of switching "
                "to a longer-term contract."
            )


        if row["MonthlyCharges"] >= 80:

            recommendations.append(
                "Review pricing and provide a "
                "loyalty offer if appropriate."
            )


    # --------------------------------------------------------
    # LOW RISK
    # --------------------------------------------------------

    else:

        recommendations.append(
            "Maintain regular customer engagement "
            "and loyalty communication."
        )


    # --------------------------------------------------------
    # RETURN MULTIPLE ACTIONS
    # --------------------------------------------------------

    return " ".join(
        recommendations
    )


# ============================================================
# GENERATE RECOMMENDATIONS
# ============================================================

print(
    "\nGenerating retention recommendations..."
)


results["Retention_Recommendation"] = (
    results.apply(
        generate_recommendation,
        axis=1
    )
)


# ============================================================
# PRIORITY
# ============================================================

def priority_level(risk):

    if risk == "High":
        return "Immediate"

    elif risk == "Medium":
        return "Monitor"

    else:
        return "Normal"


results["Retention_Priority"] = (
    results["Risk_Level"].apply(
        priority_level
    )
)


# ============================================================
# SORT CUSTOMERS
# ============================================================

results = results.sort_values(
    by="Churn_Probability",
    ascending=False
)


# ============================================================
# SAVE RESULTS
# ============================================================

results.to_csv(
    output_path,
    index=False
)


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print("\n===================================")
print("RETENTION RECOMMENDATION ENGINE")
print("===================================")

print(
    "Total customers:",
    len(results)
)

print(
    "Immediate action:",
    (
        results["Retention_Priority"]
        == "Immediate"
    ).sum()
)

print(
    "Monitor:",
    (
        results["Retention_Priority"]
        == "Monitor"
    ).sum()
)

print(
    "Normal:",
    (
        results["Retention_Priority"]
        == "Normal"
    ).sum()
)


print("\nTop 10 high-priority customers:")

print(
    results[
        [
            "Customer_ID",
            "Churn_Probability",
            "Risk_Level",
            "Retention_Priority",
            "Retention_Recommendation"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\n===================================")
print("RECOMMENDATIONS SAVED")
print("===================================")

print(output_path)