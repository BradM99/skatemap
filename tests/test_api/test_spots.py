from starlette.testclient import TestClient
from http import HTTPStatus
from main import app

app_client = TestClient(app)


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

        post_response = client.post("/spots/", json=spot_data)
        assert post_response.status_code == HTTPStatus.CREATED
        created_id = post_response.json()["id"]  # capture the id

        response = client.get("/spots/")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        spot_ids = [s["id"] for s in data]
        assert created_id in spot_ids