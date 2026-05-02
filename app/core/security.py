"""Security utilities : password and verification"""

from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from jose import JWTError, jwt

__pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """hash a plain-text password using Argon2id
    Returns:
       Encoded hash string containing algorithm, parameters, salt, and digest.
       Format: $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>
    """
    return __pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)


# JWT tokens


def create_access_token(subject: int) -> str:
    """Create a JWT access token.

    Args:
        subject: User ID to embed in the token. Stored as 'sub' claim
                 (JWT standard for subject identifier).

    Returns:
        Encoded JWT string."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(subject),  # JWT spec : 'sub' must be string
        "iat": now,  # issued at
        "exp": expire,  # expiration
    }
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> int | None:
    """Decode and validate a JWT access token
    Returns:
        User ID (int) if token is valid and not expired.
        None if token is invalid, expired, or malformed."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        sub: str | None = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (JWTError, ValueError):
        return None
