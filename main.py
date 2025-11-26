from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
import knowledge_base

app = FastAPI(title="Carbon AI Service", version="2.0")

# --- USE CASE 1 MODELS ---
class CustomItemRequest(BaseModel):
    category: str
    customItem: str
    quantity: float
    unit: str
    notes: Optional[str] = None

class CustomItemResponse(BaseModel):
    item: str
    category: str
    estimatedEmissionFactor: float
    unit: str
    confidence: float
    sourceNote: str

# --- USE CASE 2 MODELS ---
class DailyEmission(BaseModel):
    date: str
    co2: float

class WeeklySummaryRequest(BaseModel):
    userId: int
    weekStart: str
    weekEnd: str
    currentWeekTotal: float
    lastWeekTotal: float
    percentageChange: float
    categoryBreakdown: Dict[str, float] # e.g., {"FOOD": 5.2, "ENERGY": 4.0}
    dailyEmissions: List[DailyEmission]
    notes: Optional[str] = None

class RecommendationItem(BaseModel):
    title: str
    estimatedSavingsPerWeek: float
    category: str

class WeeklyInsights(BaseModel):
    trend: str
    highestCategory: str
    keyObservation: str

class NextBestAction(BaseModel):
    title: str
    estimatedImpact: float
    urgency: str

class WeeklySummaryResponse(BaseModel):
    weeklyInsights: WeeklyInsights
    recommendations: List[RecommendationItem]
    nextBestAction: NextBestAction


# --- ENDPOINTS ---

@app.post("/api/v1/get-factor", response_model=CustomItemResponse)
async def get_emission_factor(req: CustomItemRequest):
    # 1. Look up the item in our library
    data = knowledge_base.lookup_factor(req.customItem, req.category)
    
    # 2. Logic to adjust units if necessary
    # (For MVP, we assume the factor DB matches the standard unit for simplicity)
    # If input was "grams" but DB is "kg", we divide factor by 1000
    factor = data['factor']
    unit_str = data['unit']
    
    if req.unit.lower() in ["grams", "g"] and "per_kg" in unit_str:
        factor = factor / 1000
        unit_str = "kgCO2_per_gram"

    # 3. Determine confidence (Simple logic)
    # If source is "Average...", confidence is lower
    confidence = 0.5 if "Average" in data['source'] else 0.85

    return CustomItemResponse(
        item=req.customItem,
        category=req.category,
        estimatedEmissionFactor=factor,
        unit=unit_str,
        confidence=confidence,
        sourceNote=data['source']
    )


@app.post("/api/v1/analyze-week", response_model=WeeklySummaryResponse)
async def analyze_weekly_summary(req: WeeklySummaryRequest):
    # 1. Analyze Trend
    if req.percentageChange < 0:
        trend_text = f"Your emissions decreased by {abs(req.percentageChange)}% compared to last week. Great job!"
    else:
        trend_text = f"Your emissions increased by {req.percentageChange}% compared to last week."

    # 2. Find Highest Category (FIXED LINE)
    highest_cat = max(req.categoryBreakdown, key=lambda k: req.categoryBreakdown[k])
    highest_val = req.categoryBreakdown[highest_cat]

    # 3. Generate Key Observation
    observation = f"{highest_cat} was your biggest contributor ({highest_val}kg CO2)."

    # 4. Generate Recommendations (Rule Engine)
    recs = []
    
    # Add top tip from highest category
    top_cat_tips = knowledge_base.TIPS_DB.get(highest_cat, [])
    if top_cat_tips:
        recs.append(RecommendationItem(
            title=top_cat_tips[0]['title'],
            estimatedSavingsPerWeek=top_cat_tips[0]['savings'],
            category=highest_cat
        ))

    # Add tips from other categories to fill up to 3
    for cat, tips in knowledge_base.TIPS_DB.items():
        if cat != highest_cat and len(recs) < 3 and tips:
             recs.append(RecommendationItem(
                title=tips[0]['title'],
                estimatedSavingsPerWeek=tips[0]['savings'],
                category=cat
            ))

    # 5. Determine Next Best Action (The highest impact item)
    # Simply pick the recommendation with the highest savings
    if recs:
        best_rec = max(recs, key=lambda x: x.estimatedSavingsPerWeek)
    else:
        # Fallback if no tips found
        best_rec = RecommendationItem(title="Keep logging data", estimatedSavingsPerWeek=0.0, category="GENERAL")

    return WeeklySummaryResponse(
        weeklyInsights=WeeklyInsights(
            trend=trend_text,
            highestCategory=highest_cat,
            keyObservation=observation
        ),
        recommendations=recs,
        nextBestAction=NextBestAction(
            title=best_rec.title,
            estimatedImpact=best_rec.estimatedSavingsPerWeek,
            urgency="HIGH"
        )
    )