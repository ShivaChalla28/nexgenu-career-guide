import time
import uuid
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap

def generate_offline_roadmap(title, branch_name):
    """
    Generates highly detailed, realistic roadmap data purely offline based on the career title and branch.
    """
    slug = title.lower().replace(" ", "-")
    
    # 1. Determine Domain Keywords & Data
    is_software = any(kw in title.lower() for kw in ["software", "developer", "backend", "frontend", "devops", "cloud", "stack"])
    is_ai = any(kw in title.lower() for kw in ["ai", "machine learning", "data", "nlp", "vision", "analyst"])
    is_electrical = any(kw in title.lower() for kw in ["electrical", "vlsi", "power", "telecom", "hardware", "rf", "scada", "plc"])
    is_mechanical = any(kw in title.lower() for kw in ["mechanical", "automotive", "manufacturing", "thermal", "hvac", "mechatronics"])
    is_civil = any(kw in title.lower() for kw in ["civil", "structural", "construction", "geotechnical", "environmental", "urban"])
    is_management = any(kw in title.lower() for kw in ["manager", "scrum", "analyst", "writer"])

    # 2. Dynamic Skills Matrix
    core_skills = ["Problem Solving", "System Design", "Project Management"]
    tools = ["Git", "Jira", "MS Office"]
    projects_beg = ["Basic Portfolio Project", "Simple Automation Script"]
    projects_adv = ["Enterprise Grade System Integration", "Scalable Cloud Deployment"]
    
    if is_software:
        core_skills = ["Data Structures & Algorithms", "Object Oriented Programming", "RESTful APIs", "Microservices", "Database Design"]
        tools = ["VS Code", "Git/GitHub", "Docker", "Kubernetes", "AWS/Azure", "Postman"]
        projects_beg = ["Personal Portfolio Website", "Task Management REST API", "Weather App"]
        projects_adv = ["E-Commerce Microservices Platform", "Real-time Chat Application with WebSockets", "Scalable Video Streaming Backend"]
    elif is_ai:
        core_skills = ["Probability & Statistics", "Machine Learning Algorithms", "Deep Learning", "Data Processing", "Model Evaluation"]
        tools = ["Python", "TensorFlow / PyTorch", "Jupyter Notebooks", "Scikit-Learn", "Pandas", "SQL"]
        projects_beg = ["House Price Prediction Model", "Customer Segmentation with K-Means", "Spam Classifier"]
        projects_adv = ["Real-time Object Detection Pipeline", "LLM-based Custom Chatbot", "Recommendation Engine for E-commerce"]
    elif is_electrical:
        core_skills = ["Circuit Analysis", "Signal Processing", "Control Systems", "Power Electronics", "Embedded Systems"]
        tools = ["AutoCAD Electrical", "MATLAB", "Simulink", "Altium Designer", "Multisim", "Keil"]
        projects_beg = ["Basic Microcontroller Interfacing", "Power Supply Design", "Simple Home Automation"]
        projects_adv = ["SCADA System Implementation", "Smart Grid Load Balancing Simulation", "Custom PCB Design for IoT Device"]
    elif is_mechanical:
        core_skills = ["Thermodynamics", "Fluid Mechanics", "Material Science", "CAD/CAM", "Finite Element Analysis (FEA)"]
        tools = ["SolidWorks", "AutoCAD", "ANSYS", "CATIA", "MATLAB"]
        projects_beg = ["3D Modeling of Engine Components", "Basic Heat Transfer Simulation", "Static Structural Analysis"]
        projects_adv = ["Full Vehicle Chassis Design & Simulation", "Thermal Management System for EV Battery", "Robotic Arm Kinematics"]
    elif is_civil:
        core_skills = ["Structural Analysis", "Geotechnical Engineering", "Construction Planning", "Surveying", "Fluid Mechanics"]
        tools = ["AutoCAD Civil 3D", "Revit", "STAAD.Pro", "ETABS", "Primavera P6"]
        projects_beg = ["Residential Building Floor Plan", "Basic Concrete Mix Design", "Site Survey Report"]
        projects_adv = ["Multi-story Commercial Building Structural Design", "Highway Intersection Traffic Flow Simulation", "Water Treatment Plant Layout"]
    
    return {
        "career": {
            "name": title,
            "slug": slug,
            "overview": f"The {title} role is a critical position within the {branch_name} sector, focusing on designing, building, and optimizing modern solutions. It offers excellent career stability and rapid growth potential.",
            "responsibilities": [
                f"Design and implement robust solutions related to {title} technologies.",
                "Collaborate with cross-functional engineering teams to achieve project goals.",
                "Conduct testing, debugging, and continuous optimization of systems.",
                "Stay updated with industry trends and adopt emerging technologies."
            ],
            "who_can_apply": branch_name,
            "industry_demand": "Very High. Top recruiters include Fortune 500 companies, cutting-edge startups, and top engineering firms.",
            "future_scope": f"Excellent. As industries continue to evolve, the demand for highly skilled {title}s is projected to grow by 15-20% over the next decade.",
            "india_salary": "Fresher: ₹6 - ₹10 LPA, Mid-Level: ₹12 - ₹22 LPA, Senior: ₹25 - ₹45+ LPA",
            "international_salary": "Fresher: $60k - $80k, Mid-Level: $90k - $140k, Senior: $150k - $200k+",
            "remote_opportunities": "High" if (is_software or is_ai) else "Low to Moderate (Often requires on-site/lab work)",
            "growth_path": [f"Junior {title}", f"{title}", f"Senior {title}", "Lead Engineer", "Engineering Manager / Architect"]
        },
        "roadmap": {
            "title": f"The Complete {title} Roadmap",
            "description": f"A comprehensive, step-by-step learning path designed to take you from a beginner to an industry-ready {title}.",
            "skills_matrix": {
                "Core Engineering Skills": core_skills,
                "Industry Standard Tools": tools,
                "Soft Skills": ["Effective Communication", "Analytical Problem Solving", "Time Management", "Team Collaboration"]
            },
            "learning_plans": [
                {"name": "Fast Track", "duration": "4 Months", "daily_hours": "5-6 Hours (Intensive)"},
                {"name": "Standard Path", "duration": "6-8 Months", "daily_hours": "3-4 Hours (Balanced)"},
                {"name": "Flexible Path", "duration": "12 Months", "daily_hours": "1-2 Hours (While Studying/Working)"}
            ],
            "learning_steps": [
                {
                    "phase": 1, 
                    "title": "Foundational Concepts", 
                    "duration": "1-2 Months", 
                    "learn": ["Understand core mathematical and theoretical principles", "Familiarize with basic terminology and physics of the domain", "Learn the primary software tools"]
                },
                {
                    "phase": 2, 
                    "title": "Intermediate Application", 
                    "duration": "2-3 Months", 
                    "learn": ["Apply theory to small-scale practical problems", "Master at least one primary design/coding tool", "Complete guided mini-projects"]
                },
                {
                    "phase": 3, 
                    "title": "Advanced System Design", 
                    "duration": "2-3 Months", 
                    "learn": ["Architect complex systems", "Learn optimization, scaling, or efficiency techniques", "Study industry standards and compliance regulations"]
                },
                {
                    "phase": 4, 
                    "title": "Industry Readiness & Portfolio", 
                    "duration": "1 Month", 
                    "learn": ["Build 2 capstone projects", "Prepare an ATS-friendly resume", "Create a digital portfolio (GitHub/Behance/Website)", "Mock Interviews"]
                }
            ],
            "projects": {
                "Beginner Level": projects_beg,
                "Advanced / Capstone Level": projects_adv
            },
            "practice_questions": {
                "Technical Fundamentals": [f"Explain the core principles of {title} systems.", "How do you optimize performance in your designs?", "Describe a time you solved a complex engineering bug."],
                "Scenario Based": ["If your system fails under maximum load/stress, what are your first three debugging steps?", "How do you balance cost vs. efficiency in your designs?"]
            },
            "certifications": [f"Certified Professional in {title}", "Relevant Cloud/Software Certification (AWS, Azure, Autodesk, etc.)", "Project Management Professional (PMP)"],
            "interview_prep": {
                "Technical Rounds": ["Whiteboard system design", "Deep dive into past projects", "Live problem solving (Coding/CAD/Math)"],
                "HR Rounds": ["Why this company?", "Strengths and weaknesses", "Handling team conflicts"]
            },
            "readiness_checklist": [
                "Mastered 3 Core Skills",
                "Completed 1 Capstone Project",
                "Resume Reviewed by Mentor",
                "LinkedIn Profile Updated",
                "Completed 2 Mock Interviews"
            ]
        }
    }


def seed_offline():
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
        "Electrical & Electronics Engineering (EEE)": [
            # Core Careers
            "Power Systems Engineer", "Electrical Design Engineer", "Protection Engineer", 
            "Substation Engineer", "Transmission Engineer", "Distribution Engineer", 
            "Renewable Energy Engineer", "Solar Engineer", "Wind Energy Engineer",
            # Automation Careers
            "PLC Programmer", "SCADA Engineer", "Industrial Automation Engineer", 
            "Control Systems Engineer",
            # IT Careers
            "Embedded Engineer", "Robotics Engineer", "IoT Engineer",
            "AI Engineer", "Data Analyst"
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

    print("🚀 Starting MASSIVE OFFLINE SEEDING (No API Key Required)...\n")

    for branch_name, careers in BRANCH_CAREERS.items():
        print(f"\n--- Processing Branch: {branch_name} ---")
        
        branch = db.query(Branch).filter(Branch.name == branch_name).first()
        if not branch:
            slug = branch_name.lower().replace("&", "and").replace("(", "").replace(")", "").strip().replace("  ", " ").replace(" ", "-")
            branch = Branch(name=branch_name, slug=slug)
            db.add(branch)
            db.commit()
            db.refresh(branch)

        for title in careers:
            existing_career = db.query(Career).filter(Career.name == title).first()
            if existing_career:
                mapping = db.query(BranchCareerMap).filter(
                    BranchCareerMap.branch_id == branch.id, 
                    BranchCareerMap.career_id == existing_career.id
                ).first()
                if not mapping:
                    db.add(BranchCareerMap(branch_id=branch.id, career_id=existing_career.id))
                    db.commit()
                    print(f"   [+] Mapped existing career: {title}")
                continue
                
            print(f"   [+] Generating rich offline data for: {title}")
            data = generate_offline_roadmap(title, branch_name)
            c_data = data["career"]
            r_data = data["roadmap"]
            
            new_career = Career(**c_data)
            db.add(new_career)
            db.commit()
            db.refresh(new_career)
            
            r_data["career_id"] = new_career.id
            new_roadmap = Roadmap(**r_data)
            db.add(new_roadmap)
            
            db.add(BranchCareerMap(branch_id=branch.id, career_id=new_career.id))
            db.commit()
            
    print("\n✅ Seeding Complete! All branches and 40+ careers have been fully populated with highly realistic data!")

if __name__ == "__main__":
    seed_offline()
