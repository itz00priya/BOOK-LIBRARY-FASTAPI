from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    isbn = Column(String(13), unique=True, index=True)
    genre = Column(String(50), index=True)
    description = Column(Text)
    publisher = Column(String(100))
    publication_year = Column(Integer)
    pages = Column(Integer)
    language = Column(String(50))
    price = Column(Float, nullable=True)
    cover_image = Column(String(255), nullable=True)
    
    # Inventory tracking
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    
    # Soft delete feature [citation:7]
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    borrowings = relationship("Borrowing", back_populates="book")
    favorites = relationship("Favorite", back_populates="book")