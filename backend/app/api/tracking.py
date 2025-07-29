from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tracking import TrackingCreate, TrackingOut
from app.crud.tracking import create_tracking, get_trackings, get_trackings_by_user, get_tracking_by_id, remove_tracking
from app.crud.inpost import get_inpost_status, get_inpost_statuses
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
        tracking_data =  get_inpost_status(tracking.number)
        statuses_data = get_inpost_statuses()
        status_items = statuses_data.get("items", [])
        try: 
           statuses_titles = {status['name']: status['title'] for status in status_items}
           statuses_descriptions = {status['name']: status['description'] for status in status_items}
        except TypeError as e:
            raise HTTPException(500, f"Błąd przetwarzania statusów: {e}")
        
        if not tracking_data:
            raise HTTPException(404, "Brak statusu przesyłki")
        
        status_name = tracking_data.get("status")
        status_title = statuses_titles.get(status_name, "Nieznany status")
        status_description = statuses_descriptions.get(status_name, "Nieznany opis")
        tracking_attributes = tracking_data.get("custom_attributes")
        tracking_details = tracking_data.get("tracking_details")
        
        return {"tracking_number": tracking.number, "status": status_name, "title": status_title, "description": status_description, "target_machine_id": tracking_attributes['target_machine_id'], "location_description": tracking_attributes['target_machine_detail']['location_description'], "tracking_details": tracking_details}
    
    
    
    raise HTTPException(400, "Unsupported carrier")


    

  

    

