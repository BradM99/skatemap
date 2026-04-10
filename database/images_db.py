from uuid import UUID

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database.models import Spot, Image
from database.utils import get_or_404


def get_spot_images(db: Session, spot_id: UUID):
    """
    Gets all images associated with a specific spot.
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


def delete_spot_image(db: Session, spot_id: UUID, image_id: UUID) -> Image:
    """
    Deletes an image record from the database.
    Returns 404 if image cannot be found or if the image does not belong to the specified spot.
    """
    image = get_or_404(db, Image, image_id)
    if image.spot_id != spot_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found for this spot")
    db.delete(image)
    db.commit()
    return image