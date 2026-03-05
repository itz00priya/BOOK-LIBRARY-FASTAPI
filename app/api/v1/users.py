from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

from app.config.database import get_db
from app.models.users import User, UserRole
from pydantic import BaseModel, EmailStr

# --- Configuration ---
SECRET_KEY = "your_super_secret_key_change_me" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

# --- Helper Functions ---
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Security Dependencies ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return current_user

# --- Router ---
router = APIRouter(prefix="/users", tags=["users"])

# 1. REGISTER: only Student registration allowed
'''@router.post("/register", response_model=UserResponse, status_code=201)
async def register_student(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.STUDENT, # Forced role
        is_active=True
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user'''

# app/api/v1/users.py

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_student(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    query = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.student,
        is_active=True
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# 2. LOGIN: JWT Token generation with Role
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role.value
    }

# 3. GET USERS: Admin-only access to list users with pagination
@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100), 
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(admin_required) 
):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()