from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Todo(SQLModel, table=True):
    __tablename__ = "todo"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(
        max_length=255, nullable=False, description="Short sumary of the todo item"
    )
    description: Optional[str] = Field(
        default=None, description="Detailed description (optional)"
    )
    is_completed: bool = Field(
        default=False, nullable=False, description="whether the todo has been completed"
    )
    user_id: int = Field(
        nullable=False,
        foreign_key="user.id",
        index=True,
        description="Owner of this todo(FK->user.id)",
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
