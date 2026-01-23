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
from app.core import lifespan
configure_mappers()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InvoiceGen API",
    description="Complete invoicing and financial management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3030",  # Next.js development server
        "http://127.0.0.1:3030",  # Alternative localhost
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

from fastapi import Request
import json

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f" Incoming request: {request.method} {request.url}")
    
    # Try to read body for /auth/login
    if "login" in str(request.url):
        try:
            body = await request.body()
            print(f" Request Body: {body.decode()}")
            # Re-seed request body because it's a stream
            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}
            request._receive = receive
        except Exception as e:
            print(f" Could not read body: {e}")
            
    response = await call_next(request)
    print(f" Response Status: {response.status_code}")
    return response

# Include routers
app.include_router(graphql_app, prefix="/graphql")
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to InvoiceGen API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
