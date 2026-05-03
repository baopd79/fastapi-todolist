"""FastAPI dependencies for the API layer.

Centralized location for reusable dependency-injection callables.
Reduces import noise in router files.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.todo_service import TodoService

# Re-export common dependencies
# SessionDep -> Depends(get_db)-> goi get_db()-> yield Session
SessionDep = Annotated[Session, Depends(get_db)]

# HTTP Bearer scheme - tells Swagger UI to show "Authorize" button
_bearer_scheme = HTTPBearer()


def get_auth_service(session: SessionDep) -> AuthService:
    """Provide(cung cap) an AuthService instance scoped to the current request."""
    return AuthService(session)


# flow : AuthServiceDep -> depends(get_auth_service)-> Sessiondep->Depends(get_db)->goi get_db()->Session
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


# Kết luận
# AuthServiceDep = abstraction cho DI
# Lợi ích chính:
# giảm lặp
# giảm coupling
# dễ refactor
# 3. Tại sao tách file deps.py?
# Reusable: SessionDep dùng ở mọi router.
# Centralized: 1 chỗ duy nhất sửa khi đổi DI logic.
# Avoid circular imports: nếu inline trong router, dễ circular.
def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
    session: SessionDep,
) -> User:
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_repo = UserRepository(session)
    user = user_repo.get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_todo_service(session: SessionDep) -> TodoService:
    return TodoService(session)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]
