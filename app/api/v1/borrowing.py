from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
from typing import List, Optional
from app.config.database import get_db
from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.books import Book
from app.models.users import User

router = APIRouter(prefix="/borrowing", tags=["borrowing"])

@router.post("/")
async def borrow_book(
    book_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Borrow a book
    """
    # Check if book exists and is available
    book_query = select(Book).where(Book.id == book_id, Book.is_deleted == False)
    book_result = await db.execute(book_query)
    book = book_result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No copies available")
    
    # Check if user exists
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user already has this book borrowed
    existing_query = select(Borrowing).where(
        and_(
            Borrowing.book_id == book_id,
            Borrowing.user_id == user_id,
            Borrowing.status == BorrowingStatus.BORROWED
        )
    )
    existing_result = await db.execute(existing_query)
    if existing_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already has this book borrowed")
    
    # Create borrowing record
    due_date = datetime.now() + timedelta(days=14)
    borrowing = Borrowing(
        book_id=book_id,
        user_id=user_id,
        due_date=due_date,
        status=BorrowingStatus.BORROWED
    )
    
    # Update available copies
    book.available_copies -= 1
    
    db.add(borrowing)
    await db.commit()
    await db.refresh(borrowing)
    
    return borrowing

@router.post("/{borrowing_id}/return")
async def return_book(
    borrowing_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Return a borrowed book
    """
    query = select(Borrowing).where(Borrowing.id == borrowing_id)
    result = await db.execute(query)
    borrowing = result.scalar_one_or_none()
    
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    
    if borrowing.status == BorrowingStatus.RETURNED:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Update borrowing record
    borrowing.return_date = datetime.now()
    borrowing.status = BorrowingStatus.RETURNED
    
    # Calculate fine if overdue
    if borrowing.return_date > borrowing.due_date:
        days_overdue = (borrowing.return_date - borrowing.due_date).days
        borrowing.fine_amount = days_overdue * 1.0  # $1 per day fine
    
    # Update book available copies
    book_query = select(Book).where(Book.id == borrowing.book_id)
    book_result = await db.execute(book_query)
    book = book_result.scalar_one()
    book.available_copies += 1
    
    await db.commit()
    
    return {
        "message": "Book returned successfully",
        "fine_amount": borrowing.fine_amount
    }

@router.get("/")
async def get_borrowings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[BorrowingStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all borrowings with optional status filter
    """
    query = select(Borrowing)
    
    if status:
        query = query.where(Borrowing.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    borrowings = result.scalars().all()
    return borrowings

@router.get("/user/{user_id}")
async def get_user_borrowings(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all borrowings for a specific user
    """
    query = select(Borrowing).where(Borrowing.user_id == user_id)
    result = await db.execute(query)
    borrowings = result.scalars().all()
    return borrowings
