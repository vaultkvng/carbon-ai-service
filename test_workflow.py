import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_response(title, response):
    print(f"\n--- {title} ---")
    if response.status_code == 200:
        print("✅ SUCCESS")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ ERROR ({response.status_code})")
        print(response.text)

# TEST 1: Get Factor (Strict: No quantity/unit in request)
payload_factor = {
  "category": "FOOD",
  "customItem": "shrimp pasta",
  "notes": "Return only the emission factor"
}

# TEST 2: Weekly Summary (Strict: No userId/dates)
payload_weekly = {
  "currentWeekTotal": 17.5,
  "lastWeekTotal": 19.0,
  "percentageChange": -7.9,
  "categoryBreakdown": {
    "FOOD": 5.2,
    "ENERGY": 4.0,
    "TRANSPORT": 7.0,
    "WATER": 1.3
  },
  "notes": "Generate insights"
}

try:
    # Run Test 1
    r1 = requests.post(f"{BASE_URL}/get-factor", json=payload_factor)
    print_response("TEST 1: GET FACTOR", r1)

    # Run Test 2
    r2 = requests.post(f"{BASE_URL}/analyze-week", json=payload_weekly)
    print_response("TEST 2: WEEKLY ANALYSIS", r2)

except Exception as e:
    print(f"❌ Connection failed: {e}")