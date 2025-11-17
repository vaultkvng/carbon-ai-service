from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# --- 1. APP INITIALIZATION ---
app = FastAPI(
    title="Carbon Footprint AI Service",
    description="Microservice for calculating impact and generating tips.",
    version="1.0"
)

# --- 2. DATA MODELS (The Contract) ---

class RecommendationOutput(BaseModel):
    title: str
    message: str
    action_type: str        # "substitution", "praise", "warning", "behavior_change"
    severity: str           # "high", "medium", "low"
    estimated_savings_co2_kg: float

class FoodLogInput(BaseModel):
    user_id: str
    meal_type: str          # "lunch", "dinner"
    main_ingredient: str    # "beef", "chicken", "vegetables"
    portion_size: str       # "small", "medium", "large"
    side_dish: Optional[str] = None

class TransportLogInput(BaseModel):
    user_id: str
    transport_mode: str     # "car", "bus", "train", "bicycle", "walking"
    distance_km: float
    fuel_type: Optional[str] = "petrol"
    carpool: bool = False

class EnergyLogInput(BaseModel):
    user_id: str
    appliance_type: str     # "ac", "heater", "tv", "laptop"
    hours_used: float
    energy_source: str = "grid" # "grid" or "generator"

# --- 3. LOGIC FUNCTIONS (The Brain) ---

def calculate_food_impact(data: FoodLogInput) -> RecommendationOutput:
    ingredient = data.main_ingredient.lower()
    portion = data.portion_size.lower()

    # RULE 1: High Impact (Beef)
    if ingredient == "beef":
        savings = 2.5 if portion == "large" else 1.5
        return RecommendationOutput(
            title="High Impact Alert",
            message=f"Beef is a high-carbon food. Swapping this {portion} portion for chicken could save ~{savings}kg CO2.",
            action_type="substitution",
            severity="high",
            estimated_savings_co2_kg=savings
        )
    # RULE 2: Medium Impact (Chicken/Pork)
    elif ingredient in ["chicken", "pork"]:
        return RecommendationOutput(
            title="Good Balance",
            message="Chicken has a lower footprint than red meat, but a veggie option is even better!",
            action_type="info",
            severity="medium",
            estimated_savings_co2_kg=0.5
        )
    # RULE 3: Low Impact (Vegetables/Tofu)
    elif ingredient in ["vegetables", "tofu", "beans"]:
        return RecommendationOutput(
            title="Eco Warrior!",
            message="Great job! Plant-based meals have the lowest carbon footprint.",
            action_type="praise",
            severity="low",
            estimated_savings_co2_kg=0.0
        )
    else:
        return RecommendationOutput(
            title="Log Recorded",
            message=f"We've tracked your {ingredient}.",
            action_type="info",
            severity="low",
            estimated_savings_co2_kg=0.0
        )

def calculate_transport_impact(data: TransportLogInput) -> RecommendationOutput:
    mode = data.transport_mode.lower()
    distance = data.distance_km
    
    factors = {"car": 0.19, "bus": 0.10, "train": 0.04, "motorbike": 0.10, "bicycle": 0.0, "walking": 0.0}
    factor = factors.get(mode, 0.19)
    
    if mode == "car" and data.carpool:
        factor = factor / 2
        
    total_emissions = factor * distance

    # Scenario: Short Car Trip
    if mode == "car" and distance < 3:
        return RecommendationOutput(
            title="Walkable Distance Alert",
            message=f"This {distance}km trip generated {total_emissions:.2f}kg CO2. Walking next time would cut this to zero!",
            action_type="substitution",
            severity="high",
            estimated_savings_co2_kg=total_emissions
        )
    # Scenario: Zero Emissions
    elif mode in ["bicycle", "walking"]:
        return RecommendationOutput(
            title="Zero Carbon Hero!",
            message=f"You traveled {distance}km with zero emissions. Keep it up!",
            action_type="praise",
            severity="low",
            estimated_savings_co2_kg=0.19 * distance
        )
    else:
        return RecommendationOutput(
            title="Trip Logged",
            message=f"Your trip generated {total_emissions:.2f}kg CO2.",
            action_type="info",
            severity="low",
            estimated_savings_co2_kg=0.0
        )

def calculate_energy_impact(data: EnergyLogInput) -> RecommendationOutput:
    appliance = data.appliance_type.lower()
    hours = data.hours_used
    source = data.energy_source.lower()

    wattage_map = {"ac": 1500, "heater": 2000, "washing_machine": 500, "fridge": 200, "tv": 100, "laptop": 50}
    watts = wattage_map.get(appliance, 100)
    kwh = (watts * hours) / 1000
    
    # Generator vs Grid
    emission_factor = 1.27 if source == "generator" else 0.475
    total_emissions = kwh * emission_factor

    if source == "generator" and hours > 2:
         return RecommendationOutput(
            title="Generator Alert",
            message=f"Using a generator produces ~3x more CO2 than the grid. Limit heavy appliances like {appliance}.",
            action_type="warning",
            severity="high",
            estimated_savings_co2_kg=total_emissions * 0.6
        )
    elif appliance == "ac" and hours > 4:
        return RecommendationOutput(
            title="Cooling Optimization",
            message="AC is your biggest energy cost. Try using a fan for the first hour.",
            action_type="behavior_change",
            severity="medium",
            estimated_savings_co2_kg=total_emissions * 0.2
        )
    else:
        return RecommendationOutput(
            title="Energy Logged",
            message=f"Used {kwh:.2f} kWh via {source}.",
            action_type="info",
            severity="low",
            estimated_savings_co2_kg=0.0
        )

# --- 4. API ENDPOINTS ---

@app.post("/api/v1/recommend/food", response_model=RecommendationOutput)
async def get_food_recommendation(log: FoodLogInput):
    return calculate_food_impact(log)

@app.post("/api/v1/recommend/transport", response_model=RecommendationOutput)
async def get_transport_recommendation(log: TransportLogInput):
    return calculate_transport_impact(log)

@app.post("/api/v1/recommend/energy", response_model=RecommendationOutput)
async def get_energy_recommendation(log: EnergyLogInput):
    return calculate_energy_impact(log)

@app.get("/")
async def root():
    return {"message": "Carbon AI Service is Online"}


