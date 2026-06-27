"""Custom exceptions and error handling utilities."""

from fastapi import HTTPException, status


class ExpenseNotFoundException(HTTPException):
    """Raised when an expense is not found or doesn't belong to user."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )


class UserAlreadyExistsException(HTTPException):
    """Raised when trying to register with existing email or username."""
    
    def __init__(self, field: str):
        detail_map = {
            "email": "Email already registered",
            "username": "Username already taken"
        }
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_map.get(field, "User already exists")
        )


class InvalidCredentialsException(HTTPException):
    """Raised when login credentials are invalid."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
