from pydantic import BaseModel
from typing import Optional

# Schema para crear categoría
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Schema para actualizar categoría
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    

# Schema de salida
class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
