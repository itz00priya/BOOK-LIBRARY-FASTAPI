from pydantic_settings import BaseSettings
import urllib.parse
import os
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Book Library API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "book_library"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Stripe settings
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_CURRENCY: str = "usd"
    
    # Mail settings
    MAIL_USERNAME: str = "admin@example.com"
    MAIL_PASSWORD: str = "password"
    MAIL_FROM: str = "admin@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Book Library Admin"

    @property
    def DATABASE_URL(self) -> str:
        clean_password = self.DB_PASSWORD.strip().strip("'").strip('"')
        encoded_password = urllib.parse.quote(clean_password)
        return f"postgresql+asyncpg://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

# Debug output
print(f"[DEBUG] Looking for .env at: /.env - Exists: {Path('/.env').exists()}")
print(f"[DEBUG] Looking for .env at: {Path.cwd()}/.env - Exists: {(Path.cwd() / '.env').exists()}")

settings = Settings()
print(f"[DEBUG] Using DB_HOST: {settings.DB_HOST}")



'''import os
from urllib.parse import unquote
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any

# Get the project root directory - go up 3 levels from app/config/settings.py
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if running in Docker (WORKDIR is /app)
# In Docker, the .env file is at /.env, locally it might be in project root
ENV_FILE_DOCKER = "/.env"
ENV_FILE_LOCAL = os.path.join(PROJECT_ROOT, ".env")

# Use /.env in Docker (copied there), otherwise use local .env
if os.path.exists(ENV_FILE_DOCKER):
    ENV_FILE = ENV_FILE_DOCKER
else:
    ENV_FILE = ENV_FILE_LOCAL

print(f"[DEBUG] PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[DEBUG] ENV_FILE: {ENV_FILE}")
print(f"[DEBUG] ENV_FILE exists: {os.path.exists(ENV_FILE)}")

# Custom settings that reads from .env file and environment variables
# Environment variables take priority over .env file
class Settings(BaseSettings):
    APP_NAME: str = "Book Library API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DB_HOST: str = "book_library_db"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "Qsefthuko321!@#"
    DB_NAME: str = "book_library"
    DB_SSLMODE: str = "disable"  
  
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def DATABASE_URL(self) -> str:
        # URL decode the password to handle special characters
        decoded_password = unquote(self.DB_PASSWORD)
        # For asyncpg, use postgresql+asyncpg protocol
        return f"postgresql+asyncpg://{self.DB_USER}:{decoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        # Read from both .env file and environment variables
        # Environment variables take priority
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()

print(f"[DEBUG] Loaded DB_PASSWORD from settings: {settings.DB_PASSWORD}")
print(f"[DEBUG] DATABASE_URL: {settings.DATABASE_URL}")'''
