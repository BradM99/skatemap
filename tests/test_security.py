import pytest
from starlette.exceptions import HTTPException

from core.security import create_access_token, decode_access_token

class TestSecurity:

    def test_decode_access_token_valid(self):
        """A token created by create_access_token should decode back to its original payload."""
        token = create_access_token({"sub": "some-user-id"})
        payload = decode_access_token(token)
        assert payload["sub"] == "some-user-id"

    def test_decode_access_token_invalid(self):
        """A malformed/garbage token should raise a 401."""
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token("not.a.valid.token")

        assert exc_info.value.status_code == 401