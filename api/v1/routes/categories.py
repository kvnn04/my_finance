from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1.routes.auth import get_current_user
from core.dependencies import get_db
from crud.category import (
    create_category,
    delete_category,
    get_categories,
    get_category_by_id,
    update_category
)
from schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from schemas.user import Me
from api.v1.dependencies.rate_limit_dependency import rate_limit_dependency

# --- Router con rate limit aplicado a todas las rutas ---
router = APIRouter(
    dependencies=[Depends(rate_limit_dependency)]
)

# Obtener todas las categorías
@router.get("/", response_model=List[CategoryOut])
def categories_get(
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    return get_categories(db, current_user.id)

# Crear categoría
@router.post("/", response_model=CategoryOut)
def categories_post(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    return create_category(db, category_data, current_user.id)

# Ver detalles de categoría
@router.get("/{id}", response_model=CategoryOut)
def categories_id_get(
    id: int,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    category = get_category_by_id(db, id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

# Actualizar categoría
@router.put("/{id}", response_model=CategoryOut)
def categories_id_put(
    id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    category = update_category(db, id, category_data, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o no autorizada")
    return category

# Eliminar categoría
@router.delete("/{id}")
def categories_id_delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Me = Depends(get_current_user)
):
    category = delete_category(db, id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o no autorizada")
    return {"message": f"Categoría {category.name} eliminada correctamente"}
