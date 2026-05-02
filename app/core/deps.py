"""FastAPI dependencies for the API layer.

Centralized location for reusable dependency-injection callables.
Reduces import noise in router files.
"""

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_db
from app.services.auth_service import AuthService

# Re-export common dependencies
# SessionDep -> Depends(get_db)-> goi get_db()-> yield Session
SessionDep = Annotated[Session, Depends(get_db)]


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
