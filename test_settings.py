import sys
from app.config.settings import settings

print(f"Parsed DB_HOST: '{settings.DB_HOST}'")
print(f"Parsed DB_PASSWORD: '{settings.DB_PASSWORD}'")
print(f"Parsed DATABASE_URL: '{settings.DATABASE_URL}'")
