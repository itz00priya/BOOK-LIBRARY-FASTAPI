from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^(\d{10}|\d{13})$")
    genre: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    pages: Optional[int] = Field(None, ge=1)
    language: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    total_copies: int = Field(1, ge=1)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "isbn": "0330258648",
                "genre": "Science Fiction",
                "description": "Don't panic.",
                "publisher": "Pan Books",
                "publication_year": 1979,
                "pages": 224,
                "language": "English",
                "price": 19.99,
                "total_copies": 5
            }
        }
    )

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^(\d{10}|\d{13})$")
    genre: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    pages: Optional[int] = Field(None, ge=1)
    language: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy (Special Edition)",
                "author": "Douglas Adams",
                "isbn": "0330258648",
                "genre": "Science Fiction",
                "description": "Don't panic! Now with extra panic.",
                "publisher": "Pan Books",
                "publication_year": 1979,
                "pages": 224,
                "language": "English",
                "price": 24.99,
                "total_copies": 5,
                "available_copies": 4
            }
        }
    )

class BookInDB(BookBase):
    id: int
    available_copies: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
 