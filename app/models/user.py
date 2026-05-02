from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    """User table model
    Stores authentication credentials and metadata for registered users.
    Email is stored in lowercase to enforce case-insensitive uniqueness"""

    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(
        max_length=255,
        unique=True,
        nullable=False,
        description="User email, store lowercase for case-insensitive matching",
    )
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
        description="Argon2id hash, never store plaintext",
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Soft-disable flag; inactive users cannot login",
    )

    created_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    updated_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=_utc_now,
        ),
    )
