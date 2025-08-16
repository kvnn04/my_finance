from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)

    # Relación N:1 con User
    user = relationship("User", back_populates="accounts")

    # Relación 1:N con Transaction
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
