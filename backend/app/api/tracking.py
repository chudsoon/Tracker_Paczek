from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tracking import TrackingCreate, TrackingOut
from app.crud.tracking import create_tracking, get_trackings, get_trackings_by_user, get_tracking_by_id, remove_tracking
from app.crud.inpost import get_inpost_status
from app.models.tracking import Tracking
from app.db import SessionLocal, engine
from app.db import Base

Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@router.get("/", response_model=list[TrackingOut])
def list_trackigns(user_id: int, db:  Session = Depends(get_db)):
    return  get_trackings_by_user(db, user_id)




@router.post("/", response_model=TrackingOut)
def add_tracking(tracking: TrackingCreate, db: Session = Depends(get_db)):
    return create_tracking(db, tracking)

@router.delete("/{tracking_id}")
def delete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    trackings = get_trackings(db)
    tracking_to_delete = next((t for t in trackings if t.id == tracking_id), None)
    if tracking_to_delete:
        remove_tracking(db, tracking_id)
    else:
        raise HTTPException(status_code=404, detail="Tracking not found")
    

@router.get("/{tracking_number}/status")
def get_tracking_status(tracking_number: str, db: Session = Depends(get_db)):
    tracking = db.query(Tracking).filter(Tracking.number == tracking_number).first()
    if not tracking:
        raise HTTPException(404, "Tracking not found")
    if tracking.carrier == "Inpost":
        return get_inpost_status(tracking.number)
    raise HTTPException(400, "Unsupported carrier")


    

  

    

