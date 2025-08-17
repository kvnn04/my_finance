from typing import Optional
from sqlalchemy import exists, select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas.user import Me
from db.models.user import User
from core.auth import decode_access_token, hash_password

# 🔹 Funciones para obtener usuarios

def get_user_by_id(db: Session, user_id: int):
    """Devuelve un usuario por id"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Devuelve un usuario por email, o None si no existe"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Devuelve un usuario por username, o None si no existe"""
    return db.query(User).filter(User.username == username).first()

def get_user_for_login(db: Session, username: str):
    """Devuelve los datos necesarios para login: id, hashed_password y username"""
    stmt = select(User.id, User.hashed_password, User.username).where(User.username == username)
    return db.execute(stmt).first()

def get_user_for_me(db: Session, username: str) -> Optional[User]:
    """Devuelve el usuario completo a partir del username"""
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()

# 🔹 Funciones para verificar existencia

def username_exists(db: Session, username: str) -> bool:
    """Devuelve True si el username ya existe"""
    return db.query(exists().where(User.username == username)).scalar()

def email_exists(db: Session, email: str) -> bool:
    """Devuelve True si el email ya existe"""
    return db.query(exists().where(User.email == email)).scalar()

# 🔹 Crear usuario

def create_user(db: Session, username: str, email: str, password: str) -> User:
    """Crea un nuevo usuario con contraseña hasheada y lo retorna"""
    hashed = hash_password(password)  # ahora usa Argon2
    user = User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
