from app.api.v1.books import router as books_router
from app.api.v1.users import router as users_router
from app.api.v1.borrowing import router as borrowing_router

# Export the routers directly
books = books_router
users = users_router
borrowings = borrowing_router

__all__ = ["books", "users", "borrowing", "books_router", "users_router", "borrowing_router"]

