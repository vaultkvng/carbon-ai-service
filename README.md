# 🧠 Carbon Footprint AI Service (Hybrid)

## 📌 Overview
Intelligence Layer providing:
1.  **Factor Lookup:** Checks Local CSVs first -> Falls back to Gemini AI.
2.  **Weekly Analysis:** Generates insights from user logs.

## ⚙️ Setup
1.  **Install:** `pip install -r requirements.txt`
2.  **Env:** Create `.env` with `GEMINI_API_KEY=your_key`.
3.  **Run:** `uvicorn main:app --reload`

## 🔌 API Contract (Backend Integration)

### Use Case 1: Get Emission Factor
**Endpoint:** `POST /api/v1/get-factor`
* **Description:** Returns the carbon intensity for a specific item.
* **Input (JSON):**
    ```json
    {
      "category": "FOOD",
      "customItem": "shrimp pasta",
      "notes": "Optional notes"
    }
    ```
* **Output (JSON):**
    ```json
    {
      "category": "FOOD",
      "customItem": "shrimp pasta",
      "emissionFactor": 3.2,
      "unit": "kgCO2/kg"
    }
    ```

### Use Case 2: Weekly Summary & Recommendations
**Endpoint:** `POST /api/v1/analyze-week`
* **Description:** Analyzes aggregated totals and returns behavioral insights.
* **Input (JSON):**
    ```json
    {
      "currentWeekTotal": 17.5,
      "lastWeekTotal": 19.0,
      "percentageChange": -7.9,
      "categoryBreakdown": {
        "FOOD": 5.2,
        "ENERGY": 4.0,
        "TRANSPORT": 7.0,
        "WATER": 1.3
      },
      "notes": "Optional context"
    }
    ```
* **Output (JSON):**
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