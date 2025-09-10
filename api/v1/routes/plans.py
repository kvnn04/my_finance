from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db
from api.v1.routes.auth import get_current_user
from schemas.plans import PlanInput, PlanOutput
from crud import plans as crud_plans
from schemas.user import Me
from api.v1.dependencies.rate_limit_dependency import rate_limit_dependency

class Admin(Enum):
    ADMIN = 'admin'

# --- Router con rate limit aplicado a todas las rutas ---
router = APIRouter(
    dependencies=[Depends(rate_limit_dependency)]
)

# --- Ver todos los planes (solo admin) ---
@router.get("/", response_model=list[PlanOutput])
def plans_list(
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.username != Admin.ADMIN.value:
        raise HTTPException(status_code=403, detail="No autorizado")
    return crud_plans.get_all_plans(db)

# --- Crear plan ---
@router.post("/", response_model=PlanOutput)
def plans_create(
    plan_data: PlanInput,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.username != Admin.ADMIN.value:
        raise HTTPException(status_code=403, detail="No autorizado")
    return crud_plans.create_plan(db, plan_data.model_dump())

# --- Actualizar plan ---
@router.put("/{plan_id}", response_model=PlanOutput)
def plans_update(
    plan_id: int,
    updated_data: PlanInput,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.username != Admin.ADMIN.value:
        raise HTTPException(status_code=403, detail="No autorizado")
    plan = crud_plans.update_plan(db, plan_id, updated_data.model_dump())
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan

# --- Eliminar plan ---
@router.delete("/{plan_id}")
def plans_delete(
    plan_id: int,
    current_user: Me = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.username != Admin.ADMIN.value:
        raise HTTPException(status_code=403, detail="No autorizado")
    success = crud_plans.delete_plan(db, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return {"message": "Plan eliminado correctamente"}
