from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.routes.auth import get_current_user
from crud.account import get_accounts_by_user, get_account_by_id, create_account, update_account, delete_account
from schemas.account import AccountCreate, AccountUpdate, AccountOut
from core.dependencies import get_db
from schemas.user import Me

router = APIRouter()

# Obtener todas las cuentas del usuario
@router.get("/", response_model=list[AccountOut])
def accounts_get_all(
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_accounts_by_user(db, current_user.id)

# Obtener cuenta por id
@router.get("/{id}", response_model=AccountOut)
def accounts_get(
    id: int,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = get_account_by_id(db, id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return account

# Crear cuenta
@router.post("/", response_model=AccountOut)
def accounts_post(
    account_data: AccountCreate,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_account(db, account_data, current_user.id)

# Actualizar cuenta
@router.put("/{id}", response_model=AccountOut)
def accounts_put(
    id: int,
    account_data: AccountUpdate,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = update_account(db, id, account_data, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada o no autorizada")
    return account

# Eliminar cuenta
@router.delete("/{id}")
def accounts_delete(
    id: int,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = delete_account(db, id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada o no autorizada")
    return {"message": f"Cuenta {id} eliminada correctamente"}
