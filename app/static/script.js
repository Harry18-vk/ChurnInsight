// ============================================================
// CUSTOMER CHURN AI
// COMPLETE FRONTEND JAVASCRIPT
// ============================================================


// ============================================================
// GLOBAL VARIABLES
// ============================================================

let currentCustomers = [];

let selectedRisk = "";


// ============================================================
// PAGE NAVIGATION
// ============================================================

function showSection(sectionId, button = null) {

    document
        .querySelectorAll(".page-section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


    const selectedSection =
        document.getElementById(
            sectionId
        );


    if (selectedSection) {

        selectedSection.classList.add(
            "active-section"
        );

    }


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove(
                "active"
            );

        });


    if (button) {

        button.classList.add(
            "active"
        );

    }


    // Load data when required

    if (
        sectionId === "dashboard"
    ) {

        loadDashboard();

    }


    if (
        sectionId === "customers"
    ) {

        loadCustomers(
            "",
            selectedRisk
        );

    }

}


// ============================================================
// SHOW SECTION BY ID
// ============================================================

function showSectionById(
    sectionId
) {

    let button = null;


    const buttons =
        document.querySelectorAll(
            ".nav-item"
        );


    buttons.forEach(item => {

        const onclickText =
            item.getAttribute(
                "onclick"
            );


        if (
            onclickText &&
            onclickText.includes(
                "'" + sectionId + "'"
            )
        ) {

            button = item;

        }

    });


    showSection(
        sectionId,
        button
    );

}


// ============================================================
// DASHBOARD
// ============================================================

async function loadDashboard() {

    try {

        const response =
            await fetch(
                "/api/dashboard"
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            data.status !== "success"
        ) {

            console.error(
                "Dashboard error:",
                data.message
            );

            return;

        }


        // Total customers

        const total =
            document.getElementById(
                "totalCustomers"
            );


        if (total) {

            total.textContent =
                Number(
                    data.total_customers
                ).toLocaleString();

        }


        // High risk

        const high =
            document.getElementById(
                "highRisk"
            );


        if (high) {

            high.textContent =
                Number(
                    data.high_risk
                ).toLocaleString();

        }


        // Medium risk

        const medium =
            document.getElementById(
                "mediumRisk"
            );


        if (medium) {

            medium.textContent =
                Number(
                    data.medium_risk
                ).toLocaleString();

        }


        // Low risk

        const low =
            document.getElementById(
                "lowRisk"
            );


        if (low) {

            low.textContent =
                Number(
                    data.low_risk
                ).toLocaleString();

        }


        updateRiskChart(
            data
        );


    } catch (error) {

        console.error(
            "Unable to load dashboard:",
            error
        );

    }

}


// ============================================================
// RISK CHART
// ============================================================

function updateRiskChart(
    data
) {

    const high =
        Number(
            data.high_risk
        ) || 0;


    const medium =
        Number(
            data.medium_risk
        ) || 0;


    const low =
        Number(
            data.low_risk
        ) || 0;


    const maximum =
        Math.max(
            high,
            medium,
            low
        );


    if (
        maximum === 0
    ) {

        return;

    }


    const highBar =
        document.getElementById(
            "highBar"
        );


    const mediumBar =
        document.getElementById(
            "mediumBar"
        );


    const lowBar =
        document.getElementById(
            "lowBar"
        );


    if (highBar) {

        highBar.style.height =
            Math.max(
                (high / maximum) * 100,
                5
            ) + "%";

    }


    if (mediumBar) {

        mediumBar.style.height =
            Math.max(
                (medium / maximum) * 100,
                5
            ) + "%";

    }


    if (lowBar) {

        lowBar.style.height =
            Math.max(
                (low / maximum) * 100,
                5
            ) + "%";

    }

}


// ============================================================
// LOAD CUSTOMERS
// ============================================================

async function loadCustomers(
    search = "",
    risk = ""
) {

    try {

        let url =
            "/api/customers?limit=100";


        if (search) {

            url +=
                "&search=" +
                encodeURIComponent(
                    search
                );

        }


        if (risk) {

            url +=
                "&risk=" +
                encodeURIComponent(
                    risk
                );

        }


        const response =
            await fetch(
                url
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            data.status !== "success"
        ) {

            console.error(
                "Customer API error:",
                data.message
            );

            return;

        }


        currentCustomers =
            data.customers || [];


        renderCustomers(
            currentCustomers
        );


    } catch (error) {

        console.error(
            "Customer loading error:",
            error
        );

    }

}


// ============================================================
// RENDER CUSTOMER TABLE
// ============================================================

function renderCustomers(
    customers
) {

    const table =
        document.getElementById(
            "customerTable"
        );


    if (!table) {

        return;

    }


    table.innerHTML = "";


    const count =
        document.getElementById(
            "customerCount"
        );


    if (count) {

        count.textContent =
            customers.length.toLocaleString();

    }


    if (
        !customers ||
        customers.length === 0
    ) {

        table.innerHTML = `

            <tr>

                <td
                    colspan="6"
                    style="
                        text-align:center;
                        padding:40px;
                    "
                >

                    No customers found.

                </td>

            </tr>

        `;

        return;

    }


    customers.forEach(
        customer => {

            const row =
                document.createElement(
                    "tr"
                );


            const probability =
                Number(
                    customer.Churn_Probability
                ) || 0;


            const risk =
                String(
                    customer.Risk_Level ||
                    "Unknown"
                );


            const riskClass =
                getRiskClass(
                    risk
                );


            const prediction =
                String(
                    customer.Prediction ||
                    ""
                );


            const offerTag =
                customer.Offer_Tag ||
                customer.Strategy_Title ||
                (risk === "High"
                    ? "1-Yr Lock + Credit"
                    : risk === "Medium"
                    ? "10% Upgrade Discount"
                    : "Referral Bonus");

            const fullOffer =
                customer.Specific_Offer ||
                customer.Recommendation ||
                getRecommendation(risk);


            row.innerHTML = `

                <td>

                    <strong>
                        ${escapeHTML(
                            customer.Customer_ID
                        )}
                    </strong>

                </td>


                <td>

                    <div class="probability">

                        <strong>
                            ${probability.toFixed(2)}%
                        </strong>

                        <div class="probability-bar">

                            <div
                                style="
                                    width:${Math.min(
                                        probability,
                                        100
                                    )}%;
                                "
                            ></div>

                        </div>

                    </div>

                </td>


                <td>

                    <span class="${
                        prediction === "Yes"
                            ? "prediction-yes"
                            : "prediction-no"
                    }">

                        ${escapeHTML(
                            prediction
                        )}

                    </span>

                </td>


                <td>

                    <span
                        class="risk ${riskClass}"
                    >

                        ${escapeHTML(
                            risk.toUpperCase()
                        )}

                    </span>

                </td>


                <td>

                    <span class="offer-tag" title="${escapeAttribute(fullOffer)}">

                        ${escapeHTML(
                            offerTag
                        )}

                    </span>

                </td>


                <td>

                    <button
                        class="view-button"
                        onclick="viewCustomer('${escapeAttribute(
                            customer.Customer_ID
                        )}')"
                    >

                        View

                    </button>

                </td>

            `;


            table.appendChild(
                row
            );

        }
    );

}


// ============================================================
// CUSTOMER SEARCH
// ============================================================

function searchCustomer() {

    const input =
        document.getElementById(
            "customerSearch"
        );


    if (!input) {

        return;

    }


    const search =
        input.value.trim();


    loadCustomers(
        search,
        selectedRisk
    );

}


// ============================================================
// RISK FILTER
// ============================================================

function filterCustomers(
    risk
) {

    selectedRisk =
        risk || "";


    document
        .querySelectorAll(
            ".filter-button"
        )
        .forEach(button => {

            button.classList.remove(
                "active"
            );

        });


    const buttons =
        document.querySelectorAll(
            ".filter-button"
        );


    buttons.forEach(button => {

        const text =
            button.textContent
                .toLowerCase();


        if (
            (risk === "" &&
                text.includes("all")) ||

            (risk === "high" &&
                text.includes("high")) ||

            (risk === "medium" &&
                text.includes("medium")) ||

            (risk === "low" &&
                text.includes("low"))
        ) {

            button.classList.add(
                "active"
            );

        }

    });


    const searchBox =
        document.getElementById(
            "customerSearch"
        );


    const search =
        searchBox
            ? searchBox.value.trim()
            : "";


    loadCustomers(
        search,
        selectedRisk
    );

}


// ============================================================
// CUSTOMER DETAILS
// ============================================================

async function viewCustomer(
    customerId
) {

    const modal =
        document.getElementById(
            "customerModal"
        );


    if (!modal) {

        console.error(
            "Customer modal not found."
        );

        return;

    }


    try {

        const response =
            await fetch(
                "/api/customer/" +
                encodeURIComponent(
                    customerId
                )
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            data.status !== "success"
        ) {

            alert(
                data.message ||
                "Customer not found."
            );

            return;

        }


        const customer =
            data.customer;


        const probability =
            Number(
                customer.Churn_Probability
            ) || 0;


        const risk =
            String(
                customer.Risk_Level ||
                "Unknown"
            );


        // Customer ID

        const customerIdElement =
            document.getElementById(
                "modalCustomerId"
            );


        if (customerIdElement) {

            customerIdElement.textContent =
                customer.Customer_ID;

        }


        // Probability

        const probabilityElement =
            document.getElementById(
                "modalProbability"
            );


        const probabilityText =
            document.getElementById(
                "modalProbabilityText"
            );


        if (probabilityElement) {

            probabilityElement.textContent =
                probability.toFixed(2) +
                "%";

        }


        if (probabilityText) {

            probabilityText.textContent =
                probability.toFixed(2) +
                "%";

        }


        // Prediction

        const predictionElement =
            document.getElementById(
                "modalPrediction"
            );


        if (predictionElement) {

            predictionElement.textContent =
                customer.Prediction;


            predictionElement.style.color =
                customer.Prediction === "Yes"
                    ? "#dc2626"
                    : "#16a34a";

        }


        // Risk

        const riskElement =
            document.getElementById(
                "modalRisk"
            );


        if (riskElement) {

            riskElement.textContent =
                risk;

        }


        // Risk badge

        const riskBadge =
            document.getElementById(
                "modalRiskBadge"
            );


        if (riskBadge) {

            riskBadge.textContent =
                risk.toUpperCase();


            riskBadge.className =
                "risk " +
                getRiskClass(
                    risk
                );

        }


        // Recommendation & Smart Retention
        const recommendationElement =
            document.getElementById("modalRecommendation");
        const specificOfferElement =
            document.getElementById("modalSpecificOffer");
        const personaBadge =
            document.getElementById("modalPersonaBadge");
        const primaryDriverElement =
            document.getElementById("modalPrimaryDriver");
        const actionList =
            document.getElementById("modalActionList");
        const scriptBox =
            document.getElementById("modalScriptBox");
        const callScriptText =
            document.getElementById("modalCallScript");

        const targetOffer =
            customer.Specific_Offer || customer.Recommendation || getRecommendation(risk);

        if (specificOfferElement) {
            specificOfferElement.textContent = targetOffer;
        }

        if (recommendationElement) {
            recommendationElement.textContent = targetOffer;
        }

        if (personaBadge) {
            personaBadge.textContent = customer.Persona || "Standard Profile";
        }

        if (primaryDriverElement) {
            primaryDriverElement.textContent = customer.Primary_Driver || "Standard service factors";
        }

        if (actionList) {
            actionList.innerHTML = "";
            const actions = customer.Actions && customer.Actions.length > 0 
                ? customer.Actions 
                : ["Monitor customer satisfaction and review usage patterns."];
            actions.forEach(act => {
                const li = document.createElement("li");
                li.textContent = act;
                actionList.appendChild(li);
            });
        }

        if (scriptBox && callScriptText) {
            if (customer.Call_Script) {
                callScriptText.textContent = `"${customer.Call_Script}"`;
                scriptBox.style.display = "block";
            } else {
                scriptBox.style.display = "none";
            }
        }

        // Store active customer for What-If simulator
        window.activeModalCustomer = customer;
        const whatifResult = document.getElementById("whatifResult");
        if (whatifResult) {
            whatifResult.style.display = "none";
        }

        // Initialize What-If inputs from customer's current values
        const attr = customer.Attributes || {};
        const whatifContract = document.getElementById("whatif_Contract");
        const whatifTech = document.getElementById("whatif_TechSupport");
        const whatifMonthly = document.getElementById("whatif_MonthlyCharges");

        if (whatifContract) {
            whatifContract.value = attr.Contract || "Month-to-month";
        }
        if (whatifTech) {
            whatifTech.value = (attr.TechSupport === "Yes" ? "Yes" : "No");
        }
        if (whatifMonthly) {
            whatifMonthly.value = attr.MonthlyCharges || 70.00;
        }

        // Probability bar
        const probabilityBar =
            document.getElementById(
                "modalProbabilityBar"
            );

        if (probabilityBar) {
            probabilityBar.style.width =
                Math.min(
                    probability,
                    100
                ) + "%";
        }

        // Show modal
        modal.classList.add(
            "show"
        );


    } catch (error) {

        console.error(
            "Customer details error:",
            error
        );


        alert(
            "Unable to load customer details."
        );

    }

}


// ============================================================
// RISK CLASS
// ============================================================

function getRiskClass(
    risk
) {

    const level =
        String(
            risk || ""
        ).toLowerCase();


    if (
        level === "high"
    ) {

        return "high-risk";

    }


    if (
        level === "medium"
    ) {

        return "medium-risk";

    }


    if (
        level === "low"
    ) {

        return "low-risk";

    }


    return "high-risk";

}


// ============================================================
// RECOMMENDATION
// ============================================================

function getRecommendation(
    risk
) {

    const level =
        String(
            risk || ""
        ).toLowerCase();


    if (
        level === "high"
    ) {

        return (

            "Immediate retention action recommended. " +
            "Contact the customer and provide a personalized " +
            "retention offer or service improvement."

        );

    }


    if (
        level === "medium"
    ) {

        return (

            "Monitor customer engagement and consider " +
            "a targeted promotional or service offer."

        );

    }


    return (

        "Maintain regular engagement and continue " +
        "monitoring customer satisfaction."

    );

}


// ============================================================
// SHORT RECOMMENDATION
// ============================================================

function getShortRecommendation(
    risk
) {

    const level =
        String(
            risk || ""
        ).toLowerCase();


    if (
        level === "high"
    ) {

        return "Immediate retention";

    }


    if (
        level === "medium"
    ) {

        return "Monitor & engage";

    }


    return "Maintain relationship";

}


// ============================================================
// CLOSE CUSTOMER MODAL
// ============================================================

function closeCustomerModal() {

    const modal =
        document.getElementById(
            "customerModal"
        );


    if (modal) {

        modal.classList.remove(
            "show"
        );

    }

}


// ============================================================
// CSV FILE INPUT
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const fileInput =
            document.getElementById(
                "fileInput"
            );


        if (fileInput) {

            fileInput.addEventListener(
                "change",
                function (event) {

                    const file =
                        event.target.files[0];


                    if (file) {

                        uploadAndPredict(
                            file
                        );

                    }

                }
            );

        }


        // Search box

        const searchBox =
            document.getElementById(
                "customerSearch"
            );


        if (searchBox) {

            searchBox.addEventListener(
                "keypress",
                function (event) {

                    if (
                        event.key ===
                        "Enter"
                    ) {

                        searchCustomer();

                    }

                }
            );

        }


        // Drag and drop

        const dropZone =
            document.getElementById(
                "dropZone"
            );


        if (dropZone) {


            dropZone.addEventListener(
                "dragover",
                function (event) {

                    event.preventDefault();

                    dropZone.classList.add(
                        "dragover"
                    );

                }
            );


            dropZone.addEventListener(
                "dragleave",
                function () {

                    dropZone.classList.remove(
                        "dragover"
                    );

                }
            );


            dropZone.addEventListener(
                "drop",
                function (event) {

                    event.preventDefault();


                    dropZone.classList.remove(
                        "dragover"
                    );


                    const files =
                        event.dataTransfer.files;


                    if (
                        files &&
                        files.length > 0
                    ) {

                        uploadAndPredict(
                            files[0]
                        );

                    }

                }
            );

        }


        // Initial loading

        loadDashboard();

        loadCustomers();


        console.log(
            "==================================="
        );

        console.log(
            "CUSTOMER CHURN AI FRONTEND"
        );

        console.log(
            "Frontend initialized successfully."
        );

        console.log(
            "==================================="
        );

    }
);


// ============================================================
// UPLOAD + ML PREDICTION
// ============================================================

async function uploadAndPredict(
    file
) {

    const result =
        document.getElementById(
            "uploadResult"
        );


    // Validate

    if (
        !file.name
            .toLowerCase()
            .endsWith(".csv")
    ) {

        showUploadResult(
            "Please upload a valid CSV file.",
            false
        );

        return;

    }


    showUploadResult(
        "Uploading dataset and running model inference...",
        true
    );


    // FormData

    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                "/api/predict",
                {
                    method: "POST",
                    body: formData
                }
            );


        const responseText =
            await response.text();


        console.log(
            "SERVER RESPONSE:"
        );


        console.log(
            responseText
        );


        let data;


        try {

            data =
                JSON.parse(
                    responseText
                );

        } catch (error) {

            throw new Error(

                "Backend returned HTML instead of JSON. " +

                "HTTP Status: " +

                response.status +

                "\n\nServer response:\n" +

                responseText.substring(
                    0,
                    500
                )

            );

        }


        if (
            !response.ok ||
            data.status !== "success"
        ) {

            throw new Error(

                data.message ||
                "Prediction failed."

            );

        }


        // Success

        showUploadResult(

            `

            <strong>
                Dataset Processing Completed
            </strong>

            <br><br>

            File:
            ${escapeHTML(
                file.name
            )}

            <br><br>

            Total Customers:
            ${Number(
                data.total_customers
            ).toLocaleString()}

            <br>

            High Risk:
            ${Number(
                data.high_risk
            ).toLocaleString()}

            <br>

            Medium Risk:
            ${Number(
                data.medium_risk
            ).toLocaleString()}

            <br>

            Low Risk:
            ${Number(
                data.low_risk
            ).toLocaleString()}

            `,

            true

        );


        // Update dashboard

        updateDashboardFromPrediction(
            data
        );


        // Refresh customers

        loadCustomers(
            "",
            selectedRisk
        );


        // Go dashboard

        setTimeout(
            function () {

                showSectionById(
                    "dashboard"
                );

            },
            1200
        );


    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        showUploadResult(

            "Error: " +
            escapeHTML(
                error.message
            ),

            false

        );

    }

}


// ============================================================
// UPDATE DASHBOARD AFTER PREDICTION
// ============================================================

function updateDashboardFromPrediction(
    data
) {

    const total =
        document.getElementById(
            "totalCustomers"
        );


    const high =
        document.getElementById(
            "highRisk"
        );


    const medium =
        document.getElementById(
            "mediumRisk"
        );


    const low =
        document.getElementById(
            "lowRisk"
        );


    if (total) {

        total.textContent =
            Number(
                data.total_customers
            ).toLocaleString();

    }


    if (high) {

        high.textContent =
            Number(
                data.high_risk
            ).toLocaleString();

    }


    if (medium) {

        medium.textContent =
            Number(
                data.medium_risk
            ).toLocaleString();

    }


    if (low) {

        low.textContent =
            Number(
                data.low_risk
            ).toLocaleString();

    }


    updateRiskChart({

        high_risk:
            data.high_risk,

        medium_risk:
            data.medium_risk,

        low_risk:
            data.low_risk

    });

}


// ============================================================
// UPLOAD RESULT
// ============================================================

function showUploadResult(
    message,
    success = true
) {

    const result =
        document.getElementById(
            "uploadResult"
        );


    if (!result) {

        return;

    }


    result.classList.remove(
        "hidden"
    );


    result.innerHTML =
        message;


    if (success) {

        result.style.background =
            "#dcfce7";

        result.style.color =
            "#166534";

    } else {

        result.style.background =
            "#fee2e2";

        result.style.color =
            "#991b1b";

    }

}


// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHTML(
    value
) {

    return String(
        value ?? ""
    )

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


// ============================================================
// ATTRIBUTE ESCAPE
// ============================================================

function escapeAttribute(
    value
) {

    return String(
        value ?? ""
    )

        .replace(
            /\\/g,
            "\\\\"
        )

        .replace(
            /'/g,
            "\\'"
        )

        .replace(
            /"/g,
            "&quot;"
        );

}


// ============================================================
// CLOSE MODAL WITH ESCAPE
// ============================================================

document.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Escape"
        ) {

            closeCustomerModal();

        }

    }
);


// ============================================================
// WHAT-IF SIMULATION & INTERVENTIONS
// ============================================================

async function runWhatIfSimulation() {
    const cust = window.activeModalCustomer || {};
    const attr = cust.Attributes || {};

    const newContract = document.getElementById("whatif_Contract").value;
    const newTech = document.getElementById("whatif_TechSupport").value;
    const newMonthly = parseFloat(document.getElementById("whatif_MonthlyCharges").value) || 70.0;

    const simPayload = Object.assign({}, attr, {
        customerID: cust.Customer_ID || "SIM-CUST",
        Contract: newContract,
        TechSupport: newTech,
        MonthlyCharges: newMonthly,
        TotalCharges: Math.max(newMonthly * (attr.tenure || 1), newMonthly)
    });

    const resultBox = document.getElementById("whatifResult");
    resultBox.style.display = "block";
    resultBox.textContent = "Simulating with AI model...";
    resultBox.style.color = "#2563eb";

    try {
        const response = await fetch("/api/simulate-whatif", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(simPayload)
        });

        const data = await response.json();
        if (data.status === "success") {
            const originalProb = Number(cust.Churn_Probability || 50);
            const simProb = Number(data.simulated_probability);
            const diff = (originalProb - simProb).toFixed(1);

            let statusMsg = "";
            if (diff > 0) {
                resultBox.style.color = "#16a34a";
                statusMsg = `Simulated Churn Risk: <strong>${simProb.toFixed(1)}%</strong> (${diff}% Risk Reduction achieved)`;
            } else if (diff < 0) {
                resultBox.style.color = "#dc2626";
                statusMsg = `Simulated Churn Risk: <strong>${simProb.toFixed(1)}%</strong> (+${Math.abs(diff)}% Risk Increase)`;
            } else {
                resultBox.style.color = "#64748b";
                statusMsg = `Simulated Churn Risk: <strong>${simProb.toFixed(1)}%</strong> (No change)`;
            }

            const smart = data.smart_retention || {};
            let offerHtml = "";
            if (smart.specific_offer) {
                offerHtml = `<div style="margin-top:8px; padding:8px 10px; background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; font-size:12px; color:#1e293b; font-weight:500;"><strong>Simulated Retention Offer:</strong> ${escapeHTML(smart.specific_offer)}</div>`;
            }

            resultBox.innerHTML = statusMsg + offerHtml;

            if (smart.call_script) {
                const callScriptText = document.getElementById("modalCallScript");
                const scriptBox = document.getElementById("modalScriptBox");
                if (callScriptText && scriptBox) {
                    callScriptText.textContent = `"${smart.call_script}"`;
                    scriptBox.style.display = "block";
                }
            }
        } else {
            resultBox.style.color = "#dc2626";
            resultBox.textContent = data.message || "Simulation failed.";
        }
    } catch (err) {
        resultBox.style.color = "#dc2626";
        resultBox.textContent = "Simulation error: " + err.message;
    }
}

function downloadRiskCsv(risk) {
    if (risk && risk !== "all") {
        window.location.href = `/api/download-predictions?risk=${encodeURIComponent(risk)}`;
    } else {
        window.location.href = "/api/download-predictions";
    }
}

function copyCallScript() {
    const scriptText = document.getElementById("modalCallScript").textContent;
    if (scriptText) {
        navigator.clipboard.writeText(scriptText.replace(/^"|"$/g, ''));
        alert("Retention pitch script copied to clipboard.");
    }
}

// ============================================================
// ADD NEW CUSTOMER SUBMISSION
// ============================================================

async function submitNewCustomer(event) {
    event.preventDefault();
    const statusEl = document.getElementById("addCustomerStatus");
    const resultBox = document.getElementById("newCustomerResult");

    statusEl.textContent = "Running model inference...";
    statusEl.style.color = "#2563eb";
    resultBox.style.display = "none";

    const payload = {
        customerID: document.getElementById("new_customerID").value.trim(),
        Contract: document.getElementById("new_Contract").value,
        tenure: parseInt(document.getElementById("new_tenure").value) || 1,
        MonthlyCharges: parseFloat(document.getElementById("new_MonthlyCharges").value) || 70.0,
        InternetService: document.getElementById("new_InternetService").value,
        TechSupport: document.getElementById("new_TechSupport").value,
        OnlineSecurity: document.getElementById("new_OnlineSecurity").value,
        OnlineBackup: document.getElementById("new_OnlineBackup").value,
        PaymentMethod: document.getElementById("new_PaymentMethod").value,
        PaperlessBilling: document.getElementById("new_PaperlessBilling").value,
        SeniorCitizen: parseInt(document.getElementById("new_SeniorCitizen").value) || 0,
        StreamingTV: document.getElementById("new_Streaming").value,
        StreamingMovies: document.getElementById("new_Streaming").value
    };

    try {
        const res = await fetch("/api/add-customer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.status === "success") {
            const cust = data.customer;
            statusEl.textContent = "Saved to Database successfully.";
            statusEl.style.color = "#16a34a";

            const riskBadgeColor = cust.Risk_Level === "High" ? "#dc2626" : cust.Risk_Level === "Medium" ? "#f59e0b" : "#16a34a";

            resultBox.style.display = "block";
            resultBox.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #e2e8f0; padding-bottom:10px;">
                    <div>
                        <h3 style="margin:0; font-size:16px; color:#0f172a;">Customer: ${cust.Customer_ID}</h3>
                        <span style="font-size:12px; color:#64748b;">Persona: <strong>${cust.Persona}</strong></span>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:${riskBadgeColor}; color:white; font-size:12px; font-weight:700; padding:4px 10px; border-radius:6px;">
                            ${cust.Risk_Level.toUpperCase()} RISK (${cust.Churn_Probability}%)
                        </span>
                    </div>
                </div>

                <div style="margin-bottom: 12px;">
                    <strong style="font-size:13px; color:#1e293b;">Primary Risk Driver:</strong>
                    <span style="font-size:13px; color:#475569;">${cust.Primary_Driver}</span>
                </div>

                <div style="background:#ffffff; border-radius:8px; padding:12px; border:1px solid #e2e8f0; margin-bottom:12px;">
                    <div style="font-size:12px; font-weight:700; color:#2563eb; margin-bottom:4px;">What We Can Offer (Proposed Retention Concession):</div>
                    <div style="font-size:13px; font-weight:600; color:#0f172a; margin-bottom:6px;">${cust.Specific_Offer}</div>
                    <ul style="margin:0; padding-left:18px; font-size:12px; color:#334155; line-height:1.5;">
                        ${cust.Actions.map(a => `<li>${a}</li>`).join('')}
                    </ul>
                </div>

                ${cust.Call_Script ? `
                <div style="background:#f1f5f9; border-left:3px solid #2563eb; padding:10px; font-size:12px; color:#1e293b; font-style:italic;">
                    <strong>Outbound Retention Script:</strong> "${cust.Call_Script}"
                </div>` : ''}
            `;
        } else {
            statusEl.textContent = "Error: " + (data.message || "Failed to add customer");
            statusEl.style.color = "#dc2626";
        }
    } catch (err) {
        statusEl.textContent = "Error: " + err.message;
        statusEl.style.color = "#dc2626";
    }
}
