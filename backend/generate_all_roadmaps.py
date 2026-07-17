"""
generate_all_roadmaps.py
Script to iterate through all careers in the database that don't have a roadmap yet,
and use the OpenRouter LLM service to generate and save them.
"""

import time
import sys
from database import SessionLocal
import models
from llm_service import generate_career_roadmap

def main():
    print("Starting background roadmap generation...")
    db = SessionLocal()
    
    try:
        # Get all careers
        careers = db.query(models.Career).all()
        total = len(careers)
        print(f"Found {total} total careers in database.")
        
        # Find which ones need roadmaps
        careers_to_generate = []
        for c in careers:
            has_roadmap = db.query(models.Roadmap).filter(models.Roadmap.career_id == c.id).first()
            if not has_roadmap:
                careers_to_generate.append(c)
                
        remaining = len(careers_to_generate)
        print(f"{total - remaining} already have roadmaps. {remaining} left to generate.")
        
        if remaining == 0:
            print("All careers have roadmaps! Exiting.")
            return

        for i, c in enumerate(careers_to_generate, 1):
            title = c.name
            print(f"\n[{i}/{remaining}] Generating roadmap for: {title} ...")
            
            try:
                generated_data = generate_career_roadmap(title)
                
                c_data = generated_data.get("career", {})
                r_data = generated_data.get("roadmap", {})
                
                # Update career details
                if c_data.get("overview"): c.overview = c_data["overview"]
                if c_data.get("responsibilities"): c.responsibilities = c_data["responsibilities"]
                if c_data.get("who_can_apply"): c.who_can_apply = c_data["who_can_apply"]
                if c_data.get("industry_demand"): c.industry_demand = c_data["industry_demand"]
                if c_data.get("future_scope"): c.future_scope = c_data["future_scope"]
                if c_data.get("india_salary"): c.india_salary = c_data["india_salary"]
                if c_data.get("international_salary"): c.international_salary = c_data["international_salary"]
                if c_data.get("remote_opportunities"): c.remote_opportunities = c_data["remote_opportunities"]
                if c_data.get("growth_path"): c.growth_path = c_data["growth_path"]
                
                db.commit()
                
                # Create roadmap
                new_roadmap = models.Roadmap(
                    career_id=c.id,
                    title=r_data.get("title", f"{title} Complete Roadmap"),
                    description=r_data.get("description"),
                    skills_matrix=r_data.get("skills_matrix"),
                    learning_plans=r_data.get("learning_plans"),
                    learning_steps=r_data.get("learning_steps"),
                    projects=r_data.get("projects"),
                    practice_questions=r_data.get("practice_questions"),
                    certifications=r_data.get("certifications"),
                    interview_prep=r_data.get("interview_prep"),
                    readiness_checklist=r_data.get("readiness_checklist")
                )
                db.add(new_roadmap)
                db.commit()
                
                print(f"✅ Successfully saved {title} to database.")
                
            except Exception as e:
                print(f"❌ Failed on {title}: {e}")
                db.rollback()
                print("⏳ Pausing for 60 seconds to let the OpenRouter rate limits cool down...")
                time.sleep(60)
                continue
                
            # Sleep a bit to avoid hammer rate limits, even with fallbacks
            time.sleep(5)

    finally:
        db.close()
        print("\nFinished processing careers.")

if __name__ == "__main__":
    main()
