# 🧠 Carbon Footprint AI Service (Microservice)

## 📌 Overview
The Intelligence Layer for Group 1. It provides two key services:
1.  **Specialist Data Lookup:** Provides emission factors for local items (e.g., "Suya", "Danfo") that aren't in the main database.
2.  **AI Recommendations:** Generates weekly insights and behavioral nudges based on user logs.

**Architecture:** Hybrid AI
* **Tier 1:** Local CSV Database (High Accuracy, Nigerian Context).
* **Tier 2:** Google Gemini LLM Fallback (100% Coverage for unknown items).

---

## ⚙️ Setup
1.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Add Data Files:** Ensure `Carbon_Emissions.xlsx - FOOD.csv` (etc.) are in the root folder.
3.  **Run Server:**
    ```bash
    uvicorn main:app --reload
    ```
    API will run at: `http://localhost:8000`

---

## 🔌 API Contract (For Backend Integration)

### 1. Get Emission Factor (Use Case 1)
**Endpoint:** `POST /api/v1/get-factor`
* **Logic:** Checks local CSVs first. If not found, queries Gemini AI.
* **Input:**
    ```json
    {
      "category": "FOOD",
      "customItem": "shrimp pasta",
      "quantity": 250,
      "unit": "grams"
    }
    ```
* **Output:**
    ```json
    {
      "item": "shrimp pasta",
      "estimatedEmissionFactor": 0.0043,
      "unit": "kgCO2_per_gram",
      "confidence": 0.9,
      "sourceNote": "Local Database (High packaging impact)"
    }
    ```

### 2. Analyze Weekly Summary (Use Case 2)
**Endpoint:** `POST /api/v1/analyze-week`
* **Logic:** Analyzes trends and picks top 3 tips from the Rule Engine.
* **Input:**
    ```json
    {
      "userId": 123,
      "weekStart": "2025-01-01",
      "weekEnd": "2025-01-07",
      "currentWeekTotal": 17.5,
      "lastWeekTotal": 19.0,
      "percentageChange": -7.9,
      "categoryBreakdown": { "FOOD": 5.0, "TRANSPORT": 12.5 },
      "dailyEmissions": []
    }
    ```
* **Output:**
    ```json
    {
      "weeklyInsights": {
        "trend": "Your emissions decreased by 7.9%...",
        "highestCategory": "TRANSPORT",
        "keyObservation": "TRANSPORT was your biggest contributor..."
      },
      "recommendations": [
        { "title": "Carpool to work", "category": "TRANSPORT", "estimatedSavingsPerWeek": 2.0 }
      ],
      "nextBestAction": { "title": "Carpool to work", "urgency": "HIGH" }
    }
    ```