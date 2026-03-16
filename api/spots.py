from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from api_schemas import SpotCreate, SpotUpdate, SpotRead
from database import spot_db
from database.db_models import Spot

router = APIRouter(prefix="/spots", tags=["spots"])


@router.get("/", response_model=list[SpotRead], status_code=HTTPStatus.OK)
def get_all_spots(db: Session = Depends(get_db)):
    """
    Returns a sequence of spots all spots in the database
    """
    return spot_db.get_all_spots(db)

def get_spots_by_bounding_box(db: Session, min_lat: float, max_lat: float, min_lng: float, max_lng: float):
    """
    Gets all spots within a specified boundary. Easily implemented on the FE with map.getBounds() with Leaflet.js
    :param db:
    :param min_lat:
    :param max_lat:
    :param min_lng:
    :param max_lng:
    :return:
    """
    return db.query(Spot).filter(
        Spot.latitude >= min_lat,
        Spot.latitude <= max_lat,
        Spot.longitude >= min_lng,
        Spot.longitude <= max_lng,
    ).all()


@router.post("/", response_model=SpotRead, status_code=HTTPStatus.CREATED)
def create_spot(spot: SpotCreate, db: Session = Depends(get_db)):
    """
    Creates a new spot in the database
    """
    return spot_db.create_spot(db, spot)


@router.get("/{spot_id}", response_model=SpotRead, status_code=HTTPStatus.OK)
def get_spot(spot_id: str, db: Session = Depends(get_db)):
    """
    Gets a spot from the database using the spot_id.
    Raises 404 if spot does not exist.
    """
    spot = spot_db.get_spot(db, spot_id)
    if spot is None:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot