import time
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap
from llm_service import generate_career_roadmap

def seed_eee_careers():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    branch_name = "Electrical & Electronics Engineering (EEE)"
    
    # 1. Ensure the EEE Branch exists
    branch = db.query(Branch).filter(Branch.name == branch_name).first()
    if not branch:
        print(f"Branch '{branch_name}' not found. Creating it...")
        branch = Branch(
            name=branch_name, 
            slug="electrical-electronics-engineering-eee"
        )
        db.add(branch)
        db.commit()
        db.refresh(branch)

    careers_to_add = [
        # Core Careers
        "Power Systems Engineer", 
        "Electrical Design Engineer", 
        "Protection Engineer", 
        "Substation Engineer", 
        "Transmission Engineer", 
        "Distribution Engineer", 
        "Renewable Energy Engineer", 
        "Solar Engineer", 
        "Wind Energy Engineer",
        
        # Automation Careers
        "PLC Programmer", 
        "SCADA Engineer", 
        "Industrial Automation Engineer", 
        "Control Systems Engineer", 
        
        # IT Careers
        "Embedded Engineer", 
        "Robotics Engineer", 
        "IoT Engineer", 
        "AI Engineer", 
        "Data Analyst"
    ]

    print(f"Found {len(careers_to_add)} EEE Careers to generate using Gemini AI.")

    for title in careers_to_add:
        print(f"\n[{title}] Generating AI Roadmap...")
        try:
            # Check if career already exists globally
            existing_career = db.query(Career).filter(Career.name == title).first()
            if existing_career:
                print(f"[{title}] Career already exists in database. Checking branch mapping...")
                
                # Check if it's mapped to EEE branch
                mapping = db.query(BranchCareerMap).filter(
                    BranchCareerMap.branch_id == branch.id, 
                    BranchCareerMap.career_id == existing_career.id
                ).first()
                
                if not mapping:
                    print(f"[{title}] Mapping to EEE Branch...")
                    new_mapping = BranchCareerMap(branch_id=branch.id, career_id=existing_career.id)
                    db.add(new_mapping)
                    db.commit()
                continue
                
            # If not exists, use Gemini to generate
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
            
            # Map to EEE Branch
            bcm = BranchCareerMap(branch_id=branch.id, career_id=new_career.id)
            db.add(bcm)
            
            db.commit()
            print(f"[{title}] Successfully generated and saved!")
            
            # Pause to avoid hitting Gemini free tier rate limits
            time.sleep(3)
            
        except Exception as e:
            print(f"[{title}] Failed to generate: {e}")

if __name__ == "__main__":
    seed_eee_careers()
