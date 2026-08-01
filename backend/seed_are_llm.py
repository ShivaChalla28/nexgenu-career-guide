import os
import json
import time
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap
from llm_service import generate_career_roadmap
from seed_are_branch import ARE_CATEGORIES, make_slug

def seed_llm():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    branch_name = "Automation & Robotics Engineering (ARE)"
    branch = db.query(Branch).filter(Branch.name == branch_name).first()
    if not branch:
        # Create branch if it doesn't exist
        branch_slug = make_slug(branch_name)
        branch = Branch(
            name=branch_name, 
            slug=branch_slug,
            description="Automation & Robotics Engineering combines Mechanical Engineering, Electronics, Electrical Engineering, Computer Science, Artificial Intelligence, Industrial Automation, Embedded Systems, and Control Engineering to design intelligent automated systems, industrial robots, autonomous machines, and smart factories.",
            icon="🤖"
        )
        db.add(branch)
        db.commit()
        db.refresh(branch)

    total_careers = sum(len(titles) for titles in ARE_CATEGORIES.values())
    current = 0

    for category, titles in ARE_CATEGORIES.items():
        for title in titles:
            current += 1
            try:
                slug = make_slug(title)
                career = db.query(Career).filter(Career.slug == slug).first()
                # Check if roadmap exists and looks complete
                if career:
                    roadmap = db.query(Roadmap).filter(Roadmap.career_id == career.id).first()
                    # If roadmap is complete with practice_questions, we could skip. But let's generate anyway if missing or broken.
                    if roadmap and roadmap.practice_questions:
                        print(f"[{current}/{total_careers}] {title} already fully seeded. Skipping.")
                        continue
                
                print(f"[{current}/{total_careers}] {title} - Generating via OpenRouter...")
                data = generate_career_roadmap(title)
                c_data = data.get("career", {})
                r_data = data.get("roadmap", {})
                
                if not career:
                    career = Career(
                        name=c_data.get("name", title),
                        slug=slug,
                        category=category,
                        overview=c_data.get("overview"),
                        responsibilities=c_data.get("responsibilities"),
                        who_can_apply=c_data.get("who_can_apply"),
                        industry_demand=c_data.get("industry_demand"),
                        future_scope=c_data.get("future_scope"),
                        india_salary=c_data.get("india_salary"),
                        international_salary=c_data.get("international_salary"),
                        remote_opportunities=c_data.get("remote_opportunities"),
                        growth_path=c_data.get("growth_path")
                    )
                    db.add(career)
                    db.commit()
                    db.refresh(career)
                else:
                    career.overview = c_data.get("overview", career.overview)
                    career.responsibilities = c_data.get("responsibilities", career.responsibilities)
                    career.who_can_apply = c_data.get("who_can_apply", career.who_can_apply)
                    career.industry_demand = c_data.get("industry_demand", career.industry_demand)
                    career.future_scope = c_data.get("future_scope", career.future_scope)
                    career.india_salary = c_data.get("india_salary", career.india_salary)
                    career.international_salary = c_data.get("international_salary", career.international_salary)
                    career.remote_opportunities = c_data.get("remote_opportunities", career.remote_opportunities)
                    career.growth_path = c_data.get("growth_path", career.growth_path)
                    db.commit()

                # map to branch
                mapping = db.query(BranchCareerMap).filter(
                    BranchCareerMap.branch_id == branch.id,
                    BranchCareerMap.career_id == career.id
                ).first()
                if not mapping:
                    db.add(BranchCareerMap(branch_id=branch.id, career_id=career.id))
                    db.commit()

                roadmap = db.query(Roadmap).filter(Roadmap.career_id == career.id).first()
                if roadmap:
                    db.delete(roadmap)
                    db.commit()
                
                new_roadmap = Roadmap(
                    career_id=career.id,
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
                print(f"[{title}] Successfully generated and saved!")
                time.sleep(6) # Prevent extreme rate limiting
            except Exception as e:
                print(f"[{title}] Failed to generate: {e}")

if __name__ == "__main__":
    seed_llm()
