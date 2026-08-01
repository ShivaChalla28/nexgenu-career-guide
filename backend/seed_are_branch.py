import os
import json
import re
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap

# 10 Categories and their careers
ARE_CATEGORIES = {
    "ROBOTICS CAREERS": [
        "Robotics Engineer", "Industrial Robotics Engineer", "Robotics Programmer", 
        "Robotics Software Engineer", "Robotics Design Engineer", "Robot Integration Engineer", 
        "Robot Maintenance Engineer", "Collaborative Robot (Cobot) Engineer", "Mobile Robotics Engineer", 
        "Humanoid Robotics Engineer", "Service Robotics Engineer", "Robot Vision Engineer", 
        "Robot Simulation Engineer", "Robot Testing Engineer", "Robotics Research Engineer", 
        "Robotics Safety Engineer", "Field Robotics Engineer", "Robot Calibration Engineer", 
        "Autonomous Robotics Engineer", "Swarm Robotics Engineer"
    ],
    "INDUSTRIAL AUTOMATION": [
        "Automation Engineer", "Industrial Automation Engineer", "Factory Automation Engineer", 
        "Manufacturing Automation Engineer", "Process Automation Engineer", "Automation Project Engineer", 
        "Automation Validation Engineer", "Automation Commissioning Engineer", "Control Systems Engineer", 
        "Instrumentation Engineer", "PLC Programmer", "PLC Engineer", "SCADA Engineer", 
        "DCS Engineer", "HMI Engineer", "Industrial Control Engineer", "Industrial Software Engineer", 
        "Electrical Automation Engineer", "Automation Maintenance Engineer", "Automation Design Engineer"
    ],
    "INDUSTRY 4.0": [
        "Industry 4.0 Engineer", "Smart Manufacturing Engineer", "Smart Factory Engineer", 
        "Industrial Digitalization Engineer", "Digital Manufacturing Engineer", "Manufacturing Systems Engineer", 
        "Digital Twin Engineer", "Industrial Analytics Engineer", "Connected Factory Engineer", 
        "Smart Production Engineer"
    ],
    "EMBEDDED & IoT": [
        "Embedded Systems Engineer", "Embedded Software Engineer", "Embedded Hardware Engineer", 
        "Firmware Engineer", "IoT Engineer", "Industrial IoT Engineer", "AIoT Engineer", 
        "Sensor Systems Engineer", "Microcontroller Engineer", "Edge AI Engineer", 
        "Real-Time Systems Engineer"
    ],
    "AI & INTELLIGENT ROBOTICS": [
        "AI Robotics Engineer", "Machine Learning Engineer (Robotics)", "Computer Vision Engineer", 
        "SLAM Engineer", "Motion Planning Engineer", "Navigation Engineer", "Autonomous Systems Engineer", 
        "Intelligent Systems Engineer", "Reinforcement Learning Engineer", "Robot Perception Engineer"
    ],
    "AUTONOMOUS SYSTEMS": [
        "Autonomous Vehicle Engineer", "ADAS Engineer", "Drone Engineer", "UAV Engineer", 
        "UGV Engineer", "AGV Engineer", "AMR Engineer", "Marine Robotics Engineer", 
        "Aerospace Robotics Engineer", "Defense Robotics Engineer"
    ],
    "SPECIALIZED ROBOTICS": [
        "Medical Robotics Engineer", "Surgical Robotics Engineer", "Agricultural Robotics Engineer", 
        "Mining Robotics Engineer", "Warehouse Automation Engineer", "Logistics Automation Engineer", 
        "Inspection Robotics Engineer", "Construction Robotics Engineer", "Space Robotics Engineer", 
        "Disaster Response Robotics Engineer"
    ],
    "SOFTWARE & SIMULATION": [
        "ROS Developer", "ROS2 Developer", "Gazebo Simulation Engineer", "MATLAB Robotics Engineer", 
        "Digital Twin Developer", "Industrial Software Developer", "Simulation Engineer", 
        "Robot Programming Engineer", "Industrial Application Developer"
    ],
    "GOVERNMENT & PSU": [
        "Robotics Engineer - ISRO", "Robotics Engineer - DRDO", "Automation Engineer - BEL", 
        "Automation Engineer - BHEL", "Automation Engineer - HAL", "Automation Engineer - Indian Railways", 
        "Automation Engineer - NTPC", "Automation Engineer - NPCIL", "Automation Engineer - ONGC", 
        "Scientist (Automation & Robotics)", "Technical Officer", "IES / ESE", "GATE Based Recruitment"
    ],
    "HIGHER STUDIES & RESEARCH": [
        "Robotics Research Scientist", "Automation Research Engineer", "AI Research Engineer", 
        "Mechatronics Research Engineer", "Human-Robot Interaction Researcher", "PhD Research Scholar", 
        "Professor", "Research Fellow", "Innovation Engineer", "Technology Consultant"
    ]
}

def make_slug(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[&/]", "and", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

def generate_roadmap_for(title: str, category: str):
    return {
        "title": f"Complete Roadmap for {title}",
        "description": f"A specialized roadmap for {title} focusing on {category.lower()} and modern industry standards.",
        "skills_matrix": {
            "Core Skills": ["Robotics Kinematics & Dynamics", "Control Systems", "Sensor Integration", "Actuators & Motors"],
            "Programming Languages": ["C++", "Python", "C", "IEC 61131-3 (PLC)"],
            "Software": ["ROS/ROS2", "AutoCAD", "SolidWorks", "MATLAB/Simulink"],
            "Simulation Tools": ["Gazebo", "Webots", "CoppeliaSim", "RoboDK"],
            "Industrial Tools": ["TIA Portal", "RSLogix", "FactoryTalk", "LabVIEW"],
            "Automation Tools": ["PLC", "SCADA", "HMI", "DCS"],
            "Cloud": ["AWS IoT", "Azure Digital Twins", "Google Cloud IoT Core"],
            "AI": ["Computer Vision", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
            "Robotics Frameworks": ["ROS", "ROS2", "MoveIt", "Nav2", "OpenCV"],
            "Soft Skills": ["Problem Solving", "Analytical Thinking", "Project Management", "Team Collaboration"],
            "Industry Standards": ["ISO 10218 (Robot Safety)", "IEC 61508", "ISA-95", "Industry 4.0"]
        },
        "learning_plans": [
            {"name": "Fast Track", "duration": "6 Months", "daily_hours": "4 Hours/Day"},
            {"name": "Standard", "duration": "8 Months", "daily_hours": "3 Hours/Day"},
            {"name": "Balanced", "duration": "10 Months", "daily_hours": "2.5 Hours/Day"},
            {"name": "Flexible", "duration": "12 Months", "daily_hours": "2 Hours/Day"}
        ],
        "learning_steps": [
            {"phase": "M1", "title": "Month 1: Fundamentals", "duration": "4 Weeks", "learn": ["Basic Electronics", "Programming Fundamentals (C++/Python)", "Mathematics for Robotics (Linear Algebra, Calculus)"]},
            {"phase": "M2", "title": "Month 2: Core Engineering Concepts", "duration": "4 Weeks", "learn": ["Control Systems", "Sensors & Actuators", "Kinematics & Dynamics"]},
            {"phase": "M3-M4", "title": "Months 3-4: Software & Simulation", "duration": "8 Weeks", "learn": ["ROS/ROS2 Basics", "Simulation with Gazebo", "3D CAD Modeling Basics"]},
            {"phase": "M5-M6", "title": "Months 5-6: Automation & AI Integration", "duration": "8 Weeks", "learn": ["PLC Programming Basics", "Computer Vision (OpenCV)", "Basic Machine Learning for Robotics"]},
            {"phase": "M7-M8", "title": "Months 7-8: Advanced Specialization", "duration": "8 Weeks", "learn": ["Advanced ROS2/MoveIt/Nav2", "SCADA/HMI Design", "IoT & Cloud Integration"]},
            {"phase": "M9-M10", "title": "Months 9-10: Capstone & Portfolio", "duration": "8 Weeks", "learn": ["Industry-Level Capstone Project", "Digital Twin Implementation", "Portfolio Development"]},
            {"phase": "M11-M12", "title": "Months 11-12: Job Readiness", "duration": "8 Weeks", "learn": ["Interview Preparation", "Mock Interviews", "Resume & LinkedIn Optimization"]}
        ],
        "projects": {
            "Beginner": ["Line Following Robot", "Obstacle Avoidance Bot", "Basic Traffic Light PLC Logic"],
            "Intermediate": ["Pick and Place Robot Arm Simulation", "Automated Conveyor Belt System (PLC)", "Face Tracking Camera"],
            "Advanced": ["Autonomous Mobile Robot (AMR) Navigation", "SCADA System for Water Treatment", "Drone Flight Controller Logic"],
            "Industry-Level": ["Full Smart Factory Digital Twin", "AI-Powered Visual Inspection System"],
            "Capstone": ["Collaborative Robot (Cobot) Assembly Cell", "Warehouse Automation System using ROS2 and Nav2"]
        },
        "certifications": [
            "Siemens S7 PLC Certification", "Rockwell Automation (Allen-Bradley) Certification",
            "FANUC/ABB/Universal Robots Handling Tool Operation",
            "AWS Certified IoT - Specialty", "Microsoft Certified: Azure IoT Developer Specialty",
            "ISA Certified Automation Professional (CAP)"
        ],
        "interview_prep": {
            "Technical Questions": ["Explain PID control.", "How does ROS differ from traditional RTOS?", "Write ladder logic for a motor start-stop circuit."],
            "HR Questions": ["Describe a time you solved a complex system failure.", "Why choose Automation & Robotics?"],
            "Coding": ["Implement A* pathfinding algorithm.", "Write a ROS node in Python to subscribe to laser scan data."],
            "Automation": ["Differentiate between PLC and DCS.", "Explain the OSI model in the context of Industrial Ethernet."],
            "PLC": ["What is a latching relay?", "Explain timers (TON, TOF) in PLC."],
            "Robotics": ["What is inverse kinematics?", "How does SLAM work?"],
            "AI": ["Explain convolutional neural networks (CNNs) for object detection.", "What is reinforcement learning in robotics?"],
            "Scenario-Based Questions": ["Your robot arm is moving past its safety limit. How do you troubleshoot the hardware and software safety loops?"]
        },
        "readiness_checklist": [
            "Skills Completed", "Portfolio Score > 80%", "Projects Completed",
            "Certifications Acquired", "Mock Interviews Passed", "Resume Ready", "LinkedIn Ready"
        ]
    }

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    branch_name = "Automation & Robotics Engineering (ARE)"
    branch_slug = make_slug(branch_name)
    
    try:
        branch = db.query(Branch).filter(Branch.name == branch_name).first()
        if not branch:
            branch = Branch(
                name=branch_name, 
                slug=branch_slug,
                description="Automation & Robotics Engineering combines Mechanical Engineering, Electronics, Electrical Engineering, Computer Science, Artificial Intelligence, Industrial Automation, Embedded Systems, and Control Engineering to design intelligent automated systems, industrial robots, autonomous machines, and smart factories.",
                icon="🤖"
            )
            db.add(branch)
            db.commit()
            db.refresh(branch)
            print(f"[+] Created branch: {branch_name}")
        else:
            print(f"[=] Branch exists: {branch_name}")

        for category, titles in ARE_CATEGORIES.items():
            for title in titles:
                career = db.query(Career).filter(Career.name == title).first()
                if not career:
                    career = Career(
                        name=title,
                        slug=make_slug(title),
                        category=category,
                        overview=f"Career Category: {category} | A specialized role focusing on intelligent systems and automation.",
                        responsibilities=["Design automated systems", "Develop robotic software", "Integrate sensors and actuators", "Optimize manufacturing processes", "Ensure system safety and reliability"],
                        who_can_apply="Automation & Robotics Engineering, Mechanical, Electronics, Computer Science",
                        industry_demand="Extremely High. Rapidly growing in Industry 4.0 and Smart Manufacturing sectors.",
                        future_scope="Enormous potential as industries transition to fully automated and AI-driven environments.",
                        india_salary="Fresher: ₹4-8 LPA, Mid-Level: ₹8-18 LPA, Senior: ₹20-50+ LPA",
                        international_salary="USA: $80k-$150k/year, EU: €50k-€90k/year",
                        remote_opportunities="Medium. Software and simulation roles offer remote work, while hardware integration requires on-site presence.",
                        growth_path=["Junior Engineer", "Senior Engineer", "Lead Engineer", "System Architect", "Director of Automation"]
                    )
                    db.add(career)
                    db.commit()
                    db.refresh(career)
                    print(f"  [+] Created career: {title}")
                else:
                    if not career.category:
                        career.category = category
                        db.commit()

                # Map to ARE branch
                mapping = db.query(BranchCareerMap).filter(
                    BranchCareerMap.branch_id == branch.id,
                    BranchCareerMap.career_id == career.id
                ).first()
                if not mapping:
                    db.add(BranchCareerMap(branch_id=branch.id, career_id=career.id))
                    db.commit()
                
                # Check roadmap
                roadmap = db.query(Roadmap).filter(Roadmap.career_id == career.id).first()
                if not roadmap:
                    r_data = generate_roadmap_for(title, category)
                    roadmap = Roadmap(
                        career_id=career.id,
                        title=r_data["title"],
                        description=r_data["description"],
                        skills_matrix=r_data["skills_matrix"],
                        learning_plans=r_data["learning_plans"],
                        learning_steps=r_data["learning_steps"],
                        projects=r_data["projects"],
                        practice_questions=r_data["practice_questions"],
                        certifications=r_data["certifications"],
                        interview_prep=r_data["interview_prep"],
                        readiness_checklist=r_data["readiness_checklist"]
                    )
                    db.add(roadmap)
                    db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
    
    print("Seeding of ARE branch complete!")

if __name__ == "__main__":
    seed()
