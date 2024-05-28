from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from models.expense import Expense
from models.category import Category
from pydantic import BaseModel, Field
expense_router = APIRouter(tags=["Expense"])


class ExpenseDTO(BaseModel):
    name: str
    amount: float = Field(gt=0)
    description: Optional[str] = Field(default=None)
    category_id: str


@expense_router.get('/')
async def get_expenses(session: Session = Depends(get_db)):
    expenses = session.execute(select(Expense)).all()
    expenses_list = []
    print(expenses)
    for expense in expenses:
        expense = expense[0]
        category = session.execute(select(Category.name).where(
            Category.id == expense.category_id)).first()
        expense_dict = {'id': expense.id, 'name': expense.name, 'description': expense.description,
                        'amount': expense.amount, 'date': expense.date, 'time': expense.time, 'category': category[0]}
        expenses_list.append(expense_dict)
    return {'expenses': expenses_list}


@expense_router.get('/{expense_id}')
async def get_expense(expense_id: str, session: Session = Depends(get_db)):
    expense = session.execute(select(Expense).where(
        Expense.id == expense_id)).first()
    if not expense:
        raise HTTPException(status_code=404, detail='Expense not found')
    category = session.execute(select(Category.name).where(
        Category.id == expense[0].category_id)).first()
    expense = {'id': expense[0].id, 'name': expense[0].name, 'description': expense[0].description,
               'amount': expense[0].amount, 'date': expense[0].date, 'time': expense[0].time, 'category': category[0]}
    return {'expense': expense}


@expense_router.post("/")
async def add_expense(expense: ExpenseDTO, session: Session = Depends(get_db)):
    category = session.execute(select(Category).where(
        Category.id == expense.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_expense = Expense(expense.name, expense.amount,
                         expense.description, expense.category_id)
    session.add(db_expense)
    session.commit()
    return {'Status': f'Expense created sucessfully with id {db_expense.id}'}


@expense_router.put('/{expense_id}')
def update_expense(expense_id: str, expense: ExpenseDTO, session: Session = Depends(get_db)):
    category = session.execute(select(Category).where(
        Category.id == expense.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    result = session.execute(update(Expense).where(Expense.id == expense_id).values(
        {"name": expense.name, "description": expense.description, "amount": expense.amount, "category_id": expense.category_id}))
    if result.rowcount == 1:
        session.commit()
        return {'Status': 'Expense updated sucessfully'}
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


@expense_router.delete('/{expense_id}')
def remove_expense(expense_id: str, session: Session = Depends(get_db)):
    result = session.execute(delete(Expense).where(Expense.id == expense_id))
    if result.rowcount == 1:
        session.commit()
        return {'Status': 'Expense removed sucessfully'}
    else:
        raise HTTPException(status_code=404, detail="Expense not found")
