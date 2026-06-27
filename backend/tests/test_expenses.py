"""Tests for expense endpoints."""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient


class TestExpenses:
    """Test expense endpoints."""
    
    def test_create_expense_success(self, client: TestClient, auth_headers):
        """Test successful expense creation."""
        expense_data = {
            "title": "Test Expense",
            "description": "Test description",
            "amount": 100.50,
            "category": "Test Category",
            "date": "2024-01-15T10:00:00"
        }
        
        response = client.post("/expenses/", json=expense_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == expense_data["title"]
        assert data["description"] == expense_data["description"]
        assert data["amount"] == expense_data["amount"]
        assert data["category"] == expense_data["category"]
        assert "id" in data
        assert "owner_id" in data
        assert "created_at" in data
    
    def test_create_expense_unauthorized(self, client: TestClient):
        """Test expense creation without authorization fails."""
        expense_data = {
            "title": "Test Expense",
            "amount": 100.50,
            "category": "Test Category",
            "date": "2024-01-15T10:00:00"
        }
        
        response = client.post("/expenses/", json=expense_data)
        
        assert response.status_code == 401
    
    def test_create_expense_invalid_data(self, client: TestClient, auth_headers):
        """Test expense creation with invalid data fails."""
        # Missing required fields
        expense_data = {
            "title": "Test Expense"
            # Missing amount, category, date
        }
        
        response = client.post("/expenses/", json=expense_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error
    
    def test_get_expenses_success(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expenses list."""
        response = client.get("/expenses/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(test_expenses)
        
        # Check first expense
        expense = data[0]
        assert "id" in expense
        assert "title" in expense
        assert "amount" in expense
        assert "category" in expense
    
    def test_get_expenses_unauthorized(self, client: TestClient):
        """Test getting expenses without authorization fails."""
        response = client.get("/expenses/")
        
        assert response.status_code == 401
    
    def test_get_expenses_with_filters(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expenses with filters."""
        # Filter by category
        response = client.get("/expenses/?category=Food", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(expense["category"] == "Food" for expense in data)
    
    def test_get_expenses_with_pagination(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expenses with pagination."""
        response = client.get("/expenses/?skip=1&limit=1", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 1
    
    def test_get_expense_by_id_success(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expense by ID."""
        expense_id = test_expenses[0].id
        response = client.get(f"/expenses/{expense_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == expense_id
        assert data["title"] == test_expenses[0].title
    
    def test_get_expense_by_id_not_found(self, client: TestClient, auth_headers):
        """Test getting non-existent expense."""
        response = client.get("/expenses/99999", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Expense not found" in response.json()["detail"]
    
    def test_get_expense_by_id_unauthorized(self, client: TestClient, test_expenses):
        """Test getting expense by ID without authorization fails."""
        expense_id = test_expenses[0].id
        response = client.get(f"/expenses/{expense_id}")
        
        assert response.status_code == 401
    
    def test_update_expense_success(self, client: TestClient, auth_headers, test_expenses):
        """Test successful expense update."""
        expense_id = test_expenses[0].id
        update_data = {
            "title": "Updated Title",
            "amount": 200.00
        }
        
        response = client.put(f"/expenses/{expense_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == expense_id
        assert data["title"] == update_data["title"]
        assert data["amount"] == update_data["amount"]
    
    def test_update_expense_not_found(self, client: TestClient, auth_headers):
        """Test updating non-existent expense."""
        update_data = {"title": "Updated Title"}
        response = client.put("/expenses/99999", json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
        assert "Expense not found" in response.json()["detail"]
    
    def test_update_expense_unauthorized(self, client: TestClient, test_expenses):
        """Test updating expense without authorization fails."""
        expense_id = test_expenses[0].id
        update_data = {"title": "Updated Title"}
        response = client.put(f"/expenses/{expense_id}", json=update_data)
        
        assert response.status_code == 401
    
    def test_delete_expense_success(self, client: TestClient, auth_headers, test_expenses):
        """Test successful expense deletion."""
        expense_id = test_expenses[0].id
        response = client.delete(f"/expenses/{expense_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert "Expense deleted successfully" in response.json()["message"]
        
        # Verify expense is deleted
        get_response = client.get(f"/expenses/{expense_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_expense_not_found(self, client: TestClient, auth_headers):
        """Test deleting non-existent expense."""
        response = client.delete("/expenses/99999", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Expense not found" in response.json()["detail"]
    
    def test_delete_expense_unauthorized(self, client: TestClient, test_expenses):
        """Test deleting expense without authorization fails."""
        expense_id = test_expenses[0].id
        response = client.delete(f"/expenses/{expense_id}")
        
        assert response.status_code == 401
    
    def test_get_categories_success(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expense categories."""
        response = client.get("/expenses/categories/list", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "Food" in data
        assert "Transport" in data
        assert "Entertainment" in data
    
    def test_get_categories_unauthorized(self, client: TestClient):
        """Test getting categories without authorization fails."""
        response = client.get("/expenses/categories/list")
        
        assert response.status_code == 401
    
    def test_get_monthly_summary_success(self, client: TestClient, auth_headers, test_expenses):
        """Test getting monthly expense summary."""
        response = client.get("/expenses/summary/monthly?year=2024", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 12  # 12 months
        
        # Check structure of monthly data
        for month_data in data:
            assert "month" in month_data
            assert "total" in month_data
            assert isinstance(month_data["month"], int)
            assert isinstance(month_data["total"], (int, float))
    
    def test_get_monthly_summary_unauthorized(self, client: TestClient):
        """Test getting monthly summary without authorization fails."""
        response = client.get("/expenses/summary/monthly?year=2024")
        
        assert response.status_code == 401
    
    def test_get_expense_statistics_success(self, client: TestClient, auth_headers, test_expenses):
        """Test getting expense statistics."""
        response = client.get("/expenses/statistics", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_expenses" in data
        assert "total_amount" in data
        assert "average_amount" in data
        assert "most_expensive_category" in data
        assert "unique_categories" in data
        
        assert data["total_expenses"] == len(test_expenses)
        assert data["unique_categories"] == 3  # Food, Transport, Entertainment
    
    def test_get_expense_statistics_unauthorized(self, client: TestClient):
        """Test getting expense statistics without authorization fails."""
        response = client.get("/expenses/statistics")
        
        assert response.status_code == 401
    
    def test_get_expenses_date_filter(self, client: TestClient, auth_headers, test_expenses):
        """Test filtering expenses by date."""
        response = client.get("/expenses/?month=1&year=2024", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(test_expenses)  # All test expenses are from January 2024
    
    def test_user_isolation(self, client: TestClient, db_session):
        """Test that users can only access their own expenses."""
        # Create another user
        from app.models import User
        from app.auth import get_password_hash
        
        other_user = User(
            username="otheruser",
            email="other@example.com",
            hashed_password=get_password_hash("password")
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Get token for other user
        from jose import jwt
        from app.auth import SECRET_KEY, ALGORITHM
        
        other_token = jwt.encode(
            data={"sub": other_user.username},
            secret=SECRET_KEY,
            algorithm=ALGORITHM
        )
        other_headers = {"Authorization": f"Bearer {other_token}"}
        
        # Other user should not see test_user's expenses
        response = client.get("/expenses/", headers=other_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # No expenses for other user
