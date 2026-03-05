from pydantic import BaseModel
from typing import Optional

class PaymentCreate(BaseModel):
    borrowing_id: int

class PaymentResponse(BaseModel):
    checkout_url: str

class PaymentSessionInfo(BaseModel):
    session_id: str
    amount_total: int
    currency: str
    payment_status: str
    borrowing_id: Optional[int]
