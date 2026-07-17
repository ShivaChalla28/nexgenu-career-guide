"""
write_count.py
"""
import sys
import os

try:
    from database import SessionLocal
    import models
    db = SessionLocal()
    careers = db.query(models.Career).count()
    branches = db.query(models.Branch).count()
    db.close()
    
    with open("count.txt", "w") as f:
        f.write(f"{careers}\n{branches}\n")
except Exception as e:
    with open("count.txt", "w") as f:
        f.write(f"Error: {e}")
