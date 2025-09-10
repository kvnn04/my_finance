from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from core.base import Base

class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rate_limit_window: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    requests_per_window: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    users: Mapped[list["User"]] = relationship("User", back_populates="plan")  # type: ignore # string reference
