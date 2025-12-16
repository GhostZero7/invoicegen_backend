from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.routers.router import api_router
from app.db.database import Base, engine
from app.graphql import schema, get_context

# Import all models to ensure they're registered
from app.db.models import *

# Configure SQLAlchemy registry to resolve relationships
from sqlalchemy.orm import configure_mappers
configure_mappers()

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
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "https://your-frontend-domain.com"  # Add your production domain here
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# GraphQL router with context and GraphiQL interface
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True,  # Enable GraphiQL web interface
)

# Include routers
app.include_router(graphql_app, prefix="/graphql")
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to InvoiceGen API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}