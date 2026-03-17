from starlette.exceptions import HTTPException
from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from database.db_models import Spot
from api_schemas import SpotCreate, SpotUpdate

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