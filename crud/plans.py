from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from db.models.plans import Plan

# Obtener todos los planes
def get_all_plans(db: Session) -> list[Plan]:
    stmt = select(Plan)
    return db.execute(stmt).scalars().all() # type: ignore

# Obtener plan por id
def get_plan_by_id(db: Session, plan_id: int) -> Plan | None:
    stmt = select(Plan).where(Plan.id == plan_id)
    return db.execute(stmt).scalars().first()

# Crear plan
def create_plan(db: Session, plan_data: dict) -> Plan:
    plan = Plan(**plan_data)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

# Actualizar plan
def update_plan(db: Session, plan_id: int, updated_data: dict) -> Plan | None:
    stmt = select(Plan).where(Plan.id == plan_id)
    plan = db.execute(stmt).scalars().first()
    if not plan:
        return None
    for key, value in updated_data.items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan

# Eliminar plan
def delete_plan(db: Session, plan_id: int) -> bool:
    stmt = select(Plan).where(Plan.id == plan_id)
    plan = db.execute(stmt).scalars().first()
    if not plan:
        return False
    db.delete(plan)
    db.commit()
    return True
