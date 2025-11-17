import requests
import json

# Ensure your main.py is running on this URL
BASE_URL = "http://127.0.0.1:8000/api/v1/recommend"

def print_result(category, payload, response):
    print(f"\n--- TESTING {category.upper()} ---")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ STATUS: {response.status_code}")
        print(f"💡 TIP: {data['message']}")
        print(f"⚠️ SEVERITY: {data['severity']}")
        print(f"📉 SAVINGS: {data['estimated_savings_co2_kg']}kg")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)

# 1. TEST FOOD (Beef)
food_payload = {
    "user_id": "u1", 
    "meal_type": "lunch", 
    "main_ingredient": "beef", 
    "portion_size": "large"
}
print_result("Food", food_payload, requests.post(f"{BASE_URL}/food", json=food_payload))

# 2. TEST TRANSPORT (Short Car Trip)
transport_payload = {
    "user_id": "u1", 
    "transport_mode": "car", 
    "distance_km": 2.0, 
    "carpool": False
}
print_result("Transport", transport_payload, requests.post(f"{BASE_URL}/transport", json=transport_payload))

# 3. TEST ENERGY (Generator)
energy_payload = {
    "user_id": "u1", 
    "appliance_type": "ac", 
    "hours_used": 5.0, 
    "energy_source": "generator"
}
print_result("Energy", energy_payload, requests.post(f"{BASE_URL}/energy", json=energy_payload))