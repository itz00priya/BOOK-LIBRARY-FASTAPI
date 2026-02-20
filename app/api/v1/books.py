from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional, List
from app.config.database import get_db
from app.models.books import Book
from app.schemas.books import BookCreate, BookUpdate, BookInDB

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookInDB])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    genre: Optional[str] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    
    query = select(Book).where(Book.is_deleted == False)
    
    if search:
        query = query.where(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.description.ilike(f"%{search}%")
            )
        )
    
    if genre:
        query = query.where(Book.genre == genre)
    
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    books = result.scalars().all()
    return books

@router.get("/{book_id}", response_model=BookInDB)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
   
    query = select(Book).where(Book.id == book_id, Book.is_deleted == False)
    result = await db.execute(query)
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookInDB, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
  
    if book.isbn:
        query = select(Book).where(Book.isbn == book.isbn)
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="ISBN already exists")
    
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookInDB)
async def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: AsyncSession = Depends(get_db)
):
    
    query = select(Book).where(Book.id == book_id, Book.is_deleted == False)
    result = await db.execute(query)
    db_book = result.scalar_one_or_none()
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book_update.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    
    query = select(Book).where(Book.id == book_id, Book.is_deleted == False)
    result = await db.execute(query)
    db_book = result.scalar_one_or_none()
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.is_deleted = True
    await db.commit()
