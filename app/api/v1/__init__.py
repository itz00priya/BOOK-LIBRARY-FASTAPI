from app.api.v1.books import router as books_router
from app.api.v1.users import router as users_router
from app.api.v1.borrowing import router as borrowing_router
from app.api.v1.payments import router as payments_router
from app.api.v1.admin import router as admin_router

# Export the routers directly
books = books_router
users = users_router
borrowings = borrowing_router
payments = payments_router
admin = admin_router

__all__ = ["books", "users", "borrowings", "payments", "admin", "books_router", "users_router", "borrowing_router", "payments_router", "admin_router"]

