from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1.routes.auth import get_current_user
from core.dependencies import get_db
from schemas.user import Me, MeOutput, UserUpdateInput
from crud import user as crud_user

router = APIRouter()

# --- Actualizar datos de usuario ---
@router.put("/{id}", response_model=MeOutput)
def user_edit_me(
    id: int,
    updated_data: UserUpdateInput,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar este usuario")
    
    user = crud_user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos solo si vienen en updated_data
    if updated_data.username:
        user.username = updated_data.username # type: ignore
    if updated_data.email:
        user.email = updated_data.email # type: ignore
    
    db.commit()
    db.refresh(user)
    return MeOutput(id=user.id, username=user.username, email=user.email) # type: ignore

# --- Obtener datos del usuario ---
@router.get("/{id}", response_model=MeOutput)
def user_get_me(
    id: int,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para ver este usuario")
    
    user = crud_user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return MeOutput(id=user.id, username=user.username, email=user.email) # type: ignore

# --- Eliminar usuario ---
@router.delete("/{id}")
def user_delete_me(
    id: int,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este usuario")
    
    user = crud_user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"Usuario {user.username} eliminado correctamente"}
