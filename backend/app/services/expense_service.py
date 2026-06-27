"""Expense service layer for business logic and data operations."""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, func

from ..models import Expense, User
from ..schemas import ExpenseCreate, ExpenseUpdate
from ..utils.database import (
    get_user_expense_or_404,
    get_user_expenses_query,
    apply_expense_filters,
    create_user_expense,
    update_expense_from_dict,
    delete_expense,
    get_user_categories,
    calculate_monthly_summary
)


class ExpenseService:
    """Service class for expense-related operations."""
    
    @staticmethod
    def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int) -> Expense:
        """Create a new expense for a user."""
        return create_user_expense(db, expense_data.dict(), user_id)
    
    @staticmethod
    def get_expenses(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> List[Expense]:
        """Get expenses for a user with optional filtering."""
        query = get_user_expenses_query(db, user_id)
        query = apply_expense_filters(query, category, month, year)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Expense:
        """Get a specific expense by ID."""
        return get_user_expense_or_404(db, expense_id, user_id)
    
    @staticmethod
    def update_expense(
        db: Session, 
        expense_id: int, 
        expense_update: ExpenseUpdate, 
        user_id: int
    ) -> Expense:
        """Update an existing expense."""
        expense = get_user_expense_or_404(db, expense_id, user_id)
        update_data = expense_update.dict(exclude_unset=True)
        return update_expense_from_dict(expense, update_data, db)
    
    @staticmethod
    def delete_expense(db: Session, expense_id: int, user_id: int) -> Dict[str, str]:
        """Delete an expense."""
        expense = get_user_expense_or_404(db, expense_id, user_id)
        return delete_expense(db, expense)
    
    @staticmethod
    def get_categories(db: Session, user_id: int) -> List[str]:
        """Get all unique categories for a user's expenses."""
        return get_user_categories(db, user_id)
    
    @staticmethod
    def get_monthly_summary(db: Session, user_id: int, year: int) -> List[Dict[str, Any]]:
        """Get monthly expense summary for a given year."""
        return calculate_monthly_summary(db, user_id, year)
    
    @staticmethod
    def get_expense_statistics(db: Session, user_id: int) -> Dict[str, Any]:
        """Get expense statistics for a user."""
        query = get_user_expenses_query(db, user_id)
        
        total_expenses = query.count()
        
        # Handle case with no expenses
        if total_expenses == 0:
            return {
                "total_expenses": 0,
                "total_amount": 0.0,
                "average_amount": 0.0,
                "most_expensive_category": None,
                "unique_categories": 0
            }
        
        total_amount = query.with_entities(func.sum(Expense.amount)).scalar() or 0
        avg_amount = query.with_entities(func.avg(Expense.amount)).scalar() or 0
        
        # Get most expensive category
        category_totals = query.with_entities(
            Expense.category, 
            func.sum(Expense.amount).label('total')
        ).group_by(Expense.category).all()
        
        most_expensive_category = None
        if category_totals:
            try:
                most_expensive_category = max(category_totals, key=lambda x: x[1] if x[1] is not None else 0)
            except (ValueError, TypeError):
                most_expensive_category = None
        
        return {
            "total_expenses": total_expenses,
            "total_amount": float(total_amount),
            "average_amount": float(avg_amount),
            "most_expensive_category": {
                "name": most_expensive_category[0],
                "amount": float(most_expensive_category[1])
            } if most_expensive_category else None,
            "unique_categories": len(category_totals)
        }
