"""
count_careers.py
"""
from database import SessionLocal
import models
db = SessionLocal()
careers = db.query(models.Career).count()
branches = db.query(models.Branch).count()
print(f"Total Unique Careers: {careers}")
print(f"Total Branches: {branches}")
db.close()
