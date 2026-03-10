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


def create_spot(db: Session, data: SpotCreate) -> Spot:
    """
    Creates a spot and adds it to the database, returns the spot object
    """
    spot = Spot(**data.model_dump())

    db.add(spot)
    db.commit()
    db.refresh(spot)

    return spot


def get_spot(db: Session, spot_id: UUID) -> Spot | None:
    """
    Gets a spot from the database via its spot id
    """
    return db.get(Spot, spot_id)

def get_by_coords(db: Session, longitude: float, latitude: float) -> Spot | None:
    """
    Gets a Spot from the Database via its longitude and latitude
    (Unsure if this will be useful in production)
    :param db:
    :param longitude:
    :param latitude:
    :return:
    """
    statement = select(Spot).where(
        Spot.longitude == longitude,
        Spot.latitude == latitude
    )

    return db.execute(statement).scalar_one_or_none()


def get_all_spots(db: Session) -> Sequence[Spot]:
    """
    Gets and returns a sequence (list) of all spots in the database.
    """
    return db.execute(select(Spot)).scalars().all()


def get_spots_paginated(
    db: Session,
    offset: int = 0,
    limit: int = 100
) -> Sequence[Spot]:
    """
    Gets and returns a certain amount of spots from the database.
    Offset used to skip entries.
    """
    result = db.execute(
        select(Spot).offset(offset).limit(limit)
    )

    return result.scalars().all()


def update_spot(db: Session, spot: Spot, data: SpotUpdate) -> Spot:
    """
    Updates an existing spot in the database
    """
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(spot, field, value)

    db.commit()
    db.refresh(spot)

    return spot


def delete_spot(db: Session, spot: Spot) -> None:
    """
    Deletes a spot from the database
    :param db:
    :param spot:
    :return:
    """
    db.delete(spot)
    db.commit()


def delete_all_spots(db: Session) -> None:
    db.query(Spot).delete()
    db.commit()