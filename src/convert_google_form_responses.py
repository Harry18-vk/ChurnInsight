"""
Google Form to ChurnInsight CSV Converter
-----------------------------------------
This script converts exported Google Form responses (CSV) into the exact
20-column schema required by the ChurnInsight Machine Learning model.

Usage:
    python convert_google_form_responses.py [path_to_google_form_responses.csv]
"""

import sys
import os
import pandas as pd

def normalize_google_form(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} survey responses from {input_path}")

    # Standardize column mapping by detecting keywords in Google Form questions
    col_map = {}
    for col in df.columns:
        c_lower = col.lower()
        if "name" in c_lower or "id" in c_lower:
            col_map[col] = "customerID"
        elif "gender" in c_lower:
            col_map[col] = "gender"
        elif "senior" in c_lower or "60" in c_lower or "age" in c_lower:
            col_map[col] = "SeniorCitizen"
        elif "partner" in c_lower or "married" in c_lower or "spouse" in c_lower:
            col_map[col] = "Partner"
        elif "dependent" in c_lower or "children" in c_lower or "parents" in c_lower:
            col_map[col] = "Dependents"
        elif "tenure" in c_lower or "month" in c_lower or "duration" in c_lower:
            col_map[col] = "tenure"
        elif "phone service" in c_lower or "calling" in c_lower:
            col_map[col] = "PhoneService"
        elif "multiple" in c_lower or "dual sim" in c_lower or "lines" in c_lower:
            col_map[col] = "MultipleLines"
        elif "internet" in c_lower or "broadband" in c_lower:
            col_map[col] = "InternetService"
        elif "security" in c_lower or "antivirus" in c_lower:
            col_map[col] = "OnlineSecurity"
        elif "backup" in c_lower or "cloud" in c_lower:
            col_map[col] = "OnlineBackup"
        elif "device" in c_lower or "insurance" in c_lower or "warranty" in c_lower:
            col_map[col] = "DeviceProtection"
        elif "tech support" in c_lower or "customer care" in c_lower or "support" in c_lower:
            col_map[col] = "TechSupport"
        elif "streaming tv" in c_lower or "live tv" in c_lower:
            col_map[col] = "StreamingTV"
        elif "streaming movies" in c_lower or "ott" in c_lower or "netflix" in c_lower:
            col_map[col] = "StreamingMovies"
        elif "contract" in c_lower or "recharge frequency" in c_lower or "plan duration" in c_lower:
            col_map[col] = "Contract"
        elif "paperless" in c_lower or "digital bill" in c_lower:
            col_map[col] = "PaperlessBilling"
        elif "payment" in c_lower or "pay" in c_lower:
            col_map[col] = "PaymentMethod"
        elif "monthly" in c_lower or "spend" in c_lower or "charge" in c_lower or "bill" in c_lower:
            col_map[col] = "MonthlyCharges"

    records = []
    for idx, row in df.iterrows():
        raw_id = str(row.get(next((k for k, v in col_map.items() if v == "customerID"), None), f"SURVEY-{idx+1:03d}"))
        cid = f"SURVEY-{idx+1:03d}-{raw_id.strip()}" if not raw_id.startswith("SURVEY-") else raw_id.strip()

        raw_g = str(row.get(next((k for k, v in col_map.items() if v == "gender"), ""), "Male")).lower()
        gender = "Female" if "female" in raw_g else "Male"

        raw_sc = str(row.get(next((k for k, v in col_map.items() if v == "SeniorCitizen"), "0"))).lower()
        senior = 1 if ("yes" in raw_sc or "60" in raw_sc or raw_sc == "1") else 0

        raw_p = str(row.get(next((k for k, v in col_map.items() if v == "Partner"), "No"))).lower()
        partner = "Yes" if "yes" in raw_p else "No"

        raw_d = str(row.get(next((k for k, v in col_map.items() if v == "Dependents"), "No"))).lower()
        dependents = "Yes" if "yes" in raw_d else "No"

        raw_t = row.get(next((k for k, v in col_map.items() if v == "tenure"), 1))
        try:
            tenure = int(float(raw_t))
            tenure = max(1, min(tenure, 72))
        except:
            tenure = 6

        raw_ps = str(row.get(next((k for k, v in col_map.items() if v == "PhoneService"), "Yes"))).lower()
        phone_service = "No" if "no" in raw_ps else "Yes"

        raw_ml = str(row.get(next((k for k, v in col_map.items() if v == "MultipleLines"), "No"))).lower()
        if "no phone" in raw_ml or phone_service == "No":
            multi_lines = "No phone service"
        elif "yes" in raw_ml:
            multi_lines = "Yes"
        else:
            multi_lines = "No"

        raw_is = str(row.get(next((k for k, v in col_map.items() if v == "InternetService"), "Fiber optic"))).lower()
        if "fiber" in raw_is:
            internet = "Fiber optic"
        elif "dsl" in raw_is or "copper" in raw_is or "broadband" in raw_is:
            internet = "DSL"
        elif "no" in raw_is:
            internet = "No"
        else:
            internet = "Fiber optic"

        def parse_addon(field_name, default="No"):
            col_k = next((k for k, v in col_map.items() if v == field_name), None)
            val = str(row.get(col_k, default)).lower()
            if internet == "No" or "no internet" in val:
                return "No internet service"
            return "Yes" if "yes" in val else "No"

        sec = parse_addon("OnlineSecurity")
        bk = parse_addon("OnlineBackup")
        dp = parse_addon("DeviceProtection")
        ts = parse_addon("TechSupport")
        tv = parse_addon("StreamingTV")
        mv = parse_addon("StreamingMovies")

        raw_c = str(row.get(next((k for k, v in col_map.items() if v == "Contract"), "Month-to-month"))).lower()
        if "two" in raw_c or "2" in raw_c:
            contract = "Two year"
        elif "one" in raw_c or "1" in raw_c or "annual" in raw_c or "yearly" in raw_c:
            contract = "One year"
        else:
            contract = "Month-to-month"

        raw_pb = str(row.get(next((k for k, v in col_map.items() if v == "PaperlessBilling"), "Yes"))).lower()
        paperless = "No" if "no" in raw_pb else "Yes"

        raw_pm = str(row.get(next((k for k, v in col_map.items() if v == "PaymentMethod"), "Electronic check"))).lower()
        if "credit" in raw_pm or "card" in raw_pm:
            payment = "Credit card (automatic)"
        elif "bank" in raw_pm or "auto" in raw_pm or "netbanking" in raw_pm:
            payment = "Bank transfer (automatic)"
        elif "mailed" in raw_pm or "cash" in raw_pm:
            payment = "Mailed check"
        else:
            payment = "Electronic check"

        raw_mc = row.get(next((k for k, v in col_map.items() if v == "MonthlyCharges"), 499.0))
        try:
            monthly = float(raw_mc)
        except:
            monthly = 499.0

        total = round(monthly * tenure, 2)

        records.append({
            "customerID": cid,
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multi_lines,
            "InternetService": internet,
            "OnlineSecurity": sec,
            "OnlineBackup": bk,
            "DeviceProtection": dp,
            "TechSupport": ts,
            "StreamingTV": tv,
            "StreamingMovies": mv,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total
        })

    out_df = pd.DataFrame(records)
    if not output_path:
        base_dir = os.path.dirname(input_path) or "."
        output_path = os.path.join(base_dir, "cleaned_survey_for_churninsight.csv")

    out_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Success! Cleaned and converted {len(out_df)} records.")
    print(f"Saved ready-to-upload file to: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        normalize_google_form(sys.argv[1])
    else:
        print("Please provide the path to your exported Google Form CSV file.")
        print("Example: python convert_google_form_responses.py 'My_Form_Responses.csv'")
