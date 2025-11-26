# knowledge_base.py

# --- PART 1: EMISSION FACTORS ---
# Format: "item_key": {"factor": float, "unit": str, "source": str}
# Factors should be in kgCO2 per [Standard Unit]
FACTOR_DB = {
    # FOOD (kgCO2 per kg)
    "beef": {"factor": 60.0, "unit": "kgCO2_per_kg", "source": "Global Livestock Data"},
    "shrimp": {"factor": 12.0, "unit": "kgCO2_per_kg", "source": "Ocean Friendly"},
    "shrimp pasta": {"factor": 4.3, "unit": "kgCO2_per_kg", "source": "Composite Meal Est."},
    "rice": {"factor": 4.0, "unit": "kgCO2_per_kg", "source": "Agri-Stats"},
    
    # TRANSPORT (kgCO2 per km)
    "quad bike": {"factor": 0.45, "unit": "kgCO2_per_km", "source": "Offroad Vehicle Est."},
    "bus": {"factor": 0.1, "unit": "kgCO2_per_km", "source": "Public Transport"},
    
    # ENERGY (kgCO2 per kWh)
    "industrial sewing machine": {"factor": 0.5, "unit": "kgCO2_per_kWh", "source": "Industrial Grid Avg"},
    
    # WATER (kgCO2 per Liter)
    "spa tub": {"factor": 0.005, "unit": "kgCO2_per_liter", "source": "Water Heating Est."}
}

# --- PART 2: RECOMMENDATION LIBRARY ---
# Tips categorized by domain
TIPS_DB = {
    "FOOD": [
        {"title": "Try Meatless Mondays", "savings": 1.5},
        {"title": "Reduce seafood meals to once weekly", "savings": 1.1},
        {"title": "Buy local produce to cut transport carbon", "savings": 0.5}
    ],
    "TRANSPORT": [
        {"title": "Switch 1 short trip from driving to walking", "savings": 0.6},
        {"title": "Carpool for your commute", "savings": 2.0},
        {"title": "Check tire pressure to improve fuel efficiency", "savings": 0.2}
    ],
    "ENERGY": [
        {"title": "Turn off AC 30 minutes earlier", "savings": 0.3},
        {"title": "Unplug 'vampire' electronics at night", "savings": 0.1},
        {"title": "Switch to LED bulbs", "savings": 0.15}
    ],
    "WATER": [
        {"title": "Take shorter showers (under 5 mins)", "savings": 0.2},
        {"title": "Fix leaking taps immediately", "savings": 0.1}
    ]
}

def lookup_factor(item_name: str, category: str):
    """Fuzzy search for an item."""
    key = item_name.lower().strip()
    
    # 1. Exact Match
    if key in FACTOR_DB:
        return FACTOR_DB[key]
    
    # 2. Partial Match (e.g., "shrimp" inside "shrimp pasta")
    # Simple logic: return the first key that exists in the input
    for db_key in FACTOR_DB:
        if db_key in key:
            return FACTOR_DB[db_key]
            
    # 3. Category Default (Fallback)
    defaults = {
        "FOOD": {"factor": 3.0, "unit": "kgCO2_per_kg", "source": "Average Food Item"},
        "TRANSPORT": {"factor": 0.2, "unit": "kgCO2_per_km", "source": "Average Vehicle"},
        "ENERGY": {"factor": 0.5, "unit": "kgCO2_per_kWh", "source": "Average Grid"},
        "WATER": {"factor": 0.001, "unit": "kgCO2_per_liter", "source": "Water Treatment"}
    }
    return defaults.get(category, {"factor": 0.0, "unit": "unknown", "source": "Unknown"})