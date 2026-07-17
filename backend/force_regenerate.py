"""
force_regenerate.py
Deletes all roadmaps from the database so generate_all_roadmaps.py can run fresh.
"""
from database import SessionLocal
import models

db = SessionLocal()
deleted = db.query(models.Roadmap).delete()
db.commit()
db.close()

print(f"🗑️ Deleted {deleted} existing roadmaps.")
print("🚀 Now run: python generate_all_roadmaps.py")
