# from fastapi import APIRouter, Depends
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from schemas.user import Me, MeOutput, RegisterOutput, RegisterInput, SignInInput, SignInOutput
# from fastapi import APIRouter, HTTPException
# from crud.user import create_user, email_exists, get_user_by_email, get_user_by_username, get_user_for_login, get_user_for_me, username_exists
# from core.auth import create_access_token, decode_access_token, verify_password
# from core.session import get_db
# from fastapi import status

# router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/sign-in")

# # Función para obtener el usuario actual desde el token
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Me:
#     payload = decode_access_token(token)
#     username: Optional[str] = payload.get("sub") # type: ignore
#     if username is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token inválido",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     user = get_user_for_me(db=db, username=username)
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
#     return Me(username=user.username)

# @router.post("/register", response_model=RegisterOutput)
# def register(user: RegisterInput, db: Session = Depends(get_db)):
#     if username_exists(db, user.username):
#         raise HTTPException(status_code=400, detail="Username ya existe")
    
#     if email_exists(db, user.email):
#         raise HTTPException(status_code=400, detail="Email ya registrado")
    
#     new_user = create_user(db, username=user.username, email=user.email, password=user.password)
#     return RegisterOutput(id=new_user.id, username=new_user.username, email=new_user.email) # type: ignore


# # @router.post("/sign-in", response_model=SignInOutput)
# # def sign_in(credentials: SignInInput, db: Session = Depends(get_db)):
# #     user = get_user_for_login(db, credentials.username)

# #     if not user or not verify_password(credentials.password, user.hashed_password):
# #         raise HTTPException(status_code=401, detail="Credenciales inválidas")
# #     return SignInOutput(message=f"Inicio de sesión exitoso para {user.username}")

# # @router.post("/sign-in", response_model=SignInOutput)
# # def sign_in(credentials: SignInInput, db: Session = Depends(get_db)):
# #     user = get_user_for_login(db, credentials.username)

# #     if not user or not verify_password(credentials.password, user.hashed_password):
# #         raise HTTPException(status_code=401, detail="Credenciales inválidas")

# #     # Emitir JWT
# #     access_token = create_access_token(data={"sub": user.username})

# #     return SignInOutput(
# #         message=f"Inicio de sesión exitoso para {user.username}",
# #         access_token=access_token,
# #         token_type="bearer"
# #     )

# # @router.post("/me", response_model=MeOutput)
# # def me(credentials: Me, db: Session = Depends(get_db)):
# #     user = get_user_for_me(db=db, username=credentials.username)
# #     if not user:
# #         raise HTTPException(status_code=404, detail="Usuario no encontrado")
# #     # Opcional: validar contraseña con verify_password(credentials.password, user.hashed_password)

# #     return MeOutput(username=user.username, email=user.email) # type: ignore

# @router.post("/sign-in", response_model=SignInOutput)
# def sign_in(credentials: SignInInput, db: Session = Depends(get_db)):
#     print(credentials)
#     user = get_user_for_login(db, credentials.username)

#     if not user or not verify_password(credentials.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Credenciales inválidas")

#     access_token = create_access_token(data={"sub": user.username})

#     return SignInOutput(
#         message=f"Inicio de sesión exitoso para {user.username}",
#         access_token=access_token,
#         token_type="bearer"
#     )

# @router.get("/me", response_model=MeOutput)
# def me(current_user: Me = Depends(get_current_user)):
#     return MeOutput(username=current_user.username)


from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import Me, MeOutput, RegisterOutput, RegisterInput, SignInInput, SignInOutput
from crud.user import (
    create_user,
    email_exists,
    get_user_for_login,
    get_user_for_me,
    username_exists,
)
from core.auth import create_access_token, decode_access_token
from core.session import get_db
from core.auth import verify_password
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/sign-in")

# --- Dependencia para obtener el usuario actual desde el token ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Me:
    payload = decode_access_token(token)
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_for_me(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return Me(id=user.id, username=user.username, email=user.email)


# --- Registro de usuarios ---
@router.post("/register", response_model=RegisterOutput)
def register(user: RegisterInput, db: Session = Depends(get_db)):
    if username_exists(db, user.username):
        raise HTTPException(status_code=400, detail="Username ya existe")
    if email_exists(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = create_user(db, username=user.username, email=user.email, password=user.password)
    return RegisterOutput(id=new_user.id, username=new_user.username, email=new_user.email)

@router.post("/sign-in", response_model=SignInOutput)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_for_login(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": user.username})
    return SignInOutput(
        message=f"Inicio de sesión exitoso para {user.username}",
        access_token=access_token,
        token_type="bearer"
    )
# --- Ruta protegida ---
@router.get("/me", response_model=MeOutput)
def me(current_user: Me = Depends(get_current_user)):
    return MeOutput(id=current_user.id, username=current_user.username, email=current_user.email)
