import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.config.settings import settings
from app.models.books import Book

async def test_db():
    print(f"Connecting to {settings.DATABASE_URL}")
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Get book 3 or any book
        query = select(Book).where(Book.is_deleted == False).limit(1)
        result = await session.execute(query)
        db_book = result.scalar_one_or_none()
        
        if not db_book:
            print("No book found to update!")
            return
            
        print(f"Found book: {db_book.id} - {db_book.title}")
        
        # Try applying the dict representing the exact payload
        data = {
          "author": "Douglas Adams",
          "available_copies": 4,
          "description": "Don't panic! Now with extra panic.",
          "genre": "Science Fiction",
          "isbn": "0330258648",
          "language": "English",
          "pages": 224,
          "price": 24.99,
          "publication_year": 1979,
          "publisher": "Pan Books",
          "title": "The Hitchhiker's Guide to the Galaxy (Special Edition)",
          "total_copies": 3
        }
        
        for key, value in data.items():
            setattr(db_book, key, value)
            
        print("About to commit...")
        try:
            await session.commit()
            print("Commit successful!")
        except Exception as e:
            print("Commit failed with error:")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db())
