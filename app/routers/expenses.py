from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date

from app.db.database import get_db
from app.models.expense import Expense
from app.models.user import User

from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse, ExpenseUpdate

from app.core.dependencies import get_current_user


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
        user_id=current_user.id,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(Expense).filter(Expense.user_id == current_user.id)

    if category:
        query = query.filter(Expense.category == category)

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    expenses = query.offset(offset).limit(limit).all()

    return expenses


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if expense_update.amount is not None:
        expense.amount = expense_update.amount

    if expense_update.category is not None:
        expense.category = expense_update.category

    if expense_update.description is not None:
        expense.description = expense_update.description

    if expense_update.date is not None:
        expense.date = expense_update.date

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this expense"
        )

    db.delete(expense)
    db.commit()


@router.get("/monthly-summary")
def monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    result = (
        db.query(
            func.to_char(Expense.date, "YYYY-MM").label("month"),
            func.sum(Expense.amount).label("total_spent"),
        )
        .filter(Expense.user_id == current_user.id)
        .group_by(func.to_char(Expense.date, "YYYY-MM"))
        .order_by(func.to_char(Expense.date, "YYYY-MM"))
        .all()
    )

    return [{"month": row.month, "total_spent": row.total_spent} for row in result]

@router.get("/category-summary")
def category_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    result = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("total_spent")
        )
        .filter(Expense.user_id == current_user.id)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return {
        row.category: row.total_spent
        for row in result
    }