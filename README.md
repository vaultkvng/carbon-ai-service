# 🧠 Carbon Footprint AI Service (Hybrid)

## 📌 Overview
Intelligence Layer providing:
1.  **Factor Lookup:** Checks Local CSVs first -> Falls back to Gemini AI.
2.  **Weekly Analysis:** Generates insights from user logs.

## ⚙️ Setup
1.  **Install:** `pip install -r requirements.txt`
2.  **Env:** Create `.env` with `GEMINI_API_KEY=your_key`.
3.  **Run:** `uvicorn main:app --reload`

## 🔌 API Contract
**POST /api/v1/get-factor**
Input: `{ "category": "FOOD", "customItem": "shrimp", "quantity": 1, "unit": "kg" }`
Output: `{ "emissionFactor": 3.2, "unit": "kgCO2e/kg", "sourceNote": "Local DB" }`

**POST /api/v1/analyze-week**
Input: `{ "currentWeekTotal": 10.0, "categoryBreakdown": {"FOOD": 8.0} ... }`
Output: Returns insights & recommendations.