from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    from sheets_db import get_all_users as get_gsheets_users
    
    core_careers = db.query(models.Career).filter(models.Career.category == "Core Careers").count()
    it_careers = db.query(models.Career).filter(models.Career.category == "IT & Digital Careers").count()
    govt_careers = db.query(models.Career).filter(models.Career.category == "Government & PSU Careers").count()
    total_careers = db.query(models.Career).count()
    visible_careers = db.query(models.BranchCareerMap.career_id).distinct().count()
    
    # Fetch user count from Google Sheets
    gsheets_users = get_gsheets_users()
    
    pending_feedback = db.query(models.Feedback).filter(models.Feedback.is_approved == 0).count()
    approved_feedback = db.query(models.Feedback).filter(models.Feedback.is_approved == 1).count()
    
    return {
        "users": len(gsheets_users),
        "branches": db.query(models.Branch).count(),
        "careers": total_careers,
        "visible_careers": visible_careers,
        "core_careers": core_careers,
        "it_careers": it_careers,
        "govt_careers": govt_careers,
        "roadmaps": db.query(models.Roadmap).count(),
        "pending_feedback": pending_feedback,
        "approved_feedback": approved_feedback
    }

@router.get("/users")
def get_all_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from sheets_db import get_all_users as get_gsheets_users
    
    # Fetch all users from Google Sheets
    users = get_gsheets_users()
    
    # Sort them by created_at descending (newest first)
    try:
        users.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    except Exception:
        pass
        
    # Apply pagination
    paginated_users = users[skip:skip+limit]
    
    return [{"id": u.get("user_id", ""), "user_id": u.get("user_id", ""), "full_name": u.get("full_name", ""), "email": u.get("email", ""), "mobile_number": u.get("mobile_number", ""), "branch": u.get("branch", ""), "college_name": u.get("college_name", ""), "role": u.get("role", "user"), "created_at": u.get("created_at", "")} for u in paginated_users]

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}
