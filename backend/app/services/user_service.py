"""User service layer for user-related operations."""

from typing import Optional
from sqlalchemy.orm import Session

from ..models import User
from ..utils.database import (
    check_user_exists_by_email,
    check_user_exists_by_username,
    create_user
)
from ..utils.exceptions import UserAlreadyExistsException


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, hashed_password: str) -> User:
        """Create a new user after validation."""
        # Check if email already exists
        if check_user_exists_by_email(db, email):
            raise UserAlreadyExistsException("email")
        
        # Check if username already exists
        if check_user_exists_by_username(db, username):
            raise UserAlreadyExistsException("username")
        
        # Create new user (password parameter kept for API consistency but not used directly)
        return create_user(db, username, email, hashed_password)
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return check_user_exists_by_email(db, email)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return check_user_exists_by_username(db, username)
