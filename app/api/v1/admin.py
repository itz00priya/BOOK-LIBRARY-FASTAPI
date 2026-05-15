from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.config.database import get_db
from app.api.v1.users import admin_required, UserResponse
from app.models.users import User, UserRole
from app.models.books import Book
from app.models.borrowing import Borrowing, BorrowingStatus
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(admin_required)]
)

class AdminStatsResponse(BaseModel):
    total_users: int
    total_books: int
    active_borrowings: int
    total_fines: float

@router.get("/stats", response_model=AdminStatsResponse)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    # total users
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar_one()

    # total books
    books_result = await db.execute(select(func.count(Book.id)).where(Book.is_deleted == False))
    total_books = books_result.scalar_one()

    # active borrowings
    borrowings_result = await db.execute(select(func.count(Borrowing.id)).where(Borrowing.status == BorrowingStatus.BORROWED))
    active_borrowings = borrowings_result.scalar_one()

    # total fines
    fines_result = await db.execute(select(func.sum(Borrowing.fine_amount)))
    total_fines_val = fines_result.scalar_one()
    total_fines = float(total_fines_val) if total_fines_val else 0.0

    return AdminStatsResponse(
        total_users=total_users,
        total_books=total_books,
        active_borrowings=active_borrowings,
        total_fines=total_fines
    )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

class UpdateRoleRequest(BaseModel):
    role: UserRole

@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int, 
    role_req: UpdateRoleRequest, 
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_req.role
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # check if user has active borrowings
    bor_query = select(Borrowing).where(Borrowing.user_id == user_id, Borrowing.status == BorrowingStatus.BORROWED)
    bor_result = await db.execute(bor_query)
    if bor_result.scalars().first():
        raise HTTPException(status_code=400, detail="Cannot delete user with active borrowings")

    await db.delete(user)
    await db.commit()
    return None
