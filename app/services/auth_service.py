"""Authentication service : business logic for user registration and login
service layer respnsibilities(trach nhiem):
- Business rules (e.g.,"email must be unique","password must be hashed before save)
- Orchestration of repositories(dieu phoi cac repo)
- Owns transaction boundary(commit/rollback)
- Raise domain exceptions, NEVER HTTPException"""

from sqlmodel import Session

from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegisterRequest, UserResponse
from app.models.user import User
from app.core.exceptions import ResourceConflictError
from app.core.security import hash_password


class AuthService:
    """authentication and registration business logic"""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._user_repo = UserRepository(session)

    def register_user(self, payload: UserRegisterRequest) -> User:
        """Register a new user
        Args: Payload : validated registration request
        Return : Created User with id and timestamps populated
        Raise : ResourceConflictError: email already registered"""

        # business rule: email must be unique
        existing = self._user_repo.get_by_email(payload.email)
        if existing is not None:
            raise ResourceConflictError(f"Email {payload.email} is already registered")

        # business rule : never store plaintext password
        hashed = hash_password(payload.password)
        user = User(email=payload.email, hash_password=hashed, is_active=True)
        # Repository flushes (gets ID), Service commit(transaction boundary)
        created = self._user_repo.create(user)
        self._session.commit()
        self._session.refresh(created)
        return created
