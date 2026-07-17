"""
check_roadmaps.py
Inspects the roadmaps in the database.
"""
from database import SessionLocal
import models
import json

db = SessionLocal()
careers = db.query(models.Career).all()
print(f"Total careers: {len(careers)}")

roadmaps = db.query(models.Roadmap).all()
print(f"Total roadmaps: {len(roadmaps)}")

if roadmaps:
    r = roadmaps[0]
    print(f"\nSample Roadmap Title: {r.title}")
    
    # Check if the skills_matrix is a string or parsed dict
    if isinstance(r.skills_matrix, str):
        try:
            print("skills_matrix is a valid JSON string.")
        except Exception:
            print("skills_matrix is NOT valid JSON string.")
    else:
        print(f"skills_matrix type: {type(r.skills_matrix)}")
        
db.close()
