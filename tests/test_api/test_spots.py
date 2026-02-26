from starlette.testclient import TestClient
from http import HTTPStatus

from main import app

app_client = TestClient(app)


def test_create_spot(client):
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

    response = client.post("/spots/create_spot", json=spot_data)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == spot_data["name"]
    assert data["description"] == spot_data["description"]
    assert data["latitude"] == spot_data["latitude"]
    assert data["longitude"] == spot_data["longitude"]
    assert "id" in data


def test_get_all_spots(client):
    """
    Test retrieving all spots from the /spots GET endpoint.

    - First, creates a new spot via POST to ensure the database has at least one entry.
    - Uses app_client to GET all spots.
    - Asserts that the response status is 200 and the returned data is a list.
    - Checks that the list contains exactly one spot.
    """
    spot_data = {
        "name": "Test Spot",
        "description": "This is a test spot",
        "latitude": 51.5074,
        "longitude": -0.1278
    }
    response = client.post("spots/create_spot", json=spot_data)
    assert response.status_code == HTTPStatus.OK

    response = app_client.get("/spots/get_spots")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1