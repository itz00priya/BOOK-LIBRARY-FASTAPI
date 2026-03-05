import asyncio
from datetime import datetime, timedelta
from sqlalchemy import update
from app.config.database import SessionLocal
from app.models.borrowing import Borrowing, BorrowingStatus

async def create_fake_fine(borrowing_id: int):
    async with SessionLocal() as db:
        # 1. Due date ko 5 din purana kar do
        past_due_date = datetime.now() - timedelta(days=5)
        
        # 2. Database update karo taaki system ko lage ye overdue hai
        query = (
            update(Borrowing)
            .where(Borrowing.id == borrowing_id)
            .values(
                due_date=past_due_date,
                fine_amount=5.0,  # $5.00 fine manually set kar rahe hain
                status=BorrowingStatus.OVERDUE
            )
        )
        await db.execute(query)
        await db.commit()
        print(f"✅ Success! Borrowing ID {borrowing_id} par $5.00 ka fine set ho gaya hai.")

if __name__ == "__main__":
    asyncio.run(create_fake_fine(1)) # Yahan apni Borrowing ID dalo