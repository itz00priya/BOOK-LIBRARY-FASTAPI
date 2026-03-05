from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.config.database import Base

class BorrowingStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Borrowing(Base):
    __tablename__ = "borrowings"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    
    status = Column(Enum(BorrowingStatus), default=BorrowingStatus.BORROWED)
    fine_amount = Column(Float, default=0.0)
    fine_paid = Column(Boolean, default=False)
    
    # Relationships
    book = relationship("Book", back_populates="borrowings")
    user = relationship("User", back_populates="borrowings")