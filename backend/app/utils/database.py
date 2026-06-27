"""Database utility functions to reduce code duplication."""

from typing import Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, func
from fastapi import HTTPException

from ..models import Expense, User


def get_user_expense_by_id(db: Session, expense_id: int, user_id: int) -> Optional[Expense]:
    """Get expense by ID ensuring it belongs to the current user."""
    return db.query(Expense).filter(
        and_(Expense.id == expense_id, Expense.owner_id == user_id)
    ).first()


def get_user_expense_or_404(db: Session, expense_id: int, user_id: int) -> Expense:
    """Get expense by ID or raise 404 if not found or doesn't belong to user."""
    expense = get_user_expense_by_id(db, expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


def get_user_expenses_query(db: Session, user_id: int):
    """Get base query for user's expenses."""
    return db.query(Expense).filter(Expense.owner_id == user_id)


def apply_expense_filters(query, category: Optional[str] = None, 
                         month: Optional[int] = None, year: Optional[int] = None):
    """Apply common expense filters to a query."""
    # Sanitize category input
    if category:
        # Remove any potentially harmful characters and limit length
        sanitized_category = ''.join(c for c in category if c.isalnum() or c in (' ', '-', '_'))[:50]
        query = query.filter(Expense.category == sanitized_category)
    
    # Validate month and year ranges
    if month is not None:
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")
    
    if year is not None:
        if not 1900 <= year <= 2100:
            raise ValueError("Year must be between 1900 and 2100")
    
    if month and year:
        query = query.filter(
            and_(
                extract('month', Expense.date) == month,
                extract('year', Expense.date) == year
            )
        )
    
    return query


def create_user_expense(db: Session, expense_data: Dict[str, Any], user_id: int) -> Expense:
    """Create a new expense for a user."""
    # Validate required fields
    required_fields = ['title', 'amount', 'category', 'date']
    for field in required_fields:
        if field not in expense_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate amount is positive
    if expense_data.get('amount', 0) <= 0:
        raise ValueError("Amount must be greater than 0")
    
    # Sanitize expense data to only allow allowed fields
    allowed_fields = {'title', 'description', 'amount', 'category', 'date'}
    sanitized_data = {k: v for k, v in expense_data.items() if k in allowed_fields}
    
    try:
        db_expense = Expense(**sanitized_data, owner_id=user_id)
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except Exception as e:
        db.rollback()
        raise e


def update_expense_from_dict(expense: Expense, update_data: Dict[str, Any], db: Session) -> Expense:
    """Update expense with data from dictionary."""
    # Only allow updating specific fields
    allowed_fields = {'title', 'description', 'amount', 'category', 'date'}
    
    for field, value in update_data.items():
        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed for update")
        
        # Validate amount if provided
        if field == 'amount' and value <= 0:
            raise ValueError("Amount must be greater than 0")
        
        setattr(expense, field, value)
    
    try:
        db.commit()
        db.refresh(expense)
        return expense
    except Exception as e:
        db.rollback()
        raise e


def delete_expense(db: Session, expense: Expense) -> Dict[str, str]:
    """Delete an expense and return success message."""
    try:
        db.delete(expense)
        db.commit()
        return {"message": "Expense deleted successfully"}
    except Exception as e:
        db.rollback()
        raise e


def get_user_categories(db: Session, user_id: int) -> List[str]:
    """Get all unique categories for a user's expenses."""
    categories = db.query(Expense.category).filter(
        Expense.owner_id == user_id
    ).distinct().all()
    return [category[0] for category in categories]


def calculate_monthly_summary(db: Session, user_id: int, year: int) -> List[Dict[str, Any]]:
    """Calculate monthly expense summary for a given year."""
    summary = []
    for month in range(1, 13):
        total = db.query(Expense).filter(
            and_(
                Expense.owner_id == user_id,
                extract('year', Expense.date) == year,
                extract('month', Expense.date) == month
            )
        ).with_entities(func.sum(Expense.amount)).scalar() or 0
        
        summary.append({
            "month": month,
            "total": float(total)
        })
    
    return summary


def check_user_exists_by_email(db: Session, email: str) -> Optional[User]:
    """Check if user exists by email."""
    return db.query(User).filter(User.email == email).first()


def check_user_exists_by_username(db: Session, username: str) -> Optional[User]:
    """Check if user exists by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, email: str, hashed_password: str) -> User:
    """Create a new user."""
    try:
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e
