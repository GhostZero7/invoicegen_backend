from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# For Neon/PostgreSQL with SSL
Base = declarative_base()

# Build connection arguments based on database type
connect_args = {}
if "neon.tech" in settings.DATABASE_URL:
    # For Neon, require SSL
    connect_args = {
        # "sslmode": "require",
    }
elif "postgresql" in settings.DATABASE_URL and "sslmode=" not in settings.DATABASE_URL:
    # For other PostgreSQL without specified sslmode, default to require if not localhost
    if "localhost" not in settings.DATABASE_URL and "127.0.0.1" not in settings.DATABASE_URL:
        connect_args = {
            "sslmode": "require",
        }

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to False in production
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)