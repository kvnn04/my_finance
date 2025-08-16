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

class Me(BaseModel):
    username: str
    password: str
    
class MeOutput(BaseModel):
    username: str
    password: str
    