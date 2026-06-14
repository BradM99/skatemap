# TODO

## Auth System

The auth system has stub files (`api/auth.py`, `core/security.py`, `database/users_db.py`) but no implementation yet. This needs to be built in order — each step depends on the one before it.

### 1. Add User model to `database/models.py`
- Need a `users` table with at minimum: `id`, `username`, `email`, `hashed_password`, `created_at`
- This is the foundation everything else builds on
- Update the ER diagram in `docs/architecture.md` when done

### 2. Implement password hashing in `core/security.py`
- Use `passlib` with bcrypt (or `argon2`) for hashing passwords
- Add a `hash_password(plain)` and `verify_password(plain, hashed)` function
- Plain-text passwords must never be stored or logged

### 3. Implement JWT utilities in `core/security.py`
- Add `create_access_token(data)` and `decode_access_token(token)` functions
- Use `python-jose` or `PyJWT` for encoding/decoding
- Store `SECRET_KEY` and `TOKEN_EXPIRE_MINUTES` in `config.py`
- JWTs are how the API identifies authenticated users on subsequent requests

### 4. Implement user DB operations in `database/users_db.py`
- `create_user(db, data)` — hash the password before storing
- `get_user_by_email(db, email)` — needed for login lookup
- `get_user_by_username(db, username)` — needed for duplicate checks

### 5. Build auth endpoints in `api/auth.py`
- `POST /auth/register` — create a new user account, return the user (without password)
- `POST /auth/login` — verify credentials, return a JWT access token
- Add Pydantic schemas: `UserCreate`, `UserRead`, `Token`

### 6. Add a `get_current_user` dependency
- A FastAPI dependency that reads the JWT from the `Authorization` header, decodes it, and returns the user
- This can then be injected into any endpoint that requires authentication

### 7. Protect endpoints that need auth
- Spot creation, image upload, and image deletion should require a logged-in user
- Read endpoints (list spots, get spot, list images) should remain public
- Optionally track which user created each spot by adding a `created_by` foreign key to the `spots` table

### 8. Add auth tests
- Test registration, login, duplicate username/email handling
- Test that protected endpoints return 401 without a token
- Test that protected endpoints work with a valid token

---

## Testing

### Add tests for spot update and delete endpoints
- Once the update/delete routes exist, they need API-level tests
- Cover: successful update, partial update, update non-existent spot, delete, delete non-existent spot

### Add tests for bounding box and pagination
- Verify pagination returns correct slices and respects offset/limit
- Verify bounding box only returns spots within the specified coordinates

---

## Code Cleanup

### Remove `delete_all_spots` from `spot_db.py` or restrict it to tests
- This function deletes every spot in the database with no confirmation
- It has no route but could be accidentally called — it should either be removed or moved into test utilities

### Update `models.py` datetime defaults
- `datetime.now(pytz.timezone('Europe/London'))` is evaluated once at import time, not per-row
- Change to `default=lambda: datetime.now(pytz.timezone('Europe/London'))` or use `server_default` with a SQL function so each row gets the correct timestamp