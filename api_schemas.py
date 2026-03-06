from pydantic import BaseModel
from uuid import UUID


class SpotBase(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float


class SpotCreate(SpotBase):
    pass


class SpotUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class SpotRead(SpotBase):
    id: UUID

    class Config:
        from_attributes = True