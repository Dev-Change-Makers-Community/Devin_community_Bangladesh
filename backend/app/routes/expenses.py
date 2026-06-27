from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Expense, User
from ..schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..auth import get_current_user
from ..services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new expense for the current user."""
    return ExpenseService.create_expense(db, expense, current_user.id)

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get expenses for the current user with optional filtering."""
    return ExpenseService.get_expenses(
        db, current_user.id, skip, limit, category, month, year
    )

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific expense by ID."""
    return ExpenseService.get_expense_by_id(db, expense_id, current_user.id)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing expense."""
    return ExpenseService.update_expense(db, expense_id, expense_update, current_user.id)

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an expense."""
    return ExpenseService.delete_expense(db, expense_id, current_user.id)

@router.get("/categories/list")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all unique categories for the current user's expenses."""
    return ExpenseService.get_categories(db, current_user.id)

@router.get("/summary/monthly")
def get_monthly_summary(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get monthly expense summary for a given year."""
    return ExpenseService.get_monthly_summary(db, current_user.id, year)

@router.get("/statistics")
def get_expense_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get expense statistics for the current user."""
    return ExpenseService.get_expense_statistics(db, current_user.id)

