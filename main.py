import os
import json
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv 

import knowledge_base

# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

# Get key securely
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key) # type: ignore
        # Tries to use the faster 2.0 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash') # type: ignore
        HAS_LLM = True
        print("✅ Gemini AI Connected (2.0 Flash)")
    except Exception as e:
        HAS_LLM = False
        print(f"⚠️ Warning: Gemini connection error: {e}")
else:
    HAS_LLM = False
    print("⚠️ Warning: GEMINI_API_KEY not found in .env file. LLM Fallback disabled.")

app = FastAPI(title="Carbon AI Service", version="3.0")

# --- DATA MODELS ---
class CustomItemRequest(BaseModel):
    category: str
    customItem: str
    quantity: float # Included for schema validation, but not used in calculation
    unit: str
    notes: Optional[str] = None

class CustomItemResponse(BaseModel):
    item: str
    category: str
    estimatedEmissionFactor: float
    unit: str
    confidence: float
    sourceNote: str

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
    categoryBreakdown: Dict[str, float]
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

# --- HELPER FUNCTIONS ---
async def get_llm_fallback(item_name, category):
    """Asks Gemini to estimate a carbon factor."""
    if not HAS_LLM:
        return {"factor": 0.0, "unit": "unknown"}
        
    print(f"🤖 CSV miss. Asking Gemini for '{item_name}'...")
    prompt = f"""
    Act as an environmental engineer. 
    Estimate the carbon emission factor for '{item_name}' in the category '{category}'.
    
    RULES:
    1. Return ONLY a valid JSON object. Do not write markdown.
    2. JSON Format: {{"factor": <number>, "unit": "kgCO2e/unit"}}
    3. Use global averages.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return {"factor": 0.0, "unit": "unknown"}

# --- ENDPOINTS ---

@app.post("/api/v1/get-factor", response_model=CustomItemResponse)
async def get_emission_factor(req: CustomItemRequest):
    # LAYER 1: Local Knowledge Base (High Accuracy)
    data = knowledge_base.lookup_factor(req.customItem, req.category)
    
    # LOGIC FIX: Ignore "Average" defaults so we can ask Gemini for a better guess
    is_real_match = data['factor'] > 0 and "Average" not in data['source']
    
    if is_real_match:
        # Construct Source Note (Source + Advice)
        full_note = data.get('source', 'Local Database')
        if data.get('note'):
            full_note += f" ({data['note']})"
            
        return CustomItemResponse(
            item=req.customItem,
            category=req.category,
            estimatedEmissionFactor=data['factor'],
            unit=data['unit'],
            confidence=0.9,
            sourceNote=full_note
        )

    # LAYER 2: LLM Wrapper (Fallback)
    llm_data = await get_llm_fallback(req.customItem, req.category)
    confidence = 0.4 if llm_data['factor'] > 0 else 0.0
    
    return CustomItemResponse(
        item=req.customItem,
        category=req.category,
        estimatedEmissionFactor=llm_data['factor'],
        unit=llm_data.get('unit', 'kgCO2e/unit'),
        confidence=confidence, 
        sourceNote="AI Estimation (Gemini)"
    )

@app.post("/api/v1/analyze-week", response_model=WeeklySummaryResponse)
async def analyze_weekly_summary(req: WeeklySummaryRequest):
    # 1. Trend Analysis
    if req.percentageChange < 0:
        trend_text = f"Your emissions decreased by {abs(req.percentageChange)}% compared to last week."
    else:
        trend_text = f"Your emissions increased by {req.percentageChange}%."

    # 2. Identify Highest Category
    highest_cat = max(req.categoryBreakdown, key=lambda k: req.categoryBreakdown[k])
    highest_val = req.categoryBreakdown[highest_cat]

    # 3. Recommendations Strategy
    recs = []
    # Top tip for highest category
    top_cat_tips = knowledge_base.TIPS_DB.get(highest_cat, [])
    if top_cat_tips:
        recs.append(RecommendationItem(
            title=top_cat_tips[0]['title'],
            estimatedSavingsPerWeek=top_cat_tips[0]['savings'],
            category=highest_cat
        ))
    
    # Fill remaining slots with other categories
    for cat, tips in knowledge_base.TIPS_DB.items():
        if cat != highest_cat and len(recs) < 3 and tips:
             recs.append(RecommendationItem(
                title=tips[0]['title'],
                estimatedSavingsPerWeek=tips[0]['savings'],
                category=cat
            ))

    # 4. Next Best Action
    best_rec = max(recs, key=lambda x: x.estimatedSavingsPerWeek) if recs else RecommendationItem(title="Keep logging", estimatedSavingsPerWeek=0, category="General")

    return WeeklySummaryResponse(
        weeklyInsights=WeeklyInsights(
            trend=trend_text,
            highestCategory=highest_cat,
            keyObservation=f"{highest_cat} was your biggest contributor ({highest_val}kg)."
        ),
        recommendations=recs,
        nextBestAction=NextBestAction(
            title=best_rec.title,
            estimatedImpact=best_rec.estimatedSavingsPerWeek,
            urgency="HIGH"
        )
    )