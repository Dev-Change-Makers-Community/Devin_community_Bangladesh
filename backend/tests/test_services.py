"""Tests for service layer."""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.expense_service import ExpenseService
from app.services.user_service import UserService
from app.models import Expense, User
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.utils.exceptions import UserAlreadyExistsException


class TestExpenseService:
    """Test expense service layer."""
    
    def test_create_expense(self, db_session: Session, test_user):
        """Test expense creation in service layer."""
        expense_data = ExpenseCreate(
            title="Service Test Expense",
            description="Test description",
            amount=150.75,
            category="Test Category",
            date=datetime(2024, 1, 15)
        )
        
        expense = ExpenseService.create_expense(db_session, expense_data, test_user.id)
        
        assert expense.id is not None
        assert expense.title == expense_data.title
        assert expense.owner_id == test_user.id
    
    def test_get_expenses(self, db_session: Session, test_user, test_expenses):
        """Test getting expenses from service layer."""
        expenses = ExpenseService.get_expenses(db_session, test_user.id)
        
        assert len(expenses) == len(test_expenses)
        assert all(expense.owner_id == test_user.id for expense in expenses)
    
    def test_get_expenses_with_filters(self, db_session: Session, test_user, test_expenses):
        """Test getting expenses with filters."""
        # Filter by category
        expenses = ExpenseService.get_expenses(
            db_session, test_user.id, category="Food"
        )
        
        assert all(expense.category == "Food" for expense in expenses)
    
    def test_get_expense_by_id(self, db_session: Session, test_user, test_expenses):
        """Test getting expense by ID from service layer."""
        expense_id = test_expenses[0].id
        expense = ExpenseService.get_expense_by_id(db_session, expense_id, test_user.id)
        
        assert expense.id == expense_id
        assert expense.owner_id == test_user.id
    
    def test_get_expense_by_id_not_found(self, db_session: Session, test_user):
        """Test getting non-existent expense raises exception."""
        with pytest.raises(Exception):  # Should raise ExpenseNotFoundException
            ExpenseService.get_expense_by_id(db_session, 99999, test_user.id)
    
    def test_update_expense(self, db_session: Session, test_user, test_expenses):
        """Test updating expense in service layer."""
        expense_id = test_expenses[0].id
        update_data = ExpenseUpdate(
            title="Updated Title",
            amount=200.00
        )
        
        updated_expense = ExpenseService.update_expense(
            db_session, expense_id, update_data, test_user.id
        )
        
        assert updated_expense.title == "Updated Title"
        assert updated_expense.amount == 200.00
    
    def test_delete_expense(self, db_session: Session, test_user, test_expenses):
        """Test deleting expense in service layer."""
        expense_id = test_expenses[0].id
        
        result = ExpenseService.delete_expense(db_session, expense_id, test_user.id)
        
        assert "Expense deleted successfully" in result["message"]
        
        # Verify expense is deleted
        with pytest.raises(Exception):  # Should raise ExpenseNotFoundException
            ExpenseService.get_expense_by_id(db_session, expense_id, test_user.id)
    
    def test_get_categories(self, db_session: Session, test_user, test_expenses):
        """Test getting categories from service layer."""
        categories = ExpenseService.get_categories(db_session, test_user.id)
        
        assert "Food" in categories
        assert "Transport" in categories
        assert "Entertainment" in categories
    
    def test_get_monthly_summary(self, db_session: Session, test_user, test_expenses):
        """Test getting monthly summary from service layer."""
        summary = ExpenseService.get_monthly_summary(db_session, test_user.id, 2024)
        
        assert len(summary) == 12  # 12 months
        assert all("month" in month_data and "total" in month_data for month_data in summary)
    
    def test_get_expense_statistics(self, db_session: Session, test_user, test_expenses):
        """Test getting expense statistics from service layer."""
        stats = ExpenseService.get_expense_statistics(db_session, test_user.id)
        
        assert stats["total_expenses"] == len(test_expenses)
        assert stats["unique_categories"] == 3
        assert stats["total_amount"] == sum(expense.amount for expense in test_expenses)
        assert stats["most_expensive_category"] is not None


class TestUserService:
    """Test user service layer."""
    
    def test_create_user_success(self, db_session: Session):
        """Test successful user creation in service layer."""
        user = UserService.create_user(
            db_session, 
            "newuser", 
            "new@example.com", 
            "password123",
            "hashed_password"
        )
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "new@example.com"
    
    def test_create_user_duplicate_email(self, db_session: Session, test_user):
        """Test user creation with duplicate email fails."""
        with pytest.raises(UserAlreadyExistsException):
            UserService.create_user(
                db_session,
                "differentuser",
                test_user.email,  # Same email
                "password123",
                "hashed_password"
            )
    
    def test_create_user_duplicate_username(self, db_session: Session, test_user):
        """Test user creation with duplicate username fails."""
        with pytest.raises(UserAlreadyExistsException):
            UserService.create_user(
                db_session,
                test_user.username,  # Same username
                "different@example.com",
                "password123",
                "hashed_password"
            )
    
    def test_get_user_by_email(self, db_session: Session, test_user):
        """Test getting user by email."""
        user = UserService.get_user_by_email(db_session, test_user.email)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    def test_get_user_by_email_not_found(self, db_session: Session):
        """Test getting non-existent user by email."""
        user = UserService.get_user_by_email(db_session, "nonexistent@example.com")
        
        assert user is None
    
    def test_get_user_by_username(self, db_session: Session, test_user):
        """Test getting user by username."""
        user = UserService.get_user_by_username(db_session, test_user.username)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username
    
    def test_get_user_by_username_not_found(self, db_session: Session):
        """Test getting non-existent user by username."""
        user = UserService.get_user_by_username(db_session, "nonexistentuser")
        
        assert user is None
