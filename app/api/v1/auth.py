"""Authentication API Routers."""

from fastapi import APIRouter, status, HTTPException
from app.schemas.auth import UserResponse, UserRegisterRequest
from app.core.exceptions import ResourceConflictError
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
    """Register a new user with email and password.

    Returns 201 Created with the user's public information.
    Returns 409 Conflict if the email is already registered.
    """
    try:
        user = auth_service.register_user(payload)
    except ResourceConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return UserResponse.model_validate(user)
