
import asyncio
from app.config.database import SessionLocal
from app.models.borrowing import Borrowing
from sqlalchemy import update

async def set_fine():
    async with SessionLocal() as db:
        # Hum ID 1 par $10 ka fine set kar rahe hain
        await db.execute(
            update(Borrowing)
            .where(Borrowing.id == 1)
            .values(fine_amount=10.0, fine_paid=False)
        )
        await db.commit()
        print("✅ Fine updated to $10.0 for ID 1")

if __name__ == "__main__":
    asyncio.run(set_fine())