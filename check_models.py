import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load the hidden key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit()

# 2. Configure Gemini
genai.configure(api_key=api_key) # type: ignore

print("🔍 Checking available models for your API key...")
try:
    for m in genai.list_models(): # type: ignore
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")