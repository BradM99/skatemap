from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_schemas import ImageRead
from database import spot_db
from database.db import get_db

router = APIRouter(prefix="/images", tags=["spots"])

@router.get("/spots/{spot_id}/images", response_model=list[ImageRead], status_code=HTTPStatus.OK)
def get_spot_images(spot_id: str, db: Session = Depends(get_db)):
    return spot_db.get_spot_images(db, spot_id)