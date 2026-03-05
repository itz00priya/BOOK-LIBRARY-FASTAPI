import asyncio
import uuid
import stripe
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import AsyncSessionLocal
from app.models.books import Book
from app.models.users import User, UserRole
from app.models.borrowing import Borrowing, BorrowingStatus
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

async def setup_test_data() -> int:
    async with AsyncSessionLocal() as db:
        # Create a user
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        user = User(
            username=username,
            email=f"{username}@example.com",
            full_name="Test User",
            hashed_password="hashed_password",
            role=UserRole.MEMBER
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Create a book
        book = Book(
            title=f"Test Book {uuid.uuid4().hex[:8]}",
            author="Test Author",
            isbn=f"123{uuid.uuid4().hex[:6]}",
            total_copies=5,
            available_copies=5
        )
        db.add(book)
        await db.commit()
        await db.refresh(book)

        # Create a borrowing with a fine
        borrowing = Borrowing(
            user_id=user.id,
            book_id=book.id,
            fine_amount=5.00,  # $5.00 fine
            fine_paid=False,
            status=BorrowingStatus.RETURNED
        )
        db.add(borrowing)
        await db.commit()
        await db.refresh(borrowing)
        
        return borrowing.id

def test_create_checkout_session():
    # Setup test data
    borrowing_id = asyncio.run(setup_test_data())
    
    # Optional: Mock stripe to test without hitting live API, 
    # but since this uses test keys, hitting the real API validates the key config
    response = client.post(
        "/api/v1/payments/create-checkout-session",
        json={"borrowing_id": borrowing_id}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "checkout_url" in data
    assert data["checkout_url"].startswith("https://checkout.stripe.com/")

if __name__ == "__main__":
    test_create_checkout_session()
    print("Test passed successfully!")
