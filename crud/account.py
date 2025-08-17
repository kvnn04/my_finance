from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models.account import Account
from schemas.account import AccountCreate, AccountUpdate

# Obtener todas las cuentas de un usuario
def get_accounts_by_user(db: Session, user_id: int) -> list[Account]:
    stmt = select(Account).where(Account.user_id == user_id)
    return list(db.execute(stmt).scalars().all())

# Obtener cuenta por ID
def get_account_by_id(db: Session, account_id: int, user_id: int) -> Optional[Account]:
    stmt = select(Account).where(Account.id == account_id, Account.user_id == user_id)
    return db.execute(stmt).scalars().first()

# Crear cuenta
def create_account(db: Session, account_data: AccountCreate, user_id: int) -> Account:
    account = Account(
        name=account_data.name,
        user_id=user_id
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

# Actualizar cuenta
def update_account(db: Session, account_id: int, account_data: AccountUpdate, user_id: int) -> Optional[Account]:
    account = get_account_by_id(db, account_id, user_id)
    if not account:
        return None
    if account_data.name is not None:
        account.name = account_data.name  # type: ignore
    db.commit()
    db.refresh(account)
    return account

# Eliminar cuenta
def delete_account(db: Session, account_id: int, user_id: int) -> Optional[Account]:
    account = get_account_by_id(db, account_id, user_id)
    if not account:
        return None
    db.delete(account)
    db.commit()
    return account
