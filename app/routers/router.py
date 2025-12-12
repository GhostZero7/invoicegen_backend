from fastapi import APIRouter
from app.auth.router import router as auth_router
from app.invoices.router import router as invoice_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(invoice_router, prefix="/invoices", tags=["invoices"])

# Add more routers as you create them
# api_router.include_router(business_router, prefix="/business", tags=["business"])
# api_router.include_router(client_router, prefix="/clients", tags=["clients"])