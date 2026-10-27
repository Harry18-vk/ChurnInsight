# Individual Viva & Project Defense Handbook

This handbook contains tailored preparation for each member of the 4-person team. Review your specific section before the viva so you can answer questions accurately and confidently.

---

## Member 1: Divyansh Yadav (Team Leader & System Architect)

### Your Code Modules:
* `app/app.py` & `app/backend/app.py`
* `wsgi.py`, `Procfile`
* `app/static/script.js` & `app/static/style.css`
* `app/templates/index.html` & `app/templates/login.html`

### Top 4 Viva Questions & Exact Answers:

#### Q1: "Why did you build a custom web dashboard instead of just presenting a Jupyter Notebook?"
> **Answer:** *"A Jupyter Notebook is an analytical sandbox, not a deployable enterprise system. Customer success teams and call-center retention specialists cannot execute Python cells to evaluate subscriber risk. We designed ChurnInsight with an asynchronous RESTful API layer in Flask that handles real-time scoring, authentication, and dynamic counterfactual simulation in under 50ms, allowing non-technical operators to take immediate action."*

#### Q2: "How does the 'What-If' Simulation endpoint work on the backend?"
> **Answer:** *"The endpoint `/api/simulate-whatif` receives the subscriber's baseline attributes along with the counterfactual parameters selected by the retention agent (e.g. changing Contract from Month-to-Month to One Year, adding TechSupport, adjusting the bill). The backend transforms these inputs through our pipeline feature mapper, evaluates the vector with our serialized model (`best_churn_model.pkl`), computes the new probability delta, and invokes `smart_retention.py` to formulate a revised promotional script."*

#### Q3: "What prevents circular imports and how did you prepare this for cloud production?"
> **Answer:** *"In local development, developers often rely on `app.run()`. For production cloud deployment (Render/Linux), we separated the WSGI runner into `wsgi.py` and employed dynamic module loading (`importlib.util`) inside `app.py`. This ensures Gunicorn can spawn independent worker threads across CPU cores without circular namespace conflicts."*

#### Q4: "How does the system maintain security and role separation?"
> **Answer:** *"The application incorporates server-side session authentication with cryptographic signing (`app.secret_key`). Protected routes like `/dashboard` and the data APIs reject unauthenticated access via `@login_required` decorators, ensuring subscriber telemetry and predictions are accessible exclusively by authorized company retention personnel."*

---

## Member 2: Data Pipeline & Feature Engineering Specialist

### Your Code Modules:
* `src/eda.py` & `src/analyze_data.py`
* `src/preprocess.py` & `src/check_data.py`
* `data/cleaned_customer_churn.csv`

### Top 4 Viva Questions & Exact Answers:

#### Q1: "What anomalies did you discover in the raw dataset and how did you handle them?"
> **Answer:** *"In the raw Telco dataset, the `TotalCharges` column was stored as an object/string instead of numeric because 11 records contained blank spaces for new subscribers with zero tenure. Rather than naively deleting these records, we parsed them to numeric floats using `pd.to_numeric(errors='coerce')` and imputed the missing values with the median. We also stripped unique identifier columns like `customerID` before training to prevent the model from memorizing spurious IDs."*

#### Q2: "Why did you use One-Hot Encoding instead of Label Encoding for categorical variables?"
> **Answer:** *"Label Encoding assigns ordinal integers (0, 1, 2) to categories, which creates an artificial mathematical hierarchy that does not exist in features like `PaymentMethod` (e.g., Electronic check vs. Mailed check vs. Credit card). Tree models might misinterpret these integers as rank order. We utilized One-Hot Encoding to create independent binary columns, preserving categorical orthogonality without synthetic bias."*

#### Q3: "How did you address the class imbalance in the dataset?"
> **Answer:** *"The dataset exhibits a 73.5% non-churn vs. 26.5% churn distribution. In our preprocessing and model evaluation, we used stratified sampling (`stratify=y`) during the 80/20 train-test split. This ensures both training and test sets maintain identical churn ratios, preventing optimistic evaluation bias."*

#### Q4: "Did you apply feature scaling, and why is it necessary for tree models?"
> **Answer:** *"While decision trees are theoretically invariant to monotonic feature scaling, continuous features like `MonthlyCharges` (ranging from 18 to 118) and `tenure` (0 to 72) were scaled using `StandardScaler` so that baseline linear models (Logistic Regression) and regularization penalties in XGBoost converge smoothly and reliably."*

---

## Member 3: ML Algorithm Optimization & Benchmarking Modeler

### Your Code Modules:
* `src/model_optimization.py` & `src/xgboost_model.py`
* `src/save_best_model.py`
* `models/best_churn_model.pkl` & `models/scaler.pkl`

### Top 4 Viva Questions & Exact Answers:

#### Q1: "Why is Accuracy an insufficient metric for Customer Churn?"
> **Answer:** *"If a dataset has 75% non-churners, a naive model that predicts 'No Churn' for everyone achieves 75% accuracy but is practically useless because it fails to detect a single customer leaving. In business retention, a false negative (failing to identify a churning customer) costs hundreds of dollars in lost subscriber lifetime value. Therefore, we optimized primarily for **Recall (81.2%)** and **ROC-AUC (0.862)**."*

#### Q2: "How did you optimize the Random Forest classifier?"
> **Answer:** *"We used 5-fold cross-validation with grid search (`GridSearchCV`) across hyperparameter combinations: tuning `n_estimators` between 100 and 300, restricting `max_depth` to 10-14 to control tree variance and prevent overfitting, and enforcing `min_samples_split=5` and `min_samples_leaf=2`. This yielded our champion model with an 84.7% accuracy and 0.862 ROC-AUC."*

#### Q3: "What are the trade-offs between Random Forest and XGBoost in your experiments?"
> **Answer:** *"Random Forest is an ensemble bagging technique that trains independent trees in parallel to reduce variance, making it robust against noisy outliers. XGBoost is a sequential boosting technique that minimizes gradient loss on residuals, achieving slightly higher precision (76.9%). However, Random Forest provided slightly higher recall and stability on cross-validation, which is why it serves as our deployed production champion."*

#### Q4: "How do you ensure zero data leakage when evaluating the model?"
> **Answer:** *"Data leakage occurs when information from the test dataset contaminates the training phase. We strictly separated the train (80%) and test (20%) partitions prior to fitting scalers and encoders. The `StandardScaler` was fitted strictly on `X_train` and then applied to `X_test` via `.transform()`. Furthermore, all hyperparameter searches were conducted strictly inside cross-validation training folds."*

---

## Member 4: Explainable AI (XAI) & Prescriptive Retention Strategist

### Your Code Modules:
* `src/shap_analysis.py` & `src/retention_recommendation.py`
* `src/smart_retention.py`
* `data/shap_feature_importance.csv`

### Top 4 Viva Questions & Exact Answers:

#### Q1: "What is SHAP and why is it superior to built-in feature importances (Gini importance)?"
> **Answer:** *"Gini feature importance from Scikit-Learn suffers from two major flaws: it is biased toward high-cardinality continuous features, and it only provides a global average without explaining individual predictions. SHAP (Shapley Additive exPlanations) is grounded in cooperative game theory and guarantees mathematical consistency and local accuracy. It tells us not just which features matter overall, but exactly how much each individual feature pushed a specific customer's score toward or away from churn."*

#### Q2: "What did SHAP reveal as the primary churn drivers?"
> **Answer:** *"Global SHAP analysis proved that **Contract Type** is the single largest churn trigger (+0.38 mean |SHAP|), with Month-to-Month contracts multiplying churn likelihood by nearly 4.8 times. The second largest factor is **Tenure length** (+0.29 mean |SHAP|), confirming that subscribers are most vulnerable during their first 12 months. Third is high **Monthly Charges** combined with the absence of tech support and online security bundles."*

#### Q3: "How does the Smart Retention Decision Engine translate predictions into business actions?"
> **Answer:** *"In `smart_retention.py`, we built a prescriptive rule-matrix that categorizes subscribers into behavioral personas based on their attributes (e.g., 'VIP High-Roller', 'Early-Tenure Newbie', 'Payment Friction Risk'). Rather than offering generic discounts, it calculates dynamic, financial concessions in Indian Rupees (₹) — such as a 15% rate freeze on 1-year commitments, or 6 months of complimentary TechSupport — and projects protected annual revenue alongside an outbound call pitch script for the agent."*

#### Q4: "Can you provide a concrete example of counterfactual analysis in this project?"
> **Answer:** *"Consider high-risk subscriber `9300-AGZNL`, who had a 95.74% churn probability on a Month-to-Month contract paying high monthly charges. In our counterfactual simulator, the retention operator tests upgrading the contract to 1-Year with complimentary tech support and a small bill credit. The model re-evaluates the vector in real time and predicts the churn risk dropping to 53.43% — a 42.3% risk reduction — protecting over ₹1,000 in annualized subscriber revenue."*
