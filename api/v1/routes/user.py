from fastapi import APIRouter

router = APIRouter()

@router.put("/user/{id}")
def user_edit_me():
    return {"message": "Endpoint para actualizar mis datos en general"}

@router.get("/user/{id}")
def user_get_me():
    return {"message": "Endpoint para obtener mis datos"}

@router.delete("/user/{id}")
def user_delete_me():
    return {"message": "Endpoint para eliminar mis datos"}

