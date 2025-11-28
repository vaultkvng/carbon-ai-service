# 🧠 Carbon Footprint AI Service (CPE 535)

## 📌 Project Overview
This is the **Intelligence Microservice** for the Group 1 Carbon Footprint Tracker. It operates as a specialized REST API that handles:
1.  **Emission Factor Lookup:** A Hybrid engine that finds carbon data for specific items (Food, Transport, Energy).
2.  **Weekly Analysis:** A Logic Engine that generates behavioral recommendations and insights.

### 🏗️ Architecture: Hybrid AI
To ensure **Speed**, **Accuracy**, and **100% Coverage**, this service uses a two-tier approach:
* **Tier 1 (Local Specialist):** Queries a curated **Google Sheet / Local CSV** database for high-accuracy Nigerian context (e.g., "Suya", "Danfo Bus", "I-better-pass-my-neighbor").
* **Tier 2 (Generative AI):** Falls back to **Google Gemini 2.0 Flash** to estimate emission factors for unknown items (e.g., "Dragonfruit", "Electric Unicycle").

---

## ⚙️ Setup & Installation

### 1. Prerequisites
* Python 3.9+
* Google Gemini API Key (Free Tier)

### 2. Install Dependencies
Run the following command to install FastAPI, Pandas, and the Google AI SDK:
```bash
pip install -r requirements.txt
3. Security Configuration (.env)
Crucial: Create a file named .env in the root directory. Paste your API key inside it:

Ini, TOML

GEMINI_API_KEY=AIzaSyD_YOUR_REAL_KEY_HERE
4. Data Sync (Auto-Caching)
On startup, the application (knowledge_base.py) automatically:

Connects to the Master Google Sheet.

Downloads the latest data for Food, Transport, and Energy.

Saves local backups (backup_food.csv, etc.) to ensure the app works offline.

5. Run the Server
Bash

uvicorn main:app --reload
Server URL: http://127.0.0.1:8000

Interactive Docs: http://127.0.0.1:8000/docs

🔌 API Contract (Integration Guide)
🧩 Use Case 1: Get Emission Factor (Lookup)
Endpoint: POST /api/v1/get-factor

Description: Returns the carbon emission factor for a specific item.

Logic: Checks Local DB first. If missing, queries Gemini AI.

Request Body:

JSON

{
  "category": "FOOD",
  "customItem": "shrimp pasta",
  "quantity": 250,
  "unit": "grams",
  "notes": "Optional notes from user"
}
Response:

JSON

{
  "item": "shrimp pasta",
  "category": "FOOD",
  "estimatedEmissionFactor": 0.0043,
  "unit": "kgCO2_per_gram",
  "confidence": 0.9,
  "sourceNote": "Local Database (Poore & Nemecek 2018)"
}
Note: confidence is 0.9 for verified local data, and 0.4 for AI estimates.

🧩 Use Case 2: Weekly Analysis & Coaching
Endpoint: POST /api/v1/analyze-week

Description: Analyzes user logs to determine trends and suggest behavioral changes.

Logic: Identifies the highest impact category and selects specific tips from the Rule Engine.

Request Body:

JSON

{
  "userId": 123,
  "weekStart": "2025-01-01",
  "weekEnd": "2025-01-07",
  "currentWeekTotal": 17.5,
  "lastWeekTotal": 19.0,
  "percentageChange": -7.9,
  "categoryBreakdown": {
    "FOOD": 5.0,
    "TRANSPORT": 12.5,
    "ENERGY": 0.0,
    "WATER": 0.0
  },
  "dailyEmissions": []
}
Response:

JSON

{
  "weeklyInsights": {
    "trend": "Your emissions decreased by 7.9% compared to last week.",
    "highestCategory": "TRANSPORT",
    "keyObservation": "TRANSPORT was your biggest contributor (12.5kg CO2)."
  },
  "recommendations": [
    {
      "title": "Carpool to work",
      "estimatedSavingsPerWeek": 2.0,
      "category": "TRANSPORT"
    },
    {
      "title": "Try Meatless Mondays",
      "estimatedSavingsPerWeek": 1.5,
      "category": "FOOD"
    }
  ],
  "nextBestAction": {
    "title": "Carpool to work",
    "estimatedImpact": 2.0,
    "urgency": "HIGH"
  }
}
🧪 Testing
To verify the system (both Local and AI layers), run the test script:

Bash

python test_hybrid.py