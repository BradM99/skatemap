import shutil
from http import HTTPStatus
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database.db import get_db
from api_schemas import SpotCreate, SpotUpdate, SpotRead, ImageRead, ImageCreate
from database import spot_db, images_db
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
def get_spot(spot_id: UUID, db: Session = Depends(get_db)):
    """
    Gets a spot from the database using the spot_id.
    Raises 404 if spot does not exist.
    """
    spot = spot_db.get_spot(db, spot_id)
    if spot is None:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot

@router.get("/spots/{spot_id}/images", response_model=list[ImageRead], status_code=HTTPStatus.OK)
def get_spot_images(spot_id: UUID, db: Session = Depends(get_db)):
    return images_db.get_spot_images(db, spot_id)

@router.post("/spots/{spot_id}/images", response_model=ImageRead, status_code=201)
def upload_image(spot_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a new image for a specific spot.
    :param spot_id: UUID of the spot to which the image will be attached
    :param file: File to upload
    """
    save_dir = Path("static/images") / str(spot_id)
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return images_db.create_spot_image(db, spot_id, str(file_path))
