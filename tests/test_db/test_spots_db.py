from database.db_models import Spot


def test_create_spot_db(db):
    """
    Test creating a Spot directly in the database.

    - Creates a Spot ORM instance.
    - Adds and commits it to the test database.
    - Refreshes the instance to populate generated fields.
    - Asserts that an ID was assigned and fields were stored correctly.
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


def test_get_all_spots_db(db):
    """
    Test retrieving all Spot records directly from the database.

    - Inserts a Spot into the test database.
    - Queries all Spot records using the SQLAlchemy session.
    - Asserts that the result is a list containing exactly one Spot.
    - Verifies the stored data matches the inserted values.
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