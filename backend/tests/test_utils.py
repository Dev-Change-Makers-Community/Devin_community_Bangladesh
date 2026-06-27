"""Tests for utility functions."""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app.utils.database import (
    get_user_expense_by_id,
    get_user_expense_or_404,
    get_user_expenses_query,
    apply_expense_filters,
    create_user_expense,
    update_expense_from_dict,
    delete_expense,
    get_user_categories,
    calculate_monthly_summary,
    check_user_exists_by_email,
    check_user_exists_by_username,
    create_user
)
from app.utils.exceptions import ExpenseNotFoundException
from app.models import Expense, User
from app.schemas import ExpenseCreate


class TestDatabaseUtils:
    """Test database utility functions."""
    
    def test_get_user_expense_by_id(self, db_session: Session, test_user, test_expenses):
        """Test getting user expense by ID."""
        expense = test_expenses[0]
        result = get_user_expense_by_id(db_session, expense.id, test_user.id)
        
        assert result is not None
        assert result.id == expense.id
        assert result.owner_id == test_user.id
    
    def test_get_user_expense_by_id_not_found(self, db_session: Session, test_user):
        """Test getting non-existent expense returns None."""
        result = get_user_expense_by_id(db_session, 99999, test_user.id)
        assert result is None
    
    def test_get_user_expense_by_id_wrong_user(self, db_session: Session, test_user, test_expenses):
        """Test getting expense from different user returns None."""
        # Create another user
        other_user = User(
            username="otheruser",
            email="other@example.com",
            hashed_password="hashed"
        )
        db_session.add(other_user)
        db_session.commit()
        
        expense = test_expenses[0]
        result = get_user_expense_by_id(db_session, expense.id, other_user.id)
        assert result is None
    
    def test_get_user_expense_or_404_success(self, db_session: Session, test_user, test_expenses):
        """Test getting expense or 404 on success."""
        expense = test_expenses[0]
        result = get_user_expense_or_404(db_session, expense.id, test_user.id)
        
        assert result.id == expense.id
    
    def test_get_user_expense_or_404_not_found(self, db_session: Session, test_user):
        """Test getting expense or 404 raises exception."""
        with pytest.raises(ExpenseNotFoundException):
            get_user_expense_or_404(db_session, 99999, test_user.id)
    
    def test_get_user_expenses_query(self, db_session: Session, test_user):
        """Test getting user expenses query."""
        query = get_user_expenses_query(db_session, test_user.id)
        expenses = query.all()
        
        assert all(expense.owner_id == test_user.id for expense in expenses)
    
    def test_apply_expense_filters_category(self, db_session: Session, test_user):
        """Test applying category filter."""
        query = get_user_expenses_query(db_session, test_user.id)
        filtered_query = apply_expense_filters(query, category="Food")
        expenses = filtered_query.all()
        
        assert all(expense.category == "Food" for expense in expenses)
    
    def test_apply_expense_filters_date(self, db_session: Session, test_user):
        """Test applying date filter."""
        query = get_user_expenses_query(db_session, test_user.id)
        filtered_query = apply_expense_filters(query, month=1, year=2024)
        expenses = filtered_query.all()
        
        assert all(expense.date.month == 1 and expense.date.year == 2024 for expense in expenses)
    
    def test_apply_expense_filters_no_filters(self, db_session: Session, test_user):
        """Test applying no filters returns same query."""
        query = get_user_expenses_query(db_session, test_user.id)
        filtered_query = apply_expense_filters(query)
        
        # Should be the same query object
        assert query is filtered_query
    
    def test_create_user_expense(self, db_session: Session, test_user):
        """Test creating user expense."""
        expense_data = {
            "title": "Test Expense",
            "description": "Test description",
            "amount": 100.50,
            "category": "Test Category",
            "date": datetime(2024, 1, 15)
        }
        
        expense = create_user_expense(db_session, expense_data, test_user.id)
        
        assert expense.id is not None
        assert expense.title == expense_data["title"]
        assert expense.owner_id == test_user.id
    
    def test_update_expense_from_dict(self, db_session: Session, test_expenses):
        """Test updating expense from dictionary."""
        expense = test_expenses[0]
        update_data = {
            "title": "Updated Title",
            "amount": 200.00
        }
        
        updated_expense = update_expense_from_dict(expense, update_data, db_session)
        
        assert updated_expense.title == "Updated Title"
        assert updated_expense.amount == 200.00
        assert updated_expense.description == expense.description  # Unchanged
    
    def test_delete_expense(self, db_session: Session, test_expenses):
        """Test deleting expense."""
        expense = test_expenses[0]
        result = delete_expense(db_session, expense)
        
        assert "Expense deleted successfully" in result["message"]
        
        # Verify expense is deleted
        deleted_expense = db_session.query(Expense).filter(Expense.id == expense.id).first()
        assert deleted_expense is None
    
    def test_get_user_categories(self, db_session: Session, test_user, test_expenses):
        """Test getting user categories."""
        categories = get_user_categories(db_session, test_user.id)
        
        assert "Food" in categories
        assert "Transport" in categories
        assert "Entertainment" in categories
        assert len(categories) == 3
    
    def test_get_user_categories_empty(self, db_session: Session, test_user):
        """Test getting categories for user with no expenses."""
        # Create user with no expenses
        empty_user = User(
            username="emptyuser",
            email="empty@example.com",
            hashed_password="hashed"
        )
        db_session.add(empty_user)
        db_session.commit()
        
        categories = get_user_categories(db_session, empty_user.id)
        assert categories == []
    
    def test_calculate_monthly_summary(self, db_session: Session, test_user, test_expenses):
        """Test calculating monthly summary."""
        summary = calculate_monthly_summary(db_session, test_user.id, 2024)
        
        assert len(summary) == 12  # 12 months
        assert all("month" in month_data and "total" in month_data for month_data in summary)
        
        # January should have total amount
        january_total = next(month["total"] for month in summary if month["month"] == 1)
        assert january_total == sum(expense.amount for expense in test_expenses)
    
    def test_calculate_monthly_summary_empty_year(self, db_session: Session, test_user):
        """Test calculating monthly summary for year with no expenses."""
        summary = calculate_monthly_summary(db_session, test_user.id, 2023)
        
        assert len(summary) == 12
        assert all(month["total"] == 0 for month in summary)
    
    def test_check_user_exists_by_email(self, db_session: Session, test_user):
        """Test checking if user exists by email."""
        user = check_user_exists_by_email(db_session, test_user.email)
        assert user is not None
        assert user.id == test_user.id
    
    def test_check_user_exists_by_email_not_found(self, db_session: Session):
        """Test checking non-existent user by email."""
        user = check_user_exists_by_email(db_session, "nonexistent@example.com")
        assert user is None
    
    def test_check_user_exists_by_username(self, db_session: Session, test_user):
        """Test checking if user exists by username."""
        user = check_user_exists_by_username(db_session, test_user.username)
        assert user is not None
        assert user.id == test_user.id
    
    def test_check_user_exists_by_username_not_found(self, db_session: Session):
        """Test checking non-existent user by username."""
        user = check_user_exists_by_username(db_session, "nonexistentuser")
        assert user is None
    
    def test_create_user(self, db_session: Session):
        """Test creating user."""
        user = create_user(
            db_session,
            "newuser",
            "new@example.com",
            "hashed_password"
        )
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.hashed_password == "hashed_password"
