from database.images_db import get_spot_images, create_spot_image


class TestImagesDB:

    def test_get_spot_images(self, db, spot):
        """
        Tests that get_spot_images returns the correct list of images for a given spot.
        """
        image = create_spot_image(db, spot.id, "test_image.jpg")
        assert get_spot_images(db, spot.id) == [image]

    def test_upload_image(self, db, spot):
        """
        Tests that create_spot_image creates a new image record in the database.
        """
        image = create_spot_image(db, spot.id, "test_image.jpg")
        assert image is not None
        assert image.file_path == "test_image.jpg"
        assert image.spot_id == spot.id