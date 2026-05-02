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


class EmailNormalizeModel(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="Email")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class UserRegisterRequest(EmailNormalizeModel):
    """Request payload for user registration."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password(8-128 characters, no other constraints )",
    )


class UserResponse(BaseModel):
    """Public user representation returned by API.
    excludes hashed_password and other internal fields."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class LoginRequest(EmailNormalizeModel):
    """Request payload for user login"""

    password: str = Field(
        ..., min_length=1, max_length=128, description="Account Password"
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
