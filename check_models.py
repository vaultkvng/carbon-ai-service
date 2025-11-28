import google.generativeai as genai
import os

# Paste your NEW key here (the one you just made)
os.environ["GEMINI_API_KEY"] = "AIzaSyCb_mkOlRt1FN59cFCVM-uQfM5SntqJLc4"

genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # type: ignore

print("🔍 Checking available models for your API key...")
try:
    for m in genai.list_models(): # type: ignore
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")