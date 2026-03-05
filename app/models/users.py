from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.config.database import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    librarian = "librarian"
    student = "student"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student)
    is_active = Column(Boolean, default=True)
    
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    membership_date = Column(DateTime(timezone=True), server_default=func.now())
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    borrowings = relationship("Borrowing", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")









