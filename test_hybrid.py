import requests
import json

# Base URL (Ensure your server is running on port 8000)
BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_separator(title):
    print(f"\n{'='*60}\n➡️  TEST: {title}\n{'='*60}")

def print_result(data):
    print(json.dumps(data, indent=2))

# ==========================================
# TEST 1: LOCAL CSV LOOKUP (High Confidence)
# ==========================================
# We use "Rice" because we know it's in your FOOD sheet.
print_separator("LOCAL LOOKUP (Should be from Teammate/Sheet)")
payload_local = {
  "category": "FOOD",
  "customItem": "Rice",
  "quantity": 1,
  "unit": "kg"
}
try:
    r = requests.post(f"{BASE_URL}/get-factor", json=payload_local)
    data = r.json()
    print(f"✅ Item: {data['item']}")
    print(f"   Factor: {data['estimatedEmissionFactor']} {data['unit']}")
    print(f"   Source: {data['sourceNote']}") # Should say "Teammate Research" or "Online Sheet"
    print(f"   Confidence: {data['confidence']}")
except Exception as e:
    print(f"❌ Failed: {e}")


# ==========================================
# TEST 2: GEMINI AI FALLBACK (Medium Confidence)
# ==========================================
# We use "Dragonfruit" because it is definitely NOT in your sheet.
print_separator("AI FALLBACK (Should be from Gemini)")
payload_ai = {
  "category": "FOOD",
  "customItem": "Dragonfruit",
  "quantity": 1,
  "unit": "kg"
}
try:
    r = requests.post(f"{BASE_URL}/get-factor", json=payload_ai)
    data = r.json()
    print(f"✅ Item: {data['item']}")
    print(f"   Factor: {data['estimatedEmissionFactor']} {data['unit']}")
    print(f"   Source: {data['sourceNote']}") # Should say "AI Estimation (Gemini)"
    print(f"   Confidence: {data['confidence']}")
except Exception as e:
    print(f"❌ Failed: {e}")


# ==========================================
# TEST 3: WEEKLY ANALYSIS (Use Case 2)
# ==========================================
print_separator("WEEKLY RECOMMENDATIONS (Logic Engine)")
payload_weekly = {
  "userId": 123,
  "weekStart": "2025-01-01",
  "weekEnd": "2025-01-07",
  "currentWeekTotal": 17.5,
  "lastWeekTotal": 19.0,
  "percentageChange": -7.9,
  "categoryBreakdown": { "FOOD": 5.0, "TRANSPORT": 12.5 },
  "dailyEmissions": []
}
try:
    r = requests.post(f"{BASE_URL}/analyze-week", json=payload_weekly)
    data = r.json()
    print(f"✅ Trend: {data['weeklyInsights']['trend']}")
    print(f"✅ Top Recommendation: {data['recommendations'][0]['title']}")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n✨ ALL SYSTEM TESTS COMPLETE.")