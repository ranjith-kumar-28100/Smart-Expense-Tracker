import uuid
from database import Base
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    threshold = Column(Float, nullable=True)
    is_good = Column(Boolean, default=False, nullable=False)
    expenses = relationship('Expense', back_populates='category')

    def __init__(self, name, description, threshold, is_good):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.threshold = threshold
        self.is_good = is_good
