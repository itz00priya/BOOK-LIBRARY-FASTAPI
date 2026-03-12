from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.borrowing import BorrowingStatus

class BorrowCreate(BaseModel):
    book_id: int
    user_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "book_id": 1,
                "user_id": 1
            }
        }
    )

class BorrowResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowingStatus
    fine_amount: float
    fine_paid: bool

    model_config = ConfigDict(from_attributes=True)
