from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)


    # 🔗 Relación con User (cada categoría pertenece a un usuario)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación 1:N con Transaction
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")

    # Relación inversa con User
    user = relationship("User", back_populates="categories")