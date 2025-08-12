from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    return {"message": "Endpoint para registrarme"}

@router.post("/sign-in")
def sign_in():
    return {"message": "Endpont para iniciar session"}

@router.post('/me')
def me():
    return {'message': 'Endpoint para obtener datos del usuario actual'}