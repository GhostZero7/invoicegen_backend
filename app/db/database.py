from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# For Neon/PostgreSQL with SSL
Base = declarative_base()

# Build connection arguments based on database type
connect_args = {}
if "neon.tech" in settings.DATABASE_URL or "postgresql" in settings.DATABASE_URL:
    # For PostgreSQL/Neon, use sslmode in the URL or configure SSL properly
    connect_args = {
        # "sslmode": "require",
    }

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)