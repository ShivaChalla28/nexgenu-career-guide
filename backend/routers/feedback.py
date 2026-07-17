from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.post("/submit")
def submit_feedback(feedback: schemas.FeedbackSubmit, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(
        user_id=feedback.user_id,
        name=feedback.name,
        branch=feedback.branch,
        college=feedback.college,
        rating=feedback.rating,
        text=feedback.text,
        is_approved=0
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return {"message": "Feedback submitted successfully. Waiting for admin approval.", "id": new_feedback.id}

@router.get("/pending", response_model=list[schemas.Feedback])
def get_pending_feedback(db: Session = Depends(get_db)):
    # Assuming Admin only
    feedbacks = db.query(models.Feedback).filter(models.Feedback.is_approved == 0).order_by(models.Feedback.created_at.desc()).all()
    return feedbacks

import uuid

@router.get("/approved", response_model=list[schemas.Feedback])
def get_approved_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.is_approved == 1).order_by(models.Feedback.created_at.desc()).all()
    return feedbacks

@router.put("/{feedback_id}/approve")
def approve_feedback(feedback_id: uuid.UUID, db: Session = Depends(get_db)):
    # Assuming Admin only
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.is_approved = 1
    db.commit()
    return {"message": "Feedback approved successfully"}

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: uuid.UUID, db: Session = Depends(get_db)):
    # Assuming Admin only
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db.delete(feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}
