from fastapi import APIRouter

router = APIRouter()

@router.get("/boca-jr")
def boca():
    return {"message": "AGUANTE BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOCA!"}
