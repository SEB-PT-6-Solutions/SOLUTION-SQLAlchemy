# models/tea.py

from sqlalchemy import Column, Integer, String, Boolean
from .base import BaseModel
from sqlalchemy.orm import relationship

class TeaModel(BaseModel):

    # This will be used directly to make a
    # TABLE in Postgresql
    __tablename__ = "teas"

    id = Column(Integer, primary_key=True, index=True)

    # Specific columns for our Tea Table.
    name = Column(String, unique=True)
    in_stock = Column(Boolean)
    rating = Column(Integer)

    comments = relationship('CommentModel', back_populates="tea")