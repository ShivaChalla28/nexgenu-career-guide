"""
test_gemini.py - Test if the Gemini API key works.
Run: python test_gemini.py
"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GEMINI_API_KEY", "")
print(f"Key loaded: {key[:20]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"

payload = {
    "contents": [{"parts": [{"text": "Reply with exactly: {\"status\": \"ok\"}"}]}],
    "generationConfig": {"responseMimeType": "application/json", "temperature": 0}
}

print("Calling Gemini API...")
res = requests.post(url, json=payload, timeout=15)
print(f"HTTP Status: {res.status_code}")

if res.status_code == 200:
    data = res.json()
    text = data['candidates'][0]['content']['parts'][0]['text']
    print(f"✅ Gemini API works! Response: {text.strip()}")
else:
    print(f"❌ API Error: {res.text[:500]}")
    print("\nFix: Get a valid Gemini key from https://aistudio.google.com/app/apikey")
    print("Keys start with 'AIzaSy...'")
