from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import Me, MeOutput, RegisterOutput, RegisterInput, SignInInput, SignInOutput

router = APIRouter()

from fastapi import APIRouter, HTTPException
from crud.user import create_user, email_exists, get_user_by_email, get_user_by_username, get_user_for_login, username_exists, verify_password
from core.session import get_db

router = APIRouter()

@router.post("/register", response_model=RegisterOutput)
def register(user: RegisterInput, db: Session = Depends(get_db)):
    if username_exists(db, user.username):
        raise HTTPException(status_code=400, detail="Username ya existe")
    
    if email_exists(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = create_user(db, username=user.username, email=user.email, password=user.password)
    return RegisterOutput(id=new_user.id, username=new_user.username, email=new_user.email) # type: ignore


@router.post("/sign-in", response_model=SignInOutput)
def sign_in(credentials: SignInInput, db: Session = Depends(get_db)):
    user = get_user_for_login(db, credentials.username)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return SignInOutput(message=f"Inicio de sesión exitoso para {user.username}")

@router.post("/me", response_model=MeOutput)
def me(credentias: Me, db: Session = Depends(get_db)):
    user = get_user_for_login(db=db, username=credentias.username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": user.id, "email": user.email}