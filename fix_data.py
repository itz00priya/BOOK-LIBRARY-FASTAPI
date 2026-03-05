# Isse chalao taaki fine $10 ho jaye
import asyncio
from app.config.database import SessionLocal
from app.models.borrowing import Borrowing
from sqlalchemy import update

async def force_fine():
    async with SessionLocal() as db:
        await db.execute(
            update(Borrowing)
            .where(Borrowing.id == 1)
            .values(fine_amount=10.0, fine_paid=False)
        )
        await db.commit()
        print("Success: Fine set to $10 for ID 1")

asyncio.run(force_fine())