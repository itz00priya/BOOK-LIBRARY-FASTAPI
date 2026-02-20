from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Book Library API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "book_library"
    DB_SSLMODE: str = "disable"  # Use "require" for Neon.tech [citation:7]
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def DATABASE_URL(self) -> str:
        # For asyncpg, use postgresql+asyncpg protocol [citation:3]
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()