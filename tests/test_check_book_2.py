import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.config.settings import settings
from app.models.books import Book

async def check_book():
    print(f"Connecting to {settings.DATABASE_URL}")
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check if the book exists independently of is_deleted
        query_any = select(Book).where(Book.id == 2)
        result_any = await session.execute(query_any)
        book_any = result_any.scalar_one_or_none()
        
        if not book_any:
            print("Book ID 2 does NOT exist in the database at all.")
            return
            
        print(f"Book ID 2 exists. is_deleted status: {book_any.is_deleted}")

if __name__ == "__main__":
    asyncio.run(check_book())
