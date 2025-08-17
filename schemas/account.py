from pydantic import BaseModel

# Input para crear una cuenta
class AccountCreate(BaseModel):
    name: str

# Input para actualizar una cuenta
class AccountUpdate(BaseModel):
    name: str | None = None  # opcional

# Output de la cuenta
class AccountOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # reemplaza orm_mode en Pydantic v2
