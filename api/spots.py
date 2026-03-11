from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from api_schemas import SpotCreate, SpotUpdate, SpotRead
from database import spot_db

router = APIRouter(prefix="/spots", tags=["spots"])


@router.get("/", response_model=list[SpotRead])
def get_all_spots(db: Session = Depends(get_db)):
    """
    Returns a sequence of spots all spots in the database
    """
    return spot_db.get_all_spots(db)


@router.post("/", response_model=SpotRead)
def create_spot(spot: SpotCreate, db: Session = Depends(get_db)):
    """
    Creates a new spot in the database
    """
    return spot_db.create_spot(db, spot)


@router.get("/{spot_id}", response_model=SpotRead)
def get_spot(spot_id: str, db: Session = Depends(get_db)):
    """
    Gets a spot from the database using the spot_id.
    Raises 404 if spot does not exist.
    """
    spot = spot_db.get_spot(db, spot_id)
    if spot is None:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot