"""
User repository: data access layer for User model.
Repository pattern responsibilities:
- Only DB operations(CRUD, query)
- No business logic ( validation, password hashting,..etc..)
- No HTTP knowledge
- Returns domains object( User), not DTOs

This separation(su tach biet nay) make business logic testable without DB
and DB swap-able(co the trao doi)
without rewriting business logic.


"""

from sqlmodel import Session, select
from typing import Optional
from app.models.user import User


class UserRepository:
    """Repository for User table"""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Return user by primary key or None if not found"""
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """Return user by email(case-sensitive match)"""
        statement = select(User).where(User.email == email)
        return self._session.exec(statement).first()
    
    def create(self, user: User)-> User:
        """Persist a new user.

        Adds to session and flushes to obtain auto-generated ID.
        Does NOT commit — caller controls transaction boundary.
        """
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user
        
                                       
