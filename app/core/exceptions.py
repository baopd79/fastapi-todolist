"""
Domain-level exceptions
These exceptions are raised by service layer and translated to HTTP responses by the API layer. Service layer should NEVER import HTTPException directly - keep business logic decoupled from web framework
"""


class DomainError(Exception):
    """Base class for all domain-level errors."""

    pass


class ResourceConflictError(DomainError):
    """Raised when attempting to create a resource that already exists.

    Example: registering with an email that's already taken.
    Maps to HTTP 409 Conflict.
    """

    pass


class ResourceNotFoundError(DomainError):
    """Raised when a requested resource does not exist.

    Maps to HTTP 404 Not Found.
    """

    pass


class AuthenticationError(DomainError):
    """Raised when credentials are invalid or user is inactive.

    Maps to HTTP 401 Unauthorized.
    Note: We use the same exception for "wrong password" and "user not found"
    to prevent user enumeration attacks at the login endpoint.
    """

    pass
