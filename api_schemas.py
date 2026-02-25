from pydantic import BaseModel
from uuid import UUID

class SpotBase(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float

class SpotCreate(SpotBase):
    pass

class Spot(SpotBase):
    id: UUID

    class Config:
        from_attribute = True