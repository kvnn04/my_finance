from fastapi import APIRouter

router = APIRouter()

@router.get("/categories")
def categories_get():
    return {"message": "Endpoint para obtener todas las categorias"}
@router.get("/categories")
def categories_post():
    return {"message": "Endpoint para crear una categoria"}
@router.get("/categories/{id}")
def categories_id_get():
    return {"message": "Endpoint para ver detalles de una categoria"}

