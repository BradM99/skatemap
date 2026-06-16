import datetime

import pytest

from database.models import User
from database.users_db import create_user, get_user_by_id, get_user_by_email, get_user_by_username, get_all_users, delete_user

class TestUsersDB:
    """Tests for the users database operations"""

    def test_create_user(self, db):
        """Tests that a user is properly created."""
        user = create_user(
            db,
            username="username",
            email="email",
            hashed_password="password"
        )

        assert user.id is not None
        assert user.username == "username"
        assert user.email == "email"

    def test_get_user_by_id(self, db, user):
        """Tests that a user is properly retrieved from the database."""
        ret = get_user_by_id(db, user.id)

        assert ret is not None
        assert ret.id == user.id
        assert ret.username == user.username

    def test_get_user_by_username(self, db, user):
        ret = get_user_by_username(db, user.username)

        assert ret is not None
        assert ret.id == user.id
        assert ret.username == user.username

    def test_get_user_by_email(self, db, user):
        ret = get_user_by_email(db, user.email)

        assert ret is not None
        assert ret.id == user.id
        assert ret.username == user.username

    def test_get_all_users(self, db, multiple_users):
        """Tests that all users are properly returned."""
        ret = get_all_users(db)
        assert len(ret) == len(multiple_users)
        ret_usernames = {u.username for u in ret}
        expected_usernames = {u.username for u in multiple_users}

        assert ret_usernames == expected_usernames

    def test_delete_user(self, db, user):
        """Tests that a user is properly deleted from the database."""
        delete_user(db, user.id)
        ret = get_user_by_id(db, user.id)
        assert ret is None

        assert len(get_all_users(db)) >= 0
