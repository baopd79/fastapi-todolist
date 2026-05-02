"""
Pydantic schemas for authentication endpoints
These are request/response DTOs(Data Transfer Objects), separate from
the User SQLModel. Keeping schemas separate from models ensures:
-API contract is explicit and stable
-DB internals(e.g, hashed_password) never leak to API
-Validation rules live with the API layer
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """Request payload for user registration."""

    email: EmailStr = Field(
        ..., max_length=255, description="User email(will be normalized to lowercase)"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password(8-128 characters, no other constraints )",
    )

    # cls la class method khac voi self(can data object) thi cls can thong tin class(UserRegisterRequest)
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """lowercase and strip email for case-insensitive uniqueness."""
        return v.strip().lower()


class UserResponse(BaseModel):
    """Public user representation returned by API.
    excludes hashed_password and other internal fields."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
