import uuid
from datetime import datetime
from typing import List, Optional, Text

import pytz
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pathlib import Path

from db import Base


class Spot(Base):
    """
    Spot Table
    :param id: UUID for the spot
    :param name: String name for the spot
    :param description: Optional description for the spot
    :param latitude: Latitude data for the spot taken from OpenStreetMaps
    :param longitude: Longitude data for the spot taken from OpenStreetMaps
    :param created_at: Time the Spot was created in London Time
    """
    __tablename__ = "spots"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    longitude: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(pytz.timezone('Europe/London'))
    )

    images: Mapped[List["Image"]] = relationship("Image", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    spot_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("spots.id"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(
        str(200), nullable=False
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(pytz.timezone('Europe/London'))
    )
    spot: Mapped["Spot"] = relationship("Spot", back_populates="images")
