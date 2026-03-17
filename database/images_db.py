from uuid import UUID

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database.db_models import Spot, Image


def get_or_404(db: Session, model, object_id: UUID):
    """
    Get helper that returns a HTTP 404 if the database object can't be found
    """
    obj = db.get(model, object_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found"
        )
    return obj

def get_spot_images(db: Session, spot_id: UUID):
    """
    Gets all images associated with a specific spot
    """
    spot = get_or_404(db, Spot, spot_id)
    return spot.images


def create_spot_image(db: Session, spot_id: UUID, file_path: str) -> Image:
    """
    Creates a new image record in the database. Returns 404 if spot cannot be found.
    """
    spot = get_or_404(db, Spot, spot_id)
    image = Image(spot_id=spot.id, file_path=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image