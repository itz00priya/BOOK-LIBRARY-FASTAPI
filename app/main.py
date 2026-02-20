from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import books, users, borrowings
from app.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(borrowings.router, prefix="/api/v1")

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