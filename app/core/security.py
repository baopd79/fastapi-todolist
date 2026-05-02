"""Security utilities : password and verification"""

from passlib.context import CryptContext

__pwd_context = CryptContext(schemes=["Argon2"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """hash a plain-text password using Argon2id
    Returns:
       Encoded hash string containing algorithm, parameters, salt, and digest.
       Format: $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>
    """
    return __pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)
