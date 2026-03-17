from fastapi import Depends
from sqlalchemy.orm import Session

from api_schemas import SpotCreate
from database import spot_db
from database.db import get_db
from database.images_db import get_spot_images, create_spot_image


class TestImagesDB:

    def test_get_spot_images(self, db, spot):
        """
        Tests that get_spot_images returns the correct list of images for a given spot
        """
        image = create_spot_image(db, spot.id, "test_image.jpg")
        assert get_spot_images(db, spot.id) == [image]