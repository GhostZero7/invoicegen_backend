from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.router import api_router
from app.db.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InvoiceGen API",
    description="Complete invoicing and financial management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to InvoiceGen API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}