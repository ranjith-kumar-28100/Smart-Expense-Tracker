from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from database import get_db
from models.category import Category
from pydantic import BaseModel, Field

category_router = APIRouter(tags=["Category"])


class CategoryDTO(BaseModel):
    name: str
    description: Optional[str] = None
    threshold: float = Field(ge=0, default=0)
    is_good: bool = Field(default=False)


@category_router.get('/')
async def get_categories(session: Session = Depends(get_db)):
    categories = session.execute(select(Category)).all()
    categories_list = []
    for category in categories:
        category = category[0]
        category_dict = {'id': category.id, 'name': category.name,
                         'description': category.description, 'threshold': category.threshold, 'is_good': category.is_good}
        categories_list.append(category_dict)
    return {'categories': categories_list}


@category_router.get('/{category_id}')
async def get_category(category_id: str, session: Session = Depends(get_db)):
    category = session.execute(select(Category).where(
        Category.id == category_id)).one()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    category = {'id': category[0].id, 'name': category[0].name,
                'description': category[0].description, 'threshold': category[0].threshold, 'is_good': category[0].is_good}
    return {'category': category}


@category_router.post("/")
async def add_expense(category: CategoryDTO, session: Session = Depends(get_db)):
    db_category = Category(category.name, category.description,
                           category.threshold, category.is_good)
    session.add(db_category)
    session.commit()
    return {'Status': f'Category created sucessfully with id {db_category.id}'}


@category_router.put('/{category_id}')
def update_expense(category_id: str, category: CategoryDTO, session: Session = Depends(get_db)):
    result = session.execute(update(Category).where(Category.id == category_id).values(
        {"name": category.name, "description": category.description, "threshold": category.threshold, "is_good": category.is_good}))
    if result.rowcount == 1:
        session.commit()
        return {'Status': 'Category updated sucessfully'}
    else:
        raise HTTPException(status_code=404, detail="Category not found")
