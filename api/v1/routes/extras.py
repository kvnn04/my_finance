from fastapi import APIRouter

router = APIRouter()

@router.post("/notificaciones")
def notificaciones():
    return {"message": "Endpoint para aletar presupuestos o eventos"}

@router.post("/exportar/csv")
def exportar_csv():
    return {"message": "Endpoint para exportar datos en csv"}

@router.post("/exportar/txt")
def exportar_txt():
    return {"message": "Endpoint para exportar datos en txt"}


