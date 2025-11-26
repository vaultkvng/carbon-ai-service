# knowledge_base.py
# TEAMMATE INSTRUCTIONS:
# 1. Add new items to FACTOR_DB for emission factors.
# 2. Add new tips to TIPS_DB for recommendations.
# 3. DO NOT change the 'lookup_factor' function at the bottom.
# 4. Watch out for commas at the end of every line!

# --- PART 1: EMISSION FACTORS ---
# Format: "item name": {"factor": NUMBER, "unit": "UNIT", "source": "Where you found it"}
# Units MUST be: "kgCO2_per_kg", "kgCO2_per_km", "kgCO2_per_kWh", or "kgCO2_per_liter"

FACTOR_DB = {
    # === EXAMPLE ENTRIES (COPY PASTE THESE FORMATS) ===
    "beef": {"factor": 60.0, "unit": "kgCO2_per_kg", "source": "Global Livestock Data"},
    "generator_diesel": {"factor": 1.27, "unit": "kgCO2_per_kWh", "source": "Diesel Emission Factor"},
    
    # === FOOD (Add Nigerian items here) ===
    "jollof rice": {"factor": 4.5, "unit": "kgCO2_per_kg", "source": "Rice + Oil estimate"},
    "pounded yam": {"factor": 1.8, "unit": "kgCO2_per_kg", "source": "Root vegetable processing"},
    # [TEAMMATE: ADD 20 MORE FOODS HERE]


    # === TRANSPORT (Add Vehicles here) ===
    "danfo bus": {"factor": 0.15, "unit": "kgCO2_per_km", "source": "Diesel Minibus Est."},
    "keke napep": {"factor": 0.08, "unit": "kgCO2_per_km", "source": "Tricycle Est."},
    # [TEAMMATE: ADD 10 MORE VEHICLES HERE]


    # === ENERGY & APPLIANCES ===
    "standing fan": {"factor": 0.05, "unit": "kgCO2_per_kWh", "source": "Low wattage appliance"},
    "ironing": {"factor": 0.8, "unit": "kgCO2_per_kWh", "source": "Heating element"},
    # [TEAMMATE: ADD 10 MORE APPLIANCES HERE]

}


# --- PART 2: RECOMMENDATION LIBRARY ---
# Format: {"title": "Short Tip Text", "savings": Estimated_kg_saved_per_week}

TIPS_DB = {
    "FOOD": [
        {"title": "Try Meatless Mondays to cut carbon", "savings": 1.5},
        {"title": "Swap imported rice for local Ofada rice", "savings": 0.3},
        # [TEAMMATE: ADD 10 FOOD TIPS]
    ],

    "TRANSPORT": [
        {"title": "Share a ride (Carpool) to work", "savings": 2.0},
        {"title": "Walk for trips under 2km", "savings": 0.5},
        # [TEAMMATE: ADD 10 TRANSPORT TIPS]
    ],

    "ENERGY": [
        {"title": "Turn off the stabilizer when not in use", "savings": 0.2},
        {"title": "Use natural light instead of bulbs during the day", "savings": 0.1},
        # [TEAMMATE: ADD 10 ENERGY TIPS]
    ],

    "WATER": [
        {"title": "Turn off the tap while brushing teeth", "savings": 0.1},
        # [TEAMMATE: ADD 5 WATER TIPS]
    ]
}

# --- DO NOT EDIT BELOW THIS LINE ---
def lookup_factor(item_name: str, category: str):
    key = item_name.lower().strip()
    
    # 1. Exact Match
    if key in FACTOR_DB:
        return FACTOR_DB[key]
    
    # 2. Partial Match
    for db_key in FACTOR_DB:
        if db_key in key:
            return FACTOR_DB[db_key]
            
    # 3. Fallback Defaults
    defaults = {
        "FOOD": {"factor": 3.0, "unit": "kgCO2_per_kg", "source": "Average Food Item"},
        "TRANSPORT": {"factor": 0.2, "unit": "kgCO2_per_km", "source": "Average Vehicle"},
        "ENERGY": {"factor": 0.5, "unit": "kgCO2_per_kWh", "source": "Average Grid"},
        "WATER": {"factor": 0.001, "unit": "kgCO2_per_liter", "source": "Water Treatment"}
    }
    return defaults.get(category, {"factor": 0.0, "unit": "unknown", "source": "Unknown"})