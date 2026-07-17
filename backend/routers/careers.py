from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import models
from database import get_db
from llm_service import generate_career_roadmap

router = APIRouter(
    prefix="/api/careers",
    tags=["careers"]
)

@router.get("/")
def get_all_careers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    careers = db.query(models.Career).offset(skip).limit(limit).all()
    return careers

@router.get("/{slug}")
def get_or_generate_career(slug: str, db: Session = Depends(get_db)):
    # 1. Check if it exists in the DB
    career = db.query(models.Career).filter(models.Career.slug == slug).first()
    
    if career:
        # Load roadmap
        roadmap = db.query(models.Roadmap).filter(models.Roadmap.career_id == career.id).first()
        return {
            "career": career,
            "roadmap": roadmap
        }
    
    # 2. If not found, generate using LLM
    # Convert slug to title format: "ai-research-engineer" -> "AI Research Engineer"
    title = slug.replace("-", " ").title()
    
    try:
        generated_data = generate_career_roadmap(title)
        
        # 3. Save to database
        c_data = generated_data.get("career", {})
        r_data = generated_data.get("roadmap", {})
        
        new_career = models.Career(
            name=c_data.get("name", title),
            slug=c_data.get("slug", slug),
            overview=c_data.get("overview"),
            responsibilities=c_data.get("responsibilities"),
            who_can_apply=c_data.get("who_can_apply"),
            industry_demand=c_data.get("industry_demand"),
            future_scope=c_data.get("future_scope"),
            india_salary=c_data.get("india_salary"),
            international_salary=c_data.get("international_salary"),
            remote_opportunities=c_data.get("remote_opportunities"),
            growth_path=c_data.get("growth_path")
        )
        db.add(new_career)
        db.commit()
        db.refresh(new_career)
        
        new_roadmap = models.Roadmap(
            career_id=new_career.id,
            title=r_data.get("title", f"{title} Complete Roadmap"),
            description=r_data.get("description"),
            skills_matrix=r_data.get("skills_matrix"),
            learning_plans=r_data.get("learning_plans"),
            learning_steps=r_data.get("learning_steps"),
            projects=r_data.get("projects"),
            practice_questions=r_data.get("practice_questions"),
            certifications=r_data.get("certifications"),
            interview_prep=r_data.get("interview_prep"),
            readiness_checklist=r_data.get("readiness_checklist")
        )
        db.add(new_roadmap)
        db.commit()
        db.refresh(new_roadmap)
        
        return {
            "career": new_career,
            "roadmap": new_roadmap
        }
        
    except Exception as e:
        print(f"Error generating career roadmap for {title}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate career roadmap. Please try again later."
        )

@router.post("/")
def create_career(data: dict, db: Session = Depends(get_db)):
    c = models.Career(**data)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/{career_id}")
def update_career(career_id: str, data: dict, db: Session = Depends(get_db)):
    c = db.query(models.Career).filter(models.Career.id == career_id).first()
    if not c: raise HTTPException(status_code=404)
    for k, v in data.items():
        if hasattr(c, k): setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{career_id}")
def delete_career(career_id: str, db: Session = Depends(get_db)):
    c = db.query(models.Career).filter(models.Career.id == career_id).first()
    if c:
        db.query(models.BranchCareerMap).filter(models.BranchCareerMap.career_id == career_id).delete()
        db.query(models.Roadmap).filter(models.Roadmap.career_id == career_id).delete()
        db.delete(c)
        db.commit()
    return {"status": "deleted"}
