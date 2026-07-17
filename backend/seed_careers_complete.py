"""
seed_careers_complete.py
Populates all 24 engineering branches with careers organized into:
  - Core Careers
  - IT & Digital Careers
  - Government & PSU Careers
Does NOT call the LLM – creates Career rows with a stub overview so the
branch page works immediately. Roadmaps can be generated separately.
"""

from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap
import re

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Master data: { branch_name: { category: [career titles] } }
# ---------------------------------------------------------------------------
BRANCH_CAREERS = {
    "Computer Science Engineering (CSE)": {
        "Core Careers": [
            "Software Engineer", "Software Developer", "Full Stack Developer",
            "Frontend Developer", "Backend Developer", "Web Developer",
            "Mobile App Developer", "Android Developer", "iOS Developer",
            "Desktop Application Developer", "AI Engineer",
            "Machine Learning Engineer", "Data Scientist", "Data Analyst",
            "Data Engineer", "NLP Engineer", "Computer Vision Engineer",
            "MLOps Engineer", "Cloud Engineer", "AWS Engineer",
            "Azure Engineer", "Google Cloud Engineer", "DevOps Engineer",
            "Site Reliability Engineer", "Platform Engineer",
        ],
        "IT & Digital Careers": [
            "Cyber Security Analyst", "Ethical Hacker", "Penetration Tester",
            "SOC Analyst", "Security Engineer", "QA Engineer",
            "Automation Tester", "Database Administrator", "Network Engineer",
            "Blockchain Developer", "Game Developer", "AR/VR Developer",
            "Embedded Software Engineer",
        ],
        "Government & PSU Careers": [
            "Scientist/Engineer - ISRO", "Scientist - DRDO",
            "Software Engineer - CDAC", "IT Officer - IBPS/SBI",
            "Scientific Assistant - BARC", "Engineer - BEL (Electronics/Software)",
            "Technical Officer - NIC", "Engineering Services (UPSC) - IT Cadre",
            "GATE PSU Recruitment (BSNL/MTNL/ECIL)",
        ],
    },

    "Information Technology (IT)": {
        "Core Careers": [
            "Software Engineer", "System Administrator", "Network Engineer",
            "Cloud Engineer", "DevOps Engineer", "IT Support Engineer",
            "Business Analyst", "Database Administrator", "Security Analyst",
            "Full Stack Developer", "Web Developer", "QA Engineer",
        ],
        "IT & Digital Careers": [
            "Cyber Security Engineer", "Cloud Architect",
            "IT Project Manager", "Scrum Master", "Technical Writer",
            "Data Analyst", "AI Engineer",
        ],
        "Government & PSU Careers": [
            "IT Officer - IBPS/SBI", "Technical Officer - NIC",
            "Scientist - CDAC", "Engineer - ECIL",
            "Engineering Services (UPSC) - IT Cadre",
            "GATE PSU Recruitment (BSNL/MTNL)",
        ],
    },

    "Artificial Intelligence & Data Science": {
        "Core Careers": [
            "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer",
            "Data Scientist", "Data Analyst", "Data Engineer",
            "NLP Engineer", "Computer Vision Engineer", "Research Engineer",
            "Prompt Engineer", "LLM Engineer",
        ],
        "IT & Digital Careers": [
            "MLOps Engineer", "AI Product Manager", "AI Ethics Researcher",
            "Robotics AI Engineer", "Generative AI Engineer",
            "Business Intelligence Analyst",
        ],
        "Government & PSU Careers": [
            "Scientist - DRDO (AI Division)", "Research Scientist - ISRO",
            "Data Scientist - NITI Aayog",
            "AI Engineer - MeitY",
            "Scientific Officer - BARC", "GATE PSU Recruitment (AI Roles)",
        ],
    },

    "Electronics & Communication Engineering (ECE)": {
        "Core Careers": [
            "Electronics Engineer", "Communication Engineer", "RF Engineer",
            "Telecom Engineer", "PCB Design Engineer", "VLSI Design Engineer",
            "ASIC Design Engineer", "FPGA Engineer",
        ],
        "IT & Digital Careers": [
            "Embedded Systems Engineer", "Firmware Engineer", "IoT Engineer",
            "Robotics Engineer", "AIoT Engineer", "Network Engineer",
            "Cyber Security Engineer", "Software Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - BEL (Electronics)", "Scientist/Engineer - ISRO",
            "Scientist - DRDO", "Engineer - ECIL",
            "Telecom Engineer - BSNL/MTNL", "Engineer - BHEL",
            "Engineering Services (UPSC) - Electronics & Telecom",
            "GATE PSU Recruitment (BEL/ECIL/ISRO/DRDO)",
            "Indian Engineering Services (IES) - Electronics",
        ],
    },

    "Electrical & Electronics Engineering (EEE)": {
        "Core Careers": [
            "Power Systems Engineer", "Electrical Design Engineer",
            "Protection Engineer", "Substation Engineer",
            "Transmission Engineer", "Distribution Engineer",
            "Renewable Energy Engineer", "Solar Engineer", "Wind Energy Engineer",
            "PLC Programmer", "SCADA Engineer",
            "Industrial Automation Engineer", "Control Systems Engineer",
        ],
        "IT & Digital Careers": [
            "Embedded Engineer", "Robotics Engineer", "IoT Engineer",
            "AI Engineer", "Data Analyst",
        ],
        "Government & PSU Careers": [
            "Engineer - NTPC", "Engineer - NHPC", "Engineer - BHEL",
            "Engineer - PGCIL (Power Grid)", "Engineer - State Electricity Boards",
            "Scientist - BARC", "Engineer - ONGC/IOCL (Electrical)",
            "Engineering Services (UPSC) - Electrical",
            "GATE PSU Recruitment (NTPC/BHEL/PGCIL/NHPC)",
            "Indian Engineering Services (IES) - Electrical",
        ],
    },

    "Mechanical Engineering": {
        "Core Careers": [
            "Design Engineer", "Production Engineer", "Manufacturing Engineer",
            "Maintenance Engineer", "Tool Design Engineer", "Thermal Engineer",
            "HVAC Engineer", "Quality Engineer", "Industrial Engineer",
            "Plant Engineer", "CAD Engineer", "CAM Engineer",
            "CAE Engineer", "CFD Engineer",
        ],
        "IT & Digital Careers": [
            "Robotics Engineer", "Automation Engineer",
            "Digital Twin Engineer", "IoT Engineer", "Data Analyst",
        ],
        "Government & PSU Careers": [
            "Engineer - BHEL", "Engineer - DRDO (Mechanical)",
            "Scientist/Engineer - ISRO", "Engineer - IOCL/HPCL/BPCL",
            "Engineer - Indian Railways (Mechanical)",
            "Engineer - ONGC", "Engineer - SAIL",
            "Engineering Services (UPSC) - Mechanical",
            "GATE PSU Recruitment (BHEL/ONGC/IOCL/HPCL)",
            "Indian Engineering Services (IES) - Mechanical",
        ],
    },

    "Civil Engineering": {
        "Core Careers": [
            "Site Engineer", "Structural Engineer", "Construction Engineer",
            "Planning Engineer", "Highway Engineer", "Bridge Engineer",
            "Geotechnical Engineer", "Quantity Surveyor",
            "Water Resources Engineer", "Environmental Engineer",
            "BIM Engineer", "GIS Engineer", "CAD Engineer",
            "Primavera Planning Engineer",
        ],
        "IT & Digital Careers": [
            "GIS Developer", "Construction Tech Engineer",
            "Smart Cities Planner", "Infrastructure Data Analyst",
        ],
        "Government & PSU Careers": [
            "Engineer - CPWD", "Engineer - PWD (State)",
            "Engineer - NHAI", "Engineer - Indian Railways (Civil)",
            "Engineer - RVNL", "Engineer - Metro Rail Projects",
            "Engineer - MES (Military Engineering Services)",
            "Engineer - Irrigation/Water Resources Dept",
            "Engineering Services (UPSC) - Civil",
            "GATE PSU Recruitment (RITES/IRCON/NBCC)",
            "Indian Engineering Services (IES) - Civil",
        ],
    },

    "Chemical Engineering": {
        "Core Careers": [
            "Process Engineer", "Production Engineer", "Plant Engineer",
            "Safety Engineer", "Quality Control Engineer", "Refinery Engineer",
            "Petrochemical Engineer", "Polymer Engineer",
        ],
        "IT & Digital Careers": [
            "Process Automation Engineer", "Industrial IoT Engineer",
            "Manufacturing Systems Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - IOCL", "Engineer - ONGC", "Engineer - HPCL",
            "Engineer - BPCL", "Engineer - GAIL", "Engineer - NRL",
            "Scientist - BARC (Chemical)", "Engineer - DRDO",
            "Engineering Services (UPSC) - Chemical",
            "GATE PSU Recruitment (IOCL/ONGC/HPCL/GAIL)",
        ],
    },

    "Automobile Engineering": {
        "Core Careers": [
            "Automobile Engineer", "Vehicle Design Engineer",
            "Engine Design Engineer", "Vehicle Testing Engineer",
            "Production Engineer", "Service Engineer",
        ],
        "IT & Digital Careers": [
            "Electric Vehicle Engineer", "ADAS Engineer",
            "Autonomous Vehicle Engineer", "Automotive Embedded Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - DRDO (Vehicle Research)", "Engineer - Ordnance Factories",
            "Engineer - BRO (Border Roads Organisation)",
            "Automobile Engineer - Indian Army EME Corps",
            "Engineer - BEML",
        ],
    },

    "Biomedical Engineering": {
        "Core Careers": [
            "Biomedical Engineer", "Medical Device Engineer",
            "Clinical Engineer", "Medical Equipment Engineer",
            "Rehabilitation Engineer",
        ],
        "IT & Digital Careers": [
            "Health Informatics Engineer", "Bioinformatics Engineer",
            "Medical Imaging Engineer", "AI Healthcare Engineer",
        ],
        "Government & PSU Careers": [
            "Scientist - DRDO (Life Sciences)", "Technical Officer - AIIMS",
            "Biomedical Engineer - Government Hospitals",
            "Scientist - ICMR", "Engineer - BEL (Medical Electronics)",
            "Officer - Central Govt Health Scheme (CGHS)",
        ],
    },

    "Mechatronics Engineering": {
        "Core Careers": [
            "Robotics Engineer", "Automation Engineer", "Embedded Engineer",
            "PLC Programmer", "SCADA Engineer", "Firmware Engineer",
            "Control Systems Engineer", "Industrial IoT Engineer",
        ],
        "IT & Digital Careers": [
            "AI Robotics Engineer", "Digital Twin Engineer",
            "Industry 4.0 Specialist",
        ],
        "Government & PSU Careers": [
            "Scientist/Engineer - ISRO (Robotics)", "Engineer - DRDO",
            "Engineer - BHEL (Automation)", "Engineer - ECIL",
            "GATE PSU Recruitment",
        ],
    },

    "Instrumentation Engineering": {
        "Core Careers": [
            "Instrumentation Engineer", "Process Control Engineer",
            "Automation Engineer", "PLC Engineer", "SCADA Engineer",
            "Control Systems Engineer", "Industrial IoT Engineer",
        ],
        "IT & Digital Careers": [
            "Industrial Automation Consultant", "Industry 4.0 Engineer",
            "IoT Solutions Architect",
        ],
        "Government & PSU Careers": [
            "Engineer - ONGC (Instrumentation)", "Engineer - IOCL",
            "Scientist - BARC (Instrumentation)",
            "Engineer - NPCIL", "Engineer - DRDO",
            "GATE PSU Recruitment",
        ],
    },

    "Aeronautical Engineering": {
        "Core Careers": [
            "Aircraft Design Engineer", "Aerodynamics Engineer",
            "Flight Test Engineer", "Propulsion Engineer",
            "Aircraft Maintenance Engineer", "UAV/Drone Engineer",
            "Aerospace Software Engineer",
        ],
        "IT & Digital Careers": [
            "Drone Software Engineer", "Simulation Engineer",
            "Aerospace Data Analyst",
        ],
        "Government & PSU Careers": [
            "Scientist/Engineer - ISRO", "Scientist - DRDO (Aeronautics)",
            "Engineer - HAL (Hindustan Aeronautics)",
            "Engineer - NAL (National Aerospace Laboratories)",
            "Indian Air Force - Technical Branch",
            "Engineering Services (UPSC) - Aeronautical",
        ],
    },

    "Agricultural Engineering": {
        "Core Careers": [
            "Irrigation Engineer", "Farm Machinery Engineer",
            "Soil and Water Engineer", "Precision Agriculture Engineer",
            "AgriTech Engineer", "Drone Engineer", "Smart Farming Engineer",
        ],
        "IT & Digital Careers": [
            "AgriTech Data Analyst", "Remote Sensing Engineer",
            "GIS Specialist (Agriculture)",
        ],
        "Government & PSU Careers": [
            "Engineer - NABARD", "Scientist - ICAR",
            "Agricultural Engineer - State Irrigation Depts",
            "Officer - FCI (Food Corporation of India)",
            "GATE PSU Recruitment (Agriculture)",
        ],
    },

    "Marine Engineering": {
        "Core Careers": [
            "Marine Engineer", "Ship Design Engineer", "Marine Systems Engineer",
            "Port Engineer", "Offshore Engineer", "Marine Automation Engineer",
        ],
        "IT & Digital Careers": [
            "Maritime Cybersecurity Engineer", "Marine IoT Engineer",
            "Ship Simulation Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - Cochin Shipyard", "Engineer - Garden Reach Shipbuilders",
            "Engineer - Mazagon Dock", "Engineer - Indian Navy (Technical Branch)",
            "Engineer - Shipping Corporation of India",
            "Engineer - Directorate General of Shipping",
        ],
    },

    "Mining Engineering": {
        "Core Careers": [
            "Mine Planning Engineer", "Drilling Engineer", "Blasting Engineer",
            "Mineral Processing Engineer", "Mine Safety Engineer",
            "Exploration Engineer",
        ],
        "IT & Digital Careers": [
            "Mining Data Analyst", "Drone Survey Engineer",
            "Smart Mining Automation Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - Coal India Limited (CIL)", "Engineer - ONGC (Upstream)",
            "Scientist - GSI (Geological Survey of India)",
            "Engineer - NMDC", "Engineer - HCL (Hindustan Copper)",
            "GATE PSU Recruitment (CIL/NMDC)",
        ],
    },

    "Industrial Engineering": {
        "Core Careers": [
            "Industrial Engineer", "Operations Engineer",
            "Process Improvement Engineer", "Supply Chain Engineer",
            "Logistics Engineer", "Production Planner",
        ],
        "IT & Digital Careers": [
            "ERP Consultant (SAP/Oracle)", "Data Analyst (Manufacturing)",
            "Industry 4.0 Consultant", "Digital Operations Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - BHEL (Industrial)", "Engineer - SAIL",
            "Engineer - Ordnance Factories",
            "Officer - Bureau of Indian Standards (BIS)",
            "GATE PSU Recruitment",
        ],
    },

    "Production Engineering": {
        "Core Careers": [
            "Production Engineer", "Manufacturing Engineer", "Quality Engineer",
            "Lean Manufacturing Engineer", "Plant Engineer", "Operations Engineer",
        ],
        "IT & Digital Careers": [
            "Manufacturing Automation Engineer", "Digital Manufacturing Analyst",
            "Industry 4.0 Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - Ordnance Factories", "Engineer - BHEL",
            "Engineer - SAIL", "Engineer - BEML",
            "GATE PSU Recruitment",
        ],
    },

    "Metallurgical Engineering": {
        "Core Careers": [
            "Metallurgical Engineer", "Materials Engineer", "Welding Engineer",
            "Heat Treatment Engineer", "Corrosion Engineer",
            "Quality Metallurgist",
        ],
        "IT & Digital Careers": [
            "Materials Data Scientist", "Computational Materials Engineer",
        ],
        "Government & PSU Careers": [
            "Scientist - DRDO (Materials)", "Engineer - SAIL",
            "Engineer - RINL (Rashtriya Ispat Nigam)", "Engineer - NALCO",
            "Scientist - DMRL (Defence Metallurgical Research Lab)",
            "GATE PSU Recruitment",
        ],
    },

    "Petroleum Engineering": {
        "Core Careers": [
            "Drilling Engineer", "Reservoir Engineer", "Production Engineer",
            "Completion Engineer", "Well Testing Engineer", "Offshore Engineer",
        ],
        "IT & Digital Careers": [
            "Petroleum Data Analyst", "Reservoir Simulation Engineer",
            "Subsurface Data Engineer",
        ],
        "Government & PSU Careers": [
            "Engineer - ONGC", "Engineer - OIL India Limited",
            "Engineer - IOCL (Upstream)", "Engineer - HPCL",
            "Engineer - GAIL", "Geoscientist - DGH",
            "GATE PSU Recruitment (ONGC/OIL)",
        ],
    },

    "Textile Engineering": {
        "Core Careers": [
            "Textile Engineer", "Fabric Production Engineer",
            "Garment Production Engineer", "Textile Quality Engineer",
            "Textile Design Engineer",
        ],
        "IT & Digital Careers": [
            "Fashion Tech Analyst", "Smart Textile Engineer",
            "CAD Textile Designer",
        ],
        "Government & PSU Careers": [
            "Engineer - National Textile Corporation",
            "Officer - Textile Commissioner Office",
            "Scientist - CIRCOT",
            "Officer - Export Promotion Councils",
        ],
    },

    "Biotechnology Engineering": {
        "Core Careers": [
            "Biotechnologist", "Bioinformatics Engineer", "Genetic Engineer",
            "Pharmaceutical Research Associate",
            "Clinical Research Associate", "Biomedical Research Scientist",
        ],
        "IT & Digital Careers": [
            "Computational Biologist", "Healthcare Data Scientist",
            "AI Drug Discovery Engineer",
        ],
        "Government & PSU Careers": [
            "Scientist - DBT (Dept of Biotechnology)",
            "Scientist - ICMR", "Scientist - CSIR",
            "Officer - CDSCO (Drug Regulatory)", "Scientist - ICAR (Biotech)",
            "Research Associate - BIRAC",
        ],
    },

    "Food Technology": {
        "Core Careers": [
            "Food Process Engineer", "Food Safety Officer",
            "Quality Assurance Engineer", "Product Development Engineer",
            "Packaging Engineer",
        ],
        "IT & Digital Careers": [
            "Food Tech Data Analyst", "Smart Food Manufacturing Engineer",
        ],
        "Government & PSU Careers": [
            "Food Safety Officer - FSSAI",
            "Scientist - CFTRI",
            "Officer - FCI (Food Corporation of India)",
            "Officer - AGMARK / Agricultural Marketing",
            "Scientist - ICAR (Food Science)",
        ],
    },

    "Environmental Engineering": {
        "Core Careers": [
            "Environmental Engineer", "Waste Management Engineer",
            "Water Treatment Engineer", "Air Pollution Control Engineer",
            "Sustainability Consultant", "Environmental Compliance Engineer",
        ],
        "IT & Digital Careers": [
            "Environmental Data Analyst", "GIS Environmental Analyst",
            "Climate Tech Engineer", "Remote Sensing Analyst",
        ],
        "Government & PSU Careers": [
            "Scientist/Engineer - CPCB (Central Pollution Control Board)",
            "Scientist - NEERI", "Engineer - CWRDM",
            "Engineer - Ministry of Environment and Forests",
            "Environmental Officer - State PCBs",
            "Engineer - Urban Local Bodies / Municipal Corporations",
        ],
    },
}


# ---------------------------------------------------------------------------
# Helper: make a URL-safe slug
# ---------------------------------------------------------------------------
def make_slug(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[&/]", "and", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s


# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------
def seed():
    db = SessionLocal()
    total_created = 0
    total_mapped = 0
    total_skipped = 0

    try:
        for branch_name, categories in BRANCH_CAREERS.items():
            print(f"\n{'='*60}")
            print(f"Branch: {branch_name}")

            # Ensure branch exists
            branch = db.query(Branch).filter(Branch.name == branch_name).first()
            if not branch:
                branch_slug = make_slug(branch_name)
                branch = Branch(name=branch_name, slug=branch_slug)
                db.add(branch)
                db.commit()
                db.refresh(branch)
                print(f"  [+] Created branch: {branch_name}")
            else:
                print(f"  [=] Branch exists: {branch_name}")

            for category, career_titles in categories.items():
                for title in career_titles:
                    # Get or create Career
                    career = db.query(Career).filter(Career.name == title).first()
                    if not career:
                        career = Career(
                            name=title,
                            slug=make_slug(title),
                            category=category,
                            overview=f"Complete roadmap and career guide for {title}.",
                            industry_demand="High",
                        )
                        db.add(career)
                        db.commit()
                        db.refresh(career)
                        total_created += 1
                        print(f"  [+] Created career: {title} ({category})")
                    else:
                        # Update category if it is not set
                        if not career.category:
                            career.category = category
                            db.commit()
                        total_skipped += 1

                    # Ensure mapping between branch and career
                    mapping = db.query(BranchCareerMap).filter(
                        BranchCareerMap.branch_id == branch.id,
                        BranchCareerMap.career_id == career.id,
                    ).first()
                    if not mapping:
                        db.add(BranchCareerMap(branch_id=branch.id, career_id=career.id))
                        db.commit()
                        total_mapped += 1
                        print(f"  [>] Mapped: {title} -> {branch_name}")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] {e}")
        raise
    finally:
        db.close()

    print(f"\n{'='*60}")
    print(f"Done! Created: {total_created} | Mapped: {total_mapped} | Already existed: {total_skipped}")


if __name__ == "__main__":
    seed()
