from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

# Importar routers (ejemplo)
from api.v1.routes.user import router as user_router
from api.v1.routes.account import router as account_router
from api.v1.routes.categories import router as category_router
from api.v1.routes.transaccion import router as transaction_router
from api.v1.routes.auth import router as auth_router
from api.v1.routes.boka import router as boka_router
from db.create_table_db import Base
from core.session import engine
app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

# Base.metadata.create_all(bind=engine)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers por versión y módulo
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(account_router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(category_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(transaction_router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(boka_router)

# Endpoint raíz para testeo rápido
@app.get("/")
async def root():
    return {"message": "API FinanceFast está corriendo!"}
