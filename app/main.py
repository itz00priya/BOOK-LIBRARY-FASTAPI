from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import books, users, borrowings, payments
from app.config.settings import settings
from app.config.database import engine
from app.config.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup if needed
    await engine.dispose()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

print("DEBUG MODE:", settings.DEBUG)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers directly (they are already router objects)
app.include_router(books, prefix="/api/v1")
app.include_router(users, prefix="/api/v1")
app.include_router(borrowings, prefix="/api/v1")
app.include_router(payments, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Book Library API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/success")
async def payment_success(session_id: str):
    return {
        "message": "Thank you! Your fine payment has been successfully processed.", 
        "session_id": session_id
    }
