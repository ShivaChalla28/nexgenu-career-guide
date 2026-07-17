from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/branches",
    tags=["branches"]
)

@router.get("/")
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    branches = db.query(models.Branch).offset(skip).limit(limit).all()
    result = []
    for b in branches:
        mapped_count = db.query(models.BranchCareerMap).filter(models.BranchCareerMap.branch_id == b.id).count()
        result.append({
            "id": b.id,
            "name": b.name,
            "slug": b.slug,
            "description": b.description,
            "icon": b.icon,
            "created_at": b.created_at,
            "careers": [None] * mapped_count # Mock array so frontend `.length` works
        })
    return result

@router.get("/{branch_slug}/careers")
def get_careers_by_branch(branch_slug: str, db: Session = Depends(get_db)):
    # Try exact match first
    branch = db.query(models.Branch).filter(models.Branch.slug == branch_slug).first()
    
    # If not found, try partial match (e.g. 'electrical-and-electronics-engineering' matches 'electrical-and-electronics-engineering-eee')
    if not branch:
        branch = db.query(models.Branch).filter(
            models.Branch.slug.like(f"{branch_slug}%")
        ).first()
    
    if not branch:
        raise HTTPException(status_code=404, detail=f"Branch not found for slug: {branch_slug}")
    
    mappings = db.query(models.BranchCareerMap).filter(
        models.BranchCareerMap.branch_id == branch.id
    ).all()
    
    career_ids = [m.career_id for m in mappings]
    careers = db.query(models.Career).filter(models.Career.id.in_(career_ids)).all()
    
    return {"branch": branch, "careers": careers}

@router.post("/", response_model=schemas.Branch)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.put("/{branch_id}")
def update_branch(branch_id: str, data: dict, db: Session = Depends(get_db)):
    b = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not b: raise HTTPException(status_code=404)
    for k, v in data.items():
        if hasattr(b, k): setattr(b, k, v)
    db.commit()
    db.refresh(b)
    return b

@router.delete("/{branch_id}")
def delete_branch(branch_id: str, db: Session = Depends(get_db)):
    b = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if b:
        # Delete associated mappings first
        db.query(models.BranchCareerMap).filter(models.BranchCareerMap.branch_id == branch_id).delete()
        db.delete(b)
        db.commit()
    return {"status": "deleted"}
