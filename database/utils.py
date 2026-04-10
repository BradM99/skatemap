from uuid import UUID

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException


def get_or_404(db: Session, model, object_id: UUID):
    """
    Get helper that returns a HTTP 404 if the database object can't be found.
    """
    obj = db.get(model, object_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found"
        )
    return obj