"""Authentication API Routers."""

from fastapi import APIRouter, status
from app.schemas.auth import (
    UserResponse,
    UserRegisterRequest,
    LoginRequest,
    TokenResponse,
)
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


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login and get access token",
)
def login(payload: LoginRequest, auth_service: AuthServiceDep) -> TokenResponse:
    access_token = auth_service.login(payload)
    return TokenResponse(access_token=access_token)
