from sqlalchemy.orm import Session
from app import models, schemas
from app.models.tracking import Tracking
from app.schemas.tracking import TrackingCreate, TrackingOut
from app import models




def create_tracking(db: Session, tracking: TrackingCreate):
    db_tracking = Tracking(**tracking.dict())
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking

def remove_tracking(db: Session, tracking_id: int):
    db_tracking = db.query(models.Tracking).filter(models.Tracking.id == tracking_id).first()
    db.delete(db_tracking)
    db.commit()
    return {"message": "Delete"}
    
   
def get_trackings(db: Session):
    return db.query(Tracking).all()

def get_trackings_by_user(db: Session, user_id: int):
    return db.query(models.Tracking).filter(models.Tracking.user_id == user_id).all()

def get_tracking_by_id(db: Session, tracking_id: int):
    return db.query(models.Tracking).filter(models.Tracking.id == tracking_id)


