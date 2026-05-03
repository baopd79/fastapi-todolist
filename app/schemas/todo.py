"""Pydantic schemas for todo endpoints
Separates(tach biet) APIcontract from database model
Includes schemas for create,updatr(partial) and response
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TodoCreateRequest(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=255, description="Title of the todo item"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Optional detailed description"
    )


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = Field(default=None)


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
