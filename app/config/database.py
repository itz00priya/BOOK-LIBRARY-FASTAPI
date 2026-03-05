from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from app.config.base import Base

# Create async engine for PostgreSQL with asyncpg driver
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
