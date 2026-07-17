"""
llm_service.py
Generates career roadmaps using OpenRouter API (OpenAI-compatible).
Includes fallback models and retry logic for rate limits.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Fallback models in case the primary one is congested (429) or invalid (400)
MODELS = [
    "Qwen/Qwen3-4B-Instruct-2507"
]

SYSTEM_PROMPT = """You are an expert career counselor and curriculum designer for engineering students in India.
Generate a comprehensive, accurate career roadmap JSON for the requested career title.

The output MUST be a valid JSON object matching this exact schema (no extra text, just JSON):

{
  "career": {
    "name": "Full Career Title (e.g. Power Systems Engineer)",
    "slug": "url-friendly-slug",
    "overview": "2-3 sentence description of the role, what they do day-to-day, and which industries hire them",
    "responsibilities": ["Responsibility 1", "Responsibility 2", "Responsibility 3", "Responsibility 4", "Responsibility 5"],
    "who_can_apply": "Which engineering branches are eligible (e.g. EEE, ECE, Mechanical)",
    "industry_demand": "Current demand level and top 5 recruiting companies in India",
    "future_scope": "2-3 sentences on future growth, emerging technologies, and career ceiling",
    "india_salary": "Fresher: ₹X-Y LPA, Mid (3-5 yrs): ₹A-B LPA, Senior (7+ yrs): ₹C-D LPA",
    "international_salary": "USA: $X-Y/year, UAE: AED X-Y/year, Canada: CAD X-Y/year",
    "remote_opportunities": "Low/Medium/High with explanation",
    "growth_path": ["Junior Title", "Mid Title", "Senior Title", "Lead/Manager Title", "Architect/Director Title"]
  },
  "roadmap": {
    "title": "Complete Roadmap for Career Title",
    "description": "What this roadmap covers and expected outcome",
    "skills_matrix": {
      "Core Technical Skills": ["Skill 1", "Skill 2", "Skill 3", "Skill 4"],
      "Software & Tools": ["Tool 1", "Tool 2", "Tool 3"],
      "Programming & Scripting": ["Language 1", "Language 2"],
      "Domain Knowledge": ["Topic 1", "Topic 2", "Topic 3"],
      "Certifications & Standards": ["Cert 1", "Cert 2"],
      "Soft Skills": ["Communication", "Problem Solving", "Teamwork"]
    },
    "learning_plans": [
      {"name": "Fast Track", "duration": "6 Months", "daily_hours": "4 Hours"},
      {"name": "Standard", "duration": "8 Months", "daily_hours": "3 Hours"},
      {"name": "Balanced", "duration": "10 Months", "daily_hours": "2.5 Hours"},
      {"name": "Flexible", "duration": "12 Months", "daily_hours": "2 Hours"}
    ],
    "learning_steps": [
      {"phase": "M1-M2", "title": "Months 1-2: Foundations", "duration": "8 Weeks", "learn": ["Topic 1", "Topic 2", "Topic 3"]},
      {"phase": "M3-M4", "title": "Months 3-4: Core Skills", "duration": "8 Weeks", "learn": ["Topic 1", "Topic 2"]},
      {"phase": "M5-M6", "title": "Months 5-6: Advanced Topics", "duration": "8 Weeks", "learn": ["Topic 1", "Topic 2", "Topic 3"]},
      {"phase": "M7-M8", "title": "Months 7-8: Deep Dive & Specialization", "duration": "8 Weeks", "learn": ["Topic 1", "Topic 2"]},
      {"phase": "M9-M10", "title": "Months 9-10: Major Projects & Portfolio", "duration": "8 Weeks", "learn": ["Capstone Project", "Case Studies"]},
      {"phase": "M11-M12", "title": "Months 11-12: Interview & Job Readiness", "duration": "8 Weeks", "learn": ["Resume Building", "Mock Interviews", "Job Applications"]}
    ],
    "projects": {
      "Beginner": ["Project 1 – brief description", "Project 2 – brief description"],
      "Intermediate": ["Project 3 – brief description", "Project 4 – brief description"],
      "Advanced": ["Project 5 – brief description"],
      "Industry-Level": ["Project 6 – brief description (capstone)"]
    },
    "practice_questions": {
      "Topic 1": ["Question 1", "Question 2"],
      "Topic 2": ["Question 1", "Question 2"]
    },
    "certifications": ["Certification 1 (Provider)", "Certification 2 (Provider)", "Certification 3 (Provider)"],
    "interview_prep": {
      "Technical Questions": ["Q1", "Q2", "Q3", "Q4", "Q5"],
      "HR & Behavioral": ["Q1", "Q2", "Q3"]
    },
    "readiness_checklist": [
      "Checklist item 1",
      "Checklist item 2",
      "Checklist item 3",
      "Checklist item 4",
      "Checklist item 5",
      "Checklist item 6"
    ]
  }
}

IMPORTANT:
- Be specific to the Indian job market and engineering context
- Use real company names, real tools, real certifications
- Salary figures must be realistic for India 2024-2025
- All content must be directly relevant to the specific career title requested
- Do NOT use placeholder text like "Topic 1" — use real, specific topics
"""

def generate_career_roadmap(career_title: str) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing from .env file.")

    url = "https://inference.api.nscale.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    last_error = None

    print(f"[LLM] Generating roadmap for: {career_title}")

    # Try each model in the fallback list
    for model in MODELS:
        print(f"[LLM] Trying model: {model}")
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate the complete career roadmap for: {career_title}\n\nReturn ONLY valid JSON, no markdown, no explanation."}
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # If rate limited, sleep briefly then try the next model
            if response.status_code == 429:
                print(f"[LLM] Model {model} is rate limited (429). Switching to next model...")
                last_error = "Rate limit exceeded (429)"
                time.sleep(2)
                continue
                
            # If invalid model, just try next
            if response.status_code == 400 or response.status_code == 404:
                print(f"[LLM] Model {model} returned {response.status_code}. Switching...")
                last_error = f"Model error ({response.status_code})"
                continue

            if response.status_code != 200:
                print(f"[LLM] Model {model} failed with {response.status_code}. Switching...")
                last_error = f"API Error {response.status_code}: {response.text[:100]}"
                continue

            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            # Strip any markdown code fences if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            result = json.loads(content)
            print(f"[LLM] ✅ Roadmap generated successfully using {model}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"[LLM] ❌ JSON parsing failed for {model}: {e}")
            last_error = "Failed to parse JSON"
            continue
        except Exception as e:
            print(f"[LLM] ❌ Request failed for {model}: {e}")
            last_error = str(e)
            continue
            
    # If we get here, all models failed
    raise Exception(f"All fallback models failed. Last error: {last_error}")
