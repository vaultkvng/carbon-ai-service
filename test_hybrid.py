import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_separator(title):
    print(f"\n{'='*60}\n➡️  TEST: {title}\n{'='*60}")

def print_error(response):
    print(f"❌ ERROR ({response.status_code})")
    print(response.text)

# TEST 1: LOCAL CSV LOOKUP
print_separator("1. LOCAL LOOKUP (From Sheet)")
payload_local = { "category": "FOOD", "customItem": "Rice", "quantity": 1, "unit": "kg" }
try:
    r = requests.post(f"{BASE_URL}/get-factor", json=payload_local)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Item: {data['item']}")
        print(f"   Factor: {data['estimatedEmissionFactor']} {data['unit']}")
        print(f"   Source: {data['sourceNote']}") 
        print(f"   Confidence: {data['confidence']}")
    else: print_error(r)
except Exception as e: print(f"❌ Failed: {e}")

# TEST 2: AI FALLBACK
print_separator("2. AI FALLBACK (From Gemini)")
payload_ai = { "category": "FOOD", "customItem": "Dragonfruit", "quantity": 1, "unit": "kg" }
try:
    r = requests.post(f"{BASE_URL}/get-factor", json=payload_ai)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Item: {data['item']}")
        print(f"   Factor: {data['estimatedEmissionFactor']} {data['unit']}")
        print(f"   Source: {data['sourceNote']}") 
        print(f"   Confidence: {data['confidence']}")
    else: print_error(r)
except Exception as e: print(f"❌ Failed: {e}")

# TEST 3: WEEKLY ANALYSIS
print_separator("3. WEEKLY RECOMMENDATIONS")
payload_weekly = {
  "userId": 123, "weekStart": "2025-01-01", "weekEnd": "2025-01-07",
  "currentWeekTotal": 17.5, "lastWeekTotal": 19.0, "percentageChange": -7.9,
  "categoryBreakdown": { "FOOD": 5.0, "TRANSPORT": 12.5, "ENERGY": 0.0, "WATER": 0.0 },
  "dailyEmissions": []
}
try:
    r = requests.post(f"{BASE_URL}/analyze-week", json=payload_weekly)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Trend: {data['weeklyInsights']['trend']}")
        print(f"✅ Top Recommendation: {data['recommendations'][0]['title']}")
    else: print_error(r)
except Exception as e: print(f"❌ Failed: {e}")