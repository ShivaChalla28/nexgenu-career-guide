import time
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap
from llm_service import generate_career_roadmap

def seed_all_branches():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    BRANCH_CAREERS = {
        "Computer Science Engineering (CSE)": [
            "Software Engineer", "Backend Developer", "Frontend Developer", 
            "Full Stack Developer", "Mobile App Developer", "DevOps Engineer", "Cloud Architect"
        ],
        "Information Technology (IT)": [
            "Systems Administrator", "Network Engineer", "Cybersecurity Analyst", 
            "IT Support Specialist", "Database Administrator", "Cloud Security Engineer"
        ],
        "Artificial Intelligence & Data Science": [
            "Machine Learning Engineer", "Data Scientist", "Data Engineer", 
            "NLP Engineer", "Computer Vision Engineer", "Generative AI Engineer"
        ],
        "Electronics & Communication Engineering (ECE)": [
            "VLSI Design Engineer", "Telecommunications Engineer", "Network Architect", 
            "Hardware Engineer", "Signal Processing Engineer", "RF Engineer"
        ],
        "Mechanical Engineering (Career Transition)": [
            "Mechanical Design Engineer", "Automotive Engineer", "Manufacturing Engineer", 
            "Thermal Engineer", "Mechatronics Engineer", "HVAC Engineer"
        ],
        "Civil Engineering (Career Transition)": [
            "Structural Engineer", "Construction Manager", "Geotechnical Engineer", 
            "Transportation Engineer", "Environmental Engineer", "Urban Planner"
        ],
        "Any Engineering Graduate with Programming Skills": [
            "Business Analyst", "Product Manager", "Scrum Master", 
            "Technical Writer", "QA Automation Engineer", "Data Analyst"
        ]
    }

    print(f"Starting seeding process for {len(BRANCH_CAREERS)} branches...\n")

    for branch_name, careers in BRANCH_CAREERS.items():
        print(f"--- Processing Branch: {branch_name} ---")
        
        # 1. Ensure the Branch exists
        branch = db.query(Branch).filter(Branch.name == branch_name).first()
        if not branch:
            slug = branch_name.lower().replace(" ", "-").replace("&", "and").replace("(", "").replace(")", "")
            print(f"Branch '{branch_name}' not found. Creating it...")
            branch = Branch(name=branch_name, slug=slug)
            db.add(branch)
            db.commit()
            db.refresh(branch)

        for title in careers:
            try:
                # Check if career already exists globally
                existing_career = db.query(Career).filter(Career.name == title).first()
                if existing_career:
                    # Check if it's mapped to this branch
                    mapping = db.query(BranchCareerMap).filter(
                        BranchCareerMap.branch_id == branch.id, 
                        BranchCareerMap.career_id == existing_career.id
                    ).first()
                    
                    if not mapping:
                        new_mapping = BranchCareerMap(branch_id=branch.id, career_id=existing_career.id)
                        db.add(new_mapping)
                        db.commit()
                        print(f"[{title}] Mapped to {branch_name}.")
                    else:
                        print(f"[{title}] Already exists and mapped.")
                    continue
                    
                # If not exists, use Gemini (or fallback) to generate
                print(f"[{title}] Generating Roadmap...")
                data = generate_career_roadmap(title)
                c_data = data.get("career", {})
                r_data = data.get("roadmap", {})
                
                slug = c_data.get("slug", title.lower().replace(" ", "-"))
                
                new_career = Career(
                    name=c_data.get("name", title),
                    slug=slug,
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
                db.add(new_career)
                db.commit()
                db.refresh(new_career)
                
                new_roadmap = Roadmap(
                    career_id=new_career.id,
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
                
                # Map to Branch
                bcm = BranchCareerMap(branch_id=branch.id, career_id=new_career.id)
                db.add(bcm)
                
                db.commit()
                print(f"[{title}] Successfully generated and saved!")
                
                time.sleep(1) # Small pause
                
            except Exception as e:
                print(f"[{title}] Failed to generate: {e}")

if __name__ == "__main__":
    seed_all_branches()
