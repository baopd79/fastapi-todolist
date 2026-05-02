"""Domain-level exceptions with HTTP mapping.

Exceptions carry their own status_code and error code, allowing a single
centralized handler in main.py to translate them to HTTP responses.
Service layer raises these; API layer never needs try/except per exception.
"""

from typing import ClassVar


class DomainError(Exception):
    """Base  class for all domain-level errors"""

    code: ClassVar[str] = "INTERNAL_ERROR"
    status_code: ClassVar[int] = 500
    default_message: ClassVar[str] = "An unexpected error occurred"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class ResourceConflictError(DomainError):
    """Raised when attempting to create a resource that already exists.

    Example: registering with an email that's already taken.
    Maps to HTTP 409 Conflict.
    """

    code: ClassVar[str] = "RESOURCE_CONFLICT"
    status_code: ClassVar[int] = 409
    default_message: ClassVar[str] = " Resource already exists"


class ResourceNotFoundError(DomainError):
    """Raised when a requested resource does not exist.

    Maps to HTTP 404 Not Found.
    """

    code: ClassVar[str] = "RESOURCE_NOT_FOUND"
    status_code: ClassVar[int] = 404
    default_message: ClassVar[str] = "resource not found"


class AuthenticationError(DomainError):
    """Raised when credentials are invalid or user is inactive.

    Maps to HTTP 401 Unauthorized.
    Note: We use the same exception for "wrong password" and "user not found"
    to prevent user enumeration attacks at the login endpoint.
    """

    code: ClassVar[str] = "AUTHENTICATION_FAILED"
    status_code: ClassVar[int] = 401
    default_message: ClassVar[str] = "Invalid email or password"
