import uuid
from http import HTTPStatus

from config import settings


class TestSpotEndpoints:
    """
    Test class for /spots API endpoints.
    """

    def test_create_spot(self, client):
        """
        Test the /spots POST endpoint.

        Sends a new spot payload and asserts that:
        - The response status code is 200 (OK)
        - The response JSON contains the correct name, description, latitude, longitude
        - An 'id' field is present in the returned data
        """
        spot_data = {
            "name": "Test Spot",
            "description": "This is a test spot",
            "latitude": 51.5074,
            "longitude": -0.1278
        }

        response = client.post("/spots/", json=spot_data)

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == spot_data["name"]
        assert data["description"] == spot_data["description"]
        assert data["latitude"] == spot_data["latitude"]
        assert data["longitude"] == spot_data["longitude"]
        assert "id" in data

    def test_get_all_spots(self, client):
        spot_data = {
            "name": "Test Spot",
            "description": "This is a test spot",
            "latitude": 51.5074,
            "longitude": -0.1278
        }

        response = client.post("/spots/", json=spot_data)
        assert response.status_code == HTTPStatus.CREATED
        created_id = response.json()["id"]

        response = client.get("/spots/")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        spot_ids = [s["id"] for s in data]
        assert created_id in spot_ids

class TestSpotImages:

    relative_image_path = settings.BASE_DIR / "tests" / "test_images" / "test_spot.png"

    def test_add_image(self, client, spot):
        """
        Test adding an image to a spot
        """
        response = client.post(f"/spots/{spot.id}/images",
                               files={"file": open(self.relative_image_path, "rb")})
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert "id" in data

    def test_add_image_no_spot(self, client, spot):
        """
        Tests that adding an image to a spot that doesn't exist returns a 404 NOT FOUND
        """
        fake_id = uuid.uuid4()
        response = client.post(f"/spots/{fake_id}/images",
                               files={"file": open(self.relative_image_path, "rb")})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_image(self, client, spot):
        """
        Test deleting an image.
        """
        post_response = client.post(f"/spots/{spot.id}/images",
                                    files={"file": open(self.relative_image_path, "rb")})
        assert post_response.status_code == HTTPStatus.CREATED

        image_id = post_response.json()["id"]

        delete_response = client.delete(f"/spots/{spot.id}/images/{image_id}")
        assert delete_response.status_code == HTTPStatus.OK

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