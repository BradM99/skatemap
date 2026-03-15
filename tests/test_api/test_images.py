from unittest import TestCase

from starlette.testclient import TestClient

from main import app

app_client = TestClient(app)

class TestImagesAPI(TestCase):

    def test_add_image(self, client):
        """
        Test adding an image.
        """
        pass

    def test_delete_image(self, client):
        """
        Test deleting an image.
        """
        pass

    def test_list_images(self, client):
        """
        Test listing all images.
        """
        pass

    def test_update_image(self, client):
        """
        Test updating an image.
        """
        pass

