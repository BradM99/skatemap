from database.db_models import Spot
from database.spot_db import get_spot


class TestSpotDB:
    """
    Test class for Spot database operations.
    """

    def test_create_spot(self, db):
        """
        Test creating a Spot directly in the database.
        """
        spot = Spot(
            name="Test Spot",
            description="DB test",
            latitude=51.5074,
            longitude=-0.1278,
        )

        db.add(spot)
        db.commit()
        db.refresh(spot)

        assert spot.id is not None
        assert spot.name == "Test Spot"
        assert spot.description == "DB test"

    def test_get_spot_by_id(self, db):
        """
        Tests a spot is successfully retrieved from the DB using its ID
        """
        spot = Spot(
            name="Test Spot",
            description="DB test",
            latitude=51.5074,
            longitude=-0.1278,
        )

        db.add(spot)
        db.commit()

        result = get_spot(db, spot_id=spot.id)
        assert result.id == spot.id

    def test_get_all_spots(self, db):
        """
        Test retrieving all Spot records directly from the database.
        """
        spot = Spot(
            name="Test Spot",
            description="DB test",
            latitude=51.5074,
            longitude=-0.1278,
        )

        db.add(spot)
        db.commit()

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