import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# 1. PROJECT PATH
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

dataset_path = (
    project_folder
    / "data"
    / "cleaned_customer_churn.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

data = pd.read_csv(dataset_path)

print("===================================")
print("CUSTOMER CHURN MODEL OPTIMIZATION")
print("===================================")

print("\nDataset shape:", data.shape)


# ============================================================
# 3. ENCODE CATEGORICAL VARIABLES
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
# 4. CONVERT TARGET
# ============================================================

data_encoded["Churn"] = data_encoded["Churn"].map({
    "Yes": 1,
    "No": 0
})


# ============================================================
# 5. FEATURES AND TARGET
# ============================================================

X = data_encoded.drop("Churn", axis=1)
y = data_encoded["Churn"]


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 7. FEATURE SCALING
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# 8. MODELS
# ============================================================

models = {

    "Logistic Regression": (
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            random_state=42
        ),
        True
    ),

    "Decision Tree": (
        DecisionTreeClassifier(
            max_depth=6,
            min_samples_split=10,
            class_weight="balanced",
            random_state=42
        ),
        False
    ),

    "Random Forest": (
        RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ),
        False
    ),

    "Gradient Boosting": (
        GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        ),
        False
    )
}


# ============================================================
# 9. TRAIN + EVALUATE
# ============================================================

results = []

trained_models = {}


for name, (model, needs_scaling) in models.items():

    print("\n===================================")
    print(name)
    print("===================================")

    if needs_scaling:

        model.fit(
            X_train_scaled,
            y_train
        )

        predictions = model.predict(
            X_test_scaled
        )

        probabilities = model.predict_proba(
            X_test_scaled
        )[:, 1]

    else:

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        probabilities = model.predict_proba(
            X_test
        )[:, 1]


    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )


    print(
        f"Accuracy : {accuracy * 100:.2f}%"
    )

    print(
        f"Precision: {precision * 100:.2f}%"
    )

    print(
        f"Recall   : {recall * 100:.2f}%"
    )

    print(
        f"F1 Score : {f1 * 100:.2f}%"
    )

    print(
        f"ROC-AUC  : {roc_auc * 100:.2f}%"
    )


    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })

    trained_models[name] = model


# ============================================================
# 10. COMPARISON TABLE
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)


print("\n\n===================================")
print("FINAL MODEL COMPARISON")
print("===================================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1 Score": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)


# ============================================================
# 11. BEST MODEL
# ============================================================

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[
    best_model_name
]


print("\n===================================")
print("BEST MODEL")
print("===================================")

print(
    "Selected model:",
    best_model_name
)

print(
    "Selection criterion: Highest F1 Score"
)

print("\nModel optimization completed successfully!")