from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from database import create_database
from routers.expense_router import expense_router
from routers.category_router import category_router


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]


create_database()

app = FastAPI()
app.include_router(expense_router, prefix='/expenses')
app.include_router(category_router, prefix='/categories')
