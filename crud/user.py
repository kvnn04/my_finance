from sqlalchemy import exists, select
from db.models.user import User
from core.session import SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# 🔹 Cambiamos bcrypt por argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 🔹 Funciones de hash y verificación
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 🔹 Funciones para obtener usuarios
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_for_login(db: Session, username: str):
    stmt = select(User.id, User.hashed_password, User.username).where(User.username == username)
    return db.execute(stmt).first()

# 🔹 Funciones para verificar existencia
def username_exists(db: Session, username: str) -> bool:
    return db.query(exists().where(User.username == username)).scalar()

def email_exists(db: Session, email: str) -> bool:
    return db.query(exists().where(User.email == email)).scalar()

# 🔹 Crear usuario
def create_user(db: Session, username: str, email: str, password: str):
    hashed = hash_password(password)  # ahora usa Argon2
    user = User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
