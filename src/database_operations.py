import pandas as pd
import mysql.connector
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

raw_dataset_path = (
    project_folder / "data" / "customer_churn.csv"
)

prediction_path = (
    project_folder / "data" / "customer_churn_predictions.csv"
)


# ============================================================
# MYSQL CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Imakash@12",
    "database": "customer_churn_db"
}



# ============================================================
# CONNECT TO MYSQL
# ============================================================

connection = mysql.connector.connect(
    **DB_CONFIG
)

cursor = connection.cursor()

print("===================================")
print("CUSTOMER CHURN DATABASE IMPORT")
print("===================================")

print("MySQL connected successfully!")


# ============================================================
# LOAD DATASETS
# ============================================================

customers = pd.read_csv(raw_dataset_path)

predictions = pd.read_csv(prediction_path)

print("\nCustomer dataset:", customers.shape)

print("Prediction dataset:", predictions.shape)


# ============================================================
# CLEAN CUSTOMER DATA
# ============================================================

customers["TotalCharges"] = pd.to_numeric(
    customers["TotalCharges"],
    errors="coerce"
)

customers["TotalCharges"] = customers["TotalCharges"].fillna(0)


# ============================================================
# INSERT CUSTOMERS
# ============================================================

customer_sql = """
INSERT INTO customers (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON DUPLICATE KEY UPDATE
    gender = VALUES(gender),
    senior_citizen = VALUES(senior_citizen),
    partner = VALUES(partner),
    dependents = VALUES(dependents),
    tenure = VALUES(tenure),
    phone_service = VALUES(phone_service),
    multiple_lines = VALUES(multiple_lines),
    internet_service = VALUES(internet_service),
    online_security = VALUES(online_security),
    online_backup = VALUES(online_backup),
    device_protection = VALUES(device_protection),
    tech_support = VALUES(tech_support),
    streaming_tv = VALUES(streaming_tv),
    streaming_movies = VALUES(streaming_movies),
    contract = VALUES(contract),
    paperless_billing = VALUES(paperless_billing),
    payment_method = VALUES(payment_method),
    monthly_charges = VALUES(monthly_charges),
    total_charges = VALUES(total_charges)
"""


for _, row in customers.iterrows():

    values = (
        row["customerID"],
        row["gender"],
        int(row["SeniorCitizen"]),
        row["Partner"],
        row["Dependents"],
        int(row["tenure"]),
        row["PhoneService"],
        row["MultipleLines"],
        row["InternetService"],
        row["OnlineSecurity"],
        row["OnlineBackup"],
        row["DeviceProtection"],
        row["TechSupport"],
        row["StreamingTV"],
        row["StreamingMovies"],
        row["Contract"],
        row["PaperlessBilling"],
        row["PaymentMethod"],
        float(row["MonthlyCharges"]),
        float(row["TotalCharges"])
    )

    cursor.execute(customer_sql, values)


connection.commit()

print("\nCustomers imported successfully!")


# ============================================================
# CLEAR OLD PREDICTIONS
# ============================================================

cursor.execute("DELETE FROM predictions")

cursor.execute("DELETE FROM recommendations")

connection.commit()

print("Old predictions cleared.")


# ============================================================
# INSERT PREDICTIONS
# ============================================================

prediction_sql = """
INSERT INTO predictions (
    customer_id,
    churn_probability,
    prediction,
    risk_level
)
VALUES (%s, %s, %s, %s)
"""


recommendation_sql = """
INSERT INTO recommendations (
    customer_id,
    retention_priority,
    recommendation
)
VALUES (%s, %s, %s)
"""


for _, row in predictions.iterrows():

    customer_id = row["Customer_ID"]

    probability = float(
        row["Churn_Probability"]
    )

    prediction = row["Prediction"]

    risk = row["Risk_Level"]


    # Insert prediction

    cursor.execute(
        prediction_sql,
        (
            customer_id,
            probability,
            prediction,
            risk
        )
    )


    # ========================================================
    # RETENTION RECOMMENDATION
    # ========================================================

    if risk == "High":

        priority = "URGENT"

        recommendation = (
            "Contact customer immediately. "
            "Offer personalized retention discount, "
            "contract upgrade, or loyalty benefit."
        )

    elif risk == "Medium":

        priority = "MEDIUM"

        recommendation = (
            "Monitor customer and offer suitable "
            "service improvement or promotional plan."
        )

    else:

        priority = "LOW"

        recommendation = (
            "Maintain regular engagement and "
            "continue monitoring customer satisfaction."
        )


    cursor.execute(
        recommendation_sql,
        (
            customer_id,
            priority,
            recommendation
        )
    )


connection.commit()


# ============================================================
# VERIFY DATABASE
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM customers"
)

customer_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM predictions"
)

prediction_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM recommendations"
)

recommendation_count = cursor.fetchone()[0]


print("\n===================================")
print("DATABASE IMPORT COMPLETED")
print("===================================")

print(
    "Customers:",
    customer_count
)

print(
    "Predictions:",
    prediction_count
)

print(
    "Recommendations:",
    recommendation_count
)


# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()

connection.close()

print("\nMySQL connection closed.")

print("\n===================================")
print("SUCCESS")
print("===================================")