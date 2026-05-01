"""SQLModel table models
Import all models here so Alembic autogenerate can detect them.
Every new model must be added to this file.

"""

from app.models.user import User

__all__ = ["User"]
