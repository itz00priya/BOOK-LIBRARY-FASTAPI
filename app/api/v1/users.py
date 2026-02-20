from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.config.database import get_db
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all users with pagination
    """
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user by ID
    """
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=201)
async def create_user(
    username: str,
    email: str,
    full_name: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user
    """
    # Check if username exists
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # In a real app, you'd hash the password here
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user
