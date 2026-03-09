from database.db_models import Spot
from database.spot_db import get_spot, delete_spot


class TestSpotDB:
    """
    Test class for Spot database operations.
    """

    def test_create_spot(self, db, spot):
        """
        Test creating a Spot directly in the database.
        Spot fixture creates a valid spot and puts it in the database
        """
        assert spot.id is not None
        assert spot.name == "Test Spot"
        assert spot.description == "Fixture test spot"
        assert spot.longitude == -0.1278
        assert spot.latitude == 51.5074


    def test_delete_spot(self, db, spot):
        assert get_spot(db, spot.id) is not None

        delete_spot(db, spot)

        assert get_spot(db, spot.id) is None



    def test_get_spot_by_id(self, db, spot):
        """
        Tests a spot is successfully retrieved from the DB using its ID
        """
        result = get_spot(db, spot_id=spot.id)
        assert result.id == spot.id

    def test_get_all_spots(self, db, spot):
        """
        Test retrieving all Spot records directly from the database.
        """
        spots = db.query(Spot).all()

        assert isinstance(spots, list)
        assert len(spots) == 1
        assert spots[0].name == "Test Spot"

    def test_get_all_spots_empty_db(self, db):
        """
        Tests DB returns empty list if DB is empty
        """

        spots = db.query(Spot).all()

        assert spots == []