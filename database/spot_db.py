from uuid import UUID
from typing import Type, TypeVar, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.db_models import Spot
from api_schemas import SpotCreate

ModelType = TypeVar("ModelType")


def get_by_id(
    db: Session,
    model: Type[ModelType],
    obj_id,
) -> ModelType | None:
    return db.get(model, obj_id)


def create_spot(db: Session, data: SpotCreate) -> Spot:
    spot = Spot(**data.model_dump())
    db.add(spot)
    db.commit()
    db.refresh(spot)
    return spot

def get_all_spots(db: Session) -> Sequence[Spot]:
    result = db.execute(select(Spot))
    return result.scalars().all()


def get_spot(db: Session, spot_id: UUID) -> Spot | None:
    return db.get(Spot, spot_id)
