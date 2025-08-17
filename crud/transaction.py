from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models.account import Account
from db.models.category import Category
from db.models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut

# Crear transacción
def create_transaction(db: Session, transaction_data: TransactionCreate, user_id: int) -> TransactionOut:
    # Verificar que la cuenta pertenece al usuario
    stmt = select(Account).where(Account.id == transaction_data.account_id, Account.user_id == user_id)
    account = db.execute(stmt).scalars().first()
    if not account:
        raise Exception("Cuenta no encontrada o no pertenece al usuario")

    transaction = Transaction(
        account_id=transaction_data.account_id,
        category_id=transaction_data.category_id,
        amount=transaction_data.amount
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return TransactionOut(
        id=transaction.id, # type: ignore
        account_id=transaction.account_id, # type: ignore
        account_name=transaction.account.name,
        category_id=transaction.category_id, # type: ignore
        category_name=transaction.category.name if transaction.category else None,
        amount=transaction.amount, # type: ignore
        created_at=transaction.created_at # type: ignore
    )


# Listar transacciones por cuenta
def get_transactions_by_account(db: Session, account_id: int, user_id: int) -> list[TransactionOut]:
    stmt = select(Transaction).join(Account).outerjoin(Category).where(
        Transaction.account_id == account_id,
        Account.user_id == user_id
    )
    transactions = db.execute(stmt).scalars().all()

    result = []
    for t in transactions:
        result.append(TransactionOut(
            id=t.id, # type: ignore
            account_id=t.account_id, # type: ignore
            account_name=t.account.name,
            category_id=t.category_id, # type: ignore
            category_name=t.category.name if t.category else None,
            amount=t.amount, # type: ignore
            created_at=t.created_at # type: ignore
        ))
    return result


# Obtener transacción por id
def get_transaction(db: Session, transaction_id: int, user_id: int) -> TransactionOut | None:
    stmt = (
        select(Transaction)
        .join(Account)
        .outerjoin(Category)
        .where(Transaction.id == transaction_id, Account.user_id == user_id)
    )

    transaction = db.execute(stmt).scalars().first()
    if not transaction:
        return None

    return TransactionOut(
        id=transaction.id, # type: ignore
        account_id=transaction.account_id, # type: ignore
        account_name=transaction.account.name,
        category_id=transaction.category_id, # type: ignore
        category_name=transaction.category.name if transaction.category else None,
        amount=transaction.amount, # type: ignore
        created_at=transaction.created_at # type: ignore
    )


# Actualizar transacción
def update_transaction(db: Session, transaction_id: int, transaction_data: TransactionUpdate, user_id: int) -> TransactionOut | None:
    stmt = (
        select(Transaction)
        .join(Account)
        .where(Transaction.id == transaction_id, Account.user_id == user_id)
    )

    transaction = db.execute(stmt).scalars().first()
    if not transaction:
        return None

    if transaction_data.amount is not None:
        transaction.amount = transaction_data.amount # type: ignore
    if transaction_data.category_id is not None:
        transaction.category_id = transaction_data.category_id # type: ignore

    db.commit()
    db.refresh(transaction)

    return TransactionOut(
        id=transaction.id, # type: ignore
        account_id=transaction.account_id, # type: ignore
        account_name=transaction.account.name,
        category_id=transaction.category_id, # type: ignore
        category_name=transaction.category.name if transaction.category else None,
        amount=transaction.amount, # type: ignore
        created_at=transaction.created_at # type: ignore
    )


# Eliminar transacción
def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    stmt = (
        select(Transaction)
        .join(Account)
        .where(Transaction.id == transaction_id, Account.user_id == user_id)
    )

    transaction = db.execute(stmt).scalars().first()
    if not transaction:
        return False

    db.delete(transaction)
    db.commit()
    return True
