from unittest import TestCase

from starlette.testclient import TestClient

from main import app

app_client = TestClient(app)

class TestImagesAPI(TestCase):

    def test_add_image(self, client):

        pass

    def test_delete_image(self, client):
        pass

    def test_list_images(self, client):
        pass

    def test_update_image(self, client):
        pass

