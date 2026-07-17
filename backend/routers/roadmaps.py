from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(prefix="/api/roadmaps", tags=["roadmaps"])

@router.get("/")
def get_roadmaps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Roadmap).offset(skip).limit(limit).all()

@router.delete("/{roadmap_id}")
def delete_roadmap(roadmap_id: str, db: Session = Depends(get_db)):
    r = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id).first()
    if not r: raise HTTPException(status_code=404, detail="Not found")
    db.delete(r)
    db.commit()
    return {"status": "deleted"}
