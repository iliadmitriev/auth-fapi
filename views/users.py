from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from db.database import get_db
from models.users import User
from schemas.users import UserCreate, UserDB

router = APIRouter()


@router.post(
    '/users/',
    name="users:post",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user with post query",
    response_model=UserDB
)
async def user_post(user: UserCreate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).filter(User.email == user.email))
    found_users = res.scalar_one_or_none()
    if found_users:
        raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists")
    user_db = User(**user.dict())  # type: ignore
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return user_db


@router.get(
    '/users/{user_id}',
    name="users:get-by-id",
    response_model=UserDB
)
async def user_get(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).filter(User.id == user_id))
    db_user = res.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
