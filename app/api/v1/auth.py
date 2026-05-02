"""Authentication API Routers."""

from fastapi import APIRouter, status
from app.schemas.auth import UserResponse, UserRegisterRequest
from app.core.deps import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    payload: UserRegisterRequest, auth_service: AuthServiceDep
) -> UserResponse:
    user = auth_service.register_user(payload)
    return UserResponse.model_validate(user)

