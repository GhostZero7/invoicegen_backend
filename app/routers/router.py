from fastapi import APIRouter
from app.auth.router import router as auth_router
from app.invoices.router import router as invoice_router
from app.clients.router import router as client_router
from app.products.router import router as product_router
# Business endpoints moved to GraphQL - no longer using REST

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(invoice_router, prefix="/invoices", tags=["invoices"])
api_router.include_router(client_router, prefix="/clients", tags=["clients"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
# api_router.include_router(business_router, prefix="/business", tags=["business"])  # Removed - using GraphQL