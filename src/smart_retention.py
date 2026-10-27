"""
Smart Retention Decision Engine
Provides differentiated, persona-based, and financial retention strategies
for customer churn mitigation.
"""

def generate_smart_retention(customer_data, probability=None, risk_level=None):
    """
    Generate dynamic, highly differentiated retention strategies based on
    customer spend, tenure, contract type, and service pain points.
    """
    if probability is None:
        try:
            prob_raw = float(customer_data.get("Churn_Probability", 50.0))
            if prob_raw > 1.0:
                probability = prob_raw / 100.0
            else:
                probability = prob_raw
        except Exception:
            probability = 0.5
    else:
        if probability > 1.0:
            probability = probability / 100.0

    if risk_level is None:
        if probability >= 0.65:
            risk_level = "High"
        elif probability >= 0.35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

    # Extract customer features
    tenure = int(float(customer_data.get("tenure", 0)))
    monthly = float(customer_data.get("MonthlyCharges", 0.0))
    contract = str(customer_data.get("Contract", "Month-to-month"))
    tech_support = str(customer_data.get("TechSupport", "No"))
    online_security = str(customer_data.get("OnlineSecurity", "No"))
    internet = str(customer_data.get("InternetService", "DSL"))
    payment = str(customer_data.get("PaymentMethod", "Electronic check"))
    streaming = (
        str(customer_data.get("StreamingTV", "No")) == "Yes" or 
        str(customer_data.get("StreamingMovies", "No")) == "Yes"
    )

    # 1. Determine Customer Persona
    if monthly >= 80 and contract == "Month-to-month":
        persona = "VIP High-Roller at Immediate Risk"
        primary_driver = "High monthly commitment on non-binding contract"
    elif tenure <= 6 and (tech_support == "No" or online_security == "No"):
        persona = "Frustrated Early-Tenure Newbie"
        primary_driver = "Onboarding friction & lack of technical assistance"
    elif payment == "Electronic check" and tenure <= 12:
        persona = "Payment Friction Flight Risk"
        primary_driver = "Manual billing friction via electronic check"
    elif streaming and online_security == "No":
        persona = "Heavy Content Streamer with High Bill"
        primary_driver = "High streaming spend without security bundle"
    elif tenure >= 24 and contract == "Month-to-month":
        persona = "Loyal Veteran Seeking Modern Rate"
        primary_driver = "Long-term customer feeling neglected on month-to-month"
    else:
        persona = "Standard Profile"
        primary_driver = "Standard churn indicators (contract & pricing balance)"

    # 2. Dynamic Financial & Service Offer Calculation
    discount_rate = 0.15  # 15% promotional credit
    monthly_discount = round(monthly * discount_rate, 2)
    three_month_savings = round(monthly_discount * 3, 2)
    annual_revenue_protected = round((monthly * 12) - three_month_savings, 2)

    # 3. Formulate Differentiated Strategies
    if risk_level == "High":
        if persona == "VIP High-Roller at Immediate Risk":
            strategy_title = "VIP Retention: Tiered Contract Lock-in"
            offer_tag = f"1-Yr Lock + ₹{monthly_discount}/mo Credit"
            specific_offer = (
                f"Offer a ₹{monthly_discount}/month credit for 3 months "
                f"(Total customer saving: ₹{three_month_savings}) upon upgrading to a 1-year contract. "
                f"Annual protected revenue: ₹{annual_revenue_protected}."
            )
            actions = [
                "Escalate to Senior Retention Specialist for high-touch outreach.",
                f"Present the 1-Year Price-Lock Guarantee with ₹{three_month_savings} introductory credit.",
                "Conduct network latency audit for Fiber Optic connection to address speed issues."
            ]
            call_script = (
                f"Hello, we value you as one of our premium subscribers. As part of our VIP program, "
                f"we have selected your account for an exclusive rate freeze plus a ₹{monthly_discount} credit for the next 3 months "
                f"when renewing with our annual plan."
            )

        elif persona == "Frustrated Early-Tenure Newbie":
            strategy_title = "Service Care & Proactive Onboarding"
            offer_tag = "Free TechSupport & Security Bundle"
            specific_offer = (
                "Complimentary 6 months of 24/7 Dedicated TechSupport + Device Protection "
                "(Value: ₹500, Zero marginal cash cost to company)."
            )
            actions = [
                "Schedule a 1-on-1 technician or phone care onboarding session.",
                "Activate complimentary TechSupport and Online Security bundle immediately.",
                "Send a 30-day follow-up satisfaction survey to confirm service quality."
            ]
            call_script = (
                "Hello, we noticed you recently joined our service and want to ensure everything is running smoothly. "
                "We have upgraded your line with complimentary 24/7 Tech Support for the next 6 months."
            )

        elif persona == "Payment Friction Flight Risk":
            strategy_title = "Auto-Pay Migration & Bill Simplification"
            offer_tag = "AutoPay ₹200 Statement Credit"
            specific_offer = (
                "One-time ₹200 instant statement credit upon enrolling in Automated Bank Transfer (UPI/ACH) or Card Auto-pay."
            )
            actions = [
                "Trigger automated SMS/Email with 1-click Auto-Pay enrollment link.",
                "Apply instant ₹200 billing rebate on current cycle upon payment method update.",
                "Highlight hassle-free monthly receipts and protection against late payment penalties."
            ]
            call_script = (
                "Hello, save time on your monthly bill. Switch your billing from manual electronic check to automated transfer "
                "today, and we will immediately apply a ₹200 credit directly to your upcoming statement."
            )

        elif persona == "Heavy Content Streamer with High Bill":
            strategy_title = "Entertainment Bundle Optimization"
            offer_tag = "Free Security & Streaming Boost"
            specific_offer = (
                "Package existing streaming TV/Movies with free Online Security and Speed Boost at current rate."
            )
            actions = [
                "Consolidate individual addon lines into the All-Inclusive Streaming Care plan.",
                "Provide free 3 months of Device Protection for family devices.",
                "Propose a 1-year entertainment price guarantee."
            ]
            call_script = (
                "Hello, as an active streaming user, we want to make sure you get the best streaming speeds and security. "
                "We can lock in your full entertainment package with complimentary cybersecurity starting this billing cycle."
            )

        else:
            strategy_title = "Proactive Price-to-Value Alignment"
            offer_tag = f"Loyalty Rebate (₹{monthly_discount}/mo)"
            specific_offer = (
                f"Offer a ₹{monthly_discount}/month loyalty rebate for 2 months upon account health review."
            )
            actions = [
                "Reach out via email or phone to conduct a short service check-in.",
                f"Offer flexible term options with up to ₹{monthly_discount * 2} in short-term relief.",
                "Review utilized bandwidth and optimize features for the customer's budget."
            ]
            call_script = (
                "Hello, thank you for choosing our service. We are reviewing account options to make sure your package "
                "perfectly fits your needs and budget, with an available loyalty concession this month."
            )

    elif risk_level == "Medium":
        strategy_title = "Targeted Engagement & Loyalty Nurture"
        if contract == "Month-to-month":
            offer_tag = "10% Discount on 1-Yr Upgrade"
            specific_offer = "Offer 10% discount on first 2 months if moving to annual subscription."
        else:
            offer_tag = "Free Speed & Cloud Backup"
            specific_offer = "Offer free speed upgrade or 3 months of complimentary cloud backup."
        actions = [
            "Monitor product usage trends over the next 30 days.",
            "Send personalized tips and feature discovery emails.",
            "Present low-commitment loyalty incentives before contract expiry."
        ]
        call_script = (
            "Hello, we are checking in to see how your connection has been performing. We would love to share an exclusive bonus add-on "
            "as a thank-you for your continued loyalty."
        )

    else:
        # Low Risk
        strategy_title = "Loyalty Maintenance & Advocacy"
        offer_tag = "Referral Bonus (₹250 Credit)"
        specific_offer = "Eligible for referral bonuses (₹250 per friend referred) and early access to fiber upgrades."
        actions = [
            "Maintain high service reliability and standard quarterly NPS check-in.",
            "Invite to customer referral program.",
            "Consider for high-speed fiber or smart home package upsell."
        ]
        call_script = (
            "Thank you for being a valued customer. You can earn bill credits by recommending us to your colleagues or neighbors."
        )

    return {
        "risk_level": risk_level,
        "persona": persona,
        "primary_driver": primary_driver,
        "strategy_title": strategy_title,
        "offer_tag": offer_tag,
        "specific_offer": specific_offer,
        "monthly_discount": monthly_discount,
        "three_month_savings": three_month_savings,
        "annual_revenue_protected": annual_revenue_protected,
        "actions": actions,
        "call_script": call_script
    }
