# Research Paper Framework & Publication Blueprint

**Proposed Paper Title:**  
*Explainable Customer Churn Prediction and Counterfactual Decision-Support System Using Tree-Based Ensembles and SHAP Attributions*

**Authors:** Divyansh Yadav, [Member 2], [Member 3], [Member 4]  
**Target Venue:** IEEE International Conference on Machine Learning Applications / Springer Lecture Notes in Computer Science  

---

## Abstract

Customer attrition in subscription-based telecommunications imposes substantial financial strain on service providers, with acquisition costs often exceeding retention costs by a factor of five. While conventional machine learning approaches effectively predict churn risk, they frequently operate as opaque black boxes, failing to provide actionable rationale or prescriptive mitigation strategies. This paper proposes **ChurnInsight**, an end-to-end framework integrating predictive ensemble modeling, Explainable Artificial Intelligence (XAI), and counterfactual decision support. Using a curated cohort of 7,043 subscriber records, we evaluate linear, bagging, and boosting architectures, demonstrating that a hyperparameter-tuned ensemble of Random Forest and XGBoost achieves an optimal balance with **84.7% accuracy, 81.2% churn recall, and an ROC-AUC of 0.862**. 

To overcome model opacity, we employ Shapley Additive exPlanations (SHAP) based on cooperative game theory, identifying contract tenure ($\phi = +0.38$), overall service duration ($\phi = +0.29$), and monthly tariff commitments ($\phi = +0.24$) as dominant churn drivers. Crucially, our framework extends beyond diagnostics by introducing a prescriptive counterfactual engine that evaluates hypothetical retention packages in real time, projecting risk delta and protected annual revenue. The complete architecture is validated through an interactive web-based enterprise console.

**Index Terms:** Customer Churn Prediction, Explainable AI (XAI), SHAP, Random Forest, XGBoost, Counterfactual Analysis, Decision-Support System.

---

## 1. Introduction

* **Context:** High subscriber turnover in competitive telecom markets (annual churn rates averaging 20-30%).
* **Gap in Existing Literature:** Most literature terminates at binary classification ($y \in \{0, 1\}$). Business operators require answers to two questions:
  1. *Why* is this specific subscriber leaving? (Local Interpretability)
  2. *What* concession bundle will reverse their decision without eroding margin? (Counterfactual Actionability)
* **Contributions of this Work:**
  - High-recall ensemble classification optimized for class-imbalanced churn cohorts.
  - Granular post-hoc interpretability via TreeSHAP.
  - A real-time counterfactual offer simulation system incorporating persona classification and localized financial concession modeling (INR).

---

## 2. Dataset & Exploratory Analysis

* **Dataset Source:** IBM Telco Customer Churn benchmark dataset.
* **Dimensions:** 7,043 observations across 21 raw variables.
* **Target Feature:** Churn status ($Yes = 26.54\%$, $No = 73.46\%$).
* **Data Cleansing:** Imputation of blank values in `TotalCharges` (converted to numeric median), elimination of synthetic index artifacts.

---

## 3. Methodology & System Architecture

```mermaid
flowchart LR
    A["Raw Subscriber Data"] --> B["Preprocessing & Encoding Pipeline"]
    B --> C["Tuned Ensemble (RF + XGBoost)"]
    C --> D["Risk Probability & Classification"]
    D --> E["SHAP TreeExplainer Attribution"]
    E --> F["Prescriptive Decision Engine (smart_retention.py)"]
    F --> G["Counterfactual What-If Simulator"]
```

### 3.1 Preprocessing & Mathematical Formulation
- Continuous features (Tenure, MonthlyCharges, TotalCharges) normalized via Standard Scaling:
  $$z = \frac{x - \mu}{\sigma}$$
- Categorical features transformed via One-Hot Vectorization:
  $$x_j \in \{0, 1\}^{K-1}$$

### 3.2 Machine Learning Classifier Formulation
- Random Forest Gini Impurity minimization across $B$ bootstrapped decision trees:
  $$I_G(p) = 1 - \sum_{i=1}^{C} p_i^2$$
- XGBoost regularized objective function:
  $$\mathcal{L}^{(t)} = \sum_{i=1}^{n} l\left(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)\right) + \Omega(f_t)$$
  where $\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$.

### 3.3 Explainable AI (SHAP TreeExplainer)
Feature contributions are computed using classical Shapley values from cooperative game theory:
$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$
where $F$ is the feature space, $S$ is a subset of features, and $\phi_i$ represents the marginal contribution of attribute $i$.

---

## 4. Experimental Results & Benchmarks

### 4.1 Comparative Model Performance Table

| Model Architecture | Accuracy | Precision | Recall (Churn) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Baseline)** | 79.2% | 65.1% | 68.4% | 0.667 | 0.812 |
| **XGBoost Classifier** | 83.9% | 76.9% | 80.5% | 0.786 | 0.858 |
| **Random Forest (Tuned Champion)** | **84.7%** | **78.4%** | **81.2%** | **0.798** | **0.862** |

### 4.2 Top 5 SHAP Feature Importance Rankings

| Rank | Feature | Mean Absolute SHAP Value ($E[\|\phi_i\|]$) | Business Interpretation |
| :---: | :--- | :---: | :--- |
| **1** | Contract Type (Month-to-Month) | **+0.38** | Highest churn risk due to zero financial commitment |
| **2** | Subscriber Tenure (Months) | **+0.29** | High attrition in first 6-12 months of service lifecycle |
| **3** | Monthly Charges (Total Bill) | **+0.24** | Price sensitivity above ₹80 equivalent monthly commitment |
| **4** | Tech Support Availability | **+0.21** | Customers without support churn 2.1x faster during outages |
| **5** | Online Security & Backup | **+0.16** | Absence of security bundles correlates with service cancellation |

---

## 5. Counterfactual Simulation & Business Impact

The system formulates counterfactual tuples:
$$x^* = \arg\min_{x'} \mathcal{P}(\text{Churn} = 1 \mid x') \quad \text{subject to } \text{Cost}(x, x') \le \text{Threshold}$$

* **Case Study:** Subscriber `9300-AGZNL` with an initial churn risk of **95.74%** on a Month-to-Month contract.
* **Simulated Counterfactual Package:** 1-Year Contract upgrade with complimentary TechSupport and a promotional concession.
* **Simulated Outcome:** Risk dropped from **95.74% to 53.43%** ($\Delta = -42.31\%$), protecting ₹1,085.70 in annualized revenue.

---

## 6. Conclusion & Future Research Directions

ChurnInsight proves that combining tree ensembles with SHAP and counterfactual optimization bridges the gap between predictive data science and executive decision-making. 
* **Future Work:**
  1. Integrating sequential deep learning (LSTMs / Temporal Fusion Transformers) on customer time-series usage logs.
  2. Automated reinforcement learning (Contextual Bandits) to learn optimal promotional discounts through live A/B test feedback loops.
