from fastapi import APIRouter

router = APIRouter()

@router.get("/transacciones")
def transacciones_get():
    return {"message": "Endpoint para ver historial financiero"}

@router.post("/transacciones")
def transacciones_post():
    return {"message": "Endpoint para ver agregar un gasto o ingreso"}

@router.post("/transacciones/{id}")
def transacciones_id_get():
    return {"message": "Endpoint para ver detalles de una transaccion en especifico"}

@router.post("/transacciones/{id}")
def transacciones_id_put():
    return {"message": "Endpoint para actualizar una transaccion en especifico"}

