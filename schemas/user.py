from typing import Optional
from pydantic import BaseModel, EmailStr

# Input del register
class RegisterInput(BaseModel):
    username: str
    email: EmailStr
    password: str

# Output del register
class RegisterOutput(BaseModel):
    id: int
    username: str
    email: EmailStr

# Input del login
class SignInInput(BaseModel):
    username: str
    password: str

# Output del login
class SignInOutput(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

class Me(BaseModel):
    id: int
    username: str
    email:str
    
class MeOutputUpdate(BaseModel):
    id: int
    username: str
    email: str
    
class MeOutput(BaseModel):
    id: int
    username: str
    email: str
    plan: str
    
class UserUpdateInput(BaseModel):
    username: Optional[str]
    email: Optional[str]