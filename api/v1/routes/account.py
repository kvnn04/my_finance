from fastapi import APIRouter

router = APIRouter()

@router.get("/reportes/balance")
def balance():
    return {"message": "Endpoint para retornar ingreso, gasto y saldo total"}

@router.get("/reportes/gasto-by-categoria")
def gasto_by_categoria():
    return {"message": "Endpoint para ver gastos sumados por categoria"}

@router.get("/reportes/evolucion")
def evolucion():
    return {"message": "Endpoint para devolver los datos agrupados por mes"}

@router.get("/reportes/rango")
def rango():
    return {"message": "Endpoint para ver un resumen entre fechas"}
