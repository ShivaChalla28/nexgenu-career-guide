import os
from database import SessionLocal
import models
import traceback

try:
    db = SessionLocal()
    print("Branches count:", db.query(models.Branch).count())
    print("Careers count:", db.query(models.Career).count())
    db.close()
except Exception as e:
    print(traceback.format_exc())
