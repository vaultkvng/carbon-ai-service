import pandas as pd
import requests
import io
import os
from typing import Optional, Dict, List

# --- CONFIGURATION ---
# The Master Sheet ID
SHEET_ID = "1OGkCDkj_PxW9MgFV-uO5GTgCSbuUmUaD"

# YOUR SPECIFIC TAB IDs (Updated)
GIDS = {
    "FOOD": "239254558",
    "TRANSPORT": "1139057214",
    "ENERGY": "1947925401"
}

# Construct Download URLs
URLS = {
    "FOOD": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GIDS['FOOD']}",
    "TRANSPORT": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GIDS['TRANSPORT']}",
    "ENERGY": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GIDS['ENERGY']}"
}

# Local Backup Filenames (For Offline Safety)
LOCAL_FILES = {
    "FOOD": "backup_food.csv",
    "TRANSPORT": "backup_transport.csv",
    "ENERGY": "backup_energy.csv"
}

# Global Database
FACTOR_DB = {}

# Static Recommendations
TIPS_DB = {
    "FOOD": [
        {"title": "Try Meatless Mondays", "savings": 1.5},
        {"title": "Switch to local rice (Ofada)", "savings": 0.3}
    ],
    "TRANSPORT": [
        {"title": "Carpool to work", "savings": 2.0},
        {"title": "Walk for trips under 2km", "savings": 0.5}
    ],
    "ENERGY": [
        {"title": "Turn off AC 30 mins early", "savings": 0.3},
        {"title": "Use natural light during day", "savings": 0.1}
    ],
    "WATER": [
        {"title": "Fix leaking taps", "savings": 0.1}
    ]
}

def load_knowledge_base():
    """
    Loads data from Google Sheets. 
    1. Tries to download live data.
    2. Saves a local backup.
    3. Falls back to local backup if internet fails.
    """
    global FACTOR_DB
    print("🔄 Initializing Knowledge Base...")
    
    for category, url in URLS.items():
        backup_file = LOCAL_FILES[category]
        df = None
        
        # --- ATTEMPT 1: DOWNLOAD FROM GOOGLE (Online) ---
        try:
            print(f"   ☁️  Attempting sync for {category}...")
            response = requests.get(url, timeout=10) # 10 second timeout
            response.raise_for_status()
            
            # Convert to DataFrame
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            
            # SAVE BACKUP (Cache it locally!)
            df.to_csv(backup_file, index=False)
            print(f"      ✅ Download success! Saved backup to {backup_file}")
            
        except Exception as e:
            print(f"      ⚠️ Internet/Sheet failed ({e}). Checking backup...")
            
            # --- ATTEMPT 2: LOAD FROM BACKUP (Offline) ---
            if os.path.exists(backup_file):
                try:
                    df = pd.read_csv(backup_file)
                    print(f"      📂 Loaded from local backup: {backup_file}")
                except Exception as ex:
                    print(f"      ❌ Corrupt backup file: {ex}")
            else:
                print(f"      ❌ No internet and no backup found for {category}!")

        # --- PROCESS DATA (If df exists) ---
        if df is not None:
            # Normalize headers
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            # Smart Column Detection
            item_col = next((c for c in df.columns if 'item' in c or 'name' in c or 'appliance' in c or 'mode' in c or 'food' in c), None)
            factor_col = next((c for c in df.columns if 'factor' in c or 'emission' in c or 'co2' in c), None)
            unit_col = next((c for c in df.columns if 'unit' in c), None)
            source_col = next((c for c in df.columns if 'source' in c or 'ref' in c), None)
            note_col = next((c for c in df.columns if 'note' in c or 'advice' in c), None)

            if item_col and factor_col:
                count = 0
                for _, row in df.iterrows():
                    if pd.isna(row[item_col]): continue
                    item_name = str(row[item_col]).strip().lower()
                    
                    try:
                        # Handle string numbers like "1,200"
                        factor_val = float(str(row[factor_col]).replace(',', ''))
                    except ValueError:
                        continue 

                    # Get Optional Fields
                    unit_val = row[unit_col] if unit_col and not pd.isna(row[unit_col]) else "kgCO2e/unit"
                    source_val = row[source_col] if source_col and not pd.isna(row[source_col]) else "Teammate Research"
                    note_val = row[note_col] if note_col and not pd.isna(row[note_col]) else ""

                    # Add to Database
                    FACTOR_DB[item_name] = {
                        "factor": factor_val,
                        "unit": str(unit_val),
                        "source": str(source_val),
                        "note": str(note_val),
                        "category": category
                    }
                    count += 1
                print(f"      ✅ Successfully loaded {count} items for {category}")
            else:
                print(f"      ❌ Error: Required columns (Item/Factor) missing in {category}")

def lookup_factor(item_name: str, category: Optional[str] = None):
    """
    Fuzzy search for an item in the loaded database.
    """
    key = item_name.lower().strip()
    
    # 1. Exact Match
    if key in FACTOR_DB:
        return FACTOR_DB[key]
    
    # 2. Partial Match (e.g. "shrimp" inside "shrimp pasta")
    for db_key, data in FACTOR_DB.items():
        if db_key in key or key in db_key:
            # Optional: Enforce category match if provided
            if category and data.get('category') != category:
                continue
            return data
            
    # 3. Fallback Defaults
    defaults = {
        "FOOD": {"factor": 3.0, "unit": "kgCO2_per_kg", "source": "Average Food Item"},
        "TRANSPORT": {"factor": 0.2, "unit": "kgCO2_per_km", "source": "Average Vehicle"},
        "ENERGY": {"factor": 0.5, "unit": "kgCO2_per_kWh", "source": "Average Grid"},
        "WATER": {"factor": 0.001, "unit": "kgCO2_per_liter", "source": "Water Treatment"}
    }
    if category is None:
        return {"factor": 0.0, "unit": "unknown", "source": "Unknown"}
    return defaults.get(category, {"factor": 0.0, "unit": "unknown", "source": "Unknown"})

# Initialize automatically when imported
load_knowledge_base()