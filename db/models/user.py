from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from core.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("plans.id"), nullable=False, default=1)
    plan: Mapped["Plan"] = relationship("Plan", back_populates="users")  # type: ignore # string reference

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user", cascade="all, delete-orphan") # type: ignore
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="user", cascade="all, delete-orphan") # type: ignore
