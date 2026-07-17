"""
Fix all branch slugs in the database to match the frontend URL format.
Run this once: python fix_slugs.py
"""
from database import SessionLocal, engine, Base
from models import Branch

def fix_slugs():
    db = SessionLocal()
    branches = db.query(Branch).all()
    
    print(f"Found {len(branches)} branches. Fixing slugs...\n")
    
    for branch in branches:
        # Generate correct slug: replace & with and, remove (), replace spaces with dashes
        new_slug = (
            branch.name.lower()
            .replace("&", "and")
            .replace("(", "")
            .replace(")", "")
            .strip()
            .replace("  ", " ")
            .replace(" ", "-")
        )
        # Clean up any double dashes
        while "--" in new_slug:
            new_slug = new_slug.replace("--", "-")
        
        old_slug = branch.slug
        if old_slug != new_slug:
            print(f"  Fixing: '{old_slug}' → '{new_slug}'")
            branch.slug = new_slug
        else:
            print(f"  OK: '{new_slug}'")
    
    db.commit()
    print("\n✅ All branch slugs fixed!")

if __name__ == "__main__":
    fix_slugs()
