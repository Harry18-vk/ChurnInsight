from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import sys
import os
import io

# ============================================================
# CUSTOMER CHURN AI BACKEND
# ============================================================

print("===================================")
print("CHURNINSIGHT BACKEND")
print("===================================")

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
SRC_FOLDER = PROJECT_FOLDER / "src"
if str(SRC_FOLDER) not in sys.path:
    sys.path.append(str(SRC_FOLDER))

try:
    from smart_retention import generate_smart_retention
except ImportError:
    generate_smart_retention = None

# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
app.secret_key = "churn-ai-enterprise-secret-key-2026"

CORS(app)


# ============================================================
# PROJECT PATHS
# ============================================================

DATA_FOLDER = PROJECT_FOLDER / "data"
MODEL_FOLDER = PROJECT_FOLDER / "models"

MODEL_PATH = MODEL_FOLDER / "best_churn_model.pkl"
FEATURE_PATH = MODEL_FOLDER / "feature_names.pkl"

PREDICTION_PATH = (
    DATA_FOLDER / "customer_churn_predictions.csv"
)
RAW_DATA_PATH = (
    DATA_FOLDER / "customer_churn.csv"
)

# ============================================================
# AUTHENTICATION DECORATOR
# ============================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            if request.path.startswith("/api/"):
                return jsonify({
                    "status": "error",
                    "message": "Authentication required. Please login."
                }), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading model...")

try:

    model = joblib.load(MODEL_PATH)

    feature_names = joblib.load(
        FEATURE_PATH
    )

    print("Model loaded successfully!")
    print("Features:", len(feature_names))

except Exception as e:

    print("MODEL LOADING ERROR:")
    print(e)

    model = None
    feature_names = []


# ============================================================
# REQUIRED RAW DATASET COLUMNS
# ============================================================

REQUIRED_COLUMNS = [

    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
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
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges"

]


# ============================================================
# PREPROCESS DATA (ROBUST ENCODER FOR SINGLE & BATCH)
# ============================================================

def preprocess_data(data):
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    elif not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    records = []
    for _, r in data.iterrows():
        row_dict = {col: 0.0 for col in feature_names}

        # Numeric features
        row_dict["SeniorCitizen"] = float(r.get("SeniorCitizen", 0) or 0)
        tenure_val = float(r.get("tenure", 1) or 1)
        row_dict["tenure"] = tenure_val
        monthly_val = float(r.get("MonthlyCharges", 70.0) or 70.0)
        row_dict["MonthlyCharges"] = monthly_val

        # TotalCharges: if 0 or missing, compute from tenure * monthly
        tc_raw = r.get("TotalCharges", 0)
        try:
            tc_num = float(tc_raw)
            if tc_num <= 0.0 and tenure_val > 0:
                tc_num = monthly_val * tenure_val
        except Exception:
            tc_num = monthly_val * max(tenure_val, 1.0)
        row_dict["TotalCharges"] = tc_num

        # Binary & Categorical Encodings (matching feature_names.pkl exactly)
        if str(r.get("gender", "")).lower() == "male":
            row_dict["gender_Male"] = 1.0
        if str(r.get("Partner", "")).lower() == "yes":
            row_dict["Partner_Yes"] = 1.0
        if str(r.get("Dependents", "")).lower() == "yes":
            row_dict["Dependents_Yes"] = 1.0
        if str(r.get("PhoneService", "")).lower() == "yes":
            row_dict["PhoneService_Yes"] = 1.0

        ml = str(r.get("MultipleLines", ""))
        if ml == "No phone service":
            row_dict["MultipleLines_No phone service"] = 1.0
        elif ml.lower() == "yes":
            row_dict["MultipleLines_Yes"] = 1.0

        inet = str(r.get("InternetService", ""))
        if inet == "Fiber optic":
            row_dict["InternetService_Fiber optic"] = 1.0
        elif inet == "No":
            row_dict["InternetService_No"] = 1.0

        sec = str(r.get("OnlineSecurity", ""))
        if sec == "No internet service":
            row_dict["OnlineSecurity_No internet service"] = 1.0
        elif sec.lower() == "yes":
            row_dict["OnlineSecurity_Yes"] = 1.0

        bk = str(r.get("OnlineBackup", ""))
        if bk == "No internet service":
            row_dict["OnlineBackup_No internet service"] = 1.0
        elif bk.lower() == "yes":
            row_dict["OnlineBackup_Yes"] = 1.0

        dp = str(r.get("DeviceProtection", ""))
        if dp == "No internet service":
            row_dict["DeviceProtection_No internet service"] = 1.0
        elif dp.lower() == "yes":
            row_dict["DeviceProtection_Yes"] = 1.0

        ts = str(r.get("TechSupport", ""))
        if ts == "No internet service":
            row_dict["TechSupport_No internet service"] = 1.0
        elif ts.lower() == "yes":
            row_dict["TechSupport_Yes"] = 1.0

        tv = str(r.get("StreamingTV", ""))
        if tv == "No internet service":
            row_dict["StreamingTV_No internet service"] = 1.0
        elif tv.lower() == "yes":
            row_dict["StreamingTV_Yes"] = 1.0

        mv = str(r.get("StreamingMovies", ""))
        if mv == "No internet service":
            row_dict["StreamingMovies_No internet service"] = 1.0
        elif mv.lower() == "yes":
            row_dict["StreamingMovies_Yes"] = 1.0

        contract = str(r.get("Contract", ""))
        if contract == "One year":
            row_dict["Contract_One year"] = 1.0
        elif contract == "Two year":
            row_dict["Contract_Two year"] = 1.0

        if str(r.get("PaperlessBilling", "")).lower() == "yes":
            row_dict["PaperlessBilling_Yes"] = 1.0

        pm = str(r.get("PaymentMethod", ""))
        if pm == "Credit card (automatic)":
            row_dict["PaymentMethod_Credit card (automatic)"] = 1.0
        elif pm == "Electronic check":
            row_dict["PaymentMethod_Electronic check"] = 1.0
        elif pm == "Mailed check":
            row_dict["PaymentMethod_Mailed check"] = 1.0

        records.append(row_dict)

    X = pd.DataFrame(records)[feature_names].astype(float)
    return X


    # --------------------------------------------------------
    # Convert to numeric
    # --------------------------------------------------------

    X = X.astype(float)


    return X


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(probability):

    if probability >= 70:

        return "High"

    elif probability >= 40:

        return "Medium"

    else:

        return "Low"


# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(risk, customer_data=None):
    if customer_data is not None and generate_smart_retention:
        try:
            strategy = generate_smart_retention(customer_data, risk_level=risk)
            return strategy["specific_offer"]
        except Exception:
            pass

    if risk == "High":
        return (
            "Immediate retention action recommended. "
            "Contact the customer and provide a personalized "
            "retention offer or service improvement."
        )
    elif risk == "Medium":
        return (
            "Monitor customer engagement and consider "
            "a targeted promotional or service offer."
        )
    else:
        return (
            "Maintain regular engagement and continue "
            "monitoring customer satisfaction."
        )


# ============================================================
# AUTHENTICATION & PAGE ROUTES
# ============================================================

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username.lower() == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid admin credentials. Please use admin / admin123")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ============================================================
# DASHBOARD PAGE
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "index.html"
    )


# ============================================================
# DASHBOARD API
# ============================================================

@app.route("/api/dashboard")
def dashboard_api():

    try:

        if not PREDICTION_PATH.exists():

            return jsonify({

                "status": "error",

                "message":
                    "Prediction file not found."

            }), 404


        data = pd.read_csv(
            PREDICTION_PATH
        )


        total_customers = len(data)


        high_risk = int(

            (
                data["Risk_Level"]
                .astype(str)
                .str.lower()
                == "high"
            ).sum()

        )


        medium_risk = int(

            (
                data["Risk_Level"]
                .astype(str)
                .str.lower()
                == "medium"
            ).sum()

        )


        low_risk = int(

            (
                data["Risk_Level"]
                .astype(str)
                .str.lower()
                == "low"
            ).sum()

        )


        predicted_churn = int(

            (
                data["Prediction"]
                .astype(str)
                .str.lower()
                == "yes"
            ).sum()

        )


        average_probability = round(

            data["Churn_Probability"]
            .mean(),

            2

        )


        return jsonify({

            "status": "success",

            "total_customers":
                total_customers,

            "high_risk":
                high_risk,

            "medium_risk":
                medium_risk,

            "low_risk":
                low_risk,

            "predicted_churn":
                predicted_churn,

            "average_probability":
                average_probability

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# CUSTOMERS API
# ============================================================

@app.route("/api/customers")
def customers():

    try:

        if not PREDICTION_PATH.exists():

            return jsonify({

                "status": "error",

                "message":
                    "Prediction file not found."

            }), 404


        data = pd.read_csv(
            PREDICTION_PATH
        )


        search = request.args.get(
            "search",
            ""
        ).strip().lower()


        risk = request.args.get(
            "risk",
            ""
        ).strip().lower()


        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        if search:

            data = data[

                data["Customer_ID"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search,
                    na=False
                )

            ]


        # ----------------------------------------------------
        # Risk filter
        # ----------------------------------------------------

        if risk:

            data = data[

                data["Risk_Level"]
                .astype(str)
                .str.lower()
                == risk

            ]


        # ----------------------------------------------------
        # Sort highest risk first
        # ----------------------------------------------------

        data = data.sort_values(

            "Churn_Probability",

            ascending=False

        )


        # ----------------------------------------------------
        # Limit
        # ----------------------------------------------------

        try:

            limit = int(

                request.args.get(
                    "limit",
                    100
                )

            )

        except:

            limit = 100


        data = data.head(
            limit
        )


        customers_list = []

        # Load raw data lookup for rich personalized recommendations
        raw_lookup = {}
        if RAW_DATA_PATH.exists():
            try:
                raw_df = pd.read_csv(RAW_DATA_PATH)
                raw_lookup = raw_df.set_index("customerID").to_dict(orient="index")
            except Exception:
                pass

        for _, row in data.iterrows():
            cid = str(row["Customer_ID"])
            risk_level = str(row["Risk_Level"])
            c_data = raw_lookup.get(cid, {}).copy()
            c_data["Customer_ID"] = cid
            c_prob = float(row["Churn_Probability"])
            c_data["Churn_Probability"] = c_prob

            smart_ret = {}
            if generate_smart_retention:
                try:
                    smart_ret = generate_smart_retention(c_data, probability=c_prob, risk_level=risk_level)
                except Exception:
                    pass

            offer = smart_ret.get("specific_offer") or get_recommendation(risk_level, customer_data=c_data)
            offer_tag = smart_ret.get("offer_tag") or ("Contract & Credit" if risk_level == "High" else "Monitor & Nurture" if risk_level == "Medium" else "Loyalty Benefit")

            customers_list.append({
                "Customer_ID": cid,
                "Churn_Probability": round(c_prob, 2),
                "Prediction": str(row["Prediction"]),
                "Risk_Level": risk_level,
                "Recommendation": offer,
                "Specific_Offer": offer,
                "Offer_Tag": offer_tag,
                "Strategy_Title": smart_ret.get("strategy_title", "Proactive Care"),
                "Persona": smart_ret.get("persona", "Standard Profile")
            })


        return jsonify({

            "status": "success",

            "count":
                len(customers_list),

            "customers":
                customers_list

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# TOP 10 HIGH-RISK CUSTOMERS
# ============================================================

@app.route("/api/top-risk")
def top_risk():

    try:

        data = pd.read_csv(
            PREDICTION_PATH
        )


        data = data.sort_values(

            "Churn_Probability",

            ascending=False

        ).head(10)


        customers_list = []


        for _, row in data.iterrows():

            customers_list.append({

                "Customer_ID":
                    str(
                        row["Customer_ID"]
                    ),

                "Churn_Probability":
                    round(
                        float(
                            row[
                                "Churn_Probability"
                            ]
                        ),
                        2
                    ),

                "Prediction":
                    str(
                        row["Prediction"]
                    ),

                "Risk_Level":
                    str(
                        row["Risk_Level"]
                    )

            })


        return jsonify({

            "status": "success",

            "customers":
                customers_list

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# SINGLE CUSTOMER
# ============================================================

@app.route("/api/customer/<customer_id>")
def single_customer(customer_id):

    try:
        data = pd.read_csv(PREDICTION_PATH)
        result = data[
            data["Customer_ID"].astype(str).str.lower() == customer_id.lower()
        ]

        if result.empty:
            return jsonify({
                "status": "error",
                "message": "Customer not found."
            }), 404

        row = result.iloc[0]
        risk = str(row["Risk_Level"])
        prob = float(row["Churn_Probability"])

        # Retrieve raw attributes if customer_churn.csv exists
        customer_attr = {}
        if RAW_DATA_PATH.exists():
            try:
                raw_df = pd.read_csv(RAW_DATA_PATH)
                raw_match = raw_df[
                    raw_df["customerID"].astype(str).str.lower() == customer_id.lower()
                ]
                if not raw_match.empty:
                    customer_attr = raw_match.iloc[0].to_dict()
            except Exception as ex:
                print("Error reading raw customer attributes:", ex)

        # Merge prediction info into customer_attr
        full_dict = dict(customer_attr)
        full_dict["Customer_ID"] = str(row["Customer_ID"])
        full_dict["Churn_Probability"] = prob
        full_dict["Risk_Level"] = risk
        full_dict["Prediction"] = str(row["Prediction"])

        smart_ret = {}
        if generate_smart_retention:
            smart_ret = generate_smart_retention(full_dict, probability=prob, risk_level=risk)

        return jsonify({
            "status": "success",
            "customer": {
                "Customer_ID": str(row["Customer_ID"]),
                "Churn_Probability": round(prob, 2),
                "Prediction": str(row["Prediction"]),
                "Risk_Level": risk,
                "Recommendation": smart_ret.get("specific_offer", get_recommendation(risk)),
                "Persona": smart_ret.get("persona", "Standard Customer"),
                "Primary_Driver": smart_ret.get("primary_driver", "Standard service metrics"),
                "Strategy_Title": smart_ret.get("strategy_title", "Proactive Care"),
                "Offer_Tag": smart_ret.get("offer_tag", "Retention Concession"),
                "Specific_Offer": smart_ret.get("specific_offer", get_recommendation(risk)),
                "Actions": smart_ret.get("actions", []),
                "Call_Script": smart_ret.get("call_script", ""),
                "Attributes": customer_attr
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================
# ADD SINGLE NEW CUSTOMER (LIVE INFERENCE)
# ============================================================

@app.route("/api/add-customer", methods=["POST"])
def add_customer():
    try:
        req_data = request.get_json(silent=True) or request.form.to_dict()
        if not req_data:
            return jsonify({"status": "error", "message": "No customer data received."}), 400

        cid = str(req_data.get("customerID") or req_data.get("Customer_ID") or f"CUST-{np.random.randint(10000, 99999)}").strip()

        # Build clean customer record matching dataset schema
        new_customer = {
            "customerID": cid,
            "gender": req_data.get("gender", "Female"),
            "SeniorCitizen": int(req_data.get("SeniorCitizen", 0)),
            "Partner": req_data.get("Partner", "No"),
            "Dependents": req_data.get("Dependents", "No"),
            "tenure": int(req_data.get("tenure", 1)),
            "PhoneService": req_data.get("PhoneService", "Yes"),
            "MultipleLines": req_data.get("MultipleLines", "No"),
            "InternetService": req_data.get("InternetService", "Fiber optic"),
            "OnlineSecurity": req_data.get("OnlineSecurity", "No"),
            "OnlineBackup": req_data.get("OnlineBackup", "No"),
            "DeviceProtection": req_data.get("DeviceProtection", "No"),
            "TechSupport": req_data.get("TechSupport", "No"),
            "StreamingTV": req_data.get("StreamingTV", "No"),
            "StreamingMovies": req_data.get("StreamingMovies", "No"),
            "Contract": req_data.get("Contract", "Month-to-month"),
            "PaperlessBilling": req_data.get("PaperlessBilling", "Yes"),
            "PaymentMethod": req_data.get("PaymentMethod", "Electronic check"),
            "MonthlyCharges": float(req_data.get("MonthlyCharges", 70.0)),
            "TotalCharges": float(req_data.get("TotalCharges", req_data.get("MonthlyCharges", 70.0)))
        }

        # Model Inference
        df_single = pd.DataFrame([new_customer])
        X = preprocess_data(df_single)
        prob = float(model.predict_proba(X)[0, 1] * 100)
        prediction = "Yes" if prob >= 50.0 else "No"
        risk_level = get_risk_level(prob)

        smart_ret = {}
        if generate_smart_retention:
            smart_ret = generate_smart_retention(new_customer, probability=prob, risk_level=risk_level)

        # Append to prediction file
        pred_entry = pd.DataFrame([{
            "Customer_ID": cid,
            "Churn_Probability": round(prob, 2),
            "Prediction": prediction,
            "Risk_Level": risk_level
        }])

        if PREDICTION_PATH.exists():
            pred_entry.to_csv(PREDICTION_PATH, mode='a', header=False, index=False)

        # Append to raw data file
        if RAW_DATA_PATH.exists():
            new_customer_with_churn = dict(new_customer)
            new_customer_with_churn["Churn"] = prediction
            pd.DataFrame([new_customer_with_churn]).to_csv(RAW_DATA_PATH, mode='a', header=False, index=False)

        return jsonify({
            "status": "success",
            "message": f"Customer {cid} added and predicted successfully!",
            "customer": {
                "Customer_ID": cid,
                "Churn_Probability": round(prob, 2),
                "Prediction": prediction,
                "Risk_Level": risk_level,
                "Persona": smart_ret.get("persona", "Standard Profile"),
                "Primary_Driver": smart_ret.get("primary_driver", "Contract & spend"),
                "Strategy_Title": smart_ret.get("strategy_title", "Proactive Care"),
                "Offer_Tag": smart_ret.get("offer_tag", "Retention Concession"),
                "Specific_Offer": smart_ret.get("specific_offer", get_recommendation(risk_level)),
                "Actions": smart_ret.get("actions", []),
                "Call_Script": smart_ret.get("call_script", "")
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# WHAT-IF COUNTERFACTUAL SIMULATOR
# ============================================================

@app.route("/api/simulate-whatif", methods=["POST"])
def simulate_whatif():
    try:
        req_data = request.get_json(silent=True) or request.form.to_dict()
        if not req_data:
            return jsonify({"status": "error", "message": "No simulation parameters provided."}), 400

        cid = str(req_data.get("customerID") or req_data.get("Customer_ID") or "").strip()
        mock_customer = {}

        # Look up baseline customer from database/CSV if exists
        if cid and RAW_DATA_PATH.exists():
            try:
                raw_df = pd.read_csv(RAW_DATA_PATH)
                match = raw_df[raw_df["customerID"].astype(str).str.lower() == cid.lower()]
                if not match.empty:
                    mock_customer = match.iloc[0].to_dict()
            except Exception as ex:
                print("Error looking up customer for simulation:", ex)

        # Merge simulated overrides
        for k, v in req_data.items():
            if v is not None and v != "":
                mock_customer[k] = v

        # Ensure correct numeric types
        mock_customer["SeniorCitizen"] = int(mock_customer.get("SeniorCitizen", 0) or 0)
        tenure_val = int(mock_customer.get("tenure", 1) or 1)
        mock_customer["tenure"] = tenure_val
        monthly_val = float(mock_customer.get("MonthlyCharges", 70.0) or 70.0)
        mock_customer["MonthlyCharges"] = monthly_val
        mock_customer["TotalCharges"] = monthly_val * max(tenure_val, 1)

        X = preprocess_data(pd.DataFrame([mock_customer]))
        prob = float(model.predict_proba(X)[0, 1] * 100)
        risk_level = get_risk_level(prob)

        smart_ret = {}
        if generate_smart_retention:
            smart_ret = generate_smart_retention(mock_customer, probability=prob, risk_level=risk_level)

        return jsonify({
            "status": "success",
            "simulated_probability": round(prob, 2),
            "simulated_risk": risk_level,
            "smart_retention": smart_ret
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



# ============================================================
# REAL ML PREDICTION
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    print()
    print("===================================")
    print("NEW CHURN PREDICTION")
    print("===================================")


    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if model is None:

        return jsonify({

            "status": "error",

            "message":
                "ML model could not be loaded."

        }), 500


    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if "file" not in request.files:

        return jsonify({

            "status": "error",

            "message":
                "No CSV file uploaded."

        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({

            "status": "error",

            "message":
                "No file selected."

        }), 400


    if not file.filename.lower().endswith(
        ".csv"
    ):

        return jsonify({

            "status": "error",

            "message":
                "Only CSV files are supported."

        }), 400


    try:

        # ----------------------------------------------------
        # Read CSV
        # ----------------------------------------------------

        data = pd.read_csv(
            file
        )


        print(
            "Rows:",
            len(data)
        )


        print(
            "Columns:",
            len(data.columns)
        )


        # ----------------------------------------------------
        # Customer IDs
        # ----------------------------------------------------

        customer_ids = (

            data["customerID"]
            .astype(str)
            .tolist()

        )


        # ----------------------------------------------------
        # Preprocess
        # ----------------------------------------------------

        X = preprocess_data(
            data
        )


        print(
            "Features prepared:",
            X.shape
        )


        # ----------------------------------------------------
        # ML Prediction
        # ----------------------------------------------------

        probabilities = (

            model.predict_proba(X)[:, 1]

            * 100

        )


        predictions = model.predict(
            X
        )


        # ----------------------------------------------------
        # Create results
        # ----------------------------------------------------

        output = pd.DataFrame({

            "Customer_ID":
                customer_ids,

            "Churn_Probability":
                np.round(
                    probabilities,
                    2
                ),

            "Prediction":
                np.where(
                    predictions == 1,
                    "Yes",
                    "No"
                )

        })


        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        output["Risk_Level"] = (

            output[
                "Churn_Probability"
            ]

            .apply(
                get_risk_level
            )

        )


        # ----------------------------------------------------
        # Save predictions
        # ----------------------------------------------------

        DATA_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )


        output.to_csv(

            PREDICTION_PATH,

            index=False

        )


        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        high_risk = int(

            (
                output["Risk_Level"]
                == "High"
            ).sum()

        )


        medium_risk = int(

            (
                output["Risk_Level"]
                == "Medium"
            ).sum()

        )


        low_risk = int(

            (
                output["Risk_Level"]
                == "Low"
            ).sum()

        )


        print(
            "High Risk:",
            high_risk
        )


        print(
            "Medium Risk:",
            medium_risk
        )


        print(
            "Low Risk:",
            low_risk
        )


        print(
            "Predictions saved:"
        )


        print(
            PREDICTION_PATH
        )


        print(
            "Prediction completed successfully!"
        )


        # ----------------------------------------------------
        # Return JSON
        # ----------------------------------------------------

        return jsonify({

            "status":
                "success",

            "message":
                "Churn prediction completed successfully.",

            "total_customers":
                len(output),

            "high_risk":
                high_risk,

            "medium_risk":
                medium_risk,

            "low_risk":
                low_risk,

            "predictions":
                output.to_dict(
                    orient="records"
                )

        })


    except Exception as e:

        print()
        print(
            "PREDICTION ERROR:"
        )
        print(
            str(e)
        )


        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


# ============================================================
# RUN SERVER
# ============================================================
# ============================================================
# DOWNLOAD PREDICTIONS (ALL OR RISK-WISE)
# ============================================================

@app.route("/api/download-predictions")
def download_predictions():
    try:
        if not PREDICTION_PATH.exists():
            return jsonify({
                "status": "error",
                "message": "Prediction file not found."
            }), 404

        df = pd.read_csv(PREDICTION_PATH)
        risk = request.args.get("risk", "").strip().lower()

        if risk in ["high", "medium", "low"]:
            df_export = df[df["Risk_Level"].astype(str).str.lower() == risk]
            filename = f"customer_churn_{risk}_risk.csv"
        else:
            df_export = df
            filename = "all_customer_churn_predictions.csv"

        mem_buffer = io.BytesIO()
        df_export.to_csv(mem_buffer, index=False)
        mem_buffer.seek(0)

        return send_file(
            mem_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="text/csv"
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
if __name__ == "__main__":

    print()
    print(
        "Dashboard:"
    )

    print(
        "http://127.0.0.1:5000/dashboard"
    )

    print()

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )