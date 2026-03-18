from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status

from database.db_models import Users
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    bcrypt automatically generates and embeds a salt, so two calls with the
    same password produce different hashes — this is by design and prevents
    rainbow-table attacks.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored bcrypt hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str) -> Users | None:
    """
    Fetch a single user by their username.

    Used internally by both `create_user` (duplicate check) and
    `authenticate_user` (credential lookup).
    """
    return db.query(Users).filter(Users.username == username).first()


def create_user(db: Session, username: str, password: str) -> Users:
    """
    Register a new user in the database.

    Checks for username conflicts before insertion and hashes the password
    before it is ever written to the database.
    """
    if get_user_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{username}' is already taken."
        )

    user = Users(
        username=username,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> Users:
    """
    Validates a username/password pair against the database.
    """
    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Generate a signed JWT access token.

    Encodes the provided payload with an expiry timestamp (`exp`) and signs
    it using the configured JWT_SECRET_KEY and JWT_ALGORITHM.

    The `sub` (subject) claim in `data` should be a unique, stable identifier
    for the user — typically the username or user ID as a string.
    """
    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta
        else timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.

    Validates the token signature and expiry. Raises an HTTPException on any
    failure so this can be used directly as a FastAPI dependency helper.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
