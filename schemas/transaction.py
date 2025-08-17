from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    account_id: int
    category_id: Optional[int]
    amount: float

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    category_id: Optional[int]
    amount: Optional[float]

class TransactionOut(BaseModel):
    id: int
    account_id: int
    account_name: str      # nombre de la cuenta
    category_id: Optional[int]
    category_name: Optional[str]  # nombre de la categoría
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True  # versión nueva de orm_mode
