from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from api_schemas import Spot, SpotCreate
from database import spot_db

router = APIRouter(prefix="/spots", tags=["spots"])

@router.get("/spots", response_model=list[Spot])
def get_all_spots(db: Session = Depends(get_db)):
    return spot_db.get_all_spots(db)

@router.post("/spots", response_model=Spot)
def create_spots(spot: SpotCreate, db: Session = Depends(get_db)):
    return spot_db.create_spot(db, spot)