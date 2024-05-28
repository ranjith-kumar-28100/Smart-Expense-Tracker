import uuid
from datetime import datetime
from database import Base
from sqlalchemy import Column, String, Float, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    time = Column(Time,  nullable=False)
    category_id = Column(String, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="expenses")

    def __init__(self, name, amount, description, category_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.amount = amount
        self.description = description
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.category_id = category_id
