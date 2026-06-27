"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_user_success(self, client: TestClient):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "created_at" in data
        assert "hashed_password" not in data
    
    def test_register_user_duplicate_email(self, client: TestClient, test_user):
        """Test registration with duplicate email fails."""
        user_data = {
            "username": "differentuser",
            "email": test_user.email,  # Same email as test_user
            "password": "password123"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_user_duplicate_username(self, client: TestClient, test_user):
        """Test registration with duplicate username fails."""
        user_data = {
            "username": test_user.username,  # Same username as test_user
            "email": "different@example.com",
            "password": "password123"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    def test_register_user_invalid_data(self, client: TestClient):
        """Test registration with invalid data fails."""
        # Missing required fields
        user_data = {
            "username": "testuser"
            # Missing email and password
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_login_success(self, client: TestClient, test_user):
        """Test successful user login."""
        login_data = {
            "username": test_user.username,
            "password": "testpassword"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self, client: TestClient):
        """Test login with invalid username fails."""
        login_data = {
            "username": "nonexistentuser",
            "password": "somepassword"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client: TestClient, test_user):
        """Test login with invalid password fails."""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_missing_credentials(self, client: TestClient):
        """Test login without credentials fails."""
        response = client.post("/auth/login", data={})
        
        assert response.status_code == 422  # Validation error
    
    def test_protected_endpoint_without_token(self, client: TestClient):
        """Test accessing protected endpoint without token fails."""
        response = client.get("/expenses/")
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token fails."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/expenses/", headers=headers)
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token(self, client: TestClient, auth_headers):
        """Test accessing protected endpoint with valid token succeeds."""
        response = client.get("/expenses/", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
