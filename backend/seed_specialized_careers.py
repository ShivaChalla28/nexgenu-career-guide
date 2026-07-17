"""
seed_specialized_careers.py
Expands NexGenU to 447+ unique roles by adding 16 new specialized branch categories.
"""

from database import SessionLocal, engine, Base
from models import Career, Branch, BranchCareerMap
import re

Base.metadata.create_all(bind=engine)

NEW_BRANCH_CAREERS = {
    "Advanced Artificial Intelligence": {
        "Core Careers": [
            "AI Safety Engineer", "AI Ethics Engineer", "AI Evaluation Engineer",
            "AI Platform Engineer", "AI Infrastructure Engineer", "AI Deployment Engineer",
            "AI Operations Engineer", "AI Integration Engineer", "AI Application Engineer",
            "Conversational AI Engineer", "Recommendation Systems Engineer",
            "Reinforcement Learning Engineer", "Reinforcement Learning Researcher",
            "Multimodal AI Engineer", "Speech AI Engineer", "Voice AI Engineer",
            "AI Simulation Engineer", "Cognitive AI Engineer",
            "AI Explainability Engineer", "AI Security Engineer"
        ]
    },
    "Advanced Data Engineering": {
        "Core Careers": [
            "Analytics Engineer", "BI Developer", "Data Visualization Engineer",
            "Data Quality Engineer", "Data Governance Engineer", "Data Warehouse Engineer",
            "ETL Developer", "ELT Engineer", "Data Integration Engineer",
            "Streaming Data Engineer", "Hadoop Engineer", "Spark Engineer",
            "Data Platform Engineer", "Master Data Engineer", "Data Migration Engineer"
        ]
    },
    "Cloud Computing Specializations": {
        "Core Careers": [
            "Cloud Consultant", "Cloud Administrator", "Cloud Migration Engineer",
            "Cloud Operations Engineer", "FinOps Engineer", "Kubernetes Engineer",
            "Docker Engineer", "Infrastructure as Code Engineer", "Terraform Engineer",
            "Cloud Network Engineer", "Multi-Cloud Engineer", "Hybrid Cloud Engineer",
            "Cloud Reliability Engineer", "Cloud Solutions Architect", "Edge Cloud Engineer"
        ]
    },
    "DevOps & Platform Engineering": {
        "Core Careers": [
            "Release Engineer", "Build Engineer", "CI/CD Engineer",
            "Observability Engineer", "Monitoring Engineer",
            "Configuration Management Engineer", "Platform Reliability Engineer",
            "DevSecOps Engineer", "Infrastructure Automation Engineer", "GitOps Engineer"
        ]
    },
    "Cyber Security Specializations": {
        "Core Careers": [
            "Application Security Engineer", "Cloud Security Engineer",
            "Security Operations Engineer", "IAM Engineer", "Threat Intelligence Analyst",
            "Vulnerability Assessment Engineer", "Red Team Engineer", "Blue Team Engineer",
            "Purple Team Engineer", "Security Consultant", "Security Auditor",
            "Security Compliance Engineer", "GRC Analyst", "SOC Engineer",
            "Network Security Engineer", "Mobile Security Engineer", "Web Security Engineer",
            "Cryptography Engineer", "Identity Security Engineer", "Zero Trust Architect"
        ]
    },
    "Software Engineering Specializations": {
        "Core Careers": [
            "API Developer", "API Integration Engineer", "Middleware Developer",
            "Enterprise Application Developer", "Microservices Engineer",
            "Distributed Systems Engineer", "Software Performance Engineer",
            "Software Integration Engineer", "Solutions Engineer", "Technical Consultant",
            "Build Automation Engineer", "Compiler Engineer", "Runtime Engineer",
            "Systems Programmer", "Open Source Engineer"
        ]
    },
    "Mobile Development Specializations": {
        "Core Careers": [
            "Flutter Developer", "React Native Developer", "Kotlin Developer",
            "Swift Developer", "Mobile Security Engineer", "Cross Platform Developer",
            "Mobile UI Engineer", "Mobile Performance Engineer", "Wearable App Developer",
            "Mobile Game Developer"
        ]
    },
    "Web Technologies": {
        "Core Careers": [
            "React Developer", "Angular Developer", "Vue.js Developer",
            "Node.js Developer", "Next.js Developer", "Nuxt.js Developer",
            "PHP Developer", "Laravel Developer", "Django Developer",
            "Spring Boot Developer"
        ]
    },
    "UI / UX": {
        "Core Careers": [
            "UI Designer", "UX Designer", "Product Designer", "Interaction Designer",
            "UX Researcher", "Visual Designer", "Design System Engineer",
            "Accessibility Engineer", "Motion Designer", "Human Factors Engineer"
        ]
    },
    "ERP & Enterprise Applications": {
        "Core Careers": [
            "SAP ABAP Developer", "SAP FICO Consultant", "SAP MM Consultant",
            "SAP SD Consultant", "SAP HANA Consultant", "SAP Basis Administrator",
            "Salesforce Developer", "Salesforce Administrator", "Salesforce Consultant",
            "ServiceNow Developer", "ServiceNow Administrator", "Oracle ERP Consultant",
            "Oracle Fusion Developer", "Microsoft Dynamics Consultant", "Pega Developer"
        ]
    },
    "Database Engineering": {
        "Core Careers": [
            "PostgreSQL DBA", "MySQL DBA", "MongoDB Developer", "NoSQL Engineer",
            "Database Performance Engineer", "Database Security Engineer",
            "Data Modeler", "Database Migration Engineer", "Redis Engineer",
            "Cassandra Engineer"
        ]
    },
    "Networking": {
        "Core Careers": [
            "Network Architect", "Network Administrator", "Wireless Network Engineer",
            "SD-WAN Engineer", "VoIP Engineer", "Telecom Network Engineer",
            "Optical Network Engineer", "Infrastructure Support Engineer",
            "Systems Engineer", "Enterprise Network Engineer"
        ]
    },
    "Robotics & Automation": {
        "Core Careers": [
            "Robotics Programmer", "Industrial Robotics Engineer", "Automation Consultant",
            "Mechatronics Design Engineer", "Autonomous Robotics Engineer",
            "Robotic Process Automation (RPA) Developer", "RPA Consultant",
            "Cobot Engineer", "Industrial AI Engineer", "Smart Manufacturing Engineer"
        ]
    },
    "Semiconductor Industry": {
        "Core Careers": [
            "Physical Design Engineer", "DFT Engineer", "Verification Engineer",
            "Analog Design Engineer", "Digital Design Engineer", "Layout Engineer",
            "Process Engineer (Semiconductor)", "Semiconductor Test Engineer",
            "Memory Design Engineer", "EDA Tool Engineer"
        ]
    },
    "Quantum Computing": {
        "Core Careers": [
            "Quantum Software Engineer", "Quantum Algorithm Engineer",
            "Quantum ML Engineer", "Quantum Research Engineer",
            "Quantum Compiler Engineer", "Quantum Simulation Engineer",
            "Quantum Hardware Engineer", "Quantum Application Developer",
            "Quantum Security Engineer", "Quantum Computing Scientist"
        ]
    },
    "Research & Emerging Technologies": {
        "Core Careers": [
            "Digital Twin Engineer", "Metaverse Developer", "XR Developer",
            "Spatial Computing Engineer", "Edge AI Engineer", "Edge Computing Engineer",
            "High Performance Computing Engineer", "Scientific Computing Engineer",
            "Computational Scientist", "Research Software Engineer", "Innovation Engineer",
            "Technology Strategist", "Product Innovation Engineer", "Computational Engineer",
            "Digital Transformation Consultant"
        ]
    }
}

def make_slug(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[&/]", "and", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

def seed():
    db = SessionLocal()
    total_created = 0
    total_mapped = 0
    total_skipped = 0

    try:
        for branch_name, categories in NEW_BRANCH_CAREERS.items():
            branch_slug = make_slug(branch_name)
            branch = db.query(Branch).filter(Branch.slug == branch_slug).first()
            if not branch:
                branch = Branch(name=branch_name, slug=branch_slug)
                db.add(branch)
                db.commit()
                db.refresh(branch)

            for category, career_titles in categories.items():
                for title in career_titles:
                    slug = make_slug(title)
                    career = db.query(Career).filter(Career.slug == slug).first()
                    
                    if not career:
                        career = Career(
                            name=title,
                            slug=slug,
                            category=category,
                            overview=f"Complete roadmap and career guide for {title}.",
                            industry_demand="High",
                        )
                        db.add(career)
                        db.commit()
                        db.refresh(career)
                        total_created += 1
                    else:
                        total_skipped += 1

                    mapping = db.query(BranchCareerMap).filter(
                        BranchCareerMap.branch_id == branch.id,
                        BranchCareerMap.career_id == career.id,
                    ).first()
                    if not mapping:
                        db.add(BranchCareerMap(branch_id=branch.id, career_id=career.id))
                        db.commit()
                        total_mapped += 1

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

    print(f"\nDone! Created {total_created} new careers. Mapped {total_mapped}. Skipped {total_skipped}.")

if __name__ == "__main__":
    seed()
