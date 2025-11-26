import requests
import json

# Base URL (Ensure your server is running on port 8000)
BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_response(title, response):
    print(f"\n--- {title} ---")
    if response.status_code == 200:
        print("✅ SUCCESS (200 OK)")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ ERROR ({response.status_code})")
        print(response.text)

# ==========================================
# TEST 1: Get Emission Factor (Use Case 1)
# Scenario: Backend asks for "shrimp pasta"
# ==========================================
payload_factor = {
  "category": "FOOD",
  "customItem": "shrimp pasta",
  "quantity": 250,
  "unit": "grams",
  "notes": "Testing emission factor lookup"
}

try:
    response = requests.post(f"{BASE_URL}/get-factor", json=payload_factor)
    print_response("TEST 1: LOOKUP FACTOR", response)
except Exception as e:
    print(f"❌ Connection failed: {e}")


# ==========================================
# TEST 2: Weekly Analysis (Use Case 2)
# Scenario: Backend sends weekly summary
# ==========================================
payload_weekly = {
  "userId": 123,
  "weekStart": "2025-01-01",
  "weekEnd": "2025-01-07",
  "currentWeekTotal": 17.5,
  "lastWeekTotal": 19.0,
  "percentageChange": -7.9,
  "categoryBreakdown": {
    "FOOD": 5.2,
    "ENERGY": 4.0,
    "TRANSPORT": 7.0, # Highest category
    "WATER": 1.3
  },
  "dailyEmissions": [
    {"date": "2025-01-01", "co2": 2.5},
    {"date": "2025-01-02", "co2": 2.1},
    {"date": "2025-01-03", "co2": 1.8}
  ],
  "notes": "Generate insights"
}

try:
    response = requests.post(f"{BASE_URL}/analyze-week", json=payload_weekly)
    print_response("TEST 2: WEEKLY ANALYSIS", response)
except Exception as e:
    print(f"❌ Connection failed: {e}")