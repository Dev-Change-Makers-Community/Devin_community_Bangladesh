"""Simple test to verify basic functionality without complex dependencies."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that we can import our modules."""
    try:
        from app.utils.exceptions import ExpenseNotFoundException, UserAlreadyExistsException, InvalidCredentialsException
        print("✓ Successfully imported exceptions")
        
        from app.services.expense_service import ExpenseService
        print("✓ Successfully imported ExpenseService")
        
        from app.services.user_service import UserService
        print("✓ Successfully imported UserService")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_exception_creation():
    """Test that exceptions can be created properly."""
    try:
        from app.utils.exceptions import ExpenseNotFoundException, UserAlreadyExistsException, InvalidCredentialsException
        
        # Test ExpenseNotFoundException
        expense_exception = ExpenseNotFoundException()
        assert expense_exception.status_code == 404
        assert expense_exception.detail == "Expense not found"
        print("✓ ExpenseNotFoundException works correctly")
        
        # Test UserAlreadyExistsException
        email_exception = UserAlreadyExistsException("email")
        assert email_exception.status_code == 400
        assert email_exception.detail == "Email already registered"
        print("✓ UserAlreadyExistsException (email) works correctly")
        
        username_exception = UserAlreadyExistsException("username")
        assert username_exception.status_code == 400
        assert username_exception.detail == "Username already taken"
        print("✓ UserAlreadyExistsException (username) works correctly")
        
        # Test InvalidCredentialsException
        auth_exception = InvalidCredentialsException()
        assert auth_exception.status_code == 401
        assert auth_exception.detail == "Incorrect username or password"
        print("✓ InvalidCredentialsException works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Exception test failed: {e}")
        return False

def test_service_methods_exist():
    """Test that service methods exist."""
    try:
        from app.services.expense_service import ExpenseService
        from app.services.user_service import UserService
        
        # Check ExpenseService methods
        expense_methods = [
            'create_expense',
            'get_expenses', 
            'get_expense_by_id',
            'update_expense',
            'delete_expense',
            'get_categories',
            'get_monthly_summary',
            'get_expense_statistics'
        ]
        
        for method in expense_methods:
            assert hasattr(ExpenseService, method), f"ExpenseService missing method: {method}"
        print("✓ All ExpenseService methods exist")
        
        # Check UserService methods
        user_methods = [
            'create_user',
            'get_user_by_email',
            'get_user_by_username'
        ]
        
        for method in user_methods:
            assert hasattr(UserService, method), f"UserService missing method: {method}"
        print("✓ All UserService methods exist")
        
        return True
    except Exception as e:
        print(f"✗ Service methods test failed: {e}")
        return False

def test_route_files_exist():
    """Test that route files exist and have expected content."""
    try:
        import os
        
        # Check files exist
        route_files = [
            'app/routes/auth.py',
            'app/routes/expenses.py'
        ]
        
        for file_path in route_files:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            assert os.path.exists(full_path), f"Route file missing: {file_path}"
        print("✓ All route files exist")
        
        # Check route files have expected content
        with open(os.path.join(os.path.dirname(__file__), 'app/routes/auth.py'), 'r') as f:
            auth_content = f.read()
            assert 'def register' in auth_content, "auth.py missing register function"
            assert 'def login' in auth_content, "auth.py missing login function"
        print("✓ auth.py has expected functions")
        
        with open(os.path.join(os.path.dirname(__file__), 'app/routes/expenses.py'), 'r') as f:
            expenses_content = f.read()
            assert 'def create_expense' in expenses_content, "expenses.py missing create_expense function"
            assert 'def get_expenses' in expenses_content, "expenses.py missing get_expenses function"
            assert 'def update_expense' in expenses_content, "expenses.py missing update_expense function"
            assert 'def delete_expense' in expenses_content, "expenses.py missing delete_expense function"
        print("✓ expenses.py has expected functions")
        
        return True
    except Exception as e:
        print(f"✗ Route files test failed: {e}")
        return False

def main():
    """Run all simple tests."""
    print("Running simple backend tests...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_exception_creation,
        test_service_methods_exist,
        test_route_files_exist
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
            print(f"✓ {test.__name__} PASSED")
        else:
            print(f"✗ {test.__name__} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
