# ChurnInsight - Customer Churn Intelligence & Retention Platform

An enterprise-grade Customer Churn Prediction & Retention Decision Support System designed for telecom operators, customer success teams, and account managers.

ChurnInsight empowers businesses to predict customer churn before it occurs, diagnose root-cause drivers through explainable AI (SHAP), and simulate personalized retention packages with counterfactual analysis.

---

## Key Features

- **Predictive Churn Engine:** Machine Learning models (Tuned Random Forest and XGBoost) providing real-time churn risk classification and confidence probabilities.
- **Explainable AI (SHAP):** Root-cause attribution diagnostics revealing feature-level influences (contract terms, tech support, charges, payment methods).
- **Smart Retention Offer Generator:** Dynamic persona-based retention strategies and concrete concession bundles formulated in Indian Rupees (₹).
- **Interactive "What-If" Counterfactual Simulator:** Allows retention agents to test counterfactual bundles (contract upgrades, discounts, add-ons) and preview risk reductions before contacting subscribers.
- **Risk-Segmented CSV Export:** Export high, medium, and low-risk subscriber reports with single-click campaign exports.
- **Real-Time Subscriber Onboarding:** Register new subscribers with instant inference and tailored retention outreach scripts.
- **Batch Dataset Ingestion:** Drag-and-drop CSV upload for legacy billing synchronization.

---

## Tech Stack

- **Backend:** Python 3.13, Flask, Flask-CORS, Gunicorn
- **Machine Learning:** Scikit-learn, XGBoost, SHAP, Joblib, NumPy, Pandas
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla, Responsive)
- **Database:** MySQL / Local Structured Datastore

---

## Project Structure

```
Customer_Churn_Major_Project/
├── app/
│   ├── app.py                 # Main application entry point
│   ├── backend/
│   │   └── app.py             # Flask routes, API endpoints, and authentication
│   ├── static/
│   │   ├── style.css          # Clean corporate stylesheet
│   │   └── script.js          # Client-side reactivity, chart rendering, and modals
│   └── templates/
│       ├── index.html         # Main dashboard and retention console
│       └── login.html         # Secure admin login portal
├── data/
│   ├── customer_churn.csv     # Historical telecom subscriber dataset
│   └── customer_churn_predictions.csv
├── models/
│   ├── best_churn_model.pkl   # Deployed champion ML pipeline
│   └── churn_model.pkl
├── src/
│   ├── smart_retention.py     # Persona-based retention decision engine
│   └── retention_recommendation.py
├── notebooks/                 # Exploratory data analysis & model training notebooks
├── requirements.txt           # Project dependencies
├── Procfile                   # Cloud deployment command
└── README.md
```

---

## Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Harry18-vk/ChurnInsight.git
cd ChurnInsight
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app/app.py
```
Open your browser and navigate to:
- **Application URL:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Login Portal:** [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
- **Default Credentials:**
  - **Username:** `admin`
  * **Password:** `admin123`

---

## Deployment Instructions

### Deploy to Render
1. Push your repository to GitHub: `https://github.com/Harry18-vk/ChurnInsight`
2. Log into [Render](https://render.com) and click **New > Web Service**.
3. Connect your GitHub repository.
4. Configure service settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --chdir app app:app`
5. Click **Create Web Service**.

### Deploy to Railway
1. Go to [Railway](https://railway.app) and select **New Project > Deploy from GitHub repo**.
2. Select `ChurnInsight`.
3. Railway automatically detects the `Procfile` and launches the service.

---

## License
MIT License. Created by [Harry18-vk](https://github.com/Harry18-vk).
