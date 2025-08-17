from typing import Optional
from sqlalchemy import exists, select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas.user import Me
from db.models.user import User
from core.auth import decode_access_token, hash_password

# 🔹 Funciones para obtener usuarios
# 🔹 Funciones para obtener usuarios

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Devuelve un usuario por id"""
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalars().first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Devuelve un usuario por email, o None si no existe"""
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Devuelve un usuario por username, o None si no existe"""
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()


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
    stmt = select(exists().where(User.username == username))
    return bool(db.execute(stmt).scalar())


def email_exists(db: Session, email: str) -> bool:
    """Devuelve True si el email ya existe"""
    stmt = select(exists().where(User.email == email))
    return bool(db.execute(stmt).scalar())
# 🔹 Crear usuario

def create_user(db: Session, username: str, email: str, password: str) -> User:
    """Crea un nuevo usuario con contraseña hasheada y lo retorna"""
    hashed = hash_password(password)  # ahora usa Argon2
    user = User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
