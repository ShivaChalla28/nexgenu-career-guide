from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import uuid
from database import get_db

router = APIRouter(prefix="/api/ui", tags=["ui_elements"])

@router.get("/buttons")
def get_buttons(db: Session = Depends(get_db)):
    return db.query(models.DynamicButton).all()

@router.post("/buttons")
def create_button(data: dict, db: Session = Depends(get_db)):
    btn = models.DynamicButton(**data)
    db.add(btn)
    db.commit()
    db.refresh(btn)
    return btn

@router.delete("/buttons/{btn_id}")
def delete_button(btn_id: uuid.UUID, db: Session = Depends(get_db)):
    btn = db.query(models.DynamicButton).filter(models.DynamicButton.id == btn_id).first()
    if btn:
        db.delete(btn)
        db.commit()
    return {"status": "deleted"}

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()

@router.post("/alerts")
def create_alert(data: dict, db: Session = Depends(get_db)):
    a = models.Alert(**data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@router.delete("/alerts/{a_id}")
def delete_alert(a_id: uuid.UUID, db: Session = Depends(get_db)):
    a = db.query(models.Alert).filter(models.Alert.id == a_id).first()
    if a:
        db.delete(a)
        db.commit()
    return {"status": "deleted"}

@router.get("/ads")
def get_ads(db: Session = Depends(get_db)):
    return db.query(models.Ad).all()

@router.post("/ads")
def create_ad(data: dict, db: Session = Depends(get_db)):
    ad = models.Ad(**data)
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad

@router.delete("/ads/{ad_id}")
def delete_ad(ad_id: uuid.UUID, db: Session = Depends(get_db)):
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if ad:
        db.delete(ad)
        db.commit()
    return {"status": "deleted"}
