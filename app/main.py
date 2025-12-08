from fastapi import FastAPI
from app.routers.router import api_router

from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="InvoiceGen API")

app.include_router(api_router)
