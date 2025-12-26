from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"  # Default value
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Default value
    
    # SMTP Settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    # Other settings...
    class Config:
        env_file = ".env"
        case_sensitive = False  # This allows lowercase env variables

settings = Settings()