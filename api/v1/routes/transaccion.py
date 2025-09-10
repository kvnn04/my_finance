from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1.dependencies.rate_limit_dependency import rate_limit_dependency
from crud.transaction import (
    create_transaction,
    get_transaction,
    get_transactions_by_account,
    update_transaction,
    delete_transaction
)
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut
from core.dependencies import get_db
from api.v1.routes.auth import get_current_user
from schemas.user import Me


# --- Router con rate limit aplicado a todas las rutas ---
router = APIRouter(
    dependencies=[Depends(rate_limit_dependency)]
)

@router.post("/", response_model=TransactionOut)
def transaction_create(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    return create_transaction(db, transaction_data, current_user.id)

@router.get("/accounts/{account_id}", response_model=list[TransactionOut])
def transactions_list(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    return get_transactions_by_account(db, account_id, current_user.id)

@router.get("/{id}", response_model=TransactionOut)
def transaction_get(
    id: int,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    transaction = get_transaction(db, id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.put("/{id}", response_model=TransactionOut)
def transaction_update(
    id: int,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    transaction = update_transaction(db, id, transaction_data, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.delete("/{id}")
def transaction_delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    success = delete_transaction(db, id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return {"message": f"Transacción {id} eliminada correctamente"}
