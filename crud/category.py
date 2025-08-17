from sqlalchemy.orm import Session
from db.models.user import User
from db.models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate

# Obtener todas las categorías
def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

# Crear categoría
def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    category = Category(
        name=category_data.name,
        description=category_data.description,
        user_id=user_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# Obtener categoría por ID
def get_category_by_id(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

# Actualizar categoría
def update_category(db: Session, category_id: int, category_data: CategoryUpdate, user_id: int):
    category = get_category_by_id(db, category_id, user_id)
    if not category:
        return None
    if category_data.name is not None:
        category.name = category_data.name # type: ignore
    if category_data.description is not None:
        category.description = category_data.description # type: ignore

    db.commit()
    db.refresh(category)
    return category

# Eliminar categoría
def delete_category(db: Session, category_id: int, user_id: int):
    category = get_category_by_id(db, category_id, user_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category
